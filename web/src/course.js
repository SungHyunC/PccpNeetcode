(() => {
  "use strict";
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fmt = (n) => Math.round(n).toLocaleString("ko-KR");

  const store = {
    get(k, d) { try { const v = localStorage.getItem("mo:" + k); return v == null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem("mo:" + k, JSON.stringify(v)); } catch { /* 저장 불가 환경 */ } },
  };

  // ───────── 파이썬 하이라이트 ─────────
  const KW = "def|return|if|elif|else|for|while|in|not|and|or|is|None|True|False|import|from|as|class|lambda|yield|break|continue|pass|with|try|except|finally|raise|global|nonlocal|del|assert";
  const BUILTIN = "len|range|enumerate|zip|sorted|reversed|min|max|sum|abs|list|dict|set|tuple|int|str|float|bool|print|map|filter|any|all|ord|chr|divmod|isinstance|heapq|deque|Counter|defaultdict|bisect|heappush|heappop|heapify|inf";
  const TOK = new RegExp(`(#[^\\n]*)|("""[\\s\\S]*?"""|'''[\\s\\S]*?'''|"(?:\\\\.|[^"\\\\\\n])*"|'(?:\\\\.|[^'\\\\\\n])*')|\\b(\\d[\\d_]*(?:\\.\\d+)?)\\b|\\b(${KW})\\b|\\b(${BUILTIN})\\b`, "g");
  function hl(code) {
    let out = "", last = 0;
    code.replace(TOK, (m, cmt, str, num, kw, fn, idx) => {
      out += esc(code.slice(last, idx));
      out += `<span class="tk-${cmt ? "cmt" : str ? "str" : num ? "num" : kw ? "kw" : "fn"}">${esc(m)}</span>`;
      last = idx + m.length;
      return m;
    });
    return out + esc(code.slice(last));
  }
  $$("pre.code[data-code]").forEach((pre) => { pre.innerHTML = `<code>${hl(pre.dataset.code)}</code>`; });

  // ───────── 진도 ─────────
  const chapters = $$("section.chapter");
  let progress = store.get("progress", {});
  const chState = (id) => progress[id] || {};
  function markDone(id, part) {
    progress[id] = { ...chState(id), [part]: true };
    store.set("progress", progress);
    renderToc();
  }
  function ringClass(id) {
    const s = chState(id);
    const hasLab = !!$(`#${id} .lab`);
    const done = s.quiz && (!hasLab || s.lab);
    return done ? "full" : s.quiz || s.lab ? "half" : "";
  }
  function renderToc() {
    $("#toc-list").innerHTML = chapters.map((c) => `<li><a href="#${c.id}" data-ch="${c.id}"><span class="ring ${ringClass(c.id)}" aria-hidden="true"></span><span class="n">${c.dataset.num}</span><span>${esc(c.dataset.title)}</span></a></li>`).join("");
    const done = chapters.filter((c) => ringClass(c.id) === "full").length;
    $("#toc-total").textContent = `${done} / ${chapters.length} 장 완료`;
    $("#toc-meter").style.width = `${(done / chapters.length) * 100}%`;
    $("#top-prog").textContent = `${done}/${chapters.length} 완료`;
    chapters.forEach((c) => {
      const row = $(".done-row", c);
      if (!row) return;
      const s = chState(c.id);
      const hasLab = !!$(".lab", c);
      row.innerHTML = `<span class="ring ${ringClass(c.id)}"></span><span>퀴즈 ${s.quiz ? "✓" : "—"}${hasLab ? ` · 실습 ${s.lab ? "✓" : "—"}` : ""}</span>`;
    });
    if (currentCh) setCurrent(currentCh);
  }
  chapters.forEach((c) => { const d = document.createElement("div"); d.className = "done-row col"; c.appendChild(d); });
  let currentCh = null;
  function setCurrent(id) {
    currentCh = id;
    $$("#toc-list a").forEach((a) => a.classList.toggle("now", a.dataset.ch === id));
  }
  $("#reset-progress").addEventListener("click", (e) => {
    const b = e.currentTarget;
    if (b.dataset.armed) { progress = {}; store.set("progress", progress); renderToc(); b.textContent = "진도 초기화"; delete b.dataset.armed; return; }
    b.dataset.armed = "1"; b.textContent = "한 번 더 누르면 초기화";
    setTimeout(() => { b.textContent = "진도 초기화"; delete b.dataset.armed; }, 3000);
  });
  $("#toc-toggle").addEventListener("click", () => {
    const open = $("#toc").classList.toggle("open");
    $("#toc-toggle").setAttribute("aria-expanded", String(open));
  });
  $("#toc").addEventListener("click", (e) => { if (e.target.closest("a")) { $("#toc").classList.remove("open"); $("#toc-toggle").setAttribute("aria-expanded", "false"); } });

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) setCurrent(en.target.id); });
    }, { rootMargin: "-45% 0px -50% 0px" });
    chapters.forEach((c) => io.observe(c));
  }
  window.addEventListener("scroll", () => {
    const h = document.documentElement;
    const p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
    $("#readbar").style.width = `${p * 100}%`;
  }, { passive: true });

  // 히어로 카운터: 페이지를 연 뒤 경과 시간 × 10^7
  const t0 = performance.now();
  setInterval(() => { $("#op-counter").textContent = fmt(((performance.now() - t0) / 1000) * 1e7); }, 100);

  // ───────── 공통: 단계 재생기 ─────────
  const timers = new Set();
  function player(host, frames, draw) {
    let i = 0, timer = null;
    const ctl = document.createElement("div");
    ctl.className = "controls";
    ctl.innerHTML = `<button class="btn" data-a="first">처음</button><button class="btn" data-a="prev">이전</button><button class="btn primary" data-a="play">재생</button><button class="btn" data-a="next">다음</button><span class="pos"></span>`;
    host.appendChild(ctl);
    const playBtn = $('[data-a="play"]', ctl);
    const stop = () => { if (timer) { clearInterval(timer); timers.delete(timer); timer = null; } playBtn.textContent = "재생"; };
    const paint = () => { draw(frames[i], i, frames); $(".pos", ctl).textContent = `${i + 1} / ${frames.length}`; };
    ctl.addEventListener("click", (e) => {
      const a = e.target.dataset && e.target.dataset.a;
      if (!a) return;
      if (a === "first") { stop(); i = 0; }
      if (a === "prev") { stop(); i = Math.max(0, i - 1); }
      if (a === "next") { stop(); i = Math.min(frames.length - 1, i + 1); }
      if (a === "play") {
        if (timer) { stop(); return; }
        if (i >= frames.length - 1) i = 0;
        playBtn.textContent = "일시정지";
        timer = setInterval(() => { if (i >= frames.length - 1) { stop(); return; } i++; paint(); }, 600);
        timers.add(timer);
      }
      paint();
    });
    paint();
    return { destroy() { stop(); ctl.remove(); }, goto(k) { i = Math.max(0, Math.min(frames.length - 1, k)); paint(); } };
  }
  const parseNums = (s, max = 16) => s.split(/[^\d-]+/).filter((x) => x !== "" && x !== "-").map(Number).slice(0, max);
  const SUP = { "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "-": "⁻" };
  const sup = (n) => String(n).split("").map((c) => SUP[c] || c).join("");

  // ───────── 00 Big-O ─────────
  const WIDGETS = {};
  let bigoApi = null;
  WIDGETS.bigo = (fig) => {
    const log10fact = (n) => { if (n <= 1) return 0; if (n <= 200) { let s = 0; for (let k = 2; k <= n; k++) s += Math.log10(k); return s; } return n * Math.log10(n / Math.E) + 0.5 * Math.log10(2 * Math.PI * n); };
    const CLS = [
      ["O(log N)", (n) => Math.log10(Math.max(1, Math.log2(Math.max(n, 2))))],
      ["O(N)", (n) => Math.log10(n)],
      ["O(N log N)", (n) => Math.log10(n * Math.max(1, Math.log2(Math.max(n, 2))))],
      ["O(N²)", (n) => 2 * Math.log10(n)],
      ["O(2ᴺ)", (n) => n * Math.log10(2)],
      ["O(N!)", (n) => log10fact(n)],
    ];
    const opsLabel = (L) => { if (L < 4) return fmt(Math.pow(10, L)); if (L > 99) return `10${sup(Math.floor(L))}`; const e = Math.floor(L); const m = Math.pow(10, L - e); return `${m.toFixed(1)}×10${sup(e)}`; };
    const timeLabel = (L) => {
      const sec = Math.pow(10, L - 7);
      if (L - 7 > 17.6) return "우주 나이 초과";
      if (sec < 0.001) return "< 1ms";
      if (sec < 1) return `${Math.round(sec * 1000)}ms`;
      if (sec < 60) return `${sec.toFixed(sec < 10 ? 1 : 0)}초`;
      if (sec < 3600) return `${Math.round(sec / 60)}분`;
      if (sec < 86400) return `${Math.round(sec / 3600)}시간`;
      if (sec < 3.15e7) return `${Math.round(sec / 86400)}일`;
      const y = sec / 3.15e7;
      return y < 1e4 ? `${fmt(y)}년` : `10${sup(Math.floor(Math.log10(y)))}년`;
    };
    fig.innerHTML = `
      <div class="fig-title">입력 크기 N 에 따른 연산 횟수 <span class="try">슬라이더를 움직여 보세요</span></div>
      <div class="scroll-x"><svg viewBox="0 0 600 330" width="100%" style="min-width:320px;display:block" role="img" aria-label="복잡도별 연산 횟수 막대 그래프"></svg></div>
      <div class="row"><label for="bigo-n" class="small muted" style="white-space:nowrap">N =</label><b class="mono" id="bigo-nv" style="min-width:9ch"></b><input id="bigo-n" type="range" min="0" max="90" step="1" value="50" style="flex:1"></div>
      <figcaption>세로축은 로그 눈금입니다(한 칸 = 10배). 빨간 선이 파이썬의 1초(≈10⁷ 번). 선 아래 <b>초록</b>은 안전, 바로 위 <b>노랑</b>은 위험, 그 위 <b>빨강</b>은 시간 초과.</figcaption>`;
    const svg = $("svg", fig), slider = $("#bigo-n", fig);
    const W = 600, H = 330, L = 44, R = 12, T = 30, B = 52, YMAX = 20;
    const y = (v) => T + (H - T - B) * (1 - Math.min(v, YMAX) / YMAX);
    function draw(n) {
      $("#bigo-nv", fig).textContent = fmt(n);
      const bw = (W - L - R) / CLS.length;
      let s = "";
      for (let v = 0; v <= YMAX; v += 5) s += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--rule)" stroke-width="1"/><text x="${L - 6}" y="${y(v) + 4}" text-anchor="end" font-size="11" fill="var(--muted)">10${sup(v)}</text>`;
      CLS.forEach(([name, f], k) => {
        const v = f(n), x = L + k * bw + bw * 0.16, w = bw * 0.68;
        const color = v <= 7 ? "var(--ok)" : v <= 8 ? "var(--mark)" : "var(--red)";
        const top = y(v);
        s += `<rect x="${x}" y="${top}" width="${w}" height="${y(0) - top}" rx="3" fill="${color}"/>`;
        s += `<text x="${x + w / 2}" y="${Math.max(top - 16, 12)}" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">${v > YMAX ? "▲ " : ""}${opsLabel(v)}</text>`;
        s += `<text x="${x + w / 2}" y="${Math.max(top - 3, 25)}" text-anchor="middle" font-size="10.5" fill="var(--muted)">${timeLabel(v)}</text>`;
        s += `<text x="${x + w / 2}" y="${H - B + 18}" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--ink)">${name}</text>`;
      });
      s += `<line x1="${L}" x2="${W - R}" y1="${y(7)}" y2="${y(7)}" stroke="var(--red)" stroke-width="2" stroke-dasharray="6 4"/><text x="${L + 4}" y="${y(7) - 6}" text-anchor="start" font-size="11.5" font-weight="700" fill="var(--red)">파이썬 1초 ≈ 10⁷</text>`;
      s += `<text x="${L}" y="${H - 10}" font-size="11" fill="var(--muted)">연산 횟수 위 숫자 · 그 아래 예상 시간</text>`;
      svg.innerHTML = s;
    }
    const nFromSlider = () => Math.max(1, Math.round(Math.pow(10, slider.value / 10)));
    slider.addEventListener("input", () => draw(nFromSlider()));
    bigoApi = { setN(n) { slider.value = Math.round(Math.log10(n) * 10); draw(n); } };
    bigoApi.setN(100000);
  };

  // ───────── 01 해시 ─────────
  WIDGETS.hash = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">Two Sum: 해시맵이 짝을 기억하는 과정 <span class="try">숫자를 바꿔 보세요</span></div>
      <div class="row"><label for="h-nums" class="small muted">nums</label><input id="h-nums" type="text" value="3, 8, 11, 2, 7, 15" style="flex:1;min-width:140px"><label for="h-t" class="small muted">target</label><input id="h-t" type="number" value="9" style="width:80px"><button class="btn" id="h-go">적용</button></div>
      <div class="two">
        <div style="display:grid;gap:10px;min-width:0"><div class="scroll-x"><div class="ptrs" id="h-ptr"></div><div class="cells" id="h-cells"></div></div><div class="log" id="h-log"></div></div>
        <div style="display:grid;gap:10px;min-width:0"><div class="small muted">seen (값 → 인덱스)</div><div class="scroll-x"><table class="kv" id="h-kv"></table></div><div class="stats"><div class="stat"><b id="h-c1">0</b><span>해시 조회 횟수</span></div><div class="stat"><b id="h-c2">0</b><span>이중 반복이라면 비교 횟수</span></div></div></div>
      </div>`;
    let pl = null;
    const run = () => {
      if (pl) pl.destroy();
      const nums = parseNums($("#h-nums", fig).value, 14), t = +$("#h-t", fig).value;
      const frames = [], seen = new Map();
      let found = null;
      frames.push({ i: -1, seen: [], need: null, found: null, msg: `target = ${t}. 왼쪽부터 하나씩 봅니다.` });
      for (let i = 0; i < nums.length; i++) {
        const x = nums[i], need = t - x;
        if (seen.has(need)) { found = [seen.get(need), i]; frames.push({ i, seen: [...seen], need, found, msg: `nums[${i}] = ${x}, 필요한 짝 ${t} − ${x} = ${need} → seen 에 있음! 답 [${found}]` }); break; }
        frames.push({ i, seen: [...seen], need, found: null, msg: `nums[${i}] = ${x}, 필요한 짝 ${need} → seen 에 없음. ${x}:${i} 를 기록.` });
        seen.set(x, i);
      }
      if (!found) frames.push({ i: nums.length, seen: [...seen], need: null, found: null, msg: "끝까지 짝을 찾지 못했습니다." });
      const n = nums.length;
      pl = player(fig, frames, (f) => {
        $("#h-cells", fig).innerHTML = nums.map((x, k) => `<div class="cell ${f.found && f.found.includes(k) ? "good" : k === f.i ? "cur" : k < f.i ? "in" : ""}">${x}<small>${k}</small></div>`).join("");
        $("#h-ptr", fig).innerHTML = nums.map((_, k) => `<span>${k === f.i ? "i" : ""}</span>`).join("");
        $("#h-kv", fig).innerHTML = f.seen.length ? `<tr><th>값</th>${f.seen.map(([k]) => `<td class="${k === f.need ? "hit" : ""}">${k}</td>`).join("")}</tr><tr><th>인덱스</th>${f.seen.map(([, v]) => `<td>${v}</td>`).join("")}</tr>` : `<tr><td class="muted">비어 있음</td></tr>`;
        $("#h-log", fig).textContent = f.msg;
        const steps = Math.max(0, Math.min(f.i + 1, n));
        $("#h-c1", fig).textContent = steps;
        $("#h-c2", fig).textContent = fmt((steps * (steps - 1)) / 2 + (f.found ? 0 : 0));
      });
    };
    $("#h-go", fig).addEventListener("click", run);
    run();
  };

  // ───────── 02 슬라이딩 윈도우 ─────────
  WIDGETS.window = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">중복 문자 없는 가장 긴 구간 <span class="try">문자열을 바꿔 보세요</span></div>
      <div class="row"><label for="w-s" class="small muted">s</label><input id="w-s" type="text" value="pwwkewabca" maxlength="20" style="flex:1;min-width:120px"><button class="btn" id="w-go">적용</button></div>
      <div class="scroll-x"><div class="ptrs" id="w-ptr"></div><div class="cells" id="w-cells"></div></div>
      <div class="stats"><div class="stat"><b id="w-best">0</b><span>최고 길이</span></div><div class="stat"><b id="w-moves">0</b><span>l + r 이동 횟수 (≤ 2N)</span></div></div>
      <div class="log" id="w-log"></div>`;
    let pl = null;
    const run = () => {
      if (pl) pl.destroy();
      const s = [...$("#w-s", fig).value.slice(0, 20)];
      const frames = [], seen = new Set();
      let l = 0, best = 0, bestL = 0, moves = 0;
      s.forEach((ch, r) => {
        moves++;
        frames.push({ l, r, dup: seen.has(ch) ? s.indexOf(ch, l) : -1, best, bestL, moves, msg: `r = ${r}: '${ch}' 를 창에 넣으려 합니다.${seen.has(ch) ? " 이미 있음 → l 을 당깁니다." : ""}` });
        while (seen.has(ch)) {
          seen.delete(s[l]); l++; moves++;
          frames.push({ l, r, dup: seen.has(ch) ? s.indexOf(ch, l) : -1, best, bestL, moves, msg: `'${s[l - 1]}' 를 빼고 l = ${l}` });
        }
        seen.add(ch);
        if (r - l + 1 > best) { best = r - l + 1; bestL = l; }
        frames.push({ l, r, dup: -1, best, bestL, moves, msg: `창 [${l}, ${r}] = "${s.slice(l, r + 1).join("")}" 길이 ${r - l + 1}` });
      });
      if (!frames.length) frames.push({ l: 0, r: -1, dup: -1, best: 0, bestL: 0, moves: 0, msg: "빈 문자열" });
      pl = player(fig, frames, (f) => {
        $("#w-cells", fig).innerHTML = s.map((ch, k) => `<div class="cell ${k === f.dup ? "bad" : k >= f.l && k <= f.r ? "in" : "dim"}">${esc(ch)}<small>${k}</small></div>`).join("");
        $("#w-ptr", fig).innerHTML = s.map((_, k) => `<span>${[k === f.l ? "l" : "", k === f.r ? "r" : ""].filter(Boolean).join("/")}</span>`).join("");
        $("#w-best", fig).textContent = `${f.best} "${s.slice(f.bestL, f.bestL + f.best).join("")}"`;
        $("#w-moves", fig).textContent = `${f.moves} / ${2 * s.length}`;
        $("#w-log", fig).textContent = f.msg;
      });
    };
    $("#w-go", fig).addEventListener("click", run);
    run();
  };

  // ───────── 03 단조 스택 ─────────
  WIDGETS.stack = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">더 따뜻한 날까지 며칠? <span class="try">기온을 바꿔 보세요</span></div>
      <div class="row"><label for="s-t" class="small muted">기온</label><input id="s-t" type="text" value="73, 74, 75, 71, 69, 72, 76, 73" style="flex:1;min-width:160px"><button class="btn" id="s-go">적용</button></div>
      <div class="bars" id="s-bars"></div>
      <div class="scroll-x"><table class="kv" id="s-ans"></table></div>
      <div class="row small"><span class="muted">스택(대기실):</span><b class="mono" id="s-stack"></b></div>
      <div class="log" id="s-log"></div>
      <figcaption><b>노랑</b> 오늘, <b>파랑</b> 아직 답을 기다리는 날, <b>초록</b> 답을 찾은 날.</figcaption>`;
    let pl = null;
    const run = () => {
      if (pl) pl.destroy();
      const t = parseNums($("#s-t", fig).value, 14);
      const frames = [], ans = Array(t.length).fill(null), st = [];
      for (let i = 0; i < t.length; i++) {
        frames.push({ i, st: [...st], ans: [...ans], msg: `${i}일째 ${t[i]}도. 스택 맨 위와 비교합니다.` });
        while (st.length && t[st[st.length - 1]] < t[i]) {
          const j = st.pop(); ans[j] = i - j;
          frames.push({ i, st: [...st], ans: [...ans], msg: `${j}일째(${t[j]}도) < 오늘 ${t[i]}도 → pop, 답 ${i} − ${j} = ${i - j}일` });
        }
        st.push(i);
        frames.push({ i, st: [...st], ans: [...ans], msg: `${i}일째를 스택에 push. 스택의 기온은 위로 갈수록 낮아집니다.` });
      }
      frames.push({ i: -1, st: [...st], ans: ans.map((a) => (a == null ? 0 : a)), msg: `끝. 스택에 남은 날들은 더 따뜻한 날이 없으므로 0.` });
      const lo = Math.min(...t) - 3, hi = Math.max(...t);
      pl = player(fig, frames, (f) => {
        $("#s-bars", fig).innerHTML = t.map((x, k) => `<div class="b ${k === f.i ? "cur" : f.st.includes(k) ? "st" : f.ans[k] != null ? "done" : ""}" style="height:${12 + ((x - lo) / Math.max(1, hi - lo)) * 88}%"><span>${x}</span></div>`).join("");
        $("#s-ans", fig).innerHTML = `<tr><th>일</th>${t.map((_, k) => `<td>${k}</td>`).join("")}</tr><tr><th>답</th>${f.ans.map((a) => `<td>${a == null ? "" : a}</td>`).join("")}</tr>`;
        $("#s-stack", fig).textContent = `[${f.st.map((k) => `${k}(${t[k]}°)`).join(", ")}]`;
        $("#s-log", fig).textContent = f.msg;
      });
    };
    $("#s-go", fig).addEventListener("click", run);
    run();
  };

  // ───────── 04 이분 탐색 게임 ─────────
  WIDGETS.guess = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">1 ~ 1,000 숫자 맞히기 <span class="try">직접 추측하거나 이분 탐색에게 맡기세요</span></div>
      <div class="rangebar" aria-hidden="true"><i id="g-range"></i></div>
      <div class="row small muted"><span>남은 범위: <b class="mono" id="g-lohi"></b></span><span>시도: <b class="mono" id="g-tries">0</b></span></div>
      <div class="row"><label for="g-in" class="small muted">내 추측</label><input id="g-in" type="number" min="1" max="1000" style="width:110px"><button class="btn primary" id="g-try">추측</button><button class="btn" id="g-auto">이분 탐색이 한 번 추측</button><button class="btn" id="g-new">새 게임</button></div>
      <div class="log" id="g-log"></div>`;
    let secret, lo, hi, tries, history, over;
    const reset = () => { secret = 1 + Math.floor(Math.random() * 1000); lo = 1; hi = 1000; tries = 0; history = []; over = false; render("숫자를 하나 정했습니다. 가운데를 고르는 게 왜 좋은지 느껴 보세요."); };
    const render = (msg) => {
      $("#g-range", fig).style.left = `${((lo - 1) / 1000) * 100}%`;
      $("#g-range", fig).style.width = `${((hi - lo + 1) / 1000) * 100}%`;
      $("#g-lohi", fig).textContent = `${lo} ~ ${hi} (${hi - lo + 1}개)`;
      $("#g-tries", fig).textContent = tries;
      $("#g-log", fig).textContent = [msg, ...history.slice(-6).reverse()].join("\n");
    };
    const guess = (g, who) => {
      if (over || !Number.isFinite(g)) return;
      tries++;
      if (g === secret) { over = true; history.push(`${who} ${g} → 정답!`); render(`${tries}번 만에 맞혔습니다. 가운데만 고르면 1,000개 중에서도 최대 10번 (2¹⁰ = 1,024).`); return; }
      if (g < secret) { lo = Math.max(lo, g + 1); history.push(`${who} ${g} → 더 큼`); } else { hi = Math.min(hi, g - 1); history.push(`${who} ${g} → 더 작음`); }
      render(`남은 후보 ${hi - lo + 1}개.`);
    };
    $("#g-try", fig).addEventListener("click", () => guess(Math.round(+$("#g-in", fig).value), "나:"));
    $("#g-in", fig).addEventListener("keydown", (e) => { if (e.key === "Enter") guess(Math.round(+$("#g-in", fig).value), "나:"); });
    $("#g-auto", fig).addEventListener("click", () => guess(Math.floor((lo + hi) / 2), "이분 탐색:"));
    $("#g-new", fig).addEventListener("click", reset);
    reset();
  };

  WIDGETS.parametric = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">입국심사: T 분이면 몇 명? <span class="try">T 를 움직이고, 이분 탐색을 한 단계씩 실행해 보세요</span></div>
      <div class="row"><label for="p-times" class="small muted">심사 시간</label><input id="p-times" type="text" value="7, 10" style="width:120px"><label for="p-n" class="small muted">인원 n</label><input id="p-n" type="number" value="6" min="1" max="15" style="width:70px"><button class="btn" id="p-go">적용</button></div>
      <div class="pstrip" id="p-strip" aria-hidden="true"></div>
      <div class="row"><label for="p-T" class="small muted">T</label><input id="p-T" type="range" min="0" max="60" value="20" style="flex:1"></div>
      <div class="log" id="p-read"></div>
      <div class="row"><button class="btn primary" id="p-step">이분 탐색 한 단계</button><button class="btn" id="p-reset">처음부터</button></div>
      <div class="log" id="p-log"></div>
      <figcaption>칸 하나가 시각 T 입니다. <b>빨강</b> = n 명을 못 끝냄, <b>초록</b> = 끝냄. 경계가 딱 한 번만 바뀌기 때문에 이분 탐색이 가능합니다. 파란 밑줄이 현재 [lo, hi].</figcaption>`;
    let times, n, maxT, lo, hi, logs, done;
    const served = (T) => times.reduce((s, t) => s + Math.floor(T / t), 0);
    const setup = () => {
      times = parseNums($("#p-times", fig).value, 4).filter((x) => x > 0).map((x) => Math.min(x, 30));
      if (!times.length) times = [7, 10];
      n = Math.max(1, Math.min(15, Math.round(+$("#p-n", fig).value) || 6));
      maxT = Math.min(240, Math.max(...times) * n);
      $("#p-T", fig).max = maxT;
      lo = 1; hi = maxT; logs = [`lo = 1, hi = ${maxT} (가장 느린 심사관 혼자 n 명을 다 하는 시간)`]; done = false;
      draw();
    };
    const draw = () => {
      const T = +$("#p-T", fig).value;
      $("#p-strip", fig).innerHTML = Array.from({ length: maxT + 1 }, (_, k) => `<i class="${served(k) >= n ? "y" : ""} ${k === T ? "at" : ""} ${k >= lo && k <= hi ? "lohi" : ""}"></i>`).join("");
      const parts = times.map((t) => `${T}//${t}=${Math.floor(T / t)}`).join(" + ");
      $("#p-read", fig).textContent = `T = ${T}분 → ${parts} = ${served(T)}명 ${served(T) >= n ? "≥" : "<"} ${n}명 ${served(T) >= n ? "✔ 가능" : "✘ 부족"}`;
      $("#p-log", fig).textContent = logs.slice(-5).join("\n");
    };
    $("#p-T", fig).addEventListener("input", draw);
    $("#p-go", fig).addEventListener("click", setup);
    $("#p-reset", fig).addEventListener("click", setup);
    $("#p-step", fig).addEventListener("click", () => {
      if (done) return;
      if (lo >= hi) { done = true; logs.push(`lo == hi == ${lo} → 답은 ${lo}분`); $("#p-T", fig).value = lo; draw(); return; }
      const mid = Math.floor((lo + hi) / 2), ok = served(mid) >= n;
      logs.push(`mid = ${mid}: ${served(mid)}명 → ${ok ? "가능, hi = mid" : "불가능, lo = mid + 1"}`);
      if (ok) hi = mid; else lo = mid + 1;
      $("#p-T", fig).value = mid;
      draw();
    });
    setup();
  };

  // ───────── 05 트리 ─────────
  WIDGETS.tree = (fig) => {
    const vals = [8, 3, 10, 1, 6, null, 14, null, null, 4, 7, 13];
    // 레벨 순서 배열 → 노드 목록
    const nodes = [];
    const root = { v: vals[0], d: 0, l: null, r: null };
    nodes.push(root);
    const q = [root]; let i = 1;
    while (q.length && i < vals.length) {
      const nd = q.shift();
      for (const side of ["l", "r"]) {
        if (i < vals.length && vals[i] != null) { const c = { v: vals[i], d: nd.d + 1, l: null, r: null }; nd[side] = c; nodes.push(c); q.push(c); }
        i++;
      }
    }
    let k = 0; (function inord(nd) { if (!nd) return; inord(nd.l); nd.x = k++; inord(nd.r); })(root);
    const orders = {
      pre: (() => { const o = []; (function f(nd) { if (!nd) return; o.push(nd); f(nd.l); f(nd.r); })(root); return o; })(),
      in: (() => { const o = []; (function f(nd) { if (!nd) return; f(nd.l); o.push(nd); f(nd.r); })(root); return o; })(),
      post: (() => { const o = []; (function f(nd) { if (!nd) return; f(nd.l); f(nd.r); o.push(nd); })(root); return o; })(),
      level: (() => { const o = [], qq = [root]; while (qq.length) { const nd = qq.shift(); o.push(nd); if (nd.l) qq.push(nd.l); if (nd.r) qq.push(nd.r); } return o; })(),
    };
    const NAMES = { pre: "전위 (나 → 왼 → 오)", in: "중위 (왼 → 나 → 오)", post: "후위 (왼 → 오 → 나)", level: "레벨 (BFS)" };
    fig.innerHTML = `
      <div class="fig-title">같은 트리, 네 가지 방문 순서 <span class="try">순서를 골라 재생해 보세요</span></div>
      <div class="row" id="t-modes">${Object.keys(NAMES).map((m) => `<button class="btn" data-m="${m}">${NAMES[m]}</button>`).join("")}</div>
      <div class="scroll-x"><svg viewBox="0 0 560 250" width="100%" style="min-width:320px;display:block" role="img" aria-label="이진 탐색 트리"></svg></div>
      <div class="log" id="t-log"></div>`;
    const svg = $("svg", fig);
    const X = (nd) => 40 + nd.x * (480 / (k - 1)), Y = (nd) => 36 + nd.d * 62;
    let pl = null, mode = "in";
    const draw = (step) => {
      const seq = orders[mode], visited = new Map(seq.slice(0, step + 1).map((nd, j) => [nd, j + 1]));
      let s = "";
      nodes.forEach((nd) => { for (const c of [nd.l, nd.r]) if (c) s += `<line x1="${X(nd)}" y1="${Y(nd)}" x2="${X(c)}" y2="${Y(c)}" stroke="var(--rule)" stroke-width="2"/>`; });
      nodes.forEach((nd) => {
        const vis = visited.get(nd), cur = seq[step] === nd;
        s += `<circle cx="${X(nd)}" cy="${Y(nd)}" r="19" fill="${cur ? "var(--mark)" : vis ? "var(--blue-soft)" : "var(--panel)"}" stroke="${cur ? "var(--red)" : vis ? "var(--blue)" : "var(--rule)"}" stroke-width="2"/>`;
        s += `<text x="${X(nd)}" y="${Y(nd) + 5}" text-anchor="middle" font-size="14" font-weight="700" fill="${cur ? "var(--mark-ink)" : "var(--ink)"}">${nd.v}</text>`;
        if (vis) s += `<text x="${X(nd) + 22}" y="${Y(nd) - 14}" font-size="11" font-weight="700" fill="var(--red)">${vis}</text>`;
      });
      svg.innerHTML = s;
      $("#t-log", fig).textContent = `${NAMES[mode]}: ${seq.slice(0, step + 1).map((nd) => nd.v).join(" → ")}${mode === "in" && step === seq.length - 1 ? "\nBST 의 중위 순회는 정렬된 순서입니다." : ""}`;
    };
    const pick = (m) => {
      mode = m;
      $$("#t-modes .btn", fig).forEach((b) => b.classList.toggle("on", b.dataset.m === m));
      if (pl) pl.destroy();
      const frames = orders[m].map((_, j) => j);
      pl = player(fig, frames, (j) => draw(j));
      pl.goto(frames.length - 1);
    };
    $$("#t-modes .btn", fig).forEach((b) => b.addEventListener("click", () => pick(b.dataset.m)));
    pick("in");
  };

  // ───────── 06 힙 ─────────
  WIDGETS.heap = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">최소 힙: 넣고 꺼내기 <span class="try">숫자를 넣거나 최솟값을 꺼내 보세요</span></div>
      <div class="row"><label for="hp-in" class="small muted">값</label><input id="hp-in" type="number" value="2" style="width:80px"><button class="btn primary" id="hp-push">heappush</button><button class="btn" id="hp-pop">heappop</button><button class="btn" id="hp-rand">무작위 값 넣기</button><button class="btn" id="hp-reset">초기화</button></div>
      <div class="scroll-x"><svg viewBox="0 0 560 230" width="100%" style="min-width:320px;display:block" role="img" aria-label="힙 트리"></svg></div>
      <div class="scroll-x"><div class="cells" id="hp-arr"></div></div>
      <div class="log" id="hp-log"></div>
      <figcaption>위의 트리와 아래 배열은 같은 데이터입니다. i 의 아이 = 2i+1, 2i+2. <b>노랑</b> 칸이 지금 자리를 바꾸는 두 값입니다.</figcaption>`;
    const svg = $("svg", fig);
    let h = [3, 8, 5, 10, 9, 12], busy = false;
    const pos = (i) => { const d = Math.floor(Math.log2(i + 1)), first = 2 ** d - 1, cnt = 2 ** d; return [((i - first + 0.5) / cnt) * 540 + 10, 30 + d * 58]; };
    const draw = (arr, hi = [], msg = "") => {
      let s = "";
      arr.forEach((_, i) => { if (i) { const [x1, y1] = pos(i), [x2, y2] = pos((i - 1) >> 1); s += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="var(--rule)" stroke-width="2"/>`; } });
      arr.forEach((v, i) => {
        const [x, y] = pos(i), on = hi.includes(i);
        s += `<circle cx="${x}" cy="${y}" r="17" fill="${on ? "var(--mark)" : i === 0 ? "var(--ok-soft)" : "var(--panel)"}" stroke="${on ? "var(--red)" : i === 0 ? "var(--ok)" : "var(--rule)"}" stroke-width="2"/><text x="${x}" y="${y + 5}" text-anchor="middle" font-size="13" font-weight="700" fill="${on ? "var(--mark-ink)" : "var(--ink)"}">${v}</text>`;
      });
      svg.innerHTML = s || `<text x="280" y="110" text-anchor="middle" fill="var(--muted)" font-size="14">빈 힙</text>`;
      $("#hp-arr", fig).innerHTML = arr.map((v, i) => `<div class="cell ${hi.includes(i) ? "cur" : ""}">${v}<small>${i}</small></div>`).join("");
      if (msg) $("#hp-log", fig).textContent = msg;
    };
    const animate = (frames, end) => {
      busy = true;
      let k = 0;
      const tick = () => {
        const f = frames[k];
        draw(f.arr, f.hi, f.msg);
        k++;
        if (k < frames.length) { const t = setTimeout(tick, reduceMotion ? 0 : 520); timers.add(t); } else { busy = false; if (end) end(); }
      };
      tick();
    };
    const push = (v) => {
      if (busy || !Number.isFinite(v)) return;
      if (h.length >= 15) { $("#hp-log", fig).textContent = "그림이 넘치지 않도록 15개까지만 넣을 수 있습니다. 하나 꺼내 보세요."; return; }
      const a = [...h, v], frames = [{ arr: [...a], hi: [a.length - 1], msg: `${v} 를 맨 끝(인덱스 ${a.length - 1})에 붙입니다.` }];
      let i = a.length - 1, swaps = 0;
      while (i > 0 && a[(i - 1) >> 1] > a[i]) {
        const p = (i - 1) >> 1;
        frames.push({ arr: [...a], hi: [i, p], msg: `부모 ${a[p]} > ${a[i]} → 자리 바꿈` });
        [a[i], a[p]] = [a[p], a[i]]; i = p; swaps++;
      }
      frames.push({ arr: [...a], hi: [i], msg: `제자리. 교환 ${swaps}번 (높이 ≈ log₂${a.length} ≈ ${Math.log2(a.length).toFixed(1)})` });
      animate(frames, () => { h = a; });
    };
    const pop = () => {
      if (busy) return;
      if (!h.length) { $("#hp-log", fig).textContent = "힙이 비어 있습니다."; return; }
      const a = [...h], min = a[0], frames = [{ arr: [...a], hi: [0], msg: `맨 위 ${min} 이 최솟값. 꺼냅니다.` }];
      const last = a.pop();
      if (a.length) {
        a[0] = last;
        frames.push({ arr: [...a], hi: [0], msg: `맨 끝 값 ${last} 를 맨 위로 옮깁니다.` });
        let i = 0;
        for (;;) {
          const l = 2 * i + 1, r = l + 1;
          let m = i;
          if (l < a.length && a[l] < a[m]) m = l;
          if (r < a.length && a[r] < a[m]) m = r;
          if (m === i) break;
          frames.push({ arr: [...a], hi: [i, m], msg: `더 작은 아이 ${a[m]} 와 자리 바꿈` });
          [a[i], a[m]] = [a[m], a[i]]; i = m;
        }
        frames.push({ arr: [...a], hi: [i], msg: `제자리. 꺼낸 값 = ${min}` });
      } else frames.push({ arr: [], hi: [], msg: `꺼낸 값 = ${min}. 힙이 비었습니다.` });
      animate(frames, () => { h = a; });
    };
    $("#hp-push", fig).addEventListener("click", () => push(Math.round(+$("#hp-in", fig).value)));
    $("#hp-pop", fig).addEventListener("click", pop);
    $("#hp-rand", fig).addEventListener("click", () => push(1 + Math.floor(Math.random() * 30)));
    $("#hp-reset", fig).addEventListener("click", () => { if (busy) return; h = [3, 8, 5, 10, 9, 12]; draw(h, [], "초기 상태"); });
    draw(h, [], "부모 ≤ 아이 규칙만 지키면 맨 위가 항상 최솟값입니다.");
  };

  // ───────── 07 격자 BFS / DFS ─────────
  WIDGETS.grid = (fig) => {
    const R = 9, C = 13;
    const defaultWalls = ["0,3", "1,3", "2,3", "3,3", "5,1", "5,2", "5,3", "5,4", "5,5", "5,6", "1,7", "2,7", "3,7", "4,7", "6,9", "7,9", "8,9", "3,10", "3,11", "4,10"];
    let walls = new Set(store.get("gridWalls", defaultWalls)), mode = "bfs", pl = null;
    fig.innerHTML = `
      <div class="fig-title">미로 탈출: BFS vs DFS <span class="try">칸을 눌러 벽을 바꿔 보세요</span></div>
      <div class="row"><button class="btn on" data-m="bfs">BFS (큐)</button><button class="btn" data-m="dfs">DFS (스택)</button><button class="btn" id="gr-clear">벽 지우기</button><button class="btn" id="gr-reset">기본 미로</button></div>
      <div class="scroll-x"><div class="gridviz" id="gr" style="grid-template-columns:repeat(${C}, auto)"></div></div>
      <div class="stats"><div class="stat"><b id="gr-seen">0</b><span>방문한 칸</span></div><div class="stat"><b id="gr-len">-</b><span>찾은 경로 길이</span></div></div>
      <div class="log" id="gr-log"></div>
      <figcaption>숫자는 방문 순서, <b>노랑</b>은 큐/스택에서 기다리는 칸, <b>초록</b>은 최종 경로입니다.</figcaption>`;
    const key = (r, c) => r + "," + c, S = [0, 0], G = [R - 1, C - 1];
    const run = () => {
      if (pl) pl.destroy();
      store.set("gridWalls", [...walls]);
      const order = {}, parent = {}, frames = [], ds = [[1, 0], [0, 1], [-1, 0], [0, -1]];
      const list = [S], seen = new Set([key(...S)]);
      let n = 0, found = false;
      while (list.length) {
        const [r, c] = mode === "bfs" ? list.shift() : list.pop();
        if (order[key(r, c)] !== undefined) continue;
        order[key(r, c)] = ++n;
        frames.push({ order: { ...order }, front: list.map((x) => key(...x)), path: [], n, msg: `${mode === "bfs" ? "큐" : "스택"}에서 (${r}, ${c}) 꺼냄 · 대기 ${list.length}칸` });
        if (r === G[0] && c === G[1]) { found = true; break; }
        for (const [dr, dc] of mode === "bfs" ? ds : ds.slice().reverse()) {
          const nr = r + dr, nc = c + dc, k = key(nr, nc);
          if (nr < 0 || nc < 0 || nr >= R || nc >= C || walls.has(k)) continue;
          if (mode === "bfs") { if (seen.has(k)) continue; seen.add(k); parent[k] = key(r, c); list.push([nr, nc]); }
          else if (order[k] === undefined) { parent[k] = key(r, c); list.push([nr, nc]); }
        }
      }
      const path = [];
      if (found) { let k = key(...G); while (k) { path.push(k); k = parent[k]; } }
      frames.push({ order: { ...order }, front: [], path, n, msg: found ? `도착! ${mode === "bfs" ? "BFS 는 최단 경로를 보장합니다." : "DFS 는 도착은 했지만 최단이라는 보장이 없습니다."}` : "출구에 갈 수 없습니다 → -1" });
      pl = player(fig, frames, (f) => {
        const front = new Set(f.front), p = new Set(f.path);
        let html = "";
        for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) {
          const k = key(r, c), se = (r === 0 && c === 0) || (r === R - 1 && c === C - 1);
          const cls = walls.has(k) ? "wall" : p.has(k) ? "path" : front.has(k) ? "front" : f.order[k] ? "seen" : "";
          html += `<button class="gcell ${cls} ${se ? "se" : ""}" data-k="${k}" aria-label="${r}행 ${c}열${walls.has(k) ? " 벽" : ""}">${r === 0 && c === 0 ? "S" : se ? "G" : f.order[k] || ""}</button>`;
        }
        $("#gr", fig).innerHTML = html;
        $("#gr-seen", fig).textContent = f.n;
        $("#gr-len", fig).textContent = f.path.length ? f.path.length : "-";
        $("#gr-log", fig).textContent = f.msg;
      });
      pl.goto(Math.min(frames.length - 1, 40));
    };
    $("#gr", fig).addEventListener("click", (e) => {
      const k = e.target.dataset && e.target.dataset.k;
      if (!k || k === "0,0" || k === `${R - 1},${C - 1}`) return;
      walls.has(k) ? walls.delete(k) : walls.add(k);
      run();
    });
    $$("[data-m]", fig).forEach((b) => b.addEventListener("click", () => { mode = b.dataset.m; $$("[data-m]", fig).forEach((x) => x.classList.toggle("on", x === b)); run(); }));
    $("#gr-clear", fig).addEventListener("click", () => { walls = new Set(); run(); });
    $("#gr-reset", fig).addEventListener("click", () => { walls = new Set(defaultWalls); run(); });
    run();
  };

  // ───────── 08 다익스트라 ─────────
  WIDGETS.dijkstra = (fig) => {
    const P = { 1: [50, 140], 2: [210, 50], 3: [210, 230], 4: [380, 50], 5: [380, 230], 6: [520, 140] };
    const E = [[1, 2, 7], [1, 3, 2], [3, 2, 3], [2, 4, 1], [3, 4, 8], [3, 5, 5], [5, 4, 2], [4, 6, 3], [5, 6, 6]];
    fig.innerHTML = `
      <div class="fig-title">1번에서 출발하는 최단 거리 <span class="try">한 단계씩 넘겨 보세요</span></div>
      <div class="scroll-x"><svg viewBox="0 0 570 280" width="100%" style="min-width:320px;display:block" role="img" aria-label="가중치 그래프">
        <defs><marker id="dj-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--muted)"/></marker>
        <marker id="dj-arrow-hot" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--red)"/></marker></defs>
        <g id="dj-g"></g></svg></div>
      <div class="two"><div class="scroll-x"><table class="kv" id="dj-dist"></table></div><div class="log" id="dj-pq"></div></div>
      <div class="log" id="dj-log"></div>
      <figcaption><b>초록</b> 노드는 거리가 확정, <b>노랑</b>은 지금 꺼낸 노드, <b>빨간 화살표</b>는 지금 갱신을 시도하는 간선입니다. 2번 노드는 직접 가면 7이지만 3번을 거치면 5입니다.</figcaption>`;
    const frames = [], dist = { 1: 0, 2: Infinity, 3: Infinity, 4: Infinity, 5: Infinity, 6: Infinity }, done = new Set();
    let pq = [[0, 1]];
    const snap = (extra) => frames.push({ dist: { ...dist }, done: new Set(done), pq: pq.slice().sort((a, b) => a[0] - b[0]), cur: null, edge: null, ...extra });
    snap({ msg: "dist[1] = 0 으로 시작. 힙에 (0, 1)." });
    while (pq.length) {
      pq.sort((a, b) => a[0] - b[0]);
      const [d, u] = pq.shift();
      if (d > dist[u]) { snap({ cur: u, msg: `(${d}, ${u}) 꺼냄 → 이미 dist[${u}] = ${dist[u]} 로 확정된 낡은 항목. 건너뜀.` }); continue; }
      done.add(u);
      snap({ cur: u, msg: `(${d}, ${u}) 꺼냄 → ${u}번 거리 ${d} 확정.` });
      for (const [a, b, w] of E) {
        if (a !== u) continue;
        if (d + w < dist[b]) { const old = dist[b]; dist[b] = d + w; pq.push([dist[b], b]); snap({ cur: u, edge: [a, b], msg: `${u}→${b} (비용 ${w}): ${d} + ${w} = ${d + w} < ${old === Infinity ? "∞" : old} → 갱신, 힙에 (${d + w}, ${b})` }); }
        else snap({ cur: u, edge: [a, b], msg: `${u}→${b} (비용 ${w}): ${d} + ${w} = ${d + w} ≥ ${dist[b]} → 그대로` });
      }
    }
    snap({ msg: `끝. 가장 늦게 신호를 받는 노드까지 ${Math.max(...Object.values(dist))}.` });
    player(fig, frames, (f) => {
      let s = "";
      E.forEach(([a, b, w]) => {
        const [x1, y1] = P[a], [x2, y2] = P[b], hot = f.edge && f.edge[0] === a && f.edge[1] === b;
        const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy), ux = dx / len, uy = dy / len;
        s += `<line x1="${x1 + ux * 22}" y1="${y1 + uy * 22}" x2="${x2 - ux * 24}" y2="${y2 - uy * 24}" style="stroke:${hot ? "var(--red)" : "var(--muted)"}" stroke-width="${hot ? 3 : 1.5}" marker-end="url(#dj-arrow${hot ? "-hot" : ""})"/>`;
        const mx = (x1 + x2) / 2 - uy * 12, my = (y1 + y2) / 2 + ux * 12;
        s += `<text x="${mx}" y="${my + 4}" text-anchor="middle" font-size="13" font-weight="700" fill="${hot ? "var(--red)" : "var(--ink)"}">${w}</text>`;
      });
      Object.entries(P).forEach(([id, [x, y]]) => {
        const nid = +id, cur = f.cur === nid, ok = f.done.has(nid);
        s += `<circle cx="${x}" cy="${y}" r="20" fill="${cur ? "var(--mark)" : ok ? "var(--ok)" : "var(--panel)"}" stroke="${cur ? "var(--red)" : ok ? "var(--ok)" : "var(--rule)"}" stroke-width="2"/>`;
        s += `<text x="${x}" y="${y + 5}" text-anchor="middle" font-size="14" font-weight="700" fill="${cur ? "var(--mark-ink)" : ok ? "var(--panel)" : "var(--ink)"}">${id}</text>`;
        s += `<text x="${x}" y="${y + (y > 140 ? 40 : -28)}" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">${f.dist[nid] === Infinity ? "∞" : f.dist[nid]}</text>`;
      });
      $("#dj-g", fig).innerHTML = s;
      $("#dj-dist", fig).innerHTML = `<tr><th>노드</th>${Object.keys(P).map((k) => `<td>${k}</td>`).join("")}</tr><tr><th>dist</th>${Object.keys(P).map((k) => `<td class="${f.done.has(+k) ? "" : ""}">${f.dist[k] === Infinity ? "∞" : f.dist[k]}</td>`).join("")}</tr>`;
      $("#dj-pq", fig).textContent = `힙: ${f.pq.length ? f.pq.map(([d, u]) => `(${d}, ${u})`).join(" ") : "비어 있음"}`;
      $("#dj-log", fig).textContent = f.msg;
    });
  };

  // ───────── 09 DP ─────────
  WIDGETS.fib = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">f(n) 을 구하는 데 필요한 함수 호출 수 <span class="try">n 을 키우고 메모를 켜 보세요</span></div>
      <div class="row"><label for="f-n" class="small muted">n =</label><b class="mono" id="f-nv" style="min-width:3ch"></b><input id="f-n" type="range" min="2" max="40" value="6" style="flex:1"><button class="btn" id="f-memo" aria-pressed="false">메모 끄기 상태</button></div>
      <div class="stats"><div class="stat"><b id="f-naive"></b><span>메모 없이 호출 수</span></div><div class="stat"><b id="f-memo-c"></b><span>메모 사용 호출 수</span></div><div class="stat"><b id="f-time"></b><span>메모 없이 예상 시간 (호출 초당 약 300만)</span></div></div>
      <div class="scroll-x"><svg id="f-svg" style="display:block;margin:0 auto" role="img" aria-label="재귀 호출 트리"></svg></div>
      <figcaption>그림은 n ≤ 6 까지만 그립니다. <b>회색</b> 노드는 메모에서 바로 꺼낸 호출이라 그 아래로 내려가지 않습니다.</figcaption>`;
    let memo = false;
    const F = [0, 1]; for (let i = 2; i <= 45; i++) F[i] = F[i - 1] + F[i - 2];
    const naive = (n) => 2 * F[n + 1] - 1;
    const memoCalls = (n) => (n < 2 ? 1 : 2 * n - 1);
    const timeStr = (calls) => { const s = calls / 3e6; return s < 0.001 ? "< 1ms" : s < 1 ? `${Math.round(s * 1000)}ms` : s < 60 ? `${s.toFixed(1)}초` : `${(s / 60).toFixed(1)}분`; };
    function build(n, seen) {
      const node = { n, kids: [], hit: false };
      if (memo && seen.has(n)) { node.hit = true; return node; }
      if (n >= 2) { node.kids.push(build(n - 1, seen)); node.kids.push(build(n - 2, seen)); }
      seen.add(n);
      return node;
    }
    function draw() {
      const n = +$("#f-n", fig).value;
      $("#f-nv", fig).textContent = n;
      $("#f-naive", fig).textContent = fmt(naive(n));
      $("#f-memo-c", fig).textContent = fmt(memoCalls(n));
      $("#f-time", fig).textContent = timeStr(naive(n));
      const m = Math.min(n, 6), root = build(m, new Set());
      let leaf = 0, maxD = 0;
      (function lay(nd, d) { nd.d = d; maxD = Math.max(maxD, d); if (!nd.kids.length) nd.x = leaf++; else { nd.kids.forEach((c) => lay(c, d + 1)); nd.x = (nd.kids[0].x + nd.kids[nd.kids.length - 1].x) / 2; } })(root, 0);
      const W = Math.max(320, leaf * 38 + 20), H = (maxD + 1) * 50 + 10;
      const svg = $("#f-svg", fig);
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
      svg.setAttribute("width", W);
      svg.style.maxWidth = "100%";
      svg.style.height = "auto";
      const X = (nd) => 20 + nd.x * ((W - 40) / Math.max(1, leaf - 1)), Y = (nd) => 22 + nd.d * 50;
      let s = "";
      (function edges(nd) { nd.kids.forEach((c) => { s += `<line x1="${X(nd)}" y1="${Y(nd)}" x2="${X(c)}" y2="${Y(c)}" stroke="var(--rule)" stroke-width="1.5"/>`; edges(c); }); })(root);
      const counts = {};
      (function cnt(nd) { if (!nd.hit) counts[nd.n] = (counts[nd.n] || 0) + 1; nd.kids.forEach(cnt); })(root);
      (function nodes(nd) {
        const dup = !memo && counts[nd.n] > 1 && nd.n >= 2;
        s += `<circle cx="${X(nd)}" cy="${Y(nd)}" r="14" fill="${nd.hit ? "var(--code-bg)" : dup ? "var(--red-soft)" : "var(--panel)"}" stroke="${nd.hit ? "var(--rule)" : dup ? "var(--red)" : "var(--blue)"}" stroke-width="1.5"/><text x="${X(nd)}" y="${Y(nd) + 4}" text-anchor="middle" font-size="11" font-weight="700" fill="${nd.hit ? "var(--muted)" : "var(--ink)"}">f${nd.n}</text>`;
        nd.kids.forEach(nodes);
      })(root);
      svg.innerHTML = s;
    }
    $("#f-n", fig).addEventListener("input", draw);
    $("#f-memo", fig).addEventListener("click", (e) => {
      memo = !memo;
      e.currentTarget.classList.toggle("on", memo);
      e.currentTarget.setAttribute("aria-pressed", String(memo));
      e.currentTarget.textContent = memo ? "메모 켜짐" : "메모 끄기 상태";
      draw();
    });
    draw();
  };

  WIDGETS.coins = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">dp[x] = x 원을 만드는 최소 동전 수 <span class="try">동전과 금액을 바꿔 보세요</span></div>
      <div class="row"><label for="c-coins" class="small muted">동전</label><input id="c-coins" type="text" value="1, 2, 5" style="width:120px"><label for="c-amt" class="small muted">금액</label><input id="c-amt" type="number" value="11" min="1" max="24" style="width:70px"><button class="btn" id="c-go">적용</button></div>
      <div class="scroll-x"><div class="cells" id="c-cells"></div></div>
      <div class="log" id="c-log"></div>
      <figcaption><b>노랑</b> 지금 채우는 칸 dp[x], <b>파랑</b> 참고하는 칸 dp[x − c].</figcaption>`;
    let pl = null;
    const run = () => {
      if (pl) pl.destroy();
      const coins = [...new Set(parseNums($("#c-coins", fig).value, 5).filter((c) => c > 0))].sort((a, b) => a - b);
      const amt = Math.max(1, Math.min(24, Math.round(+$("#c-amt", fig).value) || 11));
      const dp = Array(amt + 1).fill(Infinity); dp[0] = 0;
      const frames = [{ dp: [...dp], x: 0, ref: -1, msg: "dp[0] = 0 (0원은 동전 0개). 나머지는 ∞ 로 시작." }];
      for (let x = 1; x <= amt; x++) for (const c of coins) {
        if (c > x) continue;
        const cand = dp[x - c] + 1, before = dp[x];
        if (cand < dp[x]) dp[x] = cand;
        frames.push({ dp: [...dp], x, ref: x - c, msg: `x = ${x}, 동전 ${c}: dp[${x - c}] + 1 = ${dp[x - c] === Infinity ? "∞" : cand} ${cand < before ? `< ${before === Infinity ? "∞" : before} → 갱신` : "→ 그대로"}  ⇒ dp[${x}] = ${dp[x] === Infinity ? "∞" : dp[x]}` });
      }
      frames.push({ dp: [...dp], x: amt, ref: -1, msg: `답: dp[${amt}] = ${dp[amt] === Infinity ? "∞ → 만들 수 없으므로 -1" : dp[amt]}. 상태 ${amt + 1}개 × 동전 ${coins.length}개 = O(금액 × 동전 수).` });
      pl = player(fig, frames, (f) => {
        $("#c-cells", fig).innerHTML = f.dp.map((v, k) => `<div class="cell ${k === f.x && f.ref >= 0 ? "cur" : k === f.ref ? "in" : k === f.x && f.ref < 0 && k ? "good" : ""}">${v === Infinity ? "∞" : v}<small>${k}</small></div>`).join("");
        $("#c-log", fig).textContent = f.msg;
      });
    };
    $("#c-go", fig).addEventListener("click", run);
    run();
  };

  // ───────── 10 구간 ─────────
  WIDGETS.intervals = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">겹치는 구간 합치기 <span class="try">구간을 바꿔 보세요</span></div>
      <div class="row"><label for="iv-in" class="small muted">구간</label><input id="iv-in" type="text" value="[[8,10],[1,3],[15,18],[2,6],[17,20],[9,12]]" style="flex:1;min-width:180px"><button class="btn" id="iv-go">적용</button></div>
      <div class="scroll-x"><svg id="iv-svg" viewBox="0 0 560 240" width="100%" style="min-width:320px;display:block" role="img" aria-label="구간 타임라인"></svg></div>
      <div class="log" id="iv-log"></div>`;
    let pl = null;
    const run = () => {
      if (pl) pl.destroy();
      let iv;
      try { iv = JSON.parse($("#iv-in", fig).value).filter((p) => Array.isArray(p) && p.length === 2).map(([a, b]) => [Math.min(a, b), Math.max(a, b)]).slice(0, 8); } catch { iv = [[1, 3], [2, 6], [8, 10]]; }
      if (!iv.length) iv = [[1, 3], [2, 6], [8, 10]];
      const sorted = iv.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
      const frames = [{ cur: -1, merged: [], sortedShown: false, msg: "입력 그대로. 먼저 시작점으로 정렬합니다." }, { cur: -1, merged: [], sortedShown: true, msg: "정렬 완료. 이제 왼쪽부터 하나씩 봅니다." }];
      const merged = [];
      sorted.forEach(([s, e], k) => {
        if (merged.length && s <= merged[merged.length - 1][1]) {
          const last = merged[merged.length - 1], old = last[1];
          last[1] = Math.max(last[1], e);
          frames.push({ cur: k, merged: merged.map((m) => [...m]), sortedShown: true, msg: `[${s}, ${e}] 의 시작 ${s} ≤ 직전 끝 ${old} → 겹침. 끝을 ${last[1]} 로.` });
        } else {
          merged.push([s, e]);
          frames.push({ cur: k, merged: merged.map((m) => [...m]), sortedShown: true, msg: merged.length === 1 ? `[${s}, ${e}] 로 시작.` : `[${s}, ${e}] 는 안 겹침 → 새 구간.` });
        }
      });
      frames.push({ cur: -1, merged: merged.map((m) => [...m]), sortedShown: true, msg: `결과: ${JSON.stringify(merged)}` });
      const lo = Math.min(...iv.map((p) => p[0])), hi = Math.max(...iv.map((p) => p[1]));
      const X = (v) => 30 + ((v - lo) / Math.max(1, hi - lo)) * 500;
      pl = player(fig, frames, (f) => {
        const list = f.sortedShown ? sorted : iv;
        let s = `<text x="30" y="14" font-size="11" fill="var(--muted)">${f.sortedShown ? "정렬된 입력" : "입력"}</text>`;
        list.forEach(([a, b], k) => {
          const y = 22 + k * 18, on = f.sortedShown && k === f.cur;
          s += `<rect x="${X(a)}" y="${y}" width="${Math.max(4, X(b) - X(a))}" height="12" rx="3" fill="${on ? "var(--mark)" : "var(--blue-soft)"}" stroke="${on ? "var(--red)" : "var(--blue)"}"/><text x="${X(b) + 6}" y="${y + 10}" font-size="10.5" fill="var(--muted)">[${a},${b}]</text>`;
        });
        const my = 30 + list.length * 18;
        s += `<text x="30" y="${my}" font-size="11" fill="var(--muted)">merged</text>`;
        f.merged.forEach(([a, b]) => { s += `<rect x="${X(a)}" y="${my + 8}" width="${Math.max(4, X(b) - X(a))}" height="16" rx="3" fill="var(--ok)"/><text x="${(X(a) + X(b)) / 2}" y="${my + 40}" text-anchor="middle" font-size="11" fill="var(--ink)">[${a},${b}]</text>`; });
        $("#iv-svg", fig).setAttribute("viewBox", `0 0 560 ${my + 52}`);
        $("#iv-svg", fig).innerHTML = s;
        $("#iv-log", fig).textContent = f.msg;
      });
    };
    $("#iv-go", fig).addEventListener("click", run);
    run();
  };

  // ───────── 11 시뮬레이션 ─────────
  WIDGETS.robot = (fig) => {
    fig.innerHTML = `
      <div class="fig-title">창고 로봇 시뮬레이션 <span class="try">명령을 바꿔 보세요 (F 전진, L 왼쪽, R 오른쪽)</span></div>
      <div class="row"><label for="rb-r" class="small muted">rows</label><input id="rb-r" type="number" value="5" min="1" max="8" style="width:64px"><label for="rb-c" class="small muted">cols</label><input id="rb-c" type="number" value="6" min="1" max="10" style="width:64px"><label for="rb-cmd" class="small muted">commands</label><input id="rb-cmd" type="text" value="FFFRFFLFFFFRFFFF" maxlength="40" style="flex:1;min-width:140px"><button class="btn" id="rb-go">적용</button></div>
      <div class="two"><div class="scroll-x"><div class="gridviz" id="rb-grid"></div></div><div style="display:grid;gap:8px;min-width:0"><table class="kv" id="rb-dir"></table><div class="log" id="rb-log"></div></div></div>`;
    let pl = null;
    const DIRS = ["북", "동", "남", "서"], ARROW = ["▲", "▶", "▼", "◀"], dr = [-1, 0, 1, 0], dc = [0, 1, 0, -1];
    const run = () => {
      if (pl) pl.destroy();
      const R = Math.max(1, Math.min(8, Math.round(+$("#rb-r", fig).value) || 5)), C = Math.max(1, Math.min(10, Math.round(+$("#rb-c", fig).value) || 6));
      const cmds = $("#rb-cmd", fig).value.toUpperCase().replace(/[^FLR]/g, "").slice(0, 40);
      let r = 0, c = 0, d = 1;
      const trail = new Set(["0,0"]), frames = [{ r, c, d, trail: new Set(trail), k: -1, bad: false, msg: "(0, 0) 에서 동쪽을 보고 시작. d = 1" }];
      [...cmds].forEach((ch, k) => {
        let bad = false, msg;
        if (ch === "L") { d = (d + 3) % 4; msg = `${k + 1}번째 'L': d = (d + 3) % 4 = ${d} (${DIRS[d]})`; }
        else if (ch === "R") { d = (d + 1) % 4; msg = `${k + 1}번째 'R': d = (d + 1) % 4 = ${d} (${DIRS[d]})`; }
        else {
          const nr = r + dr[d], nc = c + dc[d];
          if (nr >= 0 && nr < R && nc >= 0 && nc < C) { r = nr; c = nc; trail.add(`${r},${c}`); msg = `${k + 1}번째 'F': (${r}, ${c}) 로 전진`; }
          else { bad = true; msg = `${k + 1}번째 'F': (${nr}, ${nc}) 는 격자 밖 → 무시`; }
        }
        frames.push({ r, c, d, trail: new Set(trail), k, bad, msg });
      });
      frames.push({ r, c, d, trail, k: cmds.length, bad: false, msg: `최종 위치 [${r}, ${c}]` });
      $("#rb-grid", fig).style.gridTemplateColumns = `repeat(${C}, auto)`;
      pl = player(fig, frames, (f) => {
        let html = "";
        for (let i = 0; i < R; i++) for (let j = 0; j < C; j++) {
          const here = i === f.r && j === f.c;
          html += `<div class="gcell ${here ? (f.bad ? "front" : "path") : f.trail.has(`${i},${j}`) ? "seen" : ""}" style="font-size:14px">${here ? ARROW[f.d] : ""}</div>`;
        }
        $("#rb-grid", fig).innerHTML = html;
        $("#rb-dir", fig).innerHTML = `<tr><th>d</th>${DIRS.map((_, k) => `<td class="${k === f.d ? "hit" : ""}">${k}</td>`).join("")}</tr><tr><th>방향</th>${DIRS.map((x, k) => `<td class="${k === f.d ? "hit" : ""}">${x}</td>`).join("")}</tr><tr><th>dr, dc</th>${DIRS.map((_, k) => `<td class="${k === f.d ? "hit" : ""}">${dr[k]},${dc[k]}</td>`).join("")}</tr>`;
        $("#rb-log", fig).textContent = `${cmds.slice(0, f.k + 1)}${f.k >= 0 && f.k < cmds.length ? "▌" : ""}\n${f.msg}`;
      });
    };
    $("#rb-go", fig).addEventListener("click", run);
    run();
  };

  // 위젯 시작
  $$("[data-widget]").forEach((fig) => { try { WIDGETS[fig.dataset.widget](fig); } catch (e) { fig.innerHTML = `<p class="muted small">그림을 불러오지 못했습니다: ${esc(e.message)}</p>`; } });

  // 스크롤리텔링
  if ("IntersectionObserver" in window && bigoApi) {
    const steps = $$("#scrolly-bigo .step");
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        steps.forEach((s) => s.classList.toggle("active", s === en.target));
        bigoApi.setN(+en.target.dataset.n);
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach((s) => io.observe(s));
  }

  // ───────── 퀴즈 ─────────
  const QUIZ = {
    bigo: { q: "제한사항: 1 ≤ N ≤ 200,000. 처음 떠오른 풀이는 모든 쌍을 비교하는 이중 for 문입니다. 어떻게 해야 할까요?", o: ["그대로 제출한다. 파이썬은 빠르다.", "약 200억 번이므로 O(N log N) 이하의 풀이를 찾는다.", "N 이 크니 O(log N) 풀이만 가능하다.", "재귀로 바꾸면 빨라진다."], a: 1, why: "N² = 4×10¹⁰ 번은 파이썬으로 수십 분입니다. 10⁵ 급이면 정렬·해시·투 포인터처럼 O(N log N) 이하를 찾아야 합니다. O(N log N) 은 약 350만 번이라 충분합니다." },
    hash: { q: "Two Sum 을 해시맵으로 풀 때, 한 번 훑으면서 하는 일의 올바른 순서는?", o: ["seen[x] = i 를 먼저 저장하고, target − x 를 찾는다.", "target − x 가 seen 에 있는지 먼저 확인하고, 그다음 seen[x] = i 를 저장한다.", "모든 값을 먼저 저장한 뒤 정렬한다.", "seen 에 target 을 넣어 둔다."], a: 1, why: "먼저 저장하면 x 가 target 의 절반일 때 자기 자신과 짝이 됩니다(예: [3], target 6 → [0, 0]). 확인 먼저, 기록은 나중입니다." },
    window: { q: "슬라이딩 윈도우 코드에 for 문 안에 while 문이 있습니다. 전체 시간 복잡도가 O(N) 인 이유는?", o: ["while 문은 보통 금방 끝나서", "l 과 r 이 각각 뒤로 가지 않고 최대 N 번만 움직여서", "파이썬의 while 은 O(1) 이라서", "실제로는 O(N²) 이다"], a: 1, why: "각 인덱스는 창에 한 번 들어오고(r) 한 번 나갑니다(l). 이동 총합이 2N 이하이므로 O(N) 입니다. 이것이 상각 분석입니다." },
    stack: { q: "단조 스택으로 '다음으로 더 큰 값' 을 찾을 때, 스택에 남아 있는 인덱스들의 값은 어떤 순서인가요?", o: ["아래에서 위로 갈수록 커진다", "아래에서 위로 갈수록 작아진다(또는 같다)", "무작위", "항상 정렬되어 있지 않다"], a: 1, why: "새 값이 들어올 때 자신보다 작은 값을 모두 꺼내므로, 남은 값들은 위로 갈수록 작거나 같습니다. 그래서 '단조(monotonic)' 스택입니다." },
    bsearch: { q: "파라메트릭 서치를 쓸 수 있는 조건으로 가장 중요한 것은?", o: ["입력 배열이 정렬되어 있어야 한다", "답의 후보 T 에 대해 '가능한가?' 의 결과가 F…F T…T 처럼 한 번만 바뀐다", "답이 항상 짝수여야 한다", "N 이 1,000 이하여야 한다"], a: 1, why: "판정 결과가 단조(monotonic)여야 경계를 이분 탐색으로 찾을 수 있습니다. 배열 정렬은 필요 없습니다. 입국심사에서는 시간이 늘면 처리 인원이 줄지 않으니 조건을 만족합니다." },
    tree: { q: "이진 탐색 트리(BST)에서 값을 정렬된 순서로 얻으려면 어떤 순회를 쓰나요?", o: ["전위 순회", "중위 순회", "후위 순회", "레벨 순서 순회"], a: 1, why: "BST 는 '왼쪽 < 나 < 오른쪽' 이므로 왼쪽 → 나 → 오른쪽 순서인 중위 순회가 오름차순입니다." },
    heap: { q: "파이썬 heapq 로 최대 힙이 필요할 때 가장 흔한 방법은?", o: ["heapq.maxheap() 을 쓴다", "값에 −1 을 곱해서 넣고, 꺼낼 때 다시 −1 을 곱한다", "꺼낼 때마다 정렬한다", "리스트를 뒤집는다"], a: 1, why: "heapq 는 최소 힙만 제공합니다. 부호를 뒤집어 넣으면 가장 큰 값이 가장 작은 값이 되어 맨 위로 옵니다." },
    graph: { q: "격자 BFS 에서 방문 표시는 언제 하는 것이 맞을까요?", o: ["큐에서 꺼낼 때", "큐에 넣을 때", "도착했을 때만", "표시하지 않아도 된다"], a: 1, why: "꺼낼 때 표시하면 같은 칸이 여러 이웃에게서 중복으로 큐에 들어가 메모리와 시간이 폭발할 수 있습니다. 넣는 순간 표시하세요." },
    dijkstra: { q: "다익스트라를 쓰면 안 되는 그래프는?", o: ["간선이 매우 많은 그래프", "음수 가중치 간선이 있는 그래프", "방향 그래프", "노드가 10만 개인 그래프"], a: 1, why: "음수 간선이 있으면 '꺼낸 순간 확정' 이라는 전제가 깨집니다. 이때는 벨만-포드를 씁니다. 가중치가 모두 같다면 BFS 로 충분합니다." },
    dp: { q: "DP 의 시간 복잡도를 구하는 공식은?", o: ["재귀 호출 깊이 × 2", "상태의 개수 × 상태 하나를 계산하는 비용", "입력 크기의 제곱", "항상 O(N)"], a: 1, why: "동전 문제는 상태(금액) A 개 × 동전 C 개 = O(A·C). LCS 는 N·M 칸 × O(1) = O(N·M). 이 공식 하나로 대부분의 DP 를 셀 수 있습니다." },
    intervals: { q: "겹치는 구간을 합치기 전에 해야 할 일은?", o: ["끝점 기준 내림차순 정렬", "시작점 기준 정렬", "길이 기준 정렬", "정렬하지 않는다"], a: 1, why: "시작점으로 정렬하면 겹치는 구간들이 서로 이웃하게 되어, 직전에 합친 구간의 끝과만 비교하면 됩니다. (겹치지 않게 최대한 많이 고르는 문제는 끝점 정렬)" },
    sim: { q: "방향 배열을 [북, 동, 남, 서] 순서로 두었습니다. 왼쪽으로 90도 도는 코드는?", o: ["d = (d + 1) % 4", "d = (d + 3) % 4", "d = d - 1", "d = (d + 2) % 4"], a: 1, why: "시계 방향 순서에서 왼쪽 회전은 −1 입니다. d − 1 은 d = 0 일 때 −1 이 되므로 (d + 3) % 4 로 씁니다. (파이썬에서는 (d − 1) % 4 도 됩니다)" },
  };
  $$("[data-quiz]").forEach((box) => {
    const qz = QUIZ[box.dataset.quiz];
    const ch = box.closest("section").id;
    if (!qz) return;
    const render = (picked) => {
      box.innerHTML = `<div class="eyebrow">확인 문제</div><div class="q">${esc(qz.q)}</div>
        <div class="opts">${qz.o.map((o, k) => `<button class="opt ${picked != null ? (k === qz.a ? "right" : k === picked ? "wrong" : "") : ""}" data-k="${k}" ${picked != null ? "disabled" : ""}>${esc(o)}</button>`).join("")}</div>
        ${picked != null ? `<div class="why ${picked === qz.a ? "ok" : "no"}"><b>${picked === qz.a ? "정답." : "아쉽습니다."}</b> ${esc(qz.why)}${picked !== qz.a ? ` <button class="btn" data-retry>다시 풀기</button>` : ""}</div>` : ""}`;
      $$(".opt", box).forEach((b) => b.addEventListener("click", () => { const k = +b.dataset.k; if (k === qz.a) markDone(ch, "quiz"); render(k); }));
      const rb = $("[data-retry]", box); if (rb) rb.addEventListener("click", () => render(null));
    };
    render(chState(ch).quiz ? qz.a : null);
  });

  // ───────── 코드 실습 (브라우저 파이썬) ─────────
  const COURSE = window.COURSE_DATA || {};
  const CUSTOM = {
    "warmup-range": {
      title: "Warm-up: 서로 다른 값의 개수", level: "Easy", source: "실습 사용법 익히기",
      description: "정수 배열 nums 에서 서로 다른 값이 몇 개인지 return 하세요.\n\n제한사항\n- 0 ≤ len(nums) ≤ 200,000\n\n입출력 예\n[1, 2, 2, 3, 3, 3] → 3\n[] → 0\n\n이 실습은 사용법을 익히기 위한 것입니다. 그런데 생각해 보세요. 빈 리스트를 만들고 'x not in 리스트' 로 하나씩 확인하면 연산을 몇 번 할까요? N = 200,000 이면?",
      signature: "def solution(nums: list[int]) -> int:",
      hints: ["리스트의 in 은 O(N) 입니다. 반복문 안에서 쓰면 전체 O(N²).", "set 은 중복을 자동으로 없애 주고, in 이 평균 O(1) 입니다.", "return len(set(nums))"],
      reference: "def solution(nums):\n    return len(set(nums))\n",
      tests: [{ input: [[1, 2, 2, 3, 3, 3]], output: 3 }, { input: [[]], output: 0 }, { input: [[7]], output: 1 }, { input: [[-1, 1, -1, 1, 0]], output: 3 }, { input: [[5, 5, 5, 5]], output: 1 }],
    },
  };
  const CELL_CFG = { "two-sum": { compare: "sorted" }, "maximum-depth-of-binary-tree": { prep: "tree" } };
  const TREE_PRELUDE = [
    "from collections import deque",
    "class TreeNode:",
    "    def __init__(self, val=0, left=None, right=None):",
    "        self.val = val",
    "        self.left = left",
    "        self.right = right",
    "    def __repr__(self):",
    "        return 'TreeNode(' + str(self.val) + ')'",
    "def build_tree(values):",
    "    if not values or values[0] is None:",
    "        return None",
    "    root = TreeNode(values[0])",
    "    q = deque([root])",
    "    i = 1",
    "    while q and i < len(values):",
    "        node = q.popleft()",
    "        if i < len(values) and values[i] is not None:",
    "            node.left = TreeNode(values[i]); q.append(node.left)",
    "        i += 1",
    "        if i < len(values) and values[i] is not None:",
    "            node.right = TreeNode(values[i]); q.append(node.right)",
    "        i += 1",
    "    return root",
  ].join("\n");
  const HARNESS = [
    "import sys, json, copy, time, traceback",
    "from browser import window",
    "_buf = []",
    "class _W:",
    "    def write(self, s):",
    "        _buf.append(str(s))",
    "    def flush(self):",
    "        pass",
    "_old = (sys.stdout, sys.stderr)",
    "sys.stdout = _W()",
    "sys.stderr = _W()",
    "_src_lines = str(window.kdSrc).split(chr(10))",
    "def _fmt(e):",
    "    if isinstance(e, SyntaxError):",
    "        ln = getattr(e, 'lineno', None)",
    "        code = _src_lines[ln - 1].strip() if ln and 0 < ln <= len(_src_lines) else ''",
    "        return str(ln) + '번째 줄 문법 오류: ' + str(getattr(e, 'msg', e)) + (chr(10) + '    ' + code if code else '')",
    "    lines = []",
    "    for f in traceback.extract_tb(e.__traceback__):",
    "        if f.filename == '<내 코드>':",
    "            code = _src_lines[f.lineno - 1].strip() if 0 < f.lineno <= len(_src_lines) else ''",
    "            lines.append(str(f.lineno) + '번째 줄 (' + str(f.name) + '): ' + code)",
    "    return chr(10).join(lines[-3:] + [type(e).__name__ + ': ' + str(e)])",
    "def _eq(got, exp, mode):",
    "    try:",
    "        got = json.loads(json.dumps(got))",
    "    except Exception:",
    "        return False",
    "    if mode == 'sorted':",
    "        return isinstance(got, list) and sorted(got) == sorted(exp)",
    "    if mode == 'unordered':",
    "        return isinstance(got, list) and sorted(got, key=repr) == sorted(exp, key=repr)",
    "    if mode == 'float':",
    "        return isinstance(got, (int, float)) and abs(got - exp) <= 1e-6 * max(1, abs(exp))",
    "    return got == exp",
    "_res = {'error': None, 'results': []}",
    "try:",
    "    _ns = {'__name__': '__main__'}",
    "    exec(str(window.kdPrelude), _ns)",
    "    exec(compile(str(window.kdSrc), '<내 코드>', 'exec'), _ns)",
    "    if 'solution' not in _ns:",
    "        raise NameError('solution 함수가 없습니다. def solution(...) 줄을 지우지 마세요.')",
    "    _fn = _ns['solution']",
    "    _tests = json.loads(str(window.kdTests))",
    "    _mode = str(window.kdMode)",
    "    _prep = str(window.kdPrep)",
    "    for _t in _tests:",
    "        _args = copy.deepcopy(_t['input'])",
    "        if _prep == 'tree':",
    "            _args = [_ns['build_tree'](_args[0])] + _args[1:]",
    "        _start = len(_buf)",
    "        _err = None",
    "        _got = None",
    "        _t0 = time.perf_counter()",
    "        try:",
    "            _got = _fn(*_args)",
    "        except Exception as _e:",
    "            _err = _fmt(_e)",
    "        _ms = (time.perf_counter() - _t0) * 1000",
    "        _ok = _err is None and _eq(_got, _t['output'], _mode)",
    "        _res['results'].append({'ok': _ok, 'input': ', '.join(repr(a) for a in _t['input']), 'expected': repr(_t['output']), 'got': repr(_got) if _err is None else '', 'error': _err, 'ms': _ms, 'out': ''.join(_buf[_start:])})",
    "except Exception as _e:",
    "    _res['error'] = _fmt(_e)",
    "finally:",
    "    sys.stdout, sys.stderr = _old",
    "_res['stdout'] = ''.join(_buf)",
    "window.kdDone(json.dumps(_res))",
  ].join("\n");

  const BRYTHON = ["https://cdn.jsdelivr.net/npm/brython@3.13.2/brython.min.js", "https://cdn.jsdelivr.net/npm/brython@3.13.2/brython_stdlib.js"];
  let pyPromise = null;
  function loadPython() {
    if (pyPromise) return pyPromise;
    pyPromise = new Promise((resolve, reject) => {
      if (window.__BRYTHON__ && window.__BRYTHON__.runPythonSource) { resolve(); return; }
      const timer = setTimeout(() => reject(new Error("시간 초과")), 45000);
      const next = (k) => {
        if (k >= BRYTHON.length) {
          clearTimeout(timer);
          try {
            // 동적으로 불러오면 Brython 의 자동 초기화가 돌지 않으므로 직접 호출합니다
            if (typeof window.brython === "function") window.brython({ debug: 0 });
            window.__BRYTHON__.runPythonSource("import traceback, json, copy", {});
            resolve();
          } catch (e) { reject(e); }
          return;
        }
        const s = document.createElement("script");
        s.src = BRYTHON[k];
        s.onload = () => next(k + 1);
        s.onerror = () => { clearTimeout(timer); reject(new Error("스크립트를 불러오지 못했습니다")); };
        document.head.appendChild(s);
      };
      next(0);
    });
    pyPromise.catch(() => { pyPromise = null; });
    return pyPromise;
  }
  function runPython(src, cell) {
    return new Promise((resolve, reject) => {
      window.kdSrc = src;
      window.kdTests = JSON.stringify(cell.tests);
      window.kdMode = cell.compare || "exact";
      window.kdPrep = cell.prep || "";
      window.kdPrelude = cell.prep === "tree" ? TREE_PRELUDE : "";
      window.kdDone = (json) => { try { resolve(JSON.parse(json)); } catch (e) { reject(e); } };
      try { window.__BRYTHON__.runPythonSource(HARNESS, {}); } catch (e) { reject(e); }
    });
  }

  function starterFor(cell) {
    const extra = cell.prep === "tree" ? "# TreeNode(val, left, right) 를 그대로 쓸 수 있습니다. 빈 트리는 None.\n" : "";
    return `${extra}${cell.signature}\n    # 여기에 풀이를 작성하세요\n    pass\n`;
  }
  $$(".lab[data-cell]").forEach((lab) => {
    const slug = lab.dataset.cell;
    const base = CUSTOM[slug] || COURSE[slug];
    const ch = lab.closest("section").id;
    if (!base) { lab.remove(); return; }
    const cell = { ...base, ...(CELL_CFG[slug] || {}) };
    if (!cell.compare && base.compare) cell.compare = base.compare;
    const draftKey = "draft:" + slug;
    let hintN = 0;
    lab.innerHTML = `
      <div class="lab-head">
        <div class="eyebrow">실습 · 브라우저에서 바로 실행</div>
        <h4>${esc(cell.title)} <span class="tag">${esc(cell.level || "")}</span> <span class="tag">${esc(cell.source || "")}</span></h4>
        <p class="lab-desc">${esc(cell.description)}</p>
        <button class="btn" data-more style="justify-self:start">문제 전체 보기</button>
      </div>
      <div class="lab-body">
        <div class="editor-wrap">
          <label class="small muted" for="ed-${slug}" style="padding:8px 14px 0">solution 함수를 완성하세요</label>
          <textarea class="editor" id="ed-${slug}" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off"></textarea>
          <div class="lab-actions">
            <button class="btn red" data-run>실행 & 채점</button>
            <button class="btn" data-hint>힌트</button>
            <button class="btn" data-answer>모범 풀이</button>
            <button class="btn" data-reset>처음 코드로</button>
            <span class="kbd">Ctrl/⌘ + Enter 실행</span>
          </div>
        </div>
        <div class="results" aria-live="polite"><div class="muted small">테스트 ${cell.tests.length}개로 채점합니다. 처음 실행할 때 브라우저용 파이썬(약 5MB)을 한 번 불러옵니다. <code>print</code> 출력도 함께 보여 줍니다. 무한 루프를 돌면 탭이 멈출 수 있으니 조심하세요.</div></div>
      </div>
      <div class="lab-foot">
        <div data-hints></div>
        <div data-sol></div>
        ${COURSE[slug] ? `<span class="small muted">터미널에서 효율성 테스트까지 채점: <span class="cmd">python practice.py test ${esc(slug)}</span></span>` : ""}
      </div>`;
    const ed = $("textarea", lab), res = $(".results", lab);
    ed.value = store.get(draftKey, null) || starterFor(cell);
    ed.addEventListener("input", () => store.set(draftKey, ed.value));
    ed.addEventListener("keydown", (e) => {
      if (e.key === "Tab" && !e.shiftKey) { e.preventDefault(); insert(ed, "    "); }
      else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); run(); }
      else if (e.key === "Enter" && !e.isComposing) {
        const before = ed.value.slice(0, ed.selectionStart), line = before.slice(before.lastIndexOf("\n") + 1);
        const indent = (line.match(/^\s*/) || [""])[0] + (/:\s*(#.*)?$/.test(line) ? "    " : "");
        e.preventDefault(); insert(ed, "\n" + indent);
      }
    });
    function insert(t, text) {
      const s = t.selectionStart, e2 = t.selectionEnd;
      t.value = t.value.slice(0, s) + text + t.value.slice(e2);
      t.selectionStart = t.selectionEnd = s + text.length;
      store.set(draftKey, t.value);
    }
    $("[data-more]", lab).addEventListener("click", (e) => { const d = $(".lab-desc", lab); d.classList.toggle("open"); e.currentTarget.textContent = d.classList.contains("open") ? "접기" : "문제 전체 보기"; });
    $("[data-hint]", lab).addEventListener("click", () => {
      hintN = Math.min(hintN + 1, cell.hints.length);
      $("[data-hints]", lab).innerHTML = cell.hints.slice(0, hintN).map((h, k) => `<div class="hintbox"><b>힌트 ${k + 1}.</b> ${esc(h)}</div>`).join("") + (hintN >= cell.hints.length ? "" : "");
      $("[data-hints]", lab).style.display = "grid"; $("[data-hints]", lab).style.gap = "6px";
    });
    $("[data-answer]", lab).addEventListener("click", (e) => {
      const box = $("[data-sol]", lab);
      if (box.innerHTML) { box.innerHTML = ""; e.currentTarget.textContent = "모범 풀이"; return; }
      e.currentTarget.textContent = "모범 풀이 숨기기";
      box.innerHTML = `<pre class="code"><code>${hl(cell.reference)}</code></pre><button class="btn" data-use>에디터에 붙여 넣기</button>`;
      $("[data-use]", box).addEventListener("click", () => { ed.value = cell.reference; store.set(draftKey, ed.value); });
    });
    const resetBtn = $("[data-reset]", lab);
    resetBtn.addEventListener("click", () => {
      if (!resetBtn.dataset.armed) { resetBtn.dataset.armed = "1"; resetBtn.textContent = "한 번 더 누르면 초기화"; setTimeout(() => { delete resetBtn.dataset.armed; resetBtn.textContent = "처음 코드로"; }, 3000); return; }
      delete resetBtn.dataset.armed; resetBtn.textContent = "처음 코드로";
      ed.value = starterFor(cell); store.set(draftKey, ed.value);
    });
    const runBtn = $("[data-run]", lab);
    async function run() {
      runBtn.disabled = true;
      res.innerHTML = `<div class="muted small">${window.__BRYTHON__ ? "실행 중…" : "브라우저용 파이썬을 불러오는 중… (처음 한 번, 몇 초 걸립니다)"}</div>`;
      try {
        await loadPython();
      } catch (e) {
        res.innerHTML = `<div class="err">이 화면에서는 파이썬 실행기를 불러오지 못했습니다 (${esc(e.message || e)}).\n저장소의 web/course.html 을 브라우저로 직접 열거나, 터미널에서 채점하세요:\npython practice.py start ${esc(slug)}</div>`;
        runBtn.disabled = false;
        return;
      }
      res.innerHTML = `<div class="muted small">실행 중…</div>`;
      await new Promise((r) => setTimeout(r, 30));
      let out;
      try { out = await runPython(ed.value, cell); }
      catch (e) { res.innerHTML = `<div class="err">실행기 오류: ${esc(e.message || e)}</div>`; runBtn.disabled = false; return; }
      runBtn.disabled = false;
      if (out.error) {
        res.innerHTML = `<div class="verdict no">실행 오류</div><div class="err">${esc(out.error)}</div>${out.stdout ? `<div class="stdout">${esc(out.stdout)}</div>` : ""}`;
        return;
      }
      const pass = out.results.filter((r) => r.ok).length, all = out.results.length;
      const total = out.results.reduce((s, r) => s + r.ms, 0);
      res.innerHTML = `<div class="verdict ${pass === all ? "ok" : "no"}">${pass === all ? "통과" : "실패"} ${pass} / ${all}</div>
        <div class="small muted">총 ${total.toFixed(1)}ms (브라우저 파이썬은 실제 파이썬보다 느립니다)</div>
        ${out.results.map((r, k) => `<div class="tcase"><span class="m ${r.ok ? "ok" : "no"}">${r.ok ? "✓" : "✗"}</span><div><b>#${k + 1}</b> solution(${esc(r.input)})${r.ok ? ` → ${esc(r.got)}` : `<br>기댓값 ${esc(r.expected)}<br>${r.error ? `<span style="color:var(--red)">${esc(r.error)}</span>` : `내 답 &nbsp;${esc(r.got)}`}`}${r.out ? `<div class="stdout">${esc(r.out)}</div>` : ""}</div></div>`).join("")}`;
      if (pass === all) markDone(ch, "lab");
    }
    runBtn.addEventListener("click", run);
  });

  renderToc();
  window.addEventListener("pagehide", () => timers.forEach((t) => { clearInterval(t); clearTimeout(t); }));
})();
