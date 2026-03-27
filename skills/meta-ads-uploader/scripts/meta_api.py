#!/usr/bin/env python3
"""
Meta Ads Creative Uploader — Core Module
=========================================
Python client for Meta Marketing API v22.0 creative operations.
Handles image/video upload, creative creation, and ad creation.

Usage as module:
    from meta_api import MetaAdsClient
    client = MetaAdsClient()
    result = client.upload_image("hero.png")
    print(result["hash"])

Usage as CLI:
    See upload.py for the command-line interface.

API docs: https://developers.facebook.com/docs/marketing-api
"""

import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)


API_VERSION = "v22.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Character limits enforced before API call
CHAR_LIMITS = {
    "primary_text": 125,
    "headline": 40,
    "description": 25,
}

VALID_CTA_TYPES = [
    "LEARN_MORE", "SHOP_NOW", "SIGN_UP", "SUBSCRIBE", "CONTACT_US",
    "GET_OFFER", "GET_QUOTE", "DOWNLOAD", "BOOK_TRAVEL", "LISTEN_NOW",
    "WATCH_MORE", "APPLY_NOW", "BUY_NOW", "GET_DIRECTIONS", "MESSAGE_PAGE",
    "CALL_NOW", "OPEN_LINK", "NO_BUTTON",
]

VALID_FORMATS = ["single_image", "single_video"]

# Image formats Meta accepts natively
NATIVE_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
# Formats we auto-convert to PNG
CONVERTIBLE_FORMATS = {".webp", ".tiff", ".tif", ".heic", ".heif"}


# --- Exceptions ---

class MetaAdsError(Exception):
    """Base exception for Meta Ads API errors."""
    pass

class AuthError(MetaAdsError):
    """Invalid or missing access token, or app in dev mode (401/403)."""
    pass

class RateLimitError(MetaAdsError):
    """Rate limit exceeded (429)."""
    pass

class CreativeError(MetaAdsError):
    """Invalid creative specs (bad image hash, missing fields, etc)."""
    pass

class ServerError(MetaAdsError):
    """Server-side error (5xx)."""
    pass


# --- Utility functions (shared pattern from scrapecreators) ---

def find_project_root():
    """Walk up from script location looking for CLAUDE.md (repo convention)."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    cwd = Path.cwd()
    for _ in range(10):
        if (cwd / "CLAUDE.md").exists():
            return cwd
        cwd = cwd.parent
    return None


def load_env(root=None):
    """Load .env file from project root."""
    if root is None:
        root = find_project_root()
    if root is None:
        return
    env_path = root / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                os.environ.setdefault(key, value)


def convert_image(src_path, dest_path=None):
    """Convert non-native image formats to PNG. Returns path to converted file."""
    try:
        from PIL import Image
    except ImportError:
        raise MetaAdsError(
            f"Cannot convert {src_path.suffix} to PNG — install Pillow: pip install Pillow"
        )
    if dest_path is None:
        dest_path = src_path.with_suffix(".png")
    img = Image.open(src_path)
    img.save(dest_path, "PNG")
    return dest_path


# --- Client ---

class MetaAdsClient:
    """Client for Meta Marketing API creative operations.

    Args:
        access_token: Meta access token. If None, loads from META_ADS_ACCESS_TOKEN env var.
        ad_account_id: Ad account ID (e.g., "act_123456"). If None, loads from META_AD_ACCOUNT_ID.
        quiet: Suppress progress messages to stderr.
    """

    def __init__(self, access_token=None, ad_account_id=None, quiet=False):
        load_env()

        if access_token is None:
            access_token = os.environ.get("META_ADS_ACCESS_TOKEN")
        if not access_token:
            raise AuthError(
                "META_ADS_ACCESS_TOKEN not set. "
                "Get a token at: https://business.facebook.com → Business Settings → System Users"
            )

        if ad_account_id is None:
            ad_account_id = os.environ.get("META_AD_ACCOUNT_ID")
        if not ad_account_id:
            raise AuthError(
                "META_AD_ACCOUNT_ID not set. "
                "Format: act_123456789"
            )
        if not ad_account_id.startswith("act_"):
            ad_account_id = f"act_{ad_account_id}"

        self._token = access_token
        self._account_id = ad_account_id
        self._quiet = quiet
        self.calls_made = 0

    def _log(self, msg):
        if not self._quiet:
            print(msg, file=sys.stderr)

    def _request(self, method, endpoint, data=None, files=None, retries=1):
        """Make an API request with retry on 5xx.

        Returns:
            Parsed JSON response dict

        Raises:
            AuthError, RateLimitError, CreativeError, ServerError, MetaAdsError
        """
        url = f"{BASE_URL}{endpoint}"
        params = {"access_token": self._token}
        last_error = None

        for attempt in range(1 + retries):
            try:
                if method == "GET":
                    resp = requests.get(url, params={**(data or {}), **params}, timeout=60)
                elif method == "POST":
                    if files:
                        resp = requests.post(url, params=params, data=data or {}, files=files, timeout=120)
                    else:
                        resp = requests.post(url, params=params, json=data, timeout=60)
                else:
                    raise MetaAdsError(f"Unsupported method: {method}")

                body = resp.json() if resp.text else {}

                # Meta returns errors in {"error": {...}} format
                if "error" in body:
                    err = body["error"]
                    code = err.get("code", 0)
                    msg = err.get("message", str(err))

                    if code in (190, 102, 104):  # OAuth / token errors
                        raise AuthError(f"Auth failed ({code}): {msg}")
                    if code == 17 or code == 4:  # Rate limit
                        raise RateLimitError(f"Rate limit: {msg}")
                    if code == 100:  # Invalid parameter
                        raise CreativeError(f"Invalid params: {msg}")
                    if resp.status_code >= 500:
                        last_error = ServerError(f"Server error ({resp.status_code}): {msg}")
                        if attempt < retries:
                            time.sleep(2 ** attempt)
                            continue
                        raise last_error
                    raise MetaAdsError(f"API error ({code}): {msg}")

                if resp.status_code >= 500:
                    last_error = ServerError(f"Server error {resp.status_code}")
                    if attempt < retries:
                        time.sleep(2 ** attempt)
                        continue
                    raise last_error

                resp.raise_for_status()
                self.calls_made += 1
                return body

            except requests.exceptions.ConnectionError as e:
                last_error = MetaAdsError(f"Connection failed: {e}")
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise last_error
            except requests.exceptions.Timeout:
                last_error = MetaAdsError(f"Request timed out: {endpoint}")
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise last_error
            except (AuthError, RateLimitError, CreativeError):
                raise

        raise last_error

    # --- Token & Account ---

    def validate_token(self):
        """Check if access token is valid. Returns True or raises AuthError."""
        result = self._request("GET", "/me", data={"fields": "id,name"})
        self._log(f"Token valid — user: {result.get('name', 'unknown')}")
        return True

    def get_account_info(self):
        """Get ad account details."""
        result = self._request(
            "GET",
            f"/{self._account_id}",
            data={"fields": "name,currency,timezone_name,account_status"}
        )
        return {
            "id": self._account_id,
            "name": result.get("name", ""),
            "currency": result.get("currency", ""),
            "timezone": result.get("timezone_name", ""),
            "status": result.get("account_status", ""),
        }

    # --- Image Upload ---

    def upload_image(self, image_path):
        """Upload an image to the ad account.

        Auto-converts WebP/TIFF/HEIC to PNG via Pillow if needed.

        Args:
            image_path: Path to the image file

        Returns:
            {"hash": str, "url": str}
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise MetaAdsError(f"Image not found: {image_path}")

        # Auto-convert if needed
        suffix = image_path.suffix.lower()
        if suffix in CONVERTIBLE_FORMATS:
            self._log(f"Converting {suffix} → .png")
            image_path = convert_image(image_path)

        if suffix not in NATIVE_IMAGE_FORMATS and suffix not in CONVERTIBLE_FORMATS:
            raise CreativeError(
                f"Unsupported image format: {suffix}. "
                f"Supported: {', '.join(sorted(NATIVE_IMAGE_FORMATS | CONVERTIBLE_FORMATS))}"
            )

        self._log(f"Uploading image: {image_path.name}")

        with open(image_path, "rb") as f:
            result = self._request(
                "POST",
                f"/{self._account_id}/adimages",
                files={"filename": (image_path.name, f)},
            )

        # Response: {"images": {"filename": {"hash": "...", "url": "..."}}}
        images = result.get("images", {})
        if not images:
            raise CreativeError(f"Image upload failed — unexpected response: {result}")

        img_data = next(iter(images.values()))
        out = {"hash": img_data["hash"], "url": img_data.get("url", "")}
        self._log(f"Image uploaded — hash: {out['hash']}")
        return out

    # --- Video Upload ---

    def upload_video(self, video_path, title=""):
        """Upload a video to the ad account.

        Polls until processing is complete (max 5 minutes).

        Args:
            video_path: Path to the video file
            title: Optional video title

        Returns:
            {"video_id": str}
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise MetaAdsError(f"Video not found: {video_path}")

        self._log(f"Uploading video: {video_path.name}")

        data = {}
        if title:
            data["title"] = title

        with open(video_path, "rb") as f:
            result = self._request(
                "POST",
                f"/{self._account_id}/advideos",
                data=data,
                files={"source": (video_path.name, f)},
            )

        video_id = result.get("id")
        if not video_id:
            raise CreativeError(f"Video upload failed — unexpected response: {result}")

        # Poll until processing complete
        self._log(f"Video uploaded (id: {video_id}), waiting for processing...")
        max_wait = 300  # 5 minutes
        interval = 10
        elapsed = 0

        while elapsed < max_wait:
            status = self._request(
                "GET", f"/{video_id}", data={"fields": "status"}
            )
            video_status = status.get("status", {})
            processing = video_status.get("processing_phase", {})
            if processing.get("status") == "complete":
                self._log(f"Video processing complete — id: {video_id}")
                return {"video_id": video_id}
            if processing.get("status") == "error":
                raise CreativeError(
                    f"Video processing failed: {processing.get('errors', 'unknown error')}"
                )
            time.sleep(interval)
            elapsed += interval
            self._log(f"Video processing... ({elapsed}s)")

        raise MetaAdsError(f"Video processing timed out after {max_wait}s (id: {video_id})")

    # --- Creative Creation ---

    def create_creative_single(self, page_id, image_hash=None, video_id=None,
                                primary_text="", headline="", description="",
                                link_url="", cta_type="LEARN_MORE", name="",
                                instagram_actor_id=None, url_tags=""):
        """Create a single-asset ad creative (one image or video, one text set).

        Uses object_story_spec format.

        Returns:
            {"creative_id": str}
        """
        if not image_hash and not video_id:
            raise CreativeError("Must provide either image_hash or video_id")
        if image_hash and video_id:
            raise CreativeError("Provide image_hash OR video_id, not both")
        if cta_type not in VALID_CTA_TYPES:
            raise CreativeError(f"Invalid CTA: {cta_type}. Valid: {', '.join(VALID_CTA_TYPES)}")

        call_to_action = {"type": cta_type, "value": {"link": link_url}}

        if image_hash:
            link_data = {
                "message": primary_text,
                "link": link_url,
                "name": headline,
                "description": description,
                "image_hash": image_hash,
                "call_to_action": call_to_action,
            }
            story_spec = {"page_id": page_id, "link_data": link_data}
        else:
            video_data = {
                "message": primary_text,
                "video_id": video_id,
                "title": headline,
                "link_description": description,
                "call_to_action": call_to_action,
                "link_url": link_url,
            }
            story_spec = {"page_id": page_id, "video_data": video_data}

        if instagram_actor_id:
            story_spec["instagram_actor_id"] = instagram_actor_id

        creative_data = {
            "name": name or f"Creative-{int(time.time())}",
            "object_story_spec": json.dumps(story_spec),
        }
        if url_tags:
            creative_data["url_tags"] = url_tags

        self._log(f"Creating single creative: {creative_data['name']}")
        result = self._request("POST", f"/{self._account_id}/adcreatives", data=creative_data)

        creative_id = result.get("id")
        if not creative_id:
            raise CreativeError(f"Creative creation failed: {result}")

        self._log(f"Creative created — id: {creative_id}")
        return {"creative_id": creative_id}

    def create_creative_dynamic(self, page_id, image_hashes=None, video_ids=None,
                                 primary_texts=None, headlines=None, descriptions=None,
                                 link_url="", cta_type="LEARN_MORE", name="",
                                 instagram_actor_id=None, url_tags=""):
        """Create a dynamic creative (multiple text/asset variations).

        Meta auto-rotates best-performing combinations.
        Uses asset_feed_spec format.

        Returns:
            {"creative_id": str}
        """
        if not image_hashes and not video_ids:
            raise CreativeError("Must provide image_hashes or video_ids")
        if cta_type not in VALID_CTA_TYPES:
            raise CreativeError(f"Invalid CTA: {cta_type}. Valid: {', '.join(VALID_CTA_TYPES)}")

        asset_feed = {
            "bodies": [{"text": t} for t in (primary_texts or [])],
            "titles": [{"text": t} for t in (headlines or [])],
            "descriptions": [{"text": t} for t in (descriptions or [])],
            "link_urls": [{"website_url": link_url}],
            "call_to_action_types": [cta_type],
            "ad_formats": ["SINGLE_IMAGE"] if image_hashes else ["SINGLE_VIDEO"],
        }

        if image_hashes:
            asset_feed["images"] = [{"hash": h} for h in image_hashes]
        if video_ids:
            asset_feed["videos"] = [{"video_id": v} for v in video_ids]

        story_spec = {"page_id": page_id}
        if instagram_actor_id:
            story_spec["instagram_actor_id"] = instagram_actor_id

        creative_data = {
            "name": name or f"DynCreative-{int(time.time())}",
            "object_story_spec": json.dumps(story_spec),
            "asset_feed_spec": json.dumps(asset_feed),
        }
        if url_tags:
            creative_data["url_tags"] = url_tags

        self._log(f"Creating dynamic creative: {creative_data['name']}")
        result = self._request("POST", f"/{self._account_id}/adcreatives", data=creative_data)

        creative_id = result.get("id")
        if not creative_id:
            raise CreativeError(f"Dynamic creative creation failed: {result}")

        self._log(f"Dynamic creative created — id: {creative_id}")
        return {"creative_id": creative_id}

    # --- Ad Creation ---

    def create_ad(self, ad_set_id, creative_id, name="", status="PAUSED"):
        """Create an ad in an ad set. Always PAUSED by default (HITL safety).

        Args:
            ad_set_id: Target ad set
            creative_id: Creative to use
            name: Ad name
            status: Must be PAUSED (safety default)

        Returns:
            {"ad_id": str}
        """
        if status != "PAUSED":
            self._log("WARNING: Overriding status to PAUSED — ads must be activated manually")
            status = "PAUSED"

        ad_data = {
            "name": name or f"Ad-{int(time.time())}",
            "adset_id": ad_set_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": status,
        }

        self._log(f"Creating ad (PAUSED): {ad_data['name']}")
        result = self._request("POST", f"/{self._account_id}/ads", data=ad_data)

        ad_id = result.get("id")
        if not ad_id:
            raise CreativeError(f"Ad creation failed: {result}")

        self._log(f"Ad created (PAUSED) — id: {ad_id}")
        return {"ad_id": ad_id}

    # --- Utility ---

    def get_ad_preview(self, creative_id, ad_format="DESKTOP_FEED_STANDARD"):
        """Get preview URL for a creative."""
        result = self._request(
            "GET",
            f"/{creative_id}/previews",
            data={"ad_format": ad_format},
        )
        previews = result.get("data", [])
        if previews:
            return previews[0].get("body", "")
        return ""

    def summary(self):
        """Return usage summary."""
        return {"calls_made": self.calls_made}
