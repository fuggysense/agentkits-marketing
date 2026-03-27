"""
Kleo.so API Client
==================
Reverse-engineered Python client for Kleo.so AI content generation APIs.
Focuses on: AI chat/generation endpoints, SSE streaming, and content tools.

Authentication: Cookie-based JWT (Clerk auth provider)
Base URL: https://app.kleo.so
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Generator, Optional

import requests

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("kleo_api")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_URL = "https://app.kleo.so"

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://app.kleo.so",
    "referer": "https://app.kleo.so/",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}


# ---------------------------------------------------------------------------
# KleoClient
# ---------------------------------------------------------------------------
class KleoClient:
    """
    HTTP client for the Kleo.so API.

    Authentication relies on Clerk session cookies obtained after logging in
    via the Kleo web application.  Copy the cookies from your browser's
    DevTools (Application → Cookies) and pass them to the constructor.

    Required cookies
    ----------------
    - ``__session``          – RS256-signed Clerk JWT (primary auth token)
    - ``__client_uat``       – Client user-auth timestamp
    - ``clerk_active_context`` – Active session context identifier

    Optional (but recommended for stability)
    ----------------------------------------
    - ``__session_5QoeSh33`` – Instance-specific duplicate of ``__session``
    - ``__client_uat_5QoeSh33`` – Instance-specific UAT
    - ``__refresh_5QoeSh33`` – Refresh token for Clerk session renewal
    """

    def __init__(self, cookies: dict[str, str]) -> None:
        """
        Initialise the client with Clerk session cookies.

        Parameters
        ----------
        cookies:
            Dictionary of cookie name → value pairs extracted from a logged-in
            browser session on app.kleo.so.
        """
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.cookies.update(cookies)
        logger.info("KleoClient initialised (base_url=%s)", BASE_URL)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{BASE_URL}{path}"

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        """
        Perform an authenticated GET request.

        Parameters
        ----------
        path:   API path (e.g. ``/api/profile``)
        params: Optional query-string parameters.

        Returns
        -------
        Parsed JSON response body.

        Raises
        ------
        requests.HTTPError on non-2xx responses.
        """
        url = self._url(path)
        logger.debug("GET %s params=%s", url, params)
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, body: dict) -> dict:
        """
        Perform an authenticated POST request (JSON body, non-streaming).

        Parameters
        ----------
        path: API path.
        body: Request body dict; will be serialised to JSON.

        Returns
        -------
        Parsed JSON response body.

        Raises
        ------
        requests.HTTPError on non-2xx responses.
        """
        url = self._url(path)
        logger.debug("POST %s body=%s", url, json.dumps(body)[:200])
        resp = self.session.post(url, json=body, timeout=60)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Streaming helpers
    # ------------------------------------------------------------------

    def _iter_sse_events(
        self, path: str, body: dict
    ) -> Generator[dict, None, None]:
        """
        POST to *path* with *body* and yield parsed SSE event dicts.

        Kleo's chat endpoint returns ``text/event-stream`` (Server-Sent
        Events).  Each line is prefixed with ``data: `` followed by a JSON
        object, or the sentinel ``data: [DONE]``.

        Yields
        ------
        Parsed event dicts, e.g.::

            {"type": "text-delta", "id": "0", "delta": "Hello "}

        Raises
        ------
        requests.HTTPError on non-2xx responses.
        """
        url = self._url(path)
        stream_headers = {**HEADERS, "accept": "text/event-stream"}
        logger.debug("POST (SSE) %s", url)

        with self.session.post(
            url,
            json=body,
            headers=stream_headers,
            stream=True,
            timeout=120,
        ) as resp:
            resp.raise_for_status()
            for raw_line in resp.iter_lines(decode_unicode=True):
                if not raw_line:
                    continue
                if raw_line.startswith("data: "):
                    payload = raw_line[6:]
                    if payload == "[DONE]":
                        logger.debug("SSE stream finished ([DONE])")
                        return
                    try:
                        yield json.loads(payload)
                    except json.JSONDecodeError:
                        logger.warning("Could not parse SSE line: %r", raw_line)

    # ------------------------------------------------------------------
    # AI / Chat endpoints
    # ------------------------------------------------------------------

    def stream_chat(
        self,
        user_message: str,
        conversation_id: Optional[str] = None,
        flow_type: str = "plan-post-idea",
        flow_step: str = "init",
        model: str = "chat-model",
        visibility: str = "private",
        post_length: str = "Medium",
        knowledge_base_ids: Optional[list[str]] = None,
        template_id: Optional[str] = None,
        template_name: Optional[str] = None,
        framework_id: Optional[str] = None,
        framework_name: Optional[str] = None,
        audience_id: Optional[str] = None,
        offer_id: Optional[str] = None,
        offer_name: Optional[str] = None,
        swipe_ids: Optional[list[str]] = None,
        my_story: bool = False,
        web_search_enabled: bool = True,
        preview_device: str = "mobile",
        title: str = "Plan post idea",
    ) -> Generator[dict, None, None]:
        """
        Stream an AI chat/generation response from Kleo.

        This wraps the ``POST /api/chat`` endpoint which returns an SSE
        stream of incremental text deltas and control events.

        Parameters
        ----------
        user_message:
            The user's prompt / instruction.
        conversation_id:
            UUID of an existing conversation document.  If omitted a new
            UUID is generated automatically.
        flow_type:
            The generation workflow.  Observed values:

            - ``"plan-post-idea"``  – brainstorm a post idea
            - Other flow types may exist but were not captured.
        flow_step:
            Step within the flow.  Common values: ``"init"``,
            ``"idea-submitted"``.
        model:
            Model identifier.  Only ``"chat-model"`` was observed in the
            recording.
        visibility:
            Post visibility setting (``"private"`` or ``"public"``).
        post_length:
            Target post length: ``"Short"``, ``"Medium"``, or ``"Long"``.
        knowledge_base_ids:
            List of knowledge-base UUIDs to include as context.
        template_id / template_name:
            Optional content template.
        framework_id / framework_name:
            Optional writing framework (e.g. ``"slay"`` /
            ``"SLAY (Lara Acosta)"``).
        audience_id:
            UUID of the target audience profile.
        offer_id / offer_name:
            UUID and display name of the product/service offer to reference.
        swipe_ids:
            List of swipe-file UUIDs for style inspiration.
        my_story:
            Whether to incorporate the user's personal story.
        web_search_enabled:
            Whether the AI may perform web searches.
        preview_device:
            Preview context (``"mobile"`` or ``"desktop"``).
        title:
            UI title for the conversation thread.

        Yields
        ------
        Parsed SSE event dicts.  Key event types:

        - ``{"type": "start", "messageId": "..."}``        – stream open
        - ``{"type": "text-delta", "id": "0", "delta": "…"}`` – text chunk
        - ``{"type": "finish", "finishReason": "stop"}``   – stream closed

        Example
        -------
        >>> for event in client.stream_chat("Give me a post idea about AI"):
        ...     if event.get("type") == "text-delta":
        ...         print(event["delta"], end="", flush=True)
        """
        conv_id = conversation_id or str(uuid.uuid4())
        msg_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        body: dict = {
            "id": conv_id,
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": user_message}],
                "metadata": {"createdAt": created_at},
                "id": msg_id,
            },
            "selectedChatModel": model,
            "selectedVisibilityType": visibility,
            "selectedKnowledgeBaseIds": knowledge_base_ids or [],
            "selectedTemplateId": template_id,
            "selectedFrameworkId": framework_id,
            "selectedAudienceId": audience_id,
            "selectedIdentity": {
                "myStory": my_story,
                "selectedOfferId": offer_id,
                "selectedOfferName": offer_name,
            },
            "postLength": post_length,
            "selectedSwipeIds": swipe_ids or [],
            "webSearchEnabled": web_search_enabled,
            "selectedTemplateName": template_name,
            "selectedFrameworkName": framework_name,
            "previewDevice": preview_device,
            "flowType": flow_type,
            "flowStep": flow_step,
            "title": title,
        }

        logger.info(
            "Streaming chat – conv_id=%s flow=%s/%s", conv_id, flow_type, flow_step
        )
        yield from self._iter_sse_events("/api/chat", body)

    def chat(
        self,
        user_message: str,
        **kwargs,
    ) -> str:
        """
        Convenience wrapper around :meth:`stream_chat` that collects all
        ``text-delta`` events and returns the full generated text.

        Parameters
        ----------
        user_message:
            The user's prompt.
        **kwargs:
            Forwarded to :meth:`stream_chat`.

        Returns
        -------
        The complete AI-generated text as a single string.

        Example
        -------
        >>> text = client.chat("Give me 3 LinkedIn post ideas about productivity")
        >>> print(text)
        """
        parts: list[str] = []
        for event in self.stream_chat(user_message, **kwargs):
            if event.get("type") == "text-delta":
                parts.append(event.get("delta", ""))
            elif event.get("type") == "finish":
                logger.info("Chat finished – reason=%s", event.get("finishReason"))
        return "".join(parts)

    def regenerate_line(
        self,
        document_id: str,
        full_content: str,
        selected_line: str,
        regen_type: str = "angle",
        device_type: str = "mobile",
        selected_html: str = "",
    ) -> dict:
        """
        Regenerate a specific line/phrase within an existing document.

        Calls ``POST /api/regenerate-line``.

        Parameters
        ----------
        document_id:
            UUID of the document containing the line.
        full_content:
            The entire document text (used as context for generation).
        selected_line:
            The exact line/phrase to be regenerated.
        regen_type:
            Regeneration style hint.  Observed value: ``"angle"``.
        device_type:
            Preview context (``"mobile"`` or ``"desktop"``).
        selected_html:
            HTML representation of the selected region (may be empty).

        Returns
        -------
        Dict with keys:

        - ``regeneratedLine`` – the newly generated replacement text
        - ``original``        – the original selected line

        Example
        -------
        >>> result = client.regenerate_line(
        ...     document_id="f1dbef3a-...",
        ...     full_content="Full post text here...",
        ...     selected_line=" no motivation. no discipline. ",
        ... )
        >>> print(result["regeneratedLine"])
        no willpower. no routine.
        """
        body = {
            "documentId": document_id,
            "fullContent": full_content,
            "selectedLine": selected_line,
            "selectedHtml": selected_html,
            "type": regen_type,
            "deviceType": device_type,
        }
        logger.info("Regenerating line in document %s", document_id)
        return self._post("/api/regenerate-line", body)

    # ------------------------------------------------------------------
    # Visual generation
    # ------------------------------------------------------------------

    def check_visuals(self) -> dict:
        """
        Check whether a visual generation is currently active.

        Calls ``GET /api/visuals/check``.

        Returns
        -------
        Dict indicating active generation status, e.g.
        ``{"hasActiveGeneration": false}``.
        """
        return self._get("/api/visuals/check")

    def generate_visual(self, document_id: str, visual_id: str) -> dict:
        """
        Trigger visual generation for a document.

        Calls ``GET /api/visuals/generate`` with query parameters.

        Parameters
        ----------
        document_id:
            UUID of the document to generate visuals for.
        visual_id:
            Visual template/style ID.

        Returns
        -------
        Dict with generation status, e.g. ``{"hasActiveGeneration": false}``.
        """
        logger.info(
            "Generating visual for document=%s visual=%s", document_id, visual_id
        )
        return self._get(
            "/api/visuals/generate",
            params={"documentId": document_id, "id": visual_id},
        )

    # ------------------------------------------------------------------
    # User & profile endpoints
    # ------------------------------------------------------------------

    def get_profile(self) -> dict:
        """
        Retrieve the authenticated user's profile.

        Returns
        -------
        User profile dict.
        """
        return self._get("/api/profile")

    def get_credits(self) -> dict:
        """
        Retrieve the user's remaining AI credits.

        Returns
        -------
        Credits information dict.
        """
        return self._get("/api/user/credits")

    def get_offers(self) -> dict:
        """
        Retrieve the user's product/service offers configured in Kleo.

        Returns
        -------
        Offers list dict.
        """
        return self._get("/api/user/offers")

    def get_story_status(self) -> dict:
        """Return the status of the user's 'My Story' setup."""
        return self._get("/api/user/story-status")

    def get_theme_settings(self) -> dict:
        """Return the user's visual theme settings."""
        return self._get("/api/user/theme-settings")

    # ------------------------------------------------------------------
    # Content library endpoints
    # ------------------------------------------------------------------

    def get_knowledge_base(
        self, limit: int = 5, offset: int = 0
    ) -> dict:
        """
        Retrieve knowledge-base entries.

        Parameters
        ----------
        limit:  Maximum number of entries to return (default 5).
        offset: Pagination offset (default 0).

        Returns
        -------
        Knowledge-base entries dict.
        """
        return self._get(
            "/api/knowledge-base", params={"limit": limit, "offset": offset}
        )

    def get_swipe_files(
        self,
        limit: int = 5,
        page: int = 1,
        folder_id: str = "root",
    ) -> dict:
        """
        Retrieve saved swipe-file examples (style inspiration).

        Parameters
        ----------
        limit:     Results per page (default 5).
        page:      Page number (default 1).
        folder_id: Folder filter (default ``"root"``).

        Returns
        -------
        Swipe files dict.
        """
        return self._get(
            "/api/swipe-files",
            params={"limit": limit, "page": page, "folderId": folder_id},
        )

    def get_swipe_folders(self) -> dict:
        """Return all swipe-file folder structure."""
        return self._get("/api/swipe-folders")

    def get_templates(self) -> dict:
        """Return available content templates."""
        return self._get("/api/templates")

    def get_audiences(self) -> dict:
        """Return configured target audience profiles."""
        return self._get("/api/audiences")

    # ------------------------------------------------------------------
    # History & status
    # ------------------------------------------------------------------

    def get_history(self, limit: int = 20) -> dict:
        """
        Retrieve the user's recent content generation history.

        Parameters
        ----------
        limit: Maximum number of history entries (default 20).

        Returns
        -------
        History list dict.
        """
        return self._get("/api/history", params={"limit": limit})

    def get_document(self, document_id: str) -> dict:
        """
        Retrieve a specific document by ID.

        Parameters
        ----------
        document_id: UUID of the document.

        Returns
        -------
        Document dict.
        """
        return self._get("/api/document", params={"id": document_id})

    def get_gemini_status(self) -> dict:
        """Return the operational status of the Gemini AI backend."""
        return self._get("/api/status/gemini")

    def get_user_progress(self) -> dict:
        """Return the user's onboarding/feature progress."""
        return self._get("/api/user-progress")


# ---------------------------------------------------------------------------
# Example usage / quick test
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Demonstrate basic usage of the KleoClient.

    ⚠️  Replace the cookie values below with your own session cookies from
    a logged-in browser session on app.kleo.so.

    How to obtain cookies
    ---------------------
    1. Open app.kleo.so in Chrome/Firefox.
    2. Log in to your account.
    3. Open DevTools → Application → Storage → Cookies → https://app.kleo.so
    4. Copy the values for the cookies listed below.
    """

    # ------------------------------------------------------------------
    # ❗ REPLACE THESE WITH YOUR OWN COOKIE VALUES ❗
    # ------------------------------------------------------------------
    cookies = {
        "__session": "YOUR_SESSION_JWT_HERE",
        "__client_uat": "YOUR_CLIENT_UAT_HERE",
        "clerk_active_context": "YOUR_ACTIVE_CONTEXT_HERE",
        # Optional but recommended:
        # "__refresh_5QoeSh33": "YOUR_REFRESH_TOKEN_HERE",
    }
    # ------------------------------------------------------------------

    if cookies["__session"] == "YOUR_SESSION_JWT_HERE":
        print(
            "⚠️  Please set your Kleo session cookies in the `cookies` dict "
            "inside main() before running.\n"
            "See the docstring above for instructions."
        )
        return

    client = KleoClient(cookies=cookies)

    # ── 1. Check user profile ──────────────────────────────────────────
    print("Fetching profile...")
    try:
        profile = client.get_profile()
        print(f"  Profile: {json.dumps(profile, indent=2)[:300]}")
    except requests.HTTPError as exc:
        print(f"  ❌ Profile fetch failed: {exc}")

    # ── 2. Check AI credits ───────────────────────────────────────────
    print("\nFetching credits...")
    try:
        credits = client.get_credits()
        print(f"  Credits: {json.dumps(credits, indent=2)}")
    except requests.HTTPError as exc:
        print(f"  ❌ Credits fetch failed: {exc}")

    # ── 3. Stream a chat completion ───────────────────────────────────
    print("\nStreaming AI chat response...")
    try:
        print("  Response: ", end="", flush=True)
        full_text = client.chat(
            user_message="Give me 3 short LinkedIn post ideas about productivity",
            flow_type="plan-post-idea",
            flow_step="init",
            post_length="Short",
            web_search_enabled=False,
        )
        print(full_text)
    except requests.HTTPError as exc:
        print(f"\n  ❌ Chat failed: {exc}")

    # ── 4. Regenerate a line (requires a real document UUID) ──────────
    # Uncomment and fill in a real document_id from your Kleo history:
    #
    # print("\nRegenerating a line...")
    # try:
    #     result = client.regenerate_line(
    #         document_id="YOUR-DOCUMENT-UUID",
    #         full_content="Your full post text here...",
    #         selected_line=" no motivation. no discipline. ",
    #     )
    #     print(f"  Original:    {result['original']!r}")
    #     print(f"  Regenerated: {result['regeneratedLine']!r}")
    # except requests.HTTPError as exc:
    #     print(f"  ❌ Regenerate failed: {exc}")

    print("\n✅ Done.")


if __name__ == "__main__":
    main()
