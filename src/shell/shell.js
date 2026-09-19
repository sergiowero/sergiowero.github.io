
/* window.cvLang() is defined in <head>; anything rendered from JS redraws on the 'langchange' event below */
/* Years of experience, computed from the year I started working */
(function(){
  var START_YEAR=2010;
  var years=new Date().getFullYear()-START_YEAR;
  document.querySelectorAll('[data-years]').forEach(function(el){el.textContent=years;});
})();
/* Job dates rendered from data-from / data-to (YYYY-MM; no data-to = present): "Feb 2020 — Present · 6 yrs 8 mos" */
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


/* Extended History: the subject panel follows the entry currently in view */
(function(){
  var dataEl=document.getElementById('history-data'), panel=document.querySelector('.subject'); if(!dataEl||!panel) return;
  var data=JSON.parse(dataEl.textContent), entries=[].slice.call(document.querySelectorAll('.hentry'));
  var M={en:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
         es:['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']};
  var W={en:{present:'Present',inside:'inside',yr:' yr',yrs:' yrs',mo:' mo',mos:' mos'},
         es:{present:'Actualidad',inside:'dentro de',yr:' año',yrs:' años',mo:' mes',mos:' meses'}};
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
  var nav=panel.querySelector('[data-sub=nav]');
  function drawNav(){
    nav.innerHTML=data.map(function(e,i){
      if(e.level===1) return '';
      var kids=data.map(function(c,k){return c.parent===i?'<li data-i="'+k+'">'+L(c.role)+'</li>':'';}).join('');
      return '<li data-i="'+i+'">'+e.co+(kids?'<ol>'+kids+'</ol>':'')+'</li>';
    }).join('');
  }
  drawNav();
  nav.addEventListener('click',function(ev){var li=ev.target.closest('li'); if(li) entries[+li.getAttribute('data-i')].scrollIntoView({behavior:'smooth',block:'start'});});
  var current=-1, timer=null;
  function show(i){
    if(i===current) return; current=i; var e=data[i];
    panel.classList.add('swap'); clearTimeout(timer);
    timer=setTimeout(function(){
      panel.querySelector('[data-sub=slug]').textContent=e.slug;
      panel.querySelector('[data-sub=kind]').textContent=e.kind;
      panel.querySelector('[data-sub=parent]').innerHTML=(e.parent!==null&&e.parent!==undefined)?'↳ '+w().inside+' <b>'+data[e.parent].co+'</b>':'';
      panel.querySelector('[data-sub=co]').textContent=e.co;
      panel.querySelector('[data-sub=role]').innerHTML=L(e.role);
      panel.querySelector('[data-sub=when]').textContent=when(e);
      panel.querySelector('[data-sub=loc]').textContent=L(e.loc);
      panel.querySelector('[data-sub=inds]').innerHTML=e.inds.map(function(x){return '<span class="ind">'+L(x)+'</span>';}).join('');
      panel.querySelector('[data-sub=tech]').innerHTML=e.tech.map(function(x){return '<span class="dchip">'+L(x)+'</span>';}).join('');
      [].forEach.call(nav.querySelectorAll('li'),function(li){li.classList.toggle('active',+li.getAttribute('data-i')===i);});
      entries.forEach(function(el,k){el.classList.toggle('active',k===i);el.classList.toggle('parent-active',k===e.parent);});
      panel.querySelector('.sub-progress i').style.width=((i+1)/data.length*100)+'%';
      panel.classList.remove('swap');
    },120);
  }
  show(0);
  document.addEventListener('langchange',function(){var i=current;current=-1;drawNav();show(i<0?0:i);});
  // scroll spy: the entry crossing the 40% line of the viewport is the current one
  // (getBoundingClientRect is used instead of IntersectionObserver because the sheet is CSS-zoomed)
  var ticking=false;
  function spy(){
    ticking=false;
    var line=window.innerHeight*0.4, i=0;
    for(var k=0;k<entries.length;k++){ if(entries[k].getBoundingClientRect().top<=line) i=k; }
    if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-2) i=entries.length-1;  // bottom of page → last entry
    if(window.scrollY<8) i=0;   // top of page → first (top-level) entry
    show(i);
  }
  function onScroll(){ if(!ticking){ ticking=true; requestAnimationFrame(spy); } }
  window.addEventListener('scroll',onScroll,{passive:true}); window.addEventListener('resize',onScroll); spy();
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
  var full=el.textContent;
  if(window.matchMedia&&(window.matchMedia('(prefers-reduced-motion: reduce)').matches||window.matchMedia('print').matches)) return;
  el.textContent=''; var i=0;
  (function tick(){ if(i<=full.length){ el.textContent=full.slice(0,i++); setTimeout(tick,i<8?90:45);} })();
})();
