#!/usr/bin/env python3
"""
Campaign State Manager
Reads, writes, and validates campaign state YAML files.

Usage:
  python3 state_manager.py load <project> <campaign>
  python3 state_manager.py new <project> <campaign-slug> <type>
  python3 state_manager.py update <project> <campaign> --task <task-id> --status <status>
  python3 state_manager.py next <project> <campaign>
  python3 state_manager.py summary <project> <campaign>
  python3 state_manager.py list <project>
  python3 state_manager.py metrics <project> <campaign> --add <json-data>
  python3 state_manager.py --test
"""

import sys
import os
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# Resolve paths relative to repo root
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
CLIENTS_DIR = REPO_ROOT / "clients"
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates"


def read_yaml(path: Path) -> dict:
    """Read YAML without requiring PyYAML in the default macOS Python."""
    if yaml is not None:
        with open(path, "r") as f:
            return yaml.safe_load(f)

    try:
        result = subprocess.run(
            ["ruby", "-ryaml", "-rjson", "-e", "puts YAML.load(STDIN.read).to_json"],
            input=path.read_text(),
            text=True,
            capture_output=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print("ERROR: PyYAML is not installed and Ruby YAML fallback failed.")
        print("Install PyYAML with: python3 -m pip install pyyaml")
        print(f"Details: {exc}")
        sys.exit(1)

    return json.loads(result.stdout)


def write_yaml(path: Path, data: dict) -> None:
    """Write YAML. JSON is valid YAML when PyYAML is unavailable."""
    with open(path, "w") as f:
        if yaml is not None:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        else:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")


def write_json(path: Path, data: dict) -> None:
    """Write deterministic JSON for agent-readable state contracts."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def today() -> str:
    """Return today's date in YYMMDD format."""
    return datetime.now().strftime("%y%m%d")


def timestamp() -> str:
    """Return an ISO-like local timestamp for append-only event logs."""
    return datetime.now().isoformat(timespec="seconds")


def campaign_dir(project: str, campaign: str) -> Path:
    """Return the campaign directory path."""
    return CLIENTS_DIR / project / "campaigns" / campaign


def update_client_campaign_registry(project: str, slug: str, campaign_type: str) -> None:
    """Append/update the client-level campaign registry created by /project:new."""
    registry_path = CLIENTS_DIR / project / "campaigns" / "_campaigns-index.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text())
        except json.JSONDecodeError:
            registry = {}
    else:
        registry = {}

    registry.setdefault("schema_version", "1.0")
    registry.setdefault("client", project)
    registry.setdefault("purpose", "Client-level campaign registry. Use this to discover campaign-index.json files instead of guessing campaign paths.")
    campaigns = registry.setdefault("campaigns", [])

    entry = {
        "campaign_slug": slug,
        "campaign_type": campaign_type,
        "campaign_index": f"campaigns/{slug}/campaign-index.json",
        "state_file": f"campaigns/{slug}/state.yaml",
        "event_log": f"campaigns/{slug}/event-log.jsonl",
        "status": "active",
        "created": today(),
    }

    campaigns[:] = [item for item in campaigns if item.get("campaign_slug") != slug]
    campaigns.append(entry)
    write_json(registry_path, registry)


def default_campaign_selection(project: str, slug: str, campaign_type: str) -> dict:
    """Create the campaign-level source-of-truth input selection manifest."""
    return {
        "schema_version": "1.0",
        "client": project,
        "campaign": slug,
        "campaign_type": campaign_type,
        "created": today(),
        "purpose": "Campaign-level selection of client inputs. Concept workspaces reference these paths instead of copying raw inputs.",
        "client_input_root": "../../00_inputs/",
        "buyer_profile": "../../_brand/buyer-profile.md",
        "micro_persona_rule": "Use one buyer-profile.md as the source of truth for all micro-personas; select persona IDs here and in concept manifests.",
        "selected_top_level_inputs": [],
        "selected_micro_personas": [],
        "concept_selection_manifest_template": {
            "path": "video-concepts/<concept-slug>/concept-brief.json",
            "allowed_concept_input_files": [
                "concept-brief.json"
            ],
            "rule": "Do not duplicate raw client inputs inside concept workspaces. Store only the concept brief with path/ID references to selected top-level inputs."
        }
    }


def load_state(project: str, campaign: str) -> dict:
    """Load and return campaign state from YAML."""
    state_path = campaign_dir(project, campaign) / "state.yaml"
    if not state_path.exists():
        print(f"ERROR: No state file at {state_path}")
        sys.exit(1)
    return read_yaml(state_path)


def save_state(project: str, campaign: str, state: dict) -> None:
    """Write campaign state to YAML with backup."""
    cdir = campaign_dir(project, campaign)
    state_path = cdir / "state.yaml"
    backup_path = cdir / "state.yaml.bak"

    # Backup existing
    if state_path.exists():
        shutil.copy2(state_path, backup_path)

    write_yaml(state_path, state)

    print(f"State saved: {state_path}")


def new_campaign(project: str, slug: str, campaign_type: str) -> dict:
    """Create a new campaign from template."""
    cdir = campaign_dir(project, slug)
    if cdir.exists():
        print(f"ERROR: Campaign already exists at {cdir}")
        sys.exit(1)

    # Find template
    type_template = TEMPLATES_DIR / "campaign-types" / f"{campaign_type}.yaml"
    if not type_template.exists():
        # Fall back to blank template
        type_template = TEMPLATES_DIR / "state-template.yaml"
        print(f"No template for type '{campaign_type}', using blank template")

    # Create directory structure
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "assets").mkdir(exist_ok=True)
    (cdir / "metrics").mkdir(exist_ok=True)
    (cdir / "event-log.jsonl").write_text(
        json.dumps({
            "schema_version": "1.0",
            "event": "campaign_created",
            "client": project,
            "campaign": slug,
            "campaign_type": campaign_type,
            "created_at": timestamp(),
        }, ensure_ascii=False) + "\n"
    )

    campaign_index = {
        "schema_version": "1.0",
        "client": project,
        "campaign": slug,
        "campaign_type": campaign_type,
        "created": today(),
        "purpose": "Campaign-level discovery file. Read this before guessing artifact paths.",
        "state_file": "state.yaml",
        "event_log": "event-log.jsonl",
        "campaign_selection": "campaign-selection.json",
        "active_concept_slug": None,
        "concept_workspace_scaffold": "video-concepts/<concept-slug>/",
        "concept_workspace_template_source": "../../_templates/video-concept-workspace/",
        "required_concept_workspace_files": [
            "pipeline-state.json",
            "artifact-manifest.json",
            "event-log.jsonl",
            "concept-brief.json",
            "04_input-images/input-image-manifest.json"
        ],
        "input_source_contract": {
            "client_input_root": "../../00_inputs/",
            "buyer_profile": "../../_brand/buyer-profile.md",
            "campaign_selection": "campaign-selection.json",
            "concept_rule": "Concept workspaces use root concept-brief.json. Do not create concept-level 00_inputs folders or copy raw input folders into concepts."
        },
        "concept_workspaces": [],
        "fixed_system_paths": {
            "video_factory": "/Users/jerel/.claude/skills/video-factory/",
            "higgsfield_prompts": "/Users/jerel/AI workflows/higgsfield-prompts/",
            "higgsfield_repo_claude": "/Users/jerel/AI workflows/higgsfield-prompts/CLAUDE.md",
            "higgsfield_video_generation": "/Users/jerel/AI workflows/higgsfield-prompts/skills/media/video-generation/SKILL.md",
            "higgsfield_image_generation": "/Users/jerel/AI workflows/higgsfield-prompts/skills/media/image-generation/SKILL.md",
            "higgsfield_viral_presets": "/Users/jerel/AI workflows/higgsfield-prompts/skills/media/viral-presets/"
        }
    }
    write_json(cdir / "campaign-index.json", campaign_index)
    write_json(cdir / "campaign-selection.json", default_campaign_selection(project, slug, campaign_type))
    update_client_campaign_registry(project, slug, campaign_type)

    if campaign_type == "video-content":
        # Canonical video-content campaign layout (per client-onboarding SKILL.md):
        # all work lives under video-concepts/<concept-slug>/{01_strategy..07_review}.
        # The pre-Jake 0X_stage/output folders were removed 2026-05-18 — they caused
        # path drift (artifacts nested under 02_script/output/video-concepts/<concept>/).
        for rel in (
            "render-requests",
            "video-runs",
            "video-concepts",
        ):
            (cdir / rel).mkdir(parents=True, exist_ok=True)
        (cdir / "video-concepts" / "README.md").write_text(
            "# Video Concepts\n\n"
            "Before creating concepts, fill `../campaign-selection.json` with the selected "
            "top-level client inputs from `../../00_inputs/` and selected micro-persona IDs "
            "from `../../_brand/buyer-profile.md`.\n\n"
            "Create concept workspaces here:\n\n"
            "```text\n"
            "video-concepts/<concept-slug>/\n"
            "```\n\n"
            "Create each workspace by copying `../../_templates/video-concept-workspace/`, "
            "then replacing `{{campaign_slug}}` and `{{concept_slug}}` in the copied files.\n\n"
            "Every active concept workspace must contain `pipeline-state.json`, "
            "`artifact-manifest.json`, `event-log.jsonl`, `01_strategy/` through `07_review/`, "
            "`concept-brief.json`, and `04_input-images/input-image-manifest.json`. "
            "Do not create concept-level `00_inputs/` folders or copy raw input folders "
            "there. Register each workspace in `../campaign-index.json` before asking "
            "agents to work inside it.\n"
        )

    # Load template
    state = read_yaml(type_template)

    # Fill in metadata
    state["campaign"]["project"] = project
    state["campaign"]["created"] = today()

    # Copy to campaign dir
    save_state(project, slug, state)
    print(f"Created campaign: {cdir}")
    print(f"Type: {campaign_type}")
    print(f"Tasks: {len(state.get('tasks', []))}")
    return state


def get_next_actions(state: dict, limit: int = 3) -> list:
    """Get next priority actions based on dependencies and status."""
    tasks = state.get("tasks", [])
    done_ids = {t["id"] for t in tasks if t.get("status") == "done"}

    available = []
    for task in tasks:
        if task.get("status") in ("done", "scheduled"):
            continue
        deps = task.get("dependencies", [])
        if all(d in done_ids for d in deps):
            available.append(task)

    # Sort: execution > creation > planning > optimization
    phase_order = {"execution": 0, "creation": 1, "planning": 2, "optimization": 3}
    available.sort(key=lambda t: phase_order.get(t.get("phase", ""), 99))

    return available[:limit]


def update_task(state: dict, task_id: str, updates: dict) -> dict:
    """Update a specific task in the state."""
    for task in state.get("tasks", []):
        if task["id"] == task_id:
            task.update(updates)
            return state
    print(f"ERROR: Task '{task_id}' not found")
    sys.exit(1)


def add_asset(state: dict, asset_info: dict) -> dict:
    """Register a new asset in the state."""
    if "assets" not in state or state["assets"] is None:
        state["assets"] = []
    state["assets"].append(asset_info)
    return state


def add_metric_snapshot(state: dict, data: dict) -> dict:
    """Append a metrics snapshot."""
    if "metrics" not in state:
        state["metrics"] = {"snapshots": []}
    if state["metrics"] is None:
        state["metrics"] = {"snapshots": []}
    if "snapshots" not in state["metrics"] or state["metrics"]["snapshots"] is None:
        state["metrics"]["snapshots"] = []
    data["date"] = data.get("date", today())
    state["metrics"]["snapshots"].append(data)
    return state


def get_summary(state: dict) -> str:
    """One-line campaign status summary."""
    campaign = state.get("campaign", {})
    tasks = state.get("tasks", [])
    done = sum(1 for t in tasks if t.get("status") in ("done", "scheduled"))
    total = len(tasks)
    name = campaign.get("name", "Unnamed")
    phase = campaign.get("phase", "unknown")
    return f"{name} — Phase: {phase} ({done}/{total} tasks done)"


def list_campaigns(project: str) -> list:
    """List all campaigns for a project."""
    campaigns_dir = CLIENTS_DIR / project / "campaigns"
    if not campaigns_dir.exists():
        return []
    campaigns = []
    for d in sorted(campaigns_dir.iterdir()):
        if d.is_dir() and (d / "state.yaml").exists():
            state = load_state(project, d.name)
            campaigns.append({
                "slug": d.name,
                "summary": get_summary(state)
            })
    return campaigns


def display_dashboard(state: dict) -> None:
    """Print campaign dashboard."""
    summary = get_summary(state)
    status = state.get("status", {})
    last_session = status.get("last_session", "Never")
    last_action = status.get("last_action", "None")
    blockers = status.get("blockers", [])
    next_actions = get_next_actions(state)

    print(f"\n## Campaign: {summary}")
    print(f"\nLast session ({last_session}):")
    print(f"  {last_action}")
    print(f"\nNext actions:")
    for i, task in enumerate(next_actions, 1):
        agent = task.get("agent", "direct")
        desc = task.get("description", task.get("id", ""))
        print(f"  {i}. {desc} ({agent})")
    if blockers:
        print(f"\nBlockers: {', '.join(blockers)}")
    else:
        print(f"\nBlockers: None")
    print()


def run_tests() -> None:
    """Run basic state manager tests."""
    import tempfile
    global CLIENTS_DIR
    original_clients = CLIENTS_DIR

    with tempfile.TemporaryDirectory() as tmpdir:
        CLIENTS_DIR = Path(tmpdir)

        # Test: create campaign
        print("Test 1: Create campaign from template...")
        state = new_campaign("test-project", "test-campaign", "product-launch")
        assert state["campaign"]["project"] == "test-project"
        assert state["campaign"]["type"] == "product-launch"
        assert len(state["tasks"]) > 0
        print("  PASS")

        # Test: load state
        print("Test 2: Load state...")
        loaded = load_state("test-project", "test-campaign")
        assert loaded["campaign"]["project"] == "test-project"
        print("  PASS")

        # Test: get next actions
        print("Test 3: Get next actions...")
        actions = get_next_actions(loaded)
        assert len(actions) > 0
        # First action should have no dependencies
        assert len(actions[0].get("dependencies", [])) == 0
        print(f"  PASS ({len(actions)} actions available)")

        # Test: update task
        print("Test 4: Update task...")
        first_task_id = loaded["tasks"][0]["id"]
        updated = update_task(loaded, first_task_id, {"status": "done"})
        assert updated["tasks"][0]["status"] == "done"
        print("  PASS")

        # Test: save and reload
        print("Test 5: Save and reload...")
        save_state("test-project", "test-campaign", updated)
        reloaded = load_state("test-project", "test-campaign")
        assert reloaded["tasks"][0]["status"] == "done"
        print("  PASS")

        # Test: add asset
        print("Test 6: Add asset...")
        with_asset = add_asset(reloaded, {
            "path": "assets/test.md",
            "type": "copy",
            "status": "draft",
            "created": today()
        })
        assert len(with_asset["assets"]) == 1
        print("  PASS")

        # Test: add metric
        print("Test 7: Add metric snapshot...")
        with_metric = add_metric_snapshot(with_asset, {
            "source": "google-analytics",
            "data": {"visitors": 100, "signups": 5}
        })
        assert len(with_metric["metrics"]["snapshots"]) == 1
        print("  PASS")

        # Test: summary
        print("Test 8: Get summary...")
        summary = get_summary(with_metric)
        assert "done" in summary
        print(f"  PASS: {summary}")

        # Test: list campaigns
        print("Test 9: List campaigns...")
        campaigns = list_campaigns("test-project")
        assert len(campaigns) == 1
        print(f"  PASS: {len(campaigns)} campaign(s)")

        # Test: dashboard display
        print("Test 10: Display dashboard...")
        display_dashboard(with_metric)
        print("  PASS")

    CLIENTS_DIR = original_clients
    print("\nAll tests passed!")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "--test":
        run_tests()
        return

    if cmd == "load":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py load <project> <campaign>")
            sys.exit(1)
        state = load_state(sys.argv[2], sys.argv[3])
        display_dashboard(state)

    elif cmd == "new":
        if len(sys.argv) < 5:
            print("Usage: state_manager.py new <project> <campaign-slug> <type>")
            print("Types: product-launch, content-seo, lead-gen, retention")
            sys.exit(1)
        new_campaign(sys.argv[2], sys.argv[3], sys.argv[4])

    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py update <project> <campaign> --task <id> --status <status>")
            sys.exit(1)
        project, campaign_name = sys.argv[2], sys.argv[3]
        state = load_state(project, campaign_name)
        # Parse --task and --status flags
        task_id = None
        status = None
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--task" and i + 1 < len(sys.argv):
                task_id = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        if task_id and status:
            state = update_task(state, task_id, {"status": status})
            save_state(project, campaign_name, state)

    elif cmd == "next":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py next <project> <campaign>")
            sys.exit(1)
        state = load_state(sys.argv[2], sys.argv[3])
        actions = get_next_actions(state)
        for i, task in enumerate(actions, 1):
            print(f"{i}. [{task.get('phase')}] {task.get('description', task['id'])} → {task.get('agent', 'direct')}")

    elif cmd == "summary":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py summary <project> <campaign>")
            sys.exit(1)
        state = load_state(sys.argv[2], sys.argv[3])
        print(get_summary(state))

    elif cmd == "list":
        if len(sys.argv) < 3:
            print("Usage: state_manager.py list <project>")
            sys.exit(1)
        campaigns = list_campaigns(sys.argv[2])
        if not campaigns:
            print("No active campaigns")
        for c in campaigns:
            print(f"  {c['slug']}: {c['summary']}")

    elif cmd == "metrics":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py metrics <project> <campaign> --add '{json}'")
            sys.exit(1)
        project, campaign_name = sys.argv[2], sys.argv[3]
        state = load_state(project, campaign_name)
        if "--add" in sys.argv:
            idx = sys.argv.index("--add")
            if idx + 1 < len(sys.argv):
                data = json.loads(sys.argv[idx + 1])
                state = add_metric_snapshot(state, data)
                save_state(project, campaign_name, state)
        else:
            snapshots = state.get("metrics", {}).get("snapshots", [])
            for s in snapshots:
                print(f"  [{s.get('date')}] {s.get('source')}: {s.get('data', {})}")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
