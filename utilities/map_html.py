#!/usr/bin/env python3
"""map_html.py — S6 of the map. One self-contained HTML file, zero install.

The markdown view (S4) gives a search box and a graph only through
Obsidian or a Quartz build. This gives all three — search, walking, and a
local graph — to anyone with a browser: no npm, no CDN, no network, no
account. Open the file. It works offline and can be committed, emailed,
or served from GitHub Pages.

Markdown stays the source of truth. This is a second *view* of the same
generated data, not a second copy of it — both are rebuilt from
nodes.json and edges.json, so neither can drift from the corpus.

DOMAIN-AGNOSTIC. Nothing here names a project; it renders whatever
nodes and edges it is handed.

    python3 utilities/map_html.py nodes.json edges.json --out map.html
"""
import argparse
import json
import pathlib

PAGE = """<!doctype html>
<meta charset="utf-8">
<title>__TITLE__</title>
<style>
:root{--bg:#0e1116;--fg:#d7dde5;--dim:#8b95a3;--line:#232a34;--acc:#7aa2f7;--warn:#e0af68}
@media (prefers-color-scheme:light){:root{--bg:#fbfbfd;--fg:#1c2128;--dim:#6a737d;--line:#e2e5e9;--acc:#2f6feb;--warn:#9a6700}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}
header{padding:14px 18px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}
#q{width:100%;max-width:640px;padding:9px 12px;background:transparent;color:var(--fg);
   border:1px solid var(--line);border-radius:7px;font:inherit}
#q:focus{outline:none;border-color:var(--acc)}
.meta{color:var(--dim);font-size:12px;margin-top:7px}
main{display:grid;grid-template-columns:minmax(280px,1fr) minmax(0,1.4fr);gap:0;height:calc(100vh - 74px)}
#list,#pane{overflow:auto;padding:14px 18px}
#list{border-right:1px solid var(--line)}
.row{padding:6px 8px;border-radius:6px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.row:hover{background:var(--line)}
.k{color:var(--dim);font-size:11px;margin-left:6px}
.warn{color:var(--warn)}
h1{font-size:16px;margin:0 0 4px}
h2{font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:.08em;margin:18px 0 6px;font-weight:600}
a{color:var(--acc);text-decoration:none;cursor:pointer}
a:hover{text-decoration:underline}
.src{color:var(--dim);font-size:12px;margin-bottom:10px}
.flags{border-left:3px solid var(--warn);padding:6px 10px;margin:10px 0;color:var(--warn);font-size:13px}
ul{margin:4px 0;padding-left:18px}li{margin:2px 0}
svg{width:100%;height:260px;border:1px solid var(--line);border-radius:7px;margin-top:8px}
circle{cursor:pointer}
text{font:10px ui-monospace,monospace;fill:var(--dim)}
</style>
<header>
  <input id="q" placeholder="search by name or title — then click to walk" autofocus>
  <div class="meta" id="meta"></div>
</header>
<main><div id="list"></div><div id="pane"></div></main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const N={},OUT={},IN={};
D.nodes.forEach(n=>N[n.id]=n);
D.edges.forEach(e=>{(OUT[e.from]=OUT[e.from]||[]).push(e);(IN[e.to]=IN[e.to]||[]).push(e)});
document.getElementById('meta').textContent =
  D.nodes.length+" nodes · "+D.edges.length+" edges · "+
  D.nodes.filter(n=>n.flags.length).length+" not conforming · generated, not written";
const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function list(items){
  document.getElementById('list').innerHTML = items.slice(0,400).map(n=>
    `<div class="row" data-id="${esc(n.id)}">${n.flags.length?'<span class="warn">⚠ </span>':''}`+
    `${esc(n.id)}<span class="k">${esc(n.kind)}</span></div>`).join('')
    + (items.length>400?`<div class="k" style="padding:8px">… ${items.length-400} more, narrow the search</div>`:'');
}
function graph(id){
  const near=[...new Set([...(OUT[id]||[]).map(e=>e.to),...(IN[id]||[]).map(e=>e.from)])].slice(0,14);
  const cx=210,cy=125,R=95,pts=near.map((n,i)=>{
    const a=2*Math.PI*i/Math.max(near.length,1)-Math.PI/2;
    return{id:n,x:cx+R*Math.cos(a),y:cy+R*Math.sin(a)}});
  return `<svg viewBox="0 0 420 250">`+
    pts.map(p=>`<line x1="${cx}" y1="${cy}" x2="${p.x}" y2="${p.y}" stroke="var(--line)"/>`).join('')+
    pts.map(p=>`<g><circle cx="${p.x}" cy="${p.y}" r="5" fill="${N[p.id]&&N[p.id].flags.length?'var(--warn)':'var(--acc)'}" data-id="${esc(p.id)}"/>`+
      `<text x="${p.x+8}" y="${p.y+3}">${esc(p.id).slice(0,22)}</text></g>`).join('')+
    `<circle cx="${cx}" cy="${cy}" r="7" fill="var(--fg)"/></svg>`;
}
function open(id){
  const n=N[id]; if(!n){document.getElementById('pane').innerHTML='<p>not found</p>';return}
  location.hash=encodeURIComponent(id);
  const grp=es=>{const b={};(es||[]).forEach(e=>(b[e.kind]=b[e.kind]||[]).push(e));return b};
  const o=grp(OUT[id]),i=grp(IN[id]);
  const link=x=>`<a data-id="${esc(x)}">${esc(x)}</a>${N[x]&&N[x].flags.length?' <span class="warn">⚠</span>':''}`;
  let h=`<h1>${esc(n.id)}</h1><div class="src">${esc(n.kind)} · ${esc(n.file)}${n.line>1?':'+n.line:''}${n.date?' · '+esc(n.date):''}</div>`;
  if(n.title)h+=`<div>${esc(n.title)}</div>`;
  if(n.flags.length)h+=`<div class="flags"><b>Not conforming:</b> ${n.flags.join(', ')}<br>`+
    `Shown rather than skipped — the gap is visible here instead of needing something to find it.</div>`;
  h+=graph(id);
  for(const k in o){h+=`<h2>${esc(k)}</h2><ul>`+o[k].map(e=>`<li>${link(e.to)}</li>`).join('')+`</ul>`}
  for(const k in i){h+=`<h2>← ${esc(k)}</h2><ul>`+i[k].map(e=>`<li>${link(e.from)}</li>`).join('')+`</ul>`}
  if(!OUT[id]&&!IN[id])h+=`<p class="src">No gated links. Isolated in the map — itself a finding.</p>`;
  document.getElementById('pane').innerHTML=h;
}
document.addEventListener('click',e=>{const t=e.target.closest('[data-id]');if(t)open(t.dataset.id)});
document.getElementById('q').addEventListener('input',e=>{
  const q=e.target.value.toLowerCase().trim();
  list(!q?D.nodes.slice(0,400)
        :D.nodes.filter(n=>n.id.toLowerCase().includes(q)||(n.title||'').toLowerCase().includes(q)));
});
list(D.nodes.slice(0,400));
if(location.hash)open(decodeURIComponent(location.hash.slice(1)));
</script>
"""


def main():
    ap = argparse.ArgumentParser(description="One self-contained HTML map.")
    ap.add_argument("nodes")
    ap.add_argument("edges")
    ap.add_argument("--out", default="map.html")
    a = ap.parse_args()
    nj = json.loads(pathlib.Path(a.nodes).read_text())
    ej = json.loads(pathlib.Path(a.edges).read_text())
    data = {"nodes": nj["nodes"], "edges": ej["edges"]}
    title = str(nj.get("descriptor") or "map")
    html = (PAGE.replace("__TITLE__", title)
                .replace("__DATA__", json.dumps(data, separators=(",", ":"))
                         .replace("</", "<\\/")))
    out = pathlib.Path(a.out)
    out.write_text(html)
    kb = out.stat().st_size / 1024
    print(f"map_html: {len(data['nodes'])} nodes, {len(data['edges'])} edges "
          f"-> {out} ({kb:.0f} KB, self-contained, offline)")


if __name__ == "__main__":
    main()
