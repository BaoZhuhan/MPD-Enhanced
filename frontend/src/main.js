import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL || "";

const icons = {
  mark: `<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M10 27V13l10-5 10 5v14l-10 5-10-5Z"/><path d="M15 24V16m5 11V13m5 11v-8"/></svg>`,
  upload: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 15v3a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3"/></svg>`,
  file: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l4 4v14H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z"/><path d="M14 3v5h5M9 13h6m-6 4h4"/></svg>`,
  spark: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3 1.3 4.1L17 9l-3.7 1.9L12 15l-1.3-4.1L7 9l3.7-1.9L12 3Z"/><path d="m18.5 14 .8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8.8-2.2Z"/></svg>`,
  arrow: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-5-5 5 5-5 5"/></svg>`,
  check: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4L19 6"/></svg>`,
  chevron: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>`,
};

const demoReport = {
  matches: [
    {
      rank: 1,
      score: 0.784,
      song_title: "Dreams of Tomorrow — The Echoes",
      test_time: 48.2,
      test_time2: 62.8,
      library_time: 91.4,
      library_time2: 106.0,
      confidence: "78.4%",
      time_match: "输入 00:48–01:03 ↔ 曲库 01:31–01:46",
      chroma_score: 0.762,
      timbre_boost: 1.041,
      lyrics_boost: 0.988,
    },
    {
      rank: 2,
      score: 0.536,
      song_title: "Midnight Signals — Nova",
      test_time: 72.1,
      test_time2: 86.7,
      library_time: 33.8,
      library_time2: 48.4,
      confidence: "53.6%",
      time_match: "输入 01:12–01:27 ↔ 曲库 00:34–00:48",
      chroma_score: 0.548,
      timbre_boost: 1.018,
      lyrics_boost: 0.961,
    },
    {
      rank: 3,
      score: 0.421,
      song_title: "Afterglow — Static Bloom",
      test_time: 16.6,
      test_time2: 31.2,
      library_time: 118.3,
      library_time2: 132.9,
      confidence: "42.1%",
      time_match: "输入 00:17–00:31 ↔ 曲库 01:58–02:13",
      chroma_score: 0.409,
      timbre_boost: 0.994,
      lyrics_boost: 1.036,
    },
  ],
  judgment: [
    {
      verdict: "存在值得关注的实质性相似",
      confidence: 72,
      reasoning:
        "最高匹配片段在连续四小节内呈现高度接近的音高轮廓与节奏重音。音色相似度对总分有轻微正向影响，但歌词证据不足，因此目前更适合视为旋律层面的中等风险，而非直接认定侵权。",
      relevant_case: "Skidmore v. Led Zeppelin (2020)",
    },
  ],
  risk_level: "Medium",
  analysis: "建议优先复核 00:48–01:03 的主旋律，并结合创作时间线与接触可能性进行人工判断。",
  message: "success",
};

let state = { screen: "home", file: null, report: null, error: "" };

function render() {
  document.querySelector("#app").innerHTML = `
    <div class="shell">
      ${header()}
      <main>${state.screen === "report" ? reportView() : homeView()}</main>
      ${footer()}
    </div>`;
  bindEvents();
}

function header() {
  return `<header class="topbar">
    <button class="brand" data-action="home" aria-label="返回首页">
      <span class="brand-mark">${icons.mark}</span>
      <span><strong>MPD</strong><em>Enhanced</em></span>
    </button>
    <div class="topbar-right">
      <span class="status"><i></i>分析服务在线</span>
      <button class="ghost-button" data-action="demo">查看示例报告 ${icons.arrow}</button>
    </div>
  </header>`;
}

function homeView() {
  return `<section class="hero">
    <div class="eyebrow"><span>${icons.spark}</span> AI 驱动的音乐相似性取证</div>
    <h1>听见相似，<br><span>看清依据。</span></h1>
    <p class="hero-copy">从旋律、音色与歌词三个维度定位相似片段，<br class="desktop-only">再由 AI 结合法律判例生成可解释的风险报告。</p>
    ${uploadCard()}
    <div class="trust-row">
      <span>多维交叉验证</span><i></i><span>片段级时间定位</span><i></i><span>法律判例辅助判断</span>
    </div>
    <div class="dimension-grid">
      ${dimension("01", "旋律", "Melody", "四小节滑动匹配，自动适应移调与速度变化。", "#b6ff66", "wave")}
      ${dimension("02", "音色", "Timbre", "提取 192 维人声特征，识别演唱音色相似度。", "#7ce8ff", "rings")}
      ${dimension("03", "歌词", "Lyrics", "融合语义、词序与编辑距离，量化文本重合。", "#c7a7ff", "bars")}
    </div>
  </section>`;
}

function uploadCard() {
  const file = state.file;
  return `<div class="upload-card ${file ? "has-file" : ""}" id="dropzone">
    <input type="file" id="fileInput" accept="audio/mpeg,audio/wav,audio/x-wav,audio/flac,.mp3,.wav,.flac,.m4a" hidden>
    <div class="upload-inner">
      <span class="upload-icon">${file ? icons.file : icons.upload}</span>
      <div class="upload-text">
        <strong>${file ? escapeHtml(file.name) : "拖入一首歌，开始分析"}</strong>
        <span>${file ? formatSize(file.size) + " · 已准备就绪" : "支持 MP3、WAV、FLAC，单个文件不超过 100 MB"}</span>
      </div>
      <button class="primary-button" data-action="${file ? "analyze" : "choose"}">
        ${file ? "开始分析" : "选择音频"} ${icons.arrow}
      </button>
    </div>
    ${state.error ? `<p class="error-message">${escapeHtml(state.error)}</p>` : ""}
  </div>`;
}

function dimension(index, title, en, copy, color, graphic) {
  return `<article class="dimension-card" style="--accent:${color}">
    <div class="dimension-head"><span>${index}</span><em>${en}</em></div>
    <div class="mini-graphic ${graphic}">${graphicMarkup(graphic)}</div>
    <h3>${title}</h3><p>${copy}</p>
  </article>`;
}

function graphicMarkup(type) {
  if (type === "wave") return `<svg viewBox="0 0 180 52"><path d="M0 28c13 0 13-18 26-18s13 32 26 32 13-25 26-25 13 18 26 18 13-29 26-29 13 26 26 26 13-14 24-14"/></svg>`;
  if (type === "rings") return `<span></span><span></span><span></span><span></span>`;
  return `<span style="height:32%"></span><span style="height:72%"></span><span style="height:48%"></span><span style="height:92%"></span><span style="height:58%"></span><span style="height:38%"></span><span style="height:76%"></span>`;
}

function loadingView(fileName) {
  document.querySelector("main").innerHTML = `<section class="loading-view">
    <div class="analysis-orbit"><span>${icons.mark}</span><i></i><i></i></div>
    <p class="loading-label">正在分析</p>
    <h2>${escapeHtml(fileName)}</h2>
    <p class="loading-copy" id="loadingCopy">正在分离音轨与提取节拍特征…</p>
    <div class="progress"><span id="progressBar"></span></div>
    <div class="steps">
      <span class="active"><i>${icons.check}</i>特征提取</span>
      <span><i>2</i>多维匹配</span>
      <span><i>3</i>AI 判定</span>
    </div>
  </section>`;
}

function reportView() {
  const report = normalizeReport(state.report || demoReport);
  const top = report.matches[0];
  const judgment = Array.isArray(report.judgment) ? report.judgment[0] : report.judgment;
  const risk = riskMeta(report.risk_level, top?.score || 0);
  return `<section class="report">
    <div class="report-heading">
      <div><button class="back-link" data-action="home">← 新建分析</button><p class="kicker">分析报告 · ${new Date().toLocaleDateString("zh-CN")}</p>
      <h1>${escapeHtml(state.file?.name || "示例音频.mp3")}</h1></div>
      <div class="risk-pill ${risk.className}"><span>${risk.label}</span><strong>${risk.cn}</strong></div>
    </div>

    <div class="summary-grid">
      <article class="score-card">
        <p>最高综合相似度</p><div class="big-score">${Math.round((top?.score || 0) * 100)}<small>%</small></div>
        <div class="score-track"><span style="width:${Math.round((top?.score || 0) * 100)}%"></span></div>
        <span class="muted">基于旋律主分与音色、歌词修正</span>
      </article>
      <article class="judgment-card">
        <div class="card-label"><span>${icons.spark}</span> AI 法律判定 <em>${judgment?.confidence || 0}% 置信度</em></div>
        <h2>${escapeHtml(judgment?.verdict || "暂无判定")}</h2>
        <p>${escapeHtml(judgment?.reasoning || report.analysis || "后端未返回判定说明。")}</p>
        ${judgment?.relevant_case ? `<div class="precedent">参考判例 <strong>${escapeHtml(judgment.relevant_case)}</strong></div>` : ""}
      </article>
    </div>

    <div class="section-title"><div><p>TOP MATCHES</p><h2>相似片段</h2></div><span>共返回 ${report.matches.length} 个候选结果</span></div>
    <div class="matches">${report.matches.map(matchCard).join("")}</div>
    <div class="notice"><strong>使用提示</strong><p>${escapeHtml(report.analysis || "本报告用于辅助筛查，不构成法律意见。最终判断需结合创作过程、作品接触可能性及专业人士复核。")}</p></div>
  </section>`;
}

function matchCard(match, index) {
  const score = Number(match.score || 0);
  const chroma = Math.round(Number(match.chroma_score ?? score) * 100);
  const timbre = boostText(match.timbre_boost);
  const lyrics = boostText(match.lyrics_boost);
  return `<article class="match-card ${index === 0 ? "top-match" : ""}">
    <div class="rank">${String(match.rank || index + 1).padStart(2, "0")}</div>
    <div class="match-info"><p>${index === 0 ? "最高匹配" : "候选匹配"}</p><h3>${escapeHtml(match.song_title || "未知曲目")}</h3><span>${escapeHtml(formatTimeMatch(match))}</span></div>
    <div class="metric"><span>旋律</span><strong>${chroma}%</strong><i><b style="width:${chroma}%"></b></i></div>
    <div class="boost"><span>音色</span><strong class="${timbre.className}">${timbre.value}</strong></div>
    <div class="boost"><span>歌词</span><strong class="${lyrics.className}">${lyrics.value}</strong></div>
    <div class="match-score"><strong>${Math.round(score * 100)}%</strong><span>综合相似度</span></div>
    <button class="round-button" aria-label="查看片段详情">${icons.chevron}</button>
  </article>`;
}

function footer() {
  return `<footer><span>© 2026 MPD Enhanced</span><span>研究用途 · 结果不构成法律意见</span></footer>`;
}

function bindEvents() {
  document.querySelectorAll("[data-action]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.stopPropagation();
      const action = button.dataset.action;
      if (action === "home") { state = { screen: "home", file: null, report: null, error: "" }; render(); }
      if (action === "demo") { state = { ...state, screen: "report", report: demoReport }; render(); }
      if (action === "choose") document.querySelector("#fileInput")?.click();
      if (action === "analyze") analyze();
    });
  });

  const input = document.querySelector("#fileInput");
  input?.addEventListener("change", () => selectFile(input.files?.[0]));
  const zone = document.querySelector("#dropzone");
  if (zone) {
    zone.addEventListener("click", () => { if (!state.file) input?.click(); });
    zone.addEventListener("dragover", (event) => { event.preventDefault(); zone.classList.add("dragging"); });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragging"));
    zone.addEventListener("drop", (event) => { event.preventDefault(); zone.classList.remove("dragging"); selectFile(event.dataTransfer.files?.[0]); });
  }
}

function selectFile(file) {
  if (!file) return;
  const valid = /\.(mp3|wav|flac|m4a)$/i.test(file.name);
  if (!valid) { state.error = "请选择 MP3、WAV、FLAC 或 M4A 音频文件。"; render(); return; }
  if (file.size > 100 * 1024 * 1024) { state.error = "音频文件不能超过 100 MB。"; render(); return; }
  state.file = file; state.error = ""; render();
}

async function analyze() {
  if (!state.file) return;
  loadingView(state.file.name);
  animateProgress();
  try {
    let report;
    if (API_URL) {
      const body = new FormData(); body.append("audio", state.file);
      const response = await fetch(API_URL, { method: "POST", body });
      if (!response.ok) throw new Error(`分析服务返回 ${response.status}`);
      const result = await response.json();
      if (result.success === false) throw new Error(result.error || "分析失败");
      report = result.data || result;
    } else {
      await delay(3100); report = demoReport;
    }
    state.report = report; state.screen = "report"; render();
  } catch (error) {
    state.screen = "home"; state.error = `${error.message}。请检查 VITE_API_URL 与后端服务。`; render();
  }
}

function animateProgress() {
  const texts = ["正在分离音轨与提取节拍特征…", "正在比对旋律、音色与歌词…", "正在结合判例生成风险判断…"];
  const bar = document.querySelector("#progressBar");
  const copy = document.querySelector("#loadingCopy");
  requestAnimationFrame(() => { if (bar) bar.style.width = "92%"; });
  texts.slice(1).forEach((text, index) => setTimeout(() => {
    if (copy) copy.textContent = text;
    document.querySelectorAll(".steps span").forEach((step, i) => step.classList.toggle("active", i <= index + 1));
  }, (index + 1) * 1050));
}

function normalizeReport(report) {
  return {
    matches: Array.isArray(report.matches) ? report.matches : [],
    judgment: report.judgment ?? report.llm_judgment ?? null,
    analysis: report.analysis ?? report.llm_analysis ?? "",
    risk_level: report.risk_level || "Unknown",
  };
}

function riskMeta(level, score) {
  const normalized = String(level || "").toLowerCase();
  if (normalized.includes("high")) return { label: "HIGH RISK", cn: "高风险", className: "high" };
  if (normalized.includes("medium")) return { label: "MEDIUM RISK", cn: "中等风险", className: "medium" };
  if (normalized.includes("low")) return { label: "LOW RISK", cn: "低风险", className: "low" };
  if (score >= 0.8) return { label: "HIGH RISK", cn: "高风险", className: "high" };
  if (score >= 0.6) return { label: "MEDIUM RISK", cn: "中等风险", className: "medium" };
  return { label: "LOW RISK", cn: "低风险", className: "low" };
}

function boostText(value) {
  if (value == null) return { value: "—", className: "neutral" };
  const delta = (Number(value) - 1) * 100;
  return { value: `${delta >= 0 ? "+" : ""}${delta.toFixed(1)}%`, className: delta >= 0 ? "positive" : "negative" };
}

function formatTimeMatch(match) {
  if (match.time_match) return match.time_match.replace("Input:", "输入").replace("Library:", "曲库");
  return `输入 ${formatTime(match.test_time)}–${formatTime(match.test_time2)} ↔ 曲库 ${formatTime(match.library_time)}–${formatTime(match.library_time2)}`;
}

function formatTime(seconds = 0) { const s = Math.round(seconds); return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`; }
function formatSize(bytes) { return bytes < 1024 * 1024 ? `${(bytes / 1024).toFixed(0)} KB` : `${(bytes / 1024 / 1024).toFixed(1)} MB`; }
function delay(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }
function escapeHtml(value) { return String(value ?? "").replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]); }

render();
