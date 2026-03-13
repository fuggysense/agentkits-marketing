#!/usr/bin/env python3
"""
Similarity Scanner — Pure Python TF-IDF + cosine similarity.

No external dependencies. Corpus is ~75 docs so pure Python is fine.

Usage:
    scan_similarity.py                         # Scan all, default threshold 0.65
    scan_similarity.py --threshold 0.7         # Custom threshold
    scan_similarity.py --target copywriting    # Compare one against all
    scan_similarity.py --type skills           # Only scan skills
    scan_similarity.py --type agents           # Only scan agents
    scan_similarity.py --json                  # JSON output

Thresholds:
    > 0.65 = "potentially overlapping"
    > 0.80 = "likely duplicate"
"""

import sys
import json
import re
import math
from pathlib import Path
from collections import Counter, defaultdict


def find_project_root():
    """Walk up from script location to find project root."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return None


def tokenize(text):
    """Simple tokenizer: lowercase, split on non-alphanumeric, remove stopwords."""
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "out", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "both", "each", "few", "more", "most",
        "other", "some", "such", "no", "nor", "not", "only", "own", "same",
        "so", "than", "too", "very", "just", "if", "or", "and", "but", "it",
        "its", "this", "that", "these", "those", "i", "me", "my", "we", "our",
        "you", "your", "he", "him", "his", "she", "her", "they", "them", "their",
        "what", "which", "who", "whom", "use", "using", "used",
    }
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in stopwords and len(w) > 2]


def extract_doc_text(path, doc_type):
    """Extract meaningful text from a skill or agent file."""
    content = path.read_text()

    # Extract frontmatter description
    desc = ""
    match = re.search(r"description:\s*(.+?)(?:\n[a-z]|\n---)", content, re.DOTALL)
    if match:
        desc = match.group(1).strip()

    # Extract triggers if present
    triggers = ""
    match = re.search(r'"triggers":\s*\[([^\]]+)\]', content)
    if match:
        triggers = match.group(1)

    # Get first 500 chars of body (after frontmatter)
    body = ""
    parts = content.split("---", 2)
    if len(parts) >= 3:
        body = parts[2][:500]

    return f"{desc} {triggers} {body}"


def compute_tfidf(documents):
    """Compute TF-IDF vectors for a set of documents."""
    # Tokenize all docs
    doc_tokens = {}
    for doc_id, text in documents.items():
        doc_tokens[doc_id] = tokenize(text)

    # Build document frequency
    df = defaultdict(int)
    for tokens in doc_tokens.values():
        unique_tokens = set(tokens)
        for token in unique_tokens:
            df[token] += 1

    n_docs = len(documents)

    # Compute TF-IDF vectors
    tfidf = {}
    for doc_id, tokens in doc_tokens.items():
        tf = Counter(tokens)
        total = len(tokens) if tokens else 1
        vector = {}
        for token, count in tf.items():
            tf_val = count / total
            idf_val = math.log((n_docs + 1) / (df[token] + 1)) + 1
            vector[token] = tf_val * idf_val
        tfidf[doc_id] = vector

    return tfidf


def cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two sparse vectors (dicts)."""
    if not vec_a or not vec_b:
        return 0.0

    # Dot product
    common_keys = set(vec_a.keys()) & set(vec_b.keys())
    dot = sum(vec_a[k] * vec_b[k] for k in common_keys)

    # Magnitudes
    mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
    mag_b = math.sqrt(sum(v * v for v in vec_b.values()))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)


def collect_documents(root, doc_type="all"):
    """Collect all skill and agent documents."""
    documents = {}

    if doc_type in ("all", "skills"):
        skills_dir = root / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if not skill_dir.is_dir():
                    continue
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    doc_id = f"skill:{skill_dir.name}"
                    documents[doc_id] = extract_doc_text(skill_md, "skill")

    if doc_type in ("all", "agents"):
        agents_dir = root / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                name = agent_file.stem
                if name.endswith("-learnings") or name.endswith("-attribution") or name == "README":
                    continue
                doc_id = f"agent:{name}"
                documents[doc_id] = extract_doc_text(agent_file, "agent")

    return documents


def main():
    threshold = 0.65
    target = None
    doc_type = "all"
    output_json = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--threshold" and i + 1 < len(args):
            threshold = float(args[i + 1])
            i += 2
        elif args[i] == "--target" and i + 1 < len(args):
            target = args[i + 1]
            i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            doc_type = args[i + 1]
            i += 2
        elif args[i] == "--json":
            output_json = True
            i += 1
        else:
            i += 1

    root = find_project_root()
    if not root:
        print("Error: Could not find project root.")
        sys.exit(1)

    documents = collect_documents(root, doc_type)
    if len(documents) < 2:
        print("Not enough documents to compare.")
        sys.exit(0)

    tfidf = compute_tfidf(documents)

    # Compute pairwise similarities
    results = []
    doc_ids = list(tfidf.keys())
    for i in range(len(doc_ids)):
        for j in range(i + 1, len(doc_ids)):
            a, b = doc_ids[i], doc_ids[j]
            if target:
                # Match target against either side (with or without prefix)
                a_name = a.split(":", 1)[1] if ":" in a else a
                b_name = b.split(":", 1)[1] if ":" in b else b
                if target not in (a, b, a_name, b_name):
                    continue
            sim = cosine_similarity(tfidf[a], tfidf[b])
            if sim >= threshold:
                label = "LIKELY DUPLICATE" if sim > 0.80 else "POTENTIALLY OVERLAPPING"
                results.append(
                    {
                        "pair": [a, b],
                        "similarity": round(sim, 4),
                        "label": label,
                    }
                )

    results.sort(key=lambda r: -r["similarity"])

    if output_json:
        print(json.dumps(results, indent=2))
        return

    # Human-readable
    scope = f" for '{target}'" if target else ""
    print(f"# Similarity Scan{scope} (threshold: {threshold})")
    print(f"Scanned {len(documents)} documents, found {len(results)} pair(s)\n")

    if not results:
        print("No similarities above threshold.")
        return

    for r in results:
        sim_bar = "#" * int(r["similarity"] * 20)
        print(f"  [{r['label']}] {r['similarity']:.2f} {sim_bar}")
        print(f"    {r['pair'][0]}  <->  {r['pair'][1]}")
        print()


if __name__ == "__main__":
    main()
