---
for: anyone who has read a chapter   minutes: 12
---

# The Break Room {#play}

> [!RULE]
> Every game on this page is a chapter in disguise. Lose one, and you know which chapter to reread.

Two quizzes and two games about analytics agents, about three minutes each. Test what stuck, then play your way through an engagement. Nothing is saved and nobody sees your score.

This playbook was built the hard way: benchmark runs that wouldn't reproduce, traces read line by line, chapters rewritten until they held up, and more sealed questions than anyone wants to count. It took sweat, a few tears, some blood (mostly drawn by multi-table joins) and a lot of love. We wanted at least one page that is just for fun, a way to explore the world of analytics agents with nothing riding on the answer.

<div id="br-board"></div>

## Test what you know {#play-quiz}

Two quizzes. Each answer comes with the reason, so a wrong answer teaches as much as a right one.

<div id="br-quiz"></div>

## Play {#play-games}

Two games. Both have more than one ending.

<div id="br-games"></div>

<noscript><p>The quizzes and games on this page need JavaScript.</p></noscript>

<script>
(function(){
const CSS=`:host{display:block;--ok-soft:color-mix(in srgb,var(--ok) 13%,transparent);--stop-soft:color-mix(in srgb,var(--stop) 11%,transparent);font:16px/1.75 var(--body);color:var(--text)}
*{box-sizing:border-box}button{font-family:var(--body);cursor:pointer}a{color:inherit}p{margin:0 0 16px}
/* scoreboard */
.board{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:20px 0 8px}
.tile{text-align:left;font:inherit;color:inherit;width:100%;border:1px solid var(--line);border-radius:10px;padding:12px;background:var(--plate);text-decoration:none;display:block}
.tile b{display:block;font:400 10px/1.4 var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.tile span{display:block;font-size:13px;color:var(--ink);line-height:1.35;margin:4px 0 8px;min-height:36px}
.tile i{font:400 12px/1 var(--mono);font-style:normal;color:var(--muted)}
.tile.done{border-color:color-mix(in srgb,var(--ok) 45%,var(--line))}
.tile.done i{color:var(--ok)}
/* activity card */
.act{border:1px solid var(--line);border-radius:12px;background:var(--plate);margin:20px 0 28px;overflow:hidden}
.act-head{padding:20px 22px 18px;display:flex;gap:16px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap}
.act-k{font:400 11px/1.4 var(--mono);color:var(--muted);letter-spacing:.03em}
.act-k em{font-style:normal;color:var(--accent)}
.act h3{font-size:20px;font-weight:500;letter-spacing:-.025em;color:var(--ink);margin:4px 0 4px}
.act-d{font-size:14px;color:var(--muted);margin:0;max-width:52ch;line-height:1.6}
.go{font:500 12px/1 var(--mono);background:var(--ink);color:var(--bg);border:1px solid var(--ink);border-radius:999px;padding:11px 16px;white-space:nowrap}
.go:hover{opacity:.88}
.go.ghost{background:transparent;color:var(--ink);border-color:var(--line-2)}
.act-body{border-top:1px solid var(--line);padding:22px;background:var(--sheet);display:none}
.act.open .act-body{display:block}
.act.open .act-head .go{display:none}
.hud{display:flex;justify-content:space-between;align-items:center;font:400 11px/1.4 var(--mono);color:var(--muted);margin-bottom:14px;gap:10px;flex-wrap:wrap}
.pips{display:flex;gap:4px}
.pips i{width:18px;height:3px;border-radius:2px;background:var(--line-2)}
.pips i.ok{background:var(--ok)}.pips i.no{background:var(--stop)}.pips i.cur{background:var(--accent)}
.prompt{font-size:18px;line-height:1.55;color:var(--ink);margin:0 0 18px}
.prompt code,.mono{font:13.5px/1.6 var(--mono);background:var(--plate);border:1px solid var(--line);border-radius:6px;padding:1px 6px}
.opts{display:grid;gap:8px}
.opts.two{grid-template-columns:1fr 1fr}
.opt{text-align:left;font-size:14.5px;line-height:1.45;padding:12px 14px;border-radius:10px;border:1px solid var(--line);background:var(--plate);color:var(--ink)}
.opt:hover:not(:disabled){border-color:var(--accent)}
.opt small{display:block;color:var(--muted);font-size:12.5px;margin-top:2px}
.opt:disabled{cursor:default}
.opt.right{border-color:var(--ok);background:var(--ok-soft)}
.opt.wrong{border-color:var(--stop);background:var(--stop-soft)}
.fb{margin-top:14px;border-radius:10px;padding:14px 16px;font-size:14px;line-height:1.6;background:var(--plate);border:1px solid var(--line)}
.fb b{color:var(--ink);font-weight:500}
.fb.ok{border-color:color-mix(in srgb,var(--ok) 40%,var(--line))}
.fb.no{border-color:color-mix(in srgb,var(--stop) 40%,var(--line))}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.chip{font:400 11px/1 var(--mono);padding:5px 8px;border-radius:99px;border:1px solid var(--line-2);color:var(--muted)}
.chip.y{border-color:var(--ok);color:var(--ok)}.chip.n{border-color:var(--stop);color:var(--stop)}
.next{margin-top:14px}
.result{text-align:center;padding:12px 0 4px}
.result .big{font:400 64px/1 var(--pixel);color:var(--ink)}
.result .verdict{font-size:18px;color:var(--ink);margin:12px 0 6px}
.result p{color:var(--muted);font-size:14px;max-width:52ch;margin:0 auto 16px}
.readmore{font:400 11px/1.4 var(--mono);color:var(--muted);text-decoration:none;display:inline-block;margin-top:4px}
.readmore b{color:var(--accent);font-weight:400;margin-left:8px}
/* guess slider */
.slider{margin:6px 0 10px}
.slider input{width:100%;accent-color:var(--accent)}
.gv{font:400 40px/1 var(--pixel);color:var(--accent)}
.bars{margin:14px 0 4px;display:grid;gap:8px}
.barrow{display:grid;grid-template-columns:90px 1fr 54px;gap:10px;align-items:center;font:400 12px/1 var(--mono);color:var(--muted)}
.bartrack{height:10px;border-radius:5px;background:var(--panel);overflow:hidden}
.bartrack i{display:block;height:100%;border-radius:5px;background:var(--line-2);transition:width .5s}
.bartrack i.a{background:var(--accent)}
/* trace card */
.trace{border:1px solid var(--line);border-radius:10px;background:var(--plate);padding:14px 16px;margin-bottom:16px;font-size:14px}
.trace .tl{font:400 10.5px/1.4 var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em;display:block;margin-top:8px}
.trace .tl:first-child{margin-top:0}
.trace div{color:var(--ink)}
/* analyst game */
.meters{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:16px}
.meter{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--plate)}
.meter b{display:block;font:400 10px/1.4 var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.meter span{font:400 24px/1.3 var(--pixel);color:var(--ink)}
.meter .mt{height:3px;border-radius:2px;background:var(--panel);margin-top:6px;overflow:hidden}
.meter .mt i{display:block;height:100%;background:var(--ok);transition:width .4s}
.meter.low .mt i{background:var(--stop)}
.msg{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:var(--plate);margin-bottom:14px;display:flex;gap:12px}
.av{width:34px;height:34px;border-radius:8px;flex:none;display:grid;place-items:center;font:500 13px var(--mono);color:var(--accent-ink);background:var(--accent)}
.msg .who{font-size:13px;color:var(--ink);font-weight:500}
.msg .who small{color:var(--muted);font-weight:400;margin-left:6px;font-family:var(--mono);font-size:11px}
.msg .what{font-size:15.5px;color:var(--ink);line-height:1.55;margin-top:2px}
.delta{font:400 11px/1.6 var(--mono);color:var(--muted);margin-top:8px}
.delta .p{color:var(--ok)}.delta .m{color:var(--stop)}
/* hunt */
.hunt-top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.q-pill{font-size:15px;color:var(--ink)}
.q-pill b{font-weight:500}
.budget{font:400 11px/1 var(--mono);color:var(--muted);display:flex;gap:4px;align-items:center}
.budget i{width:12px;height:16px;border-radius:3px;border:1px solid var(--line-2)}
.budget i.f{background:var(--accent);border-color:var(--accent)}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--line);margin-bottom:12px;overflow-x:auto}
.tabs button{font:400 12px/1 var(--mono);background:none;border:0;border-bottom:2px solid transparent;color:var(--muted);padding:10px 12px;white-space:nowrap}
.tabs button.on{color:var(--ink);border-bottom-color:var(--accent)}
.items{display:grid;gap:8px;min-height:220px}
.item{display:flex;gap:12px;align-items:flex-start;text-align:left;border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:var(--plate);color:var(--ink);font-size:14px;line-height:1.5}
.item .src{font:400 10.5px/1.4 var(--mono);color:var(--muted);display:block;margin-bottom:2px}
.item .box{width:18px;height:18px;border-radius:5px;border:1.5px solid var(--line-2);flex:none;margin-top:2px;display:grid;place-items:center;font-size:12px;color:var(--accent-ink)}
.item.on{border-color:var(--accent);background:var(--accent-soft)}
.item.on .box{background:var(--accent);border-color:var(--accent)}
.item:hover{border-color:var(--line-2)}
.served{margin-top:14px;display:flex;gap:10px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.served small{color:var(--muted);font-size:12.5px}
.ans{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}
.ans div{border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:var(--plate)}
.ans b{display:block;font:400 10px/1.4 var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.ans span{font:400 30px/1.3 var(--pixel);color:var(--ink)}
.checks{list-style:none;margin:12px 0;padding:0;display:grid;gap:6px;font-size:14px}
.checks li{display:flex;gap:10px;line-height:1.5}
.checks li::before{content:"✓";color:var(--ok);font-weight:600;flex:none;width:14px}
.checks li.x::before{content:"✕";color:var(--stop)}
.checks li.t::before{content:"!";color:var(--warn)}
.howto{font-size:14px;line-height:1.6;color:var(--text);border:1px solid var(--line);border-radius:10px;background:var(--plate);padding:12px 14px;margin-bottom:14px}.howto b{color:var(--ink);font-weight:500}.slots{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:0 0 12px}.slot{border:1.5px dashed var(--line-2);border-radius:10px;padding:8px 10px;font-size:13px;line-height:1.35;color:var(--muted)}.slot b{display:block;font:400 10px/1.4 var(--mono);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px}.slot.full{border:1.5px solid var(--ok);background:var(--ok-soft);color:var(--ink)}.slot.full b{color:var(--ok)}.slot.half{border-style:solid;border-color:var(--warn);color:var(--ink)}.slot.half b{color:var(--warn)}
@media(max-width:640px){.slots{grid-template-columns:1fr 1fr}}
.shelf{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.shelf-col{border:1px solid var(--line);border-radius:10px;padding:12px;background:var(--plate)}.shelf-col b{display:block;font:400 10.5px/1.4 var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}.shelf-i{font-size:13px;line-height:1.45;color:var(--ink);padding:7px 0;border-top:1px solid var(--line)}.shelf-i.miss{color:var(--stop)}
@media(max-width:640px){.shelf{grid-template-columns:1fr}#b-help .opts{grid-template-columns:1fr!important}}
@media(max-width:900px){.board{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.opts.two,.ans{grid-template-columns:1fr}.meter span{font-size:18px}.act-body{padding:16px}.act-head{padding:16px}}
`;
const PARTS={"br-board":`<div class="board" id="board"></div>`,"br-quiz":`<div class="act" id="a-metric">
    <div class="act-head"><div><div class="act-k"><em>QUIZ</em> · 8 QUESTIONS · ABOUT 3 MIN</div><h3>Metric or vibe?</h3><p class="act-d">Eight definitions from real kickoff calls. Would an agent get the same number from each one twice? Spot which of the five decisions each one settles.</p></div><button class="go" data-start="metric">Start quiz</button></div>
    <div class="act-body" id="b-metric"></div>
  </div>
  <div class="act" id="a-help">
    <div class="act-head"><div><div class="act-k"><em>QUIZ</em> · 10 CARDS · ABOUT 3 MIN</div><h3>Help or noise?</h3><p class="act-d">Ten kinds of context you could give an analytics agent. Sort each one: does it change the answer, help a little, or just add noise? Finish with your own context shelf.</p></div><button class="go" data-start="help">Start quiz</button></div>
    <div class="act-body" id="b-help"></div>
  </div>`,"br-games":`<div class="act" id="a-hunt">
    <div class="act-head"><div><div class="act-k"><em>GAME</em> · ABOUT 3 MIN</div><h3>The context hunt</h3><p class="act-d">The CRO wants last quarter's pipeline. Dig through Slack, query history, the wiki and the people who know. Find the four decisions the agent needs, skip the traps, and give it six pieces of context at most.</p></div><button class="go" data-start="hunt">Start game</button></div>
    <div class="act-body" id="b-hunt"></div>
  </div>
  <div class="act" id="a-save">
    <div class="act-head"><div><div class="act-k"><em>GAME</em> · 10 REQUESTS · ABOUT 3 MIN</div><h3>Save an analyst from death by dashboard</h3><p class="act-d">Priya has 347 dashboards and a queue of Slack requests. Ten requests arrive this month. Every answer you choose costs her some sanity. Get her to Friday at 5pm.</p></div><button class="go" data-start="save">Start game</button></div>
    <div class="act-body" id="b-save"></div>
  </div>`};
const ROOTS=[];
for(const id in PARTS){const host=document.getElementById(id);if(!host)return;const r=host.attachShadow({mode:"open"});r.innerHTML="<style>"+CSS+"</style>"+PARTS[id];ROOTS.push(r)}
const $=s=>{for(const r of ROOTS){const e=r.querySelector(s);if(e)return e}return null};
const $$=s=>ROOTS.flatMap(r=>[...r.querySelectorAll(s)]);
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;");
const ACTS=[["metric","Quiz","Metric or vibe?",8],["help","Quiz","Help or noise?",10],["hunt","Game","The context hunt",null],["save","Game","Save an analyst",null]];
const SCORES={};
function drawBoard(){$("#board").innerHTML=ACTS.map(([k,t,n,max])=>{const s=SCORES[k];return `<button type="button" class="tile${s!=null?" done":""}" data-go="${k}"><b>${t}</b><span>${n}</span><i>${s!=null?s:"Not played"}</i></button>`}).join("");$$(".tile").forEach(t=>t.onclick=()=>$("#a-"+t.dataset.go).scrollIntoView({behavior:"smooth",block:"start"}))}
drawBoard();
function pips(n,cur,res){let h='<div class="pips">';for(let i=0;i<n;i++)h+=`<i class="${res[i]===true?"ok":res[i]===false?"no":i===cur?"cur":""}"></i>`;return h+"</div>"}
function rm(t,h){return `<a class="readmore" href="${h}">READ MORE<b>${t} →</b></a>`}
/* ---------- 1. METRIC OR VIBE ---------- */
const MV=[
 {t:"\"Pipeline? It's the open deals. Everyone knows what pipeline is.\"",a:"vibe",d:{population:0,grain:0,time:0,formula:0,exclusions:0},w:"Open as of when? Which stages? Partner deals in or out? Everyone knows, and everyone knows something different."},
 {t:"\"Active customer: an account with at least one login in the trailing 30 days, internal and test accounts excluded. Owner: CS Ops. Version 2.\"",a:"metric",d:{population:1,grain:1,time:1,formula:1,exclusions:1},w:"Population, time rule and exclusions are pinned down, and it has an owner and a version. One row per account settles the grain."},
 {t:"\"Churn is whatever the CS dashboard shows.\"",a:"vibe",d:{population:0,grain:0,time:0,formula:0,exclusions:0},w:"A dashboard tile is an answer, not a definition. Which filters were on? The agent cannot read them, and neither can you next quarter."},
 {t:"\"Net new ARR: SUM(arr_delta) where type = 'new' and close_date falls in the fiscal quarter, converted at the booking-date rate. Owner: Finance.\"",a:"metric",d:{population:1,grain:1,time:1,formula:1,exclusions:0},w:"Formula, population, time rule and currency rule are all settled. You might still ask Finance about exclusions, but this gives the same number twice."},
 {t:"\"Win rate is won over total. Pretty standard.\"",a:"vibe",d:{population:0,grain:0,time:0,formula:1,exclusions:0},w:"There is a formula and nothing else. Total of what? Closed deals or all deals? Which quarter, calendar or fiscal? An agent picks a default, and the default is usually the calendar quarter."},
 {t:"\"Revenue. The normal one.\"",a:"vibe",d:{population:0,grain:0,time:0,formula:0,exclusions:0},w:"Booked, billed or recognised? Three people, three numbers, one board meeting."},
 {t:"\"Slipped deal: an opportunity whose close date moved past the end of the quarter it was forecast in, counted once per opportunity, renewals excluded.\"",a:"metric",d:{population:1,grain:1,time:1,formula:1,exclusions:1},w:"All five decisions are here, in plain words. Write it as SQL, link the word \"slipped\" to it, and the agent can find it."},
 {t:"\"Top 100 customers. You know the list.\"",a:"vibe",d:{population:0,grain:0,time:0,formula:0,exclusions:0},w:"Top 100 by ARR or by deal count? Two teams own two lists. In our runs, this exact gap produced a metric that looked clean and returned the wrong total."}];
const DEC=[["population","population"],["grain","grain"],["time","time rule"],["formula","formula"],["exclusions","exclusions"]];
function startMetric(){let i=0,res=[],score=0;const b=$("#b-metric");
 function q(){const it=MV[i];b.innerHTML=`<div class="hud"><span>Question ${i+1} of ${MV.length}</span>${pips(MV.length,i,res)}</div><p class="prompt">${esc(it.t)}</p><div class="opts two"><button class="opt" data-a="metric">Metric<small>Same number every time</small></button><button class="opt" data-a="vibe">Vibe<small>Depends who you ask</small></button></div><div id="mvfb"></div>`;
  b.querySelectorAll(".opt").forEach(o=>o.onclick=()=>{const ok=o.dataset.a===it.a;res[i]=ok;if(ok)score++;b.querySelectorAll(".opt").forEach(x=>{x.disabled=true;if(x.dataset.a===it.a)x.classList.add("right");else if(x===o)x.classList.add("wrong")});
   $("#mvfb").innerHTML=`<div class="fb ${ok?"ok":"no"}"><b>${ok?"Right.":"Not quite."} It's a ${it.a}.</b> ${esc(it.w)}<div class="chips">${DEC.map(([k,l])=>`<span class="chip ${it.d[k]?"y":"n"}">${it.d[k]?"✓":"✕"} ${l}</span>`).join("")}</div></div><button class="go next">${i<MV.length-1?"Next question":"See your score"}</button>`;
   b.querySelector(".hud").innerHTML=`<span>Question ${i+1} of ${MV.length}</span>${pips(MV.length,-1,res)}`;
   b.querySelector(".next").onclick=()=>{i++;i<MV.length?q():end()}})}
 function end(){SCORES.metric=score+" / "+MV.length;drawBoard();const v=score>=7?"You think in metrics.":score>=5?"Mostly there.":"The vibes got you.";
  b.innerHTML=`<div class="result"><div class="big">${score}/${MV.length}</div><div class="verdict">${v}</div><p>A metric settles five decisions: population, grain, time rule, formula and exclusions. Miss one and the agent decides it for you, differently on each run.</p><button class="go ghost" id="mvr">Play again</button><br>${rm("The metric is the unit","#ch02")}</div>`;$("#mvr").onclick=startMetric}
 q()}
/* ---------- 2. HELP OR NOISE ---------- */
const HB=[["big","Big help","Changes the answer"],["some","A little","Better than nothing"],["none","No help, or worse","Noise, cost or confusion"]];
const HN=[
 {t:"A metric written as SQL, with an owner and a version",a:"big",w:"It settles every decision behind the number: which rows count, the grain, the time rule, the formula and the exclusions. The agent runs it instead of guessing."},
 {t:"The same metric, written as a paragraph of prose",a:"some",w:"Better than nothing, but the agent still has to translate words into SQL and can get it wrong. In our benchmark, SQL beat prose by 16 points on multi-table questions."},
 {t:"Column descriptions for every table in the warehouse",a:"some",w:"They tell the agent what a table is, not which rows count or which quarter is meant. Keep them as the floor; a big documentation push barely moves the score."},
 {t:"Queries analysts already trust, with who ran them, how often and how recently",a:"big",w:"Tested SQL for the questions people actually ask. Provenance helps the agent pick the query a team relies on over a one-off."},
 {t:"Column profiles: distinct values, null rates, min and max",a:"none",w:"They describe the shape of the data and carry no business decisions. They bloat the prompt. Look up values only when a question names one."},
 {t:"Business terms with their synonyms, linked to the right metric (\"slipped\", \"pushed\", \"moved out\")",a:"big",w:"People ask in their own words. A term with its synonyms routes the question to the right metric or query, so the good context actually gets found."},
 {t:"A generic \"how to write good SQL\" instruction pack",a:"none",w:"Generic advice competes with your domain rules and adds cost. Small, specific rules beat long general ones."},
 {t:"Usage stats: which tables and columns people query most",a:"some",w:"Knowing what's popular steers the agent toward the right tables. It still doesn't say how the number is calculated."},
 {t:"Your entire context layer, pasted into every prompt",a:"none",w:"The right context served the wrong way. The decisive piece gets lost in the pile and every question costs more. Retrieve per question instead."},
 {t:"A trusted query, trimmed to its first half to save tokens",a:"none",w:"The agent copies the start and improvises the rest, which is worse than having nothing to copy. Serve complete statements."}];
function startHelp(){let i=0,res=[],score=0;const picks=[];const b=$("#b-help");
 function q(){const it=HN[i];b.innerHTML=`<div class="hud"><span>Card ${i+1} of ${HN.length}</span>${pips(HN.length,i,res)}</div><div class="act-k" style="margin-bottom:6px">YOU SERVE THE AGENT THIS. DOES IT HELP?</div><div class="trace"><div style="font-size:17px;line-height:1.5">${esc(it.t)}</div></div><div class="opts" style="grid-template-columns:repeat(3,1fr)">${HB.map(([k,l,s])=>`<button class="opt" data-a="${k}">${l}<small>${s}</small></button>`).join("")}</div><div id="hnfb"></div>`;
  b.querySelectorAll(".opt").forEach(o=>o.onclick=()=>{const ok=o.dataset.a===it.a;res[i]=ok;picks[i]=ok;if(ok)score++;b.querySelectorAll(".opt").forEach(x=>{x.disabled=true;if(x.dataset.a===it.a)x.classList.add("right");else if(x===o)x.classList.add("wrong")});
   const lab=HB.find(x=>x[0]===it.a)[1];
   $("#hnfb").innerHTML=`<div class="fb ${ok?"ok":"no"}"><b>${ok?"Right":"Not quite"}: ${lab.toLowerCase()}.</b> ${esc(it.w)}</div><button class="go next">${i<HN.length-1?"Next card":"See your context shelf"}</button>`;
   b.querySelector(".hud").innerHTML=`<span>Card ${i+1} of ${HN.length}</span>${pips(HN.length,-1,res)}`;
   b.querySelector(".next").onclick=()=>{i++;i<HN.length?q():end()}})}
 function end(){SCORES.help=score+" / "+HN.length;drawBoard();const v=score>=8?"You'd build a lean context layer.":score>=6?"Good instincts.":"More context isn't better context.";
  const shelf=HB.map(([k,l])=>`<div class="shelf-col"><b>${l}</b>${HN.map((it,j)=>it.a===k?`<div class="shelf-i${picks[j]?"":" miss"}">${esc(it.t)}</div>`:"").join("")}</div>`).join("");
  b.innerHTML=`<div class="result"><div class="big">${score}/${HN.length}</div><div class="verdict">${v}</div><p>The context that helps most settles a business decision: how a number is calculated, and which query people trust. Context that only describes the data helps a little. Dumping everything in makes it worse.</p></div><div class="act-k" style="margin:4px 0 8px">YOUR CONTEXT SHELF · MISSED CARDS IN RED</div><div class="shelf">${shelf}</div><div style="text-align:center;margin-top:16px"><button class="go ghost" id="hnr">Play again</button><br>${rm("Where does each kind of knowledge go?","#ch02-placement")}</div>`;$("#hnr").onclick=startHelp}
 q()}
/* ---------- 4. CONTEXT HUNT ---------- */
const SRC=[["slack","Slack"],["hist","Query history"],["wiki","Wiki"],["people","People"]];
const ITEMS=[
 {id:"partner",s:"slack",src:"#revops · pinned",t:"Reminder: partner-sourced deals never count toward pipeline. They sit in the partner forecast.",k:"exclusions"},
 {id:"lol",s:"slack",src:"#sales-random",t:"pipeline is just everything in the CRM lol",k:"trap",why:"A vibe in a busy channel. Served as context, it told the agent to count every stage."},
 {id:"dashq",s:"slack",src:"#exec-staff",t:"Can someone check the Pipeline tile on the exec dashboard? Not sure what filters it uses.",k:"trap",why:"Nobody knows what the dashboard tile filters on, so it adds a second, unknown definition."},
 {id:"trusted",s:"hist",src:"pipeline_by_quarter.sql · run 140 times by 6 analysts, last run yesterday",t:"The query RevOps and Finance both use for the quarterly pipeline number.",k:"population"},
 {id:"tmp",s:"hist",src:"tmp_jk_test.sql · run once, 2023",t:"SELECT * FROM opportunity_terms WHERE amount > 0 LIMIT 500",k:"trap",why:"A one-off scratch query. Its provenance is one run by one person, years ago. Filter candidates by who ran them, how often and how recently."},
 {id:"prof",s:"hist",src:"profiling job · run nightly by a service account",t:"SELECT COUNT(*), COUNT(DISTINCT stage) FROM opportunity_terms",k:"trap",why:"Profiling describes data shape and carries no decisions. It also points the agent at the wrong table."},
 {id:"fiscal",s:"wiki",src:"Finance / Fiscal calendar",t:"Our fiscal year starts 1 February. Q1 is February to April.",k:"time"},
 {id:"stale",s:"wiki",src:"Sales Ops / Pipeline definition · last edited 2022",t:"Pipeline includes all open opportunities from stage 1 onwards.",k:"trap",why:"A stale definition that conflicts with RevOps. The agent picked one of the two silently. Flag conflicts and resolve them by provenance, then the owner."},
 {id:"grain",s:"wiki",src:"Data model / opportunity_terms",t:"One row per contract term. A three-year deal appears three times. Count deals from the opportunity table.",k:"grain"},
 {id:"revops",s:"people",src:"Dana, RevOps lead · owner of pipeline",t:"Pipeline is open opportunities at stage 2 or later, created in the quarter. If two numbers disagree, I decide.",k:"population"},
 {id:"test",s:"people",src:"Sam, data engineer",t:"Test and demo accounts are flagged is_test = true. Always filter them out.",k:"exclusions"},
 {id:"vp",s:"people",src:"Alex, VP Sales",t:"Honestly I'd just add up what my reps tell me in the forecast call.",k:"trap",why:"A forecast is an opinion, not a definition. It brought a third number into the context."}];
const NEED={population:"Population: which deals count (stage 2+, open, created in the quarter)",time:"Time rule: which quarter is \"last quarter\" (fiscal, starting 1 February)",grain:"Grain: count opportunities, not contract terms",exclusions:"Exclusions: partner-sourced deals and test accounts out"};
const WRONG={trap:"$18.4M",population:"$16.9M",time:"$9.8M",grain:"$33.6M",exclusions:"$13.5M"};
function startHunt(){const b=$("#b-hunt");let tab="slack";const pick=new Set();const CAP=6;
 const SLOTS=[["population","Which deals count"],["time","Which quarter"],["grain","What to count"],["exclusions","What to leave out"]];
 function slotState(k){if(k==="exclusions"){const n=(pick.has("partner")?1:0)+(pick.has("test")?1:0);return n===2?"full":n===1?"half":""}return ITEMS.some(x=>pick.has(x.id)&&x.k===k)?"full":""}
 function slots(){return `<div class="slots">${SLOTS.map(([k,l])=>{const st=slotState(k);return `<div class="slot ${st}"><b>${st==="full"?"✓":st==="half"?"1 of 2":"Missing"}</b>${l}</div>`}).join("")}</div>`}
 function draw(){b.innerHTML=`<div class="howto"><b>How to play.</b> The agent needs four decisions settled to get this number right. Search the tabs, tap a piece of context to give it to the agent, and watch the slots fill. Some pieces are traps: they fill nothing and give the agent a second, conflicting answer. You can give it six pieces at most.</div><div class="hunt-top"><div class="q-pill">CRO asks: <b>"What was pipeline last quarter?"</b></div><div class="budget">CONTEXT SERVED&nbsp;${Array.from({length:CAP},(_,i)=>`<i class="${i<pick.size?"f":""}"></i>`).join("")}&nbsp;${pick.size}/${CAP}</div></div>${slots()}<div class="tabs">${SRC.map(([k,l])=>`<button class="${k===tab?"on":""}" data-t="${k}">${l} · ${ITEMS.filter(x=>x.s===k).length}</button>`).join("")}</div><div class="items">${ITEMS.filter(x=>x.s===tab).map(x=>`<button class="item${pick.has(x.id)?" on":""}" data-id="${x.id}"><span class="box">${pick.has(x.id)?"✓":""}</span><span><span class="src">${esc(x.src)}</span>${esc(x.t)}</span></button>`).join("")}</div><div class="served"><small>${pick.size===CAP?"Six pieces served. Tap one again to take it back.":"Tap to give the agent a piece of context. Check every tab."}</small><button class="go" id="run" ${pick.size?"":"disabled style=\"opacity:.4\""}>Ask the agent</button></div>`;
  b.querySelectorAll(".tabs button").forEach(t=>t.onclick=()=>{tab=t.dataset.t;draw()});
  b.querySelectorAll(".item").forEach(it=>it.onclick=()=>{const id=it.dataset.id;if(pick.has(id))pick.delete(id);else if(pick.size<CAP)pick.add(id);draw()});
  $("#run").onclick=run}
 function run(){const got=ITEMS.filter(x=>pick.has(x.id));const traps=got.filter(x=>x.k==="trap");const has=k=>got.some(x=>x.k===k);
  const exA=pick.has("partner"),exB=pick.has("test");
  const missing=Object.keys(NEED).filter(k=>k==="exclusions"?!(exA&&exB):!has(k));
  const win=!traps.length&&!missing.length;
  const ans=win?"$11.2M":traps.length?WRONG.trap:WRONG[missing[0]];
  let lis=Object.keys(NEED).map(k=>{const ok=!missing.includes(k);let extra="";if(k==="exclusions"&&!ok)extra=exA?" (you had partners, missed test accounts)":exB?" (you had test accounts, missed partner deals)":"";return `<li class="${ok?"":"x"}">${NEED[k]}${extra}</li>`}).join("");
  lis+=traps.map(t=>`<li class="t">${esc(t.why)}</li>`).join("");
  const stars=win?(got.length<=5?"Lean and right.":"Right."):"";
  SCORES.hunt=win?"Solved":"Wrong number";drawBoard();
  b.innerHTML=`<div class="ans"><div><b>Agent says</b><span style="color:${win?"var(--ok)":"var(--stop)"}">${ans}</span></div><div><b>Board pack says</b><span>$11.2M</span></div></div><div class="fb ${win?"ok":"no"}"><b>${win?stars+" The agent's number matches the board pack, and it can show which metric and query it used.":"The agent sounded just as sure as it would with the right number."}</b><ul class="checks">${lis}</ul>${win?"Four decisions, five or six cards, no noise. The full layer pasted in would have scored worse than this.":"Every missing decision is one the agent made up. Every trap is a second definition it had to choose between."}</div><div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px"><button class="go" id="hback">${win?"Play again":"Go back and fix it"}</button></div><div style="margin-top:8px">${rm("Serve per question","#ch-retrieval")}</div><p style="font:400 11px/1.5 var(--mono);color:var(--muted);margin-top:10px">Figures are a composite example.</p>`;
  $("#hback").onclick=()=>{if(win){pick.clear();tab="slack"}draw()}}
 draw()}
/* ---------- 5. SAVE AN ANALYST ---------- */
const TURNS=[
 {who:"CRO",av:"CR",what:"Quick one: what was pipeline last quarter? Need it for the board deck by tonight.",o:[
   {l:"Build a dashboard for it",f:s=>{s.S-=8;s.D++;return"Dashboard #348. It answers this question, exactly this question."}},
   {l:"Write the pipeline metric: SQL, owner, version",f:s=>{s.S-=6;s.A+=14;s.pipe=1;return"Twenty minutes with RevOps. Now pipeline means one thing."}},
   {l:"Let the agent guess from the schema",f:s=>{s.S-=12;return"The agent says $1.31B. The board pack says $412M. Priya spends her evening explaining why."}}]},
 {who:"RevOps",av:"RO",what:"Can we get pipeline split by region? And next week, by segment?",auto:s=>s.pipe?(s.S+=6,"The agent answers from the pipeline metric, by region and by segment. Priya doesn't touch it."):null,o:[
   {l:"Build two more dashboards",f:s=>{s.S-=10;s.D+=2;return"Dashboards #349 and #350. Next week someone will want them by product."}},
   {l:"Write the pipeline metric now",f:s=>{s.S-=6;s.A+=14;s.pipe=1;return"Late, but it pays off from here on."}}]},
 {who:"Head of Data",av:"HD",what:"Before we tune anything: how will we know the agent is getting better?",o:[
   {l:"Seal 20 real questions with verified answers",f:s=>{s.S-=8;s.gold=1;return"A golden set. From now on every change gets a score."}},
   {l:"We'll eyeball it",f:s=>{s.S+=3;return"Cheap today. Watch what happens later."}},
   {l:"Build an accuracy dashboard",f:s=>{s.S-=5;s.D++;return"Dashboard #"+(347+s.D)+". It charts a number nobody is measuring yet."}}]},
 {who:"Analytics team",av:"AT",what:"We have years of SQL in the warehouse query history. Any use?",o:[
   {l:"Mine trusted past queries: who ran them, how often, how recently",f:s=>{s.S-=5;s.A+=16;s.past=1;return"The queries analysts actually trust, with provenance. The biggest single jump you can buy."}},
   {l:"Write descriptions for all 900 columns instead",f:s=>{s.S-=16;s.A+=4;return"Three weeks of docs. The score barely moves: descriptions carry no decisions."}},
   {l:"Ignore it",f:s=>"Years of tested SQL stay in the warehouse."}]},
 {who:"Platform engineer",av:"PE",what:"Simpler idea: let's paste the whole context layer into the prompt. Done.",o:[
   {l:"Serve it per question over MCP instead",f:s=>{s.S-=2;s.A+=(s.pipe||s.past)?8:2;return"One context call before any SQL. Less noise, lower cost."}},
   {l:"Paste it all in",f:s=>{s.A=Math.min(s.A,52);return"Cost goes up, accuracy goes down. In our benchmark: 52.3% pasted, 83.2% served per question."}}]},
 {who:"VP Sales",av:"VP",what:"What's our win rate this quarter? Exploring a hunch.",o:[
   {l:"Write the win-rate metric, with the quarter required, no default",f:s=>{s.S-=6;s.A+=8;s.win=1;return"Fiscal quarter, closed deals only. No silent calendar-quarter default."}},
   {l:"Build a dashboard",f:s=>{s.S-=8;s.D++;return"Another tile. It uses the calendar quarter. Nobody notices."}},
   {l:"Let the agent figure it out",f:s=>{s.S-=s.past?2:9;return s.past?"It finds a trusted query and shows its SQL. Good enough for a hunch.":"It picks the calendar quarter. The hunch is now wrong."}}]},
 {who:"Finance",av:"FN",what:"FYI, from this month pipeline excludes partner-sourced deals.",auto:s=>s.gold?(s.S+=4,s.A+=2,"The golden set catches the drop on the next run. Priya versions the metric in ten minutes."):(s.S-=15,s.A-=10,"Nobody notices for three weeks. The board deck goes out wrong. Priya finds out in a meeting."),o:[]},
 {who:"CFO",av:"CF",what:"The board wants net revenue retention. Can the agent just answer it?",o:[
   {l:"No metric yet, so the governed lane says no answer. Write the metric.",f:s=>{s.S-=5;s.A+=4;s.lanes=1;return"A refusal today, a governed number next week. Board numbers come from a metric or not at all."}},
   {l:"Let it improvise. It's usually close.",f:s=>{s.S-=14;return"It was close. It was not right. It was said in a board meeting."}},
   {l:"Build a dashboard",f:s=>{s.S-=8;s.D++;return"One more tile, and a second NRR definition in the company."}}]},
 {who:"Marketing",av:"MK",what:"Exploratory question: which campaigns touched the deals that slipped?",o:[
   {l:"Exploratory lane: the agent writes SQL and shows it",f:s=>{if(s.past){s.S+=6;return"Grounded in trusted past queries, with the SQL on screen. Marketing checks it themselves."}s.S-=5;return"With nothing to ground it, the agent guesses the joins. Marketing asks Priya to check."}},
   {l:"Build a dashboard",f:s=>{s.S-=9;s.D++;return"A one-off question becomes a permanent dashboard."}}]},
 {who:"CRO",av:"CR",what:"Friday, 4:52pm. Quick one: what was pipeline last quarter, by region, excluding partners?",auto:s=>{if(s.pipe&&s.gold&&s.A>=70){s.S+=10;return"The agent answers from the pipeline metric, cites it, shows the SQL. Priya closes her laptop at 5:01pm."}s.S-=12;s.D++;return"Priya builds dashboard #"+(347+s.D)+" at 6:40pm."},o:[]}];
function startSave(){const s={S:70,D:0,A:32,pipe:0,gold:0,past:0,win:0,lanes:0};let i=0;const b=$("#b-save");
 function meters(){const cap=v=>Math.max(0,Math.min(100,v));s.S=cap(s.S);s.A=Math.max(10,Math.min(90,s.A));
  return `<div class="meters"><div class="meter${s.S<35?" low":""}"><b>Priya's sanity</b><span>${s.S}</span><div class="mt"><i style="width:${s.S}%"></i></div></div><div class="meter"><b>Dashboards</b><span>${347+s.D}</span></div><div class="meter"><b>Agent accuracy</b><span>${s.gold?s.A+"%":"??"}</span><div class="act-k" style="font-size:9.5px;margin-top:4px">${s.gold?"FROM THE GOLDEN SET":"NO GOLDEN SET, NO SCORE"}</div></div></div>`}
 function turn(){const t=TURNS[i];
  const hud=`<div class="hud"><span>Request ${i+1} of ${TURNS.length}</span>${pips(TURNS.length,i,[])}</div>`;
  if(t.auto){const r=t.auto(s);if(r!==null){b.innerHTML=hud+meters()+msg(t)+`<div class="fb">${esc(r)}</div><button class="go next">${i<TURNS.length-1?"Next request":"See how Priya did"}</button>`;$("#b-save .next").onclick=adv;return}}
  b.innerHTML=hud+meters()+msg(t)+`<div class="opts">${t.o.map((o,k)=>`<button class="opt" data-k="${k}">${esc(o.l)}</button>`).join("")}</div>`;
  b.querySelectorAll(".opt").forEach(o=>o.onclick=()=>{const before={...s};const r=t.o[+o.dataset.k].f(s);const m=meters();const d=[];const ds=s.S-before.S;if(ds)d.push(`<span class="${ds>0?"p":"m"}">sanity ${ds>0?"+":""}${ds}</span>`);if(s.D!==before.D)d.push(`<span class="m">dashboards +${s.D-before.D}</span>`);
   b.innerHTML=hud+m+msg(t)+`<div class="fb"><b>${esc(t.o[+o.dataset.k].l)}.</b> ${esc(r)}${d.length?`<div class="delta">${d.join(" · ")}</div>`:""}</div><button class="go next">${i<TURNS.length-1?"Next request":"See how Priya did"}</button>`;$("#b-save .next").onclick=adv})}
 function msg(t){return `<div class="msg"><div class="av">${t.av}</div><div><div class="who">${t.who}<small>in #ask-data</small></div><div class="what">${esc(t.what)}</div></div></div>`}
 function adv(){i++;i<TURNS.length?turn():end()}
 function end(){const good=s.S>=55&&s.pipe&&s.gold&&s.A>=70,dead=s.S<25;
  const v=good?"Saved.":dead?"Death by dashboard.":"Survived. Barely.";
  const p=good?"Priya writes metrics now, not dashboards. The agent answers the repeat questions, and she gets her Fridays back.":dead?"Priya is now mostly dashboard. Every dashboard answered the question someone predicted, never the one they asked next.":"Some good calls, but something is missing. "+(!s.gold?"Without a golden set, nobody can tell if the agent is getting better. ":"")+(!s.pipe?"Pipeline still has no metric. ":"")+(!s.past?"The trusted past queries are still sitting in the warehouse.":"");
  SCORES.save=good?"Saved":dead?"Lost":"Survived";drawBoard();
  b.innerHTML=meters()+`<div class="result"><div class="verdict" style="font:400 34px/1.2 var(--pixel)">${v}</div><p>${esc(p)}</p><button class="go ghost" id="svr">Play again</button><br>${rm("The method at a glance","#start")}</div>`;$("#svr").onclick=startSave}
 turn()}
const START={metric:startMetric,help:startHelp,hunt:startHunt,save:startSave};
$$("[data-start]").forEach(btn=>btn.onclick=()=>{const k=btn.dataset.start;$("#a-"+k).classList.add("open");START[k]()});
})();
</script>
