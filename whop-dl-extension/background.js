const storage = chrome.storage.session || chrome.storage.local;
const SERVER = "http://localhost:8765";

// Clear everything on extension install/reload
chrome.runtime.onInstalled.addListener(() => {
  storage.clear();
  chrome.action.setBadgeText({ text: "" });
});

function saveCapture(url, tabId) {
  // New URL = clear old job results
  storage.remove(["jobStatus", "jobResult"]);
  storage.set({
    capturedUrl: url,
    capturedAt: Date.now(),
    tabId: tabId || -1,
  });
  chrome.action.setBadgeText({ text: "✓" });
  chrome.action.setBadgeBackgroundColor({ color: "#22c55e" });
}

chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    const url = details.url;
    if (!url.includes("token=")) return;
    const path = new URL(url).pathname;
    const segments = path.split("/").filter(Boolean);
    if (segments.length > 2) return;
    saveCapture(url, details.tabId);
  },
  { urls: ["*://stream.mux.com/*.m3u8*"] }
);

chrome.runtime.onMessage.addListener((msg, sender) => {
  if ((msg.type === "capturedFromPage" || msg.type === "scanResult") && msg.url) {
    saveCapture(msg.url, sender.tab?.id || msg.tabId);
  }

  if (msg.type === "startTranscription") {
    storage.set({ jobStatus: "processing" });

    fetch(SERVER, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: msg.url, action: msg.action }),
    })
      .then((r) => r.json())
      .then((result) => {
        if (result.error) {
          storage.set({ jobStatus: "error", jobResult: result });
        } else {
          storage.set({ jobStatus: "done", jobResult: result });
          // Auto-copy transcript
          if (result.transcript) {
            chrome.action.setBadgeText({ text: "✓" });
            chrome.action.setBadgeBackgroundColor({ color: "#22c55e" });
          }
        }
      })
      .catch((e) => {
        const errMsg = e.message.includes("Failed to fetch")
          ? "Server not running. Start it: python3 server.py"
          : "Error: " + e.message;
        storage.set({ jobStatus: "error", jobResult: { error: errMsg } });
      });
  }
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
  if (changeInfo.status === "loading") {
    storage.get("tabId", (data) => {
      if (data.tabId === tabId) {
        storage.remove(["capturedUrl", "capturedAt", "tabId", "jobStatus", "jobResult"]);
        chrome.action.setBadgeText({ text: "" });
      }
    });
  }
});
