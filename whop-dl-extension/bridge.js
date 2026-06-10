// Content script — ISOLATED world, runs at document_start on Whop pages.
// Multiple capture strategies to find Mux m3u8 stream URLs.

const MUX_PATTERN = /https?:\/\/stream\.mux\.com\/[^\s"']+\.m3u8\?token=[^\s"']+/;
let found = false;

// === Strategy 1: Inject fetch/XHR interceptor into MAIN world ===
// Uses a script element to bypass ISOLATED world restrictions.
// May be blocked by CSP — that's OK, other strategies cover it.
try {
  const interceptCode = `(function() {
    var MUX_RE = /stream\\.mux\\.com\\/.*\\.m3u8.*token=/;
    function notify(url) {
      window.postMessage({ type: "__WHOP_GRABBER__", url: url }, "*");
    }
    var _fetch = window.fetch;
    window.fetch = function() {
      var url = typeof arguments[0] === "string" ? arguments[0] : (arguments[0] && arguments[0].url) || "";
      if (MUX_RE.test(url)) notify(url);
      return _fetch.apply(this, arguments);
    };
    var _open = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
      if (typeof url === "string" && MUX_RE.test(url)) notify(url);
      return _open.apply(this, arguments);
    };
  })();`;
  const s = document.createElement("script");
  s.textContent = interceptCode;
  (document.documentElement || document.head).appendChild(s);
  s.remove();
} catch (e) { /* CSP blocked — other strategies handle it */ }

// Listen for messages from MAIN world injector
window.addEventListener("message", (event) => {
  if (event.source !== window) return;
  if (event.data?.type !== "__WHOP_GRABBER__") return;
  if (event.data.url && !found) {
    found = true;
    sendToBackground(event.data.url);
  }
});

// === Strategy 2: DOM scanning ===
// Scan <video>, <source>, and <iframe> elements for Mux stream URLs.
// Also scans all element attributes and page HTML for the URL pattern.
function scanDOM() {
  if (found) return;

  // Check video/source elements
  const mediaEls = document.querySelectorAll("video, video source, iframe");
  for (const el of mediaEls) {
    const src = el.src || el.getAttribute("src") || "";
    if (MUX_PATTERN.test(src)) {
      found = true;
      sendToBackground(src.match(MUX_PATTERN)[0]);
      return;
    }
  }

  // Check for Mux player data attributes
  const muxPlayers = document.querySelectorAll("mux-player, mux-video, [data-mux-src]");
  for (const el of muxPlayers) {
    for (const attr of el.attributes) {
      if (MUX_PATTERN.test(attr.value)) {
        found = true;
        sendToBackground(attr.value.match(MUX_PATTERN)[0]);
        return;
      }
    }
  }

  // Brute scan: check all script tags and inline JSON for the URL
  const scripts = document.querySelectorAll("script:not([src])");
  for (const s of scripts) {
    const match = s.textContent.match(MUX_PATTERN);
    if (match) {
      found = true;
      sendToBackground(match[0]);
      return;
    }
  }
}

// === Strategy 3: MutationObserver ===
// Watch for dynamically added elements containing the URL.
const observer = new MutationObserver((mutations) => {
  if (found) { observer.disconnect(); return; }
  for (const mutation of mutations) {
    for (const node of mutation.addedNodes) {
      if (node.nodeType !== 1) continue; // element nodes only

      // Check the node itself
      const html = node.outerHTML || "";
      const match = html.match(MUX_PATTERN);
      if (match) {
        found = true;
        sendToBackground(match[0]);
        observer.disconnect();
        return;
      }
    }
  }
  // Also do a targeted scan after DOM changes
  scanDOM();
});

observer.observe(document.documentElement || document, {
  childList: true,
  subtree: true,
});

// === Strategy 4: Periodic DOM scan ===
// Fallback polling in case MutationObserver misses dynamically loaded content.
let pollCount = 0;
const poller = setInterval(() => {
  scanDOM();
  pollCount++;
  if (found || pollCount > 60) {
    clearInterval(poller);
    observer.disconnect();
  }
}, 2000);

// Also try PerformanceObserver (may not work cross-origin but worth trying)
try {
  const perfObserver = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (MUX_PATTERN.test(entry.name)) {
        found = true;
        sendToBackground(entry.name.match(MUX_PATTERN)[0]);
        perfObserver.disconnect();
        clearInterval(poller);
        observer.disconnect();
        return;
      }
    }
  });
  perfObserver.observe({ type: "resource", buffered: true });
} catch (e) { /* not supported */ }

function sendToBackground(url) {
  try {
    chrome.runtime.sendMessage({ type: "capturedFromPage", url });
  } catch (e) { /* extension context invalidated */ }
}
