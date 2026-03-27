# Kleo.so API Client

Reverse-engineered Python client for [Kleo.so](https://app.kleo.so) — an AI-powered personal brand and LinkedIn content tool.

---

## APIs Discovered

| Endpoint | Method | Description |
|---|---|---|
| `/api/chat` | POST | **Main AI generation endpoint** — returns a streaming SSE response with incremental text deltas |
| `/api/regenerate-line` | POST | Regenerate a specific line within an existing document |
| `/api/visuals/generate` | GET | Trigger AI visual generation for a document |
| `/api/visuals/check` | GET | Check whether a visual generation job is active |
| `/api/profile` | GET | Authenticated user profile |
| `/api/user/credits` | GET | Remaining AI generation credits |
| `/api/user/offers` | GET | Product/service offers configured in Kleo |
| `/api/user/story-status` | GET | Status of the user's "My Story" setup |
| `/api/user/theme-settings` | GET | Visual theme/branding settings |
| `/api/knowledge-base` | GET | Paginated knowledge-base entries |
| `/api/swipe-files` | GET | Saved swipe-file examples for style inspiration |
| `/api/swipe-folders` | GET | Swipe-file folder structure |
| `/api/templates` | GET | Available content templates |
| `/api/audiences` | GET | Target audience profiles |
| `/api/history` | GET | Recent content generation history |
| `/api/document` | GET | Retrieve a document by UUID |
| `/api/status/gemini` | GET | Gemini AI backend operational status |
| `/api/user-progress` | GET | Onboarding and feature progress |

---

## How Authentication Works

Kleo uses **[Clerk](https://clerk.com)** as its authentication provider.
Authentication is entirely **cookie-based** — no `Authorization: Bearer` headers are sent to the Kleo API.

### Required Cookies

| Cookie Name | Description |
|---|---|
| `__session` | RS256-signed Clerk JWT (primary auth token). Contains user ID, email, subscription status, etc. |
| `__client_uat` | Client user-auth Unix timestamp |
| `clerk_active_context` | Active session context identifier (`sess_...`) |

### Optional (but recommended)

| Cookie Name | Description |
|---|---|
| `__session_5QoeSh33` | Instance-specific duplicate of `__session` |
| `__client_uat_5QoeSh33` | Instance-specific UAT |
| `__refresh_5QoeSh33` | Refresh token for session renewal |

### How to Obtain Cookies

1. Open [app.kleo.so](https://app.kleo.so) in Chrome or Firefox.
2. Log in to your Kleo account.
3. Open **DevTools** → **Application** → **Storage** → **Cookies** → `https://app.kleo.so`.
4. Copy the values for `__session`, `__client_uat`, and `clerk_active_context`.

> **Note:** The `__session` JWT expires (check the `exp` claim).
> When it expires, log in again and grab a fresh cookie.

---

## Installation

```bash
pip install requests
```

No other dependencies are required.

---

## Quick Start

```python
from api_client import KleoClient

cookies = {
    "__session": "eyJhbGci...",          # your JWT
    "__client_uat": "1774396494",
    "clerk_active_context": "sess_3BPh...",
}

client = KleoClient(cookies=cookies)

# Simple chat — returns full text
text = client.chat("Give me 3 LinkedIn post ideas about AI productivity")
print(text)
```

---

## Function Reference

### `stream_chat()` — Streaming AI generation

Calls `POST /api/chat` and yields SSE events as they arrive.

```python
for event in client.stream_chat(
    user_message="I want to write a post about morning routines",
    flow_type="plan-post-idea",
    flow_step="init",
    post_length="Medium",
    web_search_enabled=True,
):
    if event["type"] == "text-delta":
        print(event["delta"], end="", flush=True)
```

**Key parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_message` | `str` | required | The user's prompt |
| `conversation_id` | `str \| None` | auto-generated UUID | Conversation document UUID |
| `flow_type` | `str` | `"plan-post-idea"` | Generation workflow type |
| `flow_step` | `str` | `"init"` | Step within the workflow |
| `post_length` | `str` | `"Medium"` | `"Short"`, `"Medium"`, or `"Long"` |
| `knowledge_base_ids` | `list[str]` | `[]` | Knowledge-base UUIDs for context |
| `framework_id` / `framework_name` | `str \| None` | `None` | Writing framework (e.g. `"slay"`) |
| `audience_id` | `str \| None` | `None` | Target audience UUID |
| `offer_id` / `offer_name` | `str \| None` | `None` | Product/service offer reference |
| `web_search_enabled` | `bool` | `True` | Allow AI web search |

**SSE event types:**

| Event type | Description |
|---|---|
| `start` | Stream opened; includes `messageId` |
| `start-step` | A processing step began |
| `text-start` | Text generation started |
| `text-delta` | Incremental text chunk (`delta` field) |
| `text-end` | Text generation finished |
| `finish-step` | Processing step complete |
| `finish` | Stream closed; includes `finishReason` (`"stop"`) |

---

### `chat()` — Blocking AI generation

Convenience wrapper; collects all deltas and returns a single string.

```python
text = client.chat(
    "Give me a hook for a post about overcoming procrastination",
    flow_step="idea-submitted",
    post_length="Short",
)
print(text)
```

---

### `regenerate_line()` — Rewrite a specific line

```python
result = client.regenerate_line(
    document_id="f1dbef3a-ced6-472e-b035-cb88192c5153",
    full_content="Full document text goes here...",
    selected_line=" no motivation. no discipline. ",
    regen_type="angle",
)
print(result["regeneratedLine"])  # e.g. "no willpower. no routine."
print(result["original"])         # " no motivation. no discipline. "
```

---

### `generate_visual()` — Trigger visual generation

```python
status = client.generate_visual(
    document_id="f1dbef3a-ced6-472e-b035-cb88192c5153",
    visual_id="your-visual-template-id",
)
print(status)  # {"hasActiveGeneration": False}
```

---

### Utility endpoints

```python
profile  = client.get_profile()
credits  = client.get_credits()
offers   = client.get_offers()
history  = client.get_history(limit=10)
kb       = client.get_knowledge_base(limit=5, offset=0)
swipes   = client.get_swipe_files(limit=5, page=1)
doc      = client.get_document("f1dbef3a-...")
status   = client.get_gemini_status()
```

---

## Example: Full Content Generation Flow

```python
from api_client import KleoClient

client = KleoClient(cookies={...})

# 1. Check credits
credits = client.get_credits()
print("Credits:", credits)

# 2. Load your audiences and offers
audiences = client.get_audiences()
audience_id = audiences[0]["id"] if audiences else None

offers = client.get_offers()
offer_id   = offers[0]["id"]   if offers else None
offer_name = offers[0]["name"] if offers else None

# 3. Brainstorm ideas (streaming)
print("Ideas:\n")
for event in client.stream_chat(
    user_message="give me a few ideas",
    flow_type="plan-post-idea",
    flow_step="idea-submitted",
    audience_id=audience_id,
    offer_id=offer_id,
    offer_name=offer_name,
    post_length="Short",
):
    if event.get("type") == "text-delta":
        print(event["delta"], end="", flush=True)
print()

# 4. Regenerate a weak line (if you have a document UUID)
# result = client.regenerate_line(
#     document_id="...",
#     full_content="...",
#     selected_line=" weak phrase here ",
# )
# print("New line:", result["regeneratedLine"])
```

---

## Limitations & Requirements

- **Cookie expiry:** Clerk JWTs have a short TTL.  You will need to refresh them periodically by logging in again and extracting new cookie values.
- **No public API:** Kleo does not expose a documented public API; this client is based on reverse-engineered traffic and may break if Kleo changes its API.
- **Rate limiting:** Kleo enforces credit-based rate limits on generation endpoints.  Monitor `/api/user/credits` to avoid hitting limits.
- **Subscription required:** The `/api/chat` endpoint requires an active Kleo subscription (`subscriptionStatus: "active"` in the JWT payload).
- **LLM provider abstraction:** Kleo proxies requests to an LLM backend (observed: Gemini via `/api/status/gemini`).  No direct LLM provider API keys are exposed to the client.
- **Streaming:** The `/api/chat` endpoint uses HTTP/2 SSE.  Ensure your environment supports streaming HTTP responses (the `requests` library with `stream=True` handles this correctly).

---

## Discovered in HAR Recording

- **Recording date:** 2026-03-24
- **Total requests captured:** 1,071 (673 GET, 398 POST)
- **Auth provider:** Clerk (`clerk.kleo.so`)
- **Hosting:** Vercel (TLS 1.3)
- **LLM backend:** Gemini (inferred from `/api/status/gemini` and model routing)
