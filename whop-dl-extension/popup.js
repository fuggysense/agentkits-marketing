const storage = chrome.storage.session || chrome.storage.local;

const statusEl = document.getElementById("status");
const statusText = document.getElementById("status-text");
const urlDisplay = document.getElementById("url-display");
const urlText = document.getElementById("url-text");
const timestampEl = document.getElementById("timestamp");
const manualSection = document.getElementById("manual-section");
const manualInput = document.getElementById("manual-url");
const btnUseUrl = document.getElementById("btn-use-url");
const progressSection = document.getElementById("progress-section");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");
const transcriptSection = document.getElementById("transcript-section");
const transcriptText = document.getElementById("transcript-text");
const btnTranscribe = document.getElementById("btn-transcribe");
const btnCopy = document.getElementById("btn-copy");
const btnDownload = document.getElementById("btn-download");
const btnClear = document.getElementById("btn-clear");

let capturedUrl = null;

function showToast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg || "Copied!";
  el.classList.remove("hidden");
  el.style.animation = "none";
  el.offsetHeight;
  el.style.animation = "";
  setTimeout(() => el.classList.add("hidden"), 1600);
}

function timeAgo(ts) {
  const diff = Math.floor((Date.now() - ts) / 1000);
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  return `${Math.floor(diff / 3600)}h ago`;
}

function renderUrl(data) {
  if (data.capturedUrl) {
    capturedUrl = data.capturedUrl;
    statusEl.className = "status captured";
    statusText.textContent = "Stream captured!";
    urlDisplay.classList.remove("hidden");
    manualSection.classList.add("hidden");
    try {
      const url = new URL(capturedUrl);
      urlText.textContent = `${url.origin}${url.pathname}?token=...`;
    } catch {
      urlText.textContent = capturedUrl.substring(0, 60) + "...";
    }
    timestampEl.textContent = data.capturedAt
      ? `Captured ${timeAgo(data.capturedAt)}`
      : "";
  } else {
    capturedUrl = null;
    statusEl.className = "status listening";
    statusText.textContent = "Play a video — or paste URL below";
    urlDisplay.classList.add("hidden");
    manualSection.classList.remove("hidden");
  }
}

function renderJob(data) {
  const status = data.jobStatus;
  const result = data.jobResult;

  if (status === "processing") {
    progressSection.classList.remove("hidden");
    progressFill.style.background = "";
    progressFill.className = "progress-fill processing";
    progressText.textContent = "Downloading & transcribing... (check terminal for progress)";
    btnTranscribe.disabled = true;
    btnDownload.disabled = true;
    return;
  }

  if (status === "error" && result) {
    progressSection.classList.remove("hidden");
    progressFill.className = "progress-fill";
    progressFill.style.width = "100%";
    progressFill.style.background = "#ef4444";
    progressText.textContent = result.error;
    btnTranscribe.disabled = false;
    btnDownload.disabled = false;
    return;
  }

  if (status === "done" && result) {
    progressSection.classList.remove("hidden");
    progressFill.className = "progress-fill done";
    progressText.textContent = "Done!";
    btnTranscribe.disabled = false;
    btnDownload.disabled = false;

    if (result.transcript) {
      transcriptSection.classList.remove("hidden");
      transcriptText.value = result.transcript;
      btnCopy.classList.remove("hidden");
    }
    return;
  }

  // No job running
  btnTranscribe.disabled = !capturedUrl;
  btnDownload.disabled = !capturedUrl;
  btnClear.disabled = !capturedUrl;
}

function loadState() {
  storage.get(["capturedUrl", "capturedAt", "jobStatus", "jobResult"], (data) => {
    renderUrl(data);
    renderJob(data);
  });
}

// Load on popup open
loadState();

// Auto-update when anything changes in storage
chrome.storage.onChanged.addListener(() => loadState());

// Start transcription via background worker
function startJob(action) {
  if (!capturedUrl) return;
  storage.remove(["jobStatus", "jobResult"]);
  chrome.runtime.sendMessage({
    type: "startTranscription",
    url: capturedUrl,
    action,
  });
  // Show progress immediately
  progressSection.classList.remove("hidden");
  progressFill.className = "progress-fill processing";
  progressText.textContent = "Starting...";
  btnTranscribe.disabled = true;
  btnDownload.disabled = true;
}

// Manual URL input
btnUseUrl.addEventListener("click", () => {
  const url = manualInput.value.trim();
  if (!url) return;
  if (!url.includes(".m3u8")) {
    showToast("Not a valid m3u8 URL");
    return;
  }
  storage.set({ capturedUrl: url, capturedAt: Date.now(), tabId: -1 });
  chrome.action.setBadgeText({ text: "✓" });
  chrome.action.setBadgeBackgroundColor({ color: "#22c55e" });
  showToast("URL saved!");
});

manualInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") btnUseUrl.click();
});

btnTranscribe.addEventListener("click", () => startJob("transcribe"));
btnDownload.addEventListener("click", () => startJob("download"));

btnCopy.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(transcriptText.value);
    showToast("Copied!");
  } catch (e) {
    console.error("Clipboard write failed:", e);
  }
});

btnClear.addEventListener("click", () => {
  storage.remove(["capturedUrl", "capturedAt", "tabId", "jobStatus", "jobResult"]);
  chrome.action.setBadgeText({ text: "" });
  progressSection.classList.add("hidden");
  transcriptSection.classList.add("hidden");
  btnCopy.classList.add("hidden");
  loadState();
});
