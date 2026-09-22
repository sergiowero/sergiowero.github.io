
/* window.cvLang() is defined in <head>; anything rendered from JS redraws on the 'langchange' event below */
/* Years of experience, computed from the year I started working */
(function(){
  var START_YEAR=2010;
  var years=new Date().getFullYear()-START_YEAR;
  document.querySelectorAll('[data-years]').forEach(function(el){el.textContent=years;});
})();
/* Job dates rendered from data-from / data-to (YYYY-MM; no data-to = present): "Mar 2020 — Present · 6 yrs 8 mos" */
(function(){
  var M={en:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
         es:['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']};
  var W={en:{present:'Present',yr:' yr',yrs:' yrs',mo:' mo',mos:' mos'},
         es:{present:'Actualidad',yr:' año',yrs:' años',mo:' mes',mos:' meses'}};
  function ym(s){var p=s.split('-');return {y:+p[0],m:+p[1]};}
  function draw(){
  var L=window.cvLang(), w=W[L];
  function label(d){return M[L][d.m-1]+' '+d.y;}
  var now=new Date(), nowS=now.getFullYear()+'-'+(now.getMonth()+1);
  document.querySelectorAll('[data-from]').forEach(function(el){
    var toAttr=el.getAttribute('data-to');
    var a=ym(el.getAttribute('data-from')), b=ym(toAttr||nowS);
    var months=(b.y-a.y)*12+(b.m-a.m)+1; // inclusive count, like LinkedIn
    var y=Math.floor(months/12), m=months%12, parts=[];
    if(y) parts.push(y+(y===1?w.yr:w.yrs));
    if(m) parts.push(m+(m===1?w.mo:w.mos));
    el.textContent=label(a)+' — '+(toAttr?label(b):w.present);
    var d=document.createElement('span'); d.className='dur'; d.textContent=' · '+parts.join(' ');
    el.appendChild(d);
  });
  }
  draw();
  document.addEventListener('langchange',draw);
})();
/* Language switch (ES/EN): remembered across pages; header labels swap via html[data-lang];
   on a page that has a translation (body[data-alt-es|en]) it navigates to it */
(function(){
  var KEY='cv-lang';
  function apply(l){
    if(l==='es') document.documentElement.setAttribute('data-lang','es'); else document.documentElement.removeAttribute('data-lang');
    document.querySelectorAll('.tab[data-lang]').forEach(function(el){el.classList.toggle('active',el.getAttribute('data-lang')===l);});
    document.dispatchEvent(new CustomEvent('langchange',{detail:l}));
  }
  var saved='en'; try{saved=localStorage.getItem(KEY)||'en';}catch(e){}
  apply(saved);
  document.querySelectorAll('.tab[data-lang]').forEach(function(el){
    el.addEventListener('click',function(){
      var l=el.getAttribute('data-lang'); apply(l); try{localStorage.setItem(KEY,l);}catch(e){}
      var alt=document.body.getAttribute('data-alt-'+l); if(alt) location.href=alt;
    });
  });
})();
/* Fits the A4 sheet to the available width: grows on wide screens (up to 1.5x)
   and shrinks on narrow ones so there is never horizontal scroll. Not applied when printing. */
(function(){
  var sheet=document.querySelector('.sheet');
  if(!sheet) return;
  var MAX=1.5;
  function fit(){
    if(window.matchMedia&&window.matchMedia('print').matches){sheet.style.zoom='';return;}
    sheet.style.zoom='1';
    var natW=sheet.offsetWidth;
    var body=sheet.parentElement, cs=getComputedStyle(body);
    var avail=body.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
    var scale=avail/natW;
    if(scale>MAX) scale=MAX;
    sheet.style.zoom=scale;
  }
  fit();
  window.addEventListener('resize',fit);
  window.addEventListener('load',fit);
  if(window.matchMedia){
    var mq=window.matchMedia('print');
    if(mq.addEventListener) mq.addEventListener('change',fit);
    else if(mq.addListener) mq.addListener(fit);
  }
})();


/* Extended History: the subject panel follows the entry currently in view; the grep bar above the timeline filters it */
(function(){
  var dataEl=document.getElementById('history-data'), panel=document.querySelector('.subject'); if(!dataEl||!panel) return;
  var data=JSON.parse(dataEl.textContent), entries=[].slice.call(document.querySelectorAll('.hentry'));
  var M={en:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
         es:['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']};
  var W={en:{present:'Present',inside:'inside',yr:' yr',yrs:' yrs',mo:' mo',mos:' mos',clear:'Clear search'},
         es:{present:'Actualidad',inside:'dentro de',yr:' año',yrs:' años',mo:' mes',mos:' meses',clear:'Limpiar búsqueda'}};
  /* bilingual values from the JSON arrive as {en, es} */
  function L(v){return (v&&typeof v==='object'&&!Array.isArray(v))?(v[window.cvLang()]||v.en):v;}
  function w(){return W[window.cvLang()];}
  function ym(s){var p=s.split('-');return {y:+p[0],m:+p[1]};}
  function label(s){var d=ym(s);return M[window.cvLang()][d.m-1]+' '+d.y;}
  function when(e){
    if(!e.frm) return e.dur?L(e.dur):'';
    if(e.to==='single') return label(e.frm);
    var now=new Date(), a=ym(e.frm), b=ym(e.to||(now.getFullYear()+'-'+(now.getMonth()+1)));
    var months=(b.y-a.y)*12+(b.m-a.m)+1, y=Math.floor(months/12), m=months%12, parts=[];
    if(y) parts.push(y+(y===1?w().yr:w().yrs)); if(m) parts.push(m+(m===1?w().mo:w().mos));
    return label(e.frm)+' — '+(e.to?label(e.to):w().present)+' · '+parts.join(' ');
  }
  /* `live` = the entries the reader can land on: all of them, or only the ones the search kept (.dim = filtered out) */
  var live=[];
  function relive(){ live=[]; entries.forEach(function(el,i){ if(!el.classList.contains('dim')) live.push(i); }); }
  relive();
  var nav=panel.querySelector('[data-sub=nav]');
  function dimAttr(i){ return entries[i].classList.contains('dim')?' class="dim"':''; }
  function drawNav(){
    nav.innerHTML=data.map(function(e,i){
      if(e.level===1) return '';
      var kids=data.map(function(c,k){return c.parent===i?'<li data-i="'+k+'"'+dimAttr(k)+'>'+(c.co||L(c.role))+'</li>':'';}).join('');
      return '<li data-i="'+i+'"'+dimAttr(i)+'>'+e.co+(kids?'<ol>'+kids+'</ol>':'')+'</li>';
    }).join('');
  }
  drawNav();
  /* The reading line: 20% down the viewport at the top of the page, sweeping down as the page is scrolled so that
     at the very end it sits on the last entry's bottom edge — otherwise the last entries could never reach it.
     (.htl has bottom padding so that sweep stays short and each entry keeps a fair stretch of scrolling.) */
  function maxScroll(){return Math.max(1,document.documentElement.scrollHeight-window.innerHeight);}
  function lineTop(){return window.innerHeight*0.2;}
  function lineEnd(){ var last=entries[live[live.length-1]].getBoundingClientRect().bottom+window.scrollY-maxScroll(); return Math.max(lineTop(),Math.min(window.innerHeight,last)); }
  function sweep(){return 1+(lineEnd()-lineTop())/maxScroll();}   // how much faster the line moves than the page
  function lineAt(scrollY){ return lineTop()+(lineEnd()-lineTop())*Math.min(1,scrollY/maxScroll()); }
  /* Zone k = the stretch of the reading line over which live entry k is current: [starts[k], starts[k+1]), viewport px.
     Naturally each entry owns its own height, but a short one (a two-line client, a degree) would own less than a
     wheel notch and get skipped. So short entries first borrow from neighbours with room to spare, and a run of
     entries still short then splits its total stretch evenly. MIN is ~120px of actual scrolling. */
  function zones(){
    var n=live.length, r=live.map(function(i){return entries[i].getBoundingClientRect();}), tops=r.map(function(b){return b.top;});
    var MIN=120*Math.min(2,sweep());
    var len=tops.map(function(t,k){return (k+1<n?tops[k+1]:r[n-1].bottom)-t;});
    var spare=len.map(function(l){return Math.max(0,l-MIN);}), up=[], down=[];
    for(var k=0;k<n;k++){
      var need=Math.max(0,MIN-len[k]);
      up[k]=k>0?Math.min(need,spare[k-1]):0; if(k>0) spare[k-1]-=up[k]; need-=up[k];
      down[k]=k+1<n?Math.min(need,spare[k+1]):0; if(k+1<n) spare[k+1]-=down[k];
    }
    var starts=tops.map(function(t,k){return t-up[k]+(k>0?down[k-1]:0);}), ends=starts.slice(1).concat([r[n-1].bottom]);
    for(k=0;k<n;){
      var j=k; while(j<n&&ends[j]-starts[j]<MIN) j++;
      if(j-k>1){ var span=(ends[j-1]-starts[k])/(j-k); for(var m=k+1;m<j;m++) starts[m]=starts[k]+span*(m-k); }
      k=j>k?j:k+1;
    }
    return starts;
  }
  /* scroll so the reading line lands just inside the entry's zone — where the spy picks it, whatever its height */
  function goTo(i,smooth){
    var k=live.indexOf(i); if(k<0) return;   // a filtered-out entry cannot be the subject
    var s=zones(), zoneEnd=k+1<s.length?s[k+1]:entries[i].getBoundingClientRect().bottom, t=lineTop();
    var target=s[k]+Math.min(24,(zoneEnd-s[k])/2)+window.scrollY;   // page px the line must reach
    var y=(target-t)/sweep();
    window.scrollTo({top:Math.min(maxScroll(),Math.max(0,y)),behavior:smooth?'smooth':'auto'});
  }
  nav.addEventListener('click',function(ev){var li=ev.target.closest('li'); if(li) goTo(+li.getAttribute('data-i'),true);});
  var current=-1, timer=null;
  function show(i){
    if(i===current) return; current=i; var e=data[i];
    panel.classList.add('swap'); clearTimeout(timer);
    timer=setTimeout(function(){
      panel.querySelector('[data-sub=slug]').textContent=e.slug;
      panel.querySelector('[data-sub=kind]').textContent=L(e.kind_label);
      panel.querySelector('[data-sub=parent]').innerHTML=(e.parent!==null&&e.parent!==undefined)?'↳ '+w().inside+' <b>'+data[e.parent].co+'</b>':'';
      panel.querySelector('[data-sub=co]').textContent=e.co;
      panel.querySelector('[data-sub=role]').innerHTML=L(e.role);
      panel.querySelector('[data-sub=when]').textContent=when(e);
      panel.querySelector('[data-sub=loc]').textContent=L(e.loc);
      panel.querySelector('[data-sub=inds]').innerHTML=e.inds.map(function(x){return '<span class="ind">'+L(x)+'</span>';}).join('');
      panel.querySelector('[data-sub=tech]').innerHTML=e.tech.map(function(x){return '<span class="dchip">'+L(x)+'</span>';}).join('');
      [].forEach.call(nav.querySelectorAll('li'),function(li){li.classList.toggle('active',+li.getAttribute('data-i')===i);});
      entries.forEach(function(el,k){el.classList.toggle('active',k===i);el.classList.toggle('parent-active',k===e.parent);});
      panel.querySelector('.sub-progress i').style.width=((live.indexOf(i)+1)/live.length*100)+'%';
      panel.classList.remove('swap');
    },120);
  }
  show(0);
  document.addEventListener('langchange',function(){var i=current;current=-1;drawNav();show(i<0?0:i);});
  // scroll spy: the live entry whose zone holds the reading line is the current one
  // (getBoundingClientRect is used instead of IntersectionObserver because the sheet is CSS-zoomed)
  var ticking=false;
  function spy(){
    ticking=false; if(!live.length) return;
    var s=zones(), y=lineAt(window.scrollY), k=0;
    for(var j=0;j<s.length;j++){ if(s[j]<=y) k=j; }
    if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-2) k=s.length-1;  // bottom of page → last entry
    if(window.scrollY<8) k=0;   // top of page → first (top-level) entry
    show(live[k]);
  }
  function onScroll(){ if(!ticking){ ticking=true; requestAnimationFrame(spy); } }
  window.addEventListener('scroll',onScroll,{passive:true}); window.addEventListener('resize',onScroll);
  spy();
  // #h-<slug> in the URL: place that entry at the reading line (the browser alone puts it at the very top, which
  // the spy reads as the entry after it). The browser does its own fragment jump around load, so this runs after.
  var target=location.hash&&document.getElementById(location.hash.slice(1)), ti=target?entries.indexOf(target):-1;
  if(ti>=0){ var place=function(){setTimeout(function(){goTo(ti,false); spy();},0);}; if(document.readyState==='complete') place(); else window.addEventListener('load',place); }

  /* ---- grep bar: ?q= filters the timeline. Words are OR-ed; each is looked for in the visible language, ignoring
     case and accents; a 4-digit year (or year-year) also matches every entry whose period covers it.
     An entry with no hit dims to its head (title, company, dates); in a kept entry the blocks the query does not
     touch fold into a one-line `▸ // label` row (click to open); hits are wrapped in <mark>. ---- */
  var box=document.querySelector('.hq'); if(!box) return;
  var input=box.querySelector('.hq-in'), clearBtn=box.querySelector('.hq-x'), count=box.querySelector('.hq-count'),
      empty=box.querySelector('.hq-empty'), more=box.querySelector('.hq-more'), facets=box.querySelector('.hq-facets');
  var DIA=new RegExp('['+String.fromCharCode(0x300)+'-'+String.fromCharCode(0x36f)+']','g');
  function fold(s){ return s.normalize('NFD').replace(DIA,'').toLowerCase(); }
  var TOK=/"([^"]*)"|(\S+)/g, YEAR=/^([0-9]{4})(?:-([0-9]{4}))?$/;
  function tokens(q){   // words, or "quoted phrases"; y0..y1 set when the token is a year or a year range
    var out=[], m; TOK.lastIndex=0;
    while((m=TOK.exec(q))){ var t=fold(m[1]!==undefined?m[1]:m[2]).trim(); if(!t) continue;
      var y=YEAR.exec(t); out.push({t:t,y0:y?+y[1]:0,y1:y?+(y[2]||y[1]):0}); }
    return out;
  }
  function hiddenLang(){ return window.cvLang()==='es'?'i18n-en':'i18n-es'; }
  function textNodes(root){   // the text a reader actually sees: the other language's spans are skipped
    var out=[], skip=hiddenLang(), walker=document.createTreeWalker(root,NodeFilter.SHOW_ELEMENT|NodeFilter.SHOW_TEXT,{acceptNode:function(n){
      if(n.nodeType===1) return n.classList.contains(skip)?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_SKIP;
      return n.nodeValue.trim()?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_SKIP; }});
    var n; while((n=walker.nextNode())) out.push(n); return out;
  }
  function textOf(el){ return textNodes(el).map(function(n){return n.nodeValue;}).join(' ').replace(/\s+/g,' '); }
  var idx=null;   // built on the first query, dropped on langchange (the visible language is what gets indexed)
  function index(){
    idx=entries.map(function(el,i){
      var e=data[i], p=(e.parent!==null&&e.parent!==undefined)?data[e.parent]:null, src=e.frm?e:(p||e);   // an undated child spans its parent's period
      var y0=src.frm?+src.frm.slice(0,4):0, y1=!src.frm?0:src.to==='single'?y0:src.to?+src.to.slice(0,4):new Date().getFullYear();
      return {head:fold(textOf(el.querySelector('.hhead'))+' '+e.kind_label.en+' '+e.kind_label.es),
              blocks:[].slice.call(el.querySelectorAll('.hbody .hblock')).map(function(b){return {el:b,t:fold(textOf(b))};}), y0:y0, y1:y1};
    });
  }
  function hit(text,toks){ for(var k=0;k<toks.length;k++){ if(text.indexOf(toks[k].t)>=0) return true; } return false; }
  function yearHit(x,toks){ for(var k=0;k<toks.length;k++){ var t=toks[k]; if(t.y0&&x.y0&&t.y0<=x.y1&&t.y1>=x.y0) return true; } return false; }
  function markNode(n,toks){   // wrap every hit inside one text node; folded string → original offsets, so accents do not shift things
    var s=n.nodeValue, f=[], map=[];
    for(var i=0;i<s.length;i++){ var c=fold(s[i]); for(var j=0;j<c.length;j++){ f.push(c[j]); map.push(i); } }
    f=f.join('');
    var ranges=[];
    toks.forEach(function(t){ var at=0, p; while((p=f.indexOf(t.t,at))>=0){ ranges.push([map[p],map[p+t.t.length-1]+1]); at=p+t.t.length; } });
    if(!ranges.length) return;
    ranges.sort(function(a,b){return a[0]-b[0];});
    var merged=[]; ranges.forEach(function(r){ var l=merged[merged.length-1]; if(l&&r[0]<=l[1]) l[1]=Math.max(l[1],r[1]); else merged.push(r.slice()); });
    var frag=document.createDocumentFragment(), at=0;
    merged.forEach(function(r){ if(r[0]>at) frag.appendChild(document.createTextNode(s.slice(at,r[0])));
      var m=document.createElement('mark'); m.className='hm'; m.textContent=s.slice(r[0],r[1]); frag.appendChild(m); at=r[1]; });
    if(at<s.length) frag.appendChild(document.createTextNode(s.slice(at)));
    n.parentNode.replaceChild(frag,n);
  }
  function mark(el,toks){
    var roots=[el.querySelector('.hhead')].concat([].slice.call(el.querySelectorAll('.hbody .hblock:not(.fold)')));
    roots.forEach(function(r){ textNodes(r).forEach(function(n){ markNode(n,toks); }); });
  }
  function unmark(){ [].forEach.call(document.querySelectorAll('mark.hm'),function(m){ var p=m.parentNode; p.replaceChild(document.createTextNode(m.textContent),m); p.normalize(); }); }
  function termOf(chip){ return chip.getAttribute('data-term-'+window.cvLang())||chip.getAttribute('data-term-en'); }
  function hasTerm(chip){ var t=fold(termOf(chip)); return tokens(input.value).some(function(k){return k.t===t;}); }
  var q='';
  function apply(){
    var toks=tokens(input.value); q=input.value.trim();
    unmark();
    entries.forEach(function(el){ el.classList.remove('dim'); [].forEach.call(el.querySelectorAll('.hblock.fold'),function(b){b.classList.remove('fold');}); });
    clearBtn.hidden=!q;
    if(toks.length){
      if(!idx) index();
      var own=idx.map(function(x){ return {head:hit(x.head,toks)||yearHit(x,toks), blocks:x.blocks.map(function(b){return hit(b.t,toks);})}; });
      var self=own.map(function(o){ return o.head||o.blocks.some(Boolean); });
      // a parent stays for a matching child; a child of a matching parent only stays on its own merit
      var keep=self.map(function(s,i){ return s||data.some(function(c,k){ return c.parent===i&&self[k]; }); });
      entries.forEach(function(el,i){
        if(!keep[i]){ el.classList.add('dim'); return; }
        var o=own[i], any=o.blocks.some(Boolean);
        // some block hit → the others fold; only the head (or the period) hit → the whole entry is the answer, nothing folds;
        // kept only for a child → everything folds, the child tells the story
        if(any||!o.head) idx[i].blocks.forEach(function(b,k){ if(!o.blocks[k]) b.el.classList.add('fold'); });
        mark(el,toks);
      });
    }
    relive(); drawNav();
    var kept=live.length;
    count.textContent=toks.length?kept+'/'+entries.length:'';
    empty.hidden=!(toks.length&&!kept);
    [].forEach.call(facets.querySelectorAll('.dchip'),function(c){ c.classList.toggle('on',hasTerm(c)); });
    current=-1;
    if(kept) spy(); else panel.classList.add('swap');
  }
  function sync(){ var u=new URL(location.href); if(q) u.searchParams.set('q',q); else u.searchParams.delete('q'); history.replaceState(null,'',u); }
  function set(v){ input.value=v; apply(); sync(); }
  function toggleTerm(chip){   // add the chip's word to the query, or take it out when it is already there
    var t=termOf(chip), f=fold(t), parts=[], m, found=false, v=input.value; TOK.lastIndex=0;
    while((m=TOK.exec(v))){ if(fold(m[1]!==undefined?m[1]:m[2]).trim()===f) found=true; else parts.push(m[0]); }
    if(!found) parts.push(/\s/.test(t)?'"'+t+'"':t);
    set(parts.join(' ')); input.focus();
  }
  var syncT=null;
  input.addEventListener('input',function(){ apply(); clearTimeout(syncT); syncT=setTimeout(sync,150); });
  input.addEventListener('keydown',function(ev){ if(ev.key==='Escape'){ if(input.value) set(''); else input.blur(); } });
  clearBtn.addEventListener('click',function(){ set(''); input.focus(); });
  more.addEventListener('click',function(){ var open=facets.hidden; facets.hidden=!open; more.setAttribute('aria-expanded',open?'true':'false'); });
  facets.addEventListener('click',function(ev){
    var chip=ev.target.closest('.dchip'); if(chip){ toggleTerm(chip); return; }
    var mc=ev.target.closest('.hq-morechips'); if(mc) mc.closest('.hq-facet').classList.add('all');
  });
  document.querySelector('.htl').addEventListener('click',function(ev){ var b=ev.target.closest('.hblock.fold'); if(b){ b.classList.remove('fold'); onScroll(); } });
  document.addEventListener('keydown',function(ev){   // `/` focuses the search, like on GitHub
    if(ev.key!=='/'||ev.ctrlKey||ev.metaKey||ev.altKey) return;
    var a=document.activeElement; if(a&&(a.tagName==='INPUT'||a.tagName==='TEXTAREA'||a.isContentEditable)) return;
    ev.preventDefault(); input.focus(); input.select();
  });
  function relabel(){ clearBtn.setAttribute('aria-label',w().clear); clearBtn.title=w().clear; }
  relabel();
  // the date labels are redrawn by a later script on langchange, so the reindex waits a tick
  document.addEventListener('langchange',function(){ relabel(); setTimeout(function(){ unmark(); idx=null; apply(); },0); });
  var q0=new URL(location.href).searchParams.get('q'); if(q0) input.value=q0;
  // the dates are drawn by a later script; the first query waits until every inline script has run
  function boot(){ if(input.value) apply(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot); else boot();
})();


/* Dark / light toggle from the header (one button, sun or moon via CSS); the choice is remembered in localStorage */
(function(){
  var KEY='cv-theme';
  function apply(t){
    if(t==='dark') document.documentElement.setAttribute('data-theme','dark'); else document.documentElement.removeAttribute('data-theme');
    var hint=t==='dark'?'Switch to light':'Switch to dark';
    document.querySelectorAll('[data-toggle-theme]').forEach(function(el){el.title=hint;el.setAttribute('aria-label',hint);});
  }
  var saved=null; try{saved=localStorage.getItem(KEY);}catch(e){}
  apply(saved||'light');
  document.querySelectorAll('[data-toggle-theme]').forEach(function(el){
    el.addEventListener('click',function(){var t=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';apply(t);try{localStorage.setItem(KEY,t);}catch(e){}});
  });
})();


/* ASCII skill bars sized to fill the column: [████████░░] with as many cells as fit */
(function(){
  function draw(){
    document.querySelectorAll('.sk-dots').forEach(function(el){
      var lvl=+el.parentElement.getAttribute('data-lvl')||0, max=+el.parentElement.getAttribute('data-max')||10;
      var probe=document.createElement('span'); probe.textContent='██████████'; probe.style.cssText='position:absolute;visibility:hidden;white-space:pre;font:inherit;';
      el.appendChild(probe); var cw=probe.getBoundingClientRect().width/10; probe.remove();
      var w=el.getBoundingClientRect().width;   // same (zoomed) units as the probe
      if(!cw||!w) return;
      var n=Math.min(80,Math.floor(w/cw)-2), f=Math.round(n*lvl/max);
      if(n<3) return;
      el.className='sk-dots ascii';
      el.innerHTML='<span class="b">[</span><span class="f">'+'█'.repeat(f)+'</span><span class="e">'+'░'.repeat(n-f)+'</span><span class="b">]</span>';
    });
  }
  draw();
  window.addEventListener('load',draw);
  // the web font can arrive after `load`; redraw whenever a font finishes loading so the cell count matches its metrics
  if(document.fonts){ document.fonts.ready.then(draw); document.fonts.addEventListener('loadingdone',draw); }
  setTimeout(draw,1500); setTimeout(draw,4000);
})();


/* Typewriter effect on the name (skipped when the user prefers reduced motion or when printing) */
(function(){
  var el=document.getElementById('typed'); if(!el) return;
  if(window.matchMedia&&(window.matchMedia('(prefers-reduced-motion: reduce)').matches||window.matchMedia('print').matches)) return;
  /* a bilingual title holds one span per language (CSS shows one): type each on its own */
  var els=el.querySelectorAll('.i18n-en,.i18n-es'); if(!els.length) els=[el];
  Array.prototype.forEach.call(els,function(t){
    var full=t.textContent; t.textContent=''; var i=0;
    (function tick(){ if(i<=full.length){ t.textContent=full.slice(0,i++); setTimeout(tick,i<8?90:45);} })();
    /* printing mid-animation would catch half a name: finish it at once */
    window.addEventListener('beforeprint',function(){ i=full.length+1; t.textContent=full; });
  });
})();
