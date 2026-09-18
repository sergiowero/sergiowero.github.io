
/* Years of experience, computed from the year I started working */
(function(){
  var START_YEAR=2010;
  var years=new Date().getFullYear()-START_YEAR;
  document.querySelectorAll('[data-years]').forEach(function(el){el.textContent=years;});
})();
/* Job dates rendered from data-from / data-to (YYYY-MM; no data-to = present): "Feb 2020 — Present · 6 yrs 8 mos" */
(function(){
  var M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function ym(s){var p=s.split('-');return {y:+p[0],m:+p[1]};}
  function label(d){return M[d.m-1]+' '+d.y;}
  var now=new Date(), nowS=now.getFullYear()+'-'+(now.getMonth()+1);
  document.querySelectorAll('[data-from]').forEach(function(el){
    var toAttr=el.getAttribute('data-to');
    var a=ym(el.getAttribute('data-from')), b=ym(toAttr||nowS);
    var months=(b.y-a.y)*12+(b.m-a.m)+1; // inclusive count, like LinkedIn
    var y=Math.floor(months/12), m=months%12, parts=[];
    if(y) parts.push(y+(y===1?' yr':' yrs'));
    if(m) parts.push(m+(m===1?' mo':' mos'));
    el.textContent=label(a)+' — '+(toAttr?label(b):'Present');
    var d=document.createElement('span'); d.className='dur'; d.textContent=' · '+parts.join(' ');
    el.appendChild(d);
  });
})();
/* Language switch (ES/EN): remembered across pages; header labels swap via html[data-lang];
   on a page that has a translation (body[data-alt-es|en]) it navigates to it */
(function(){
  var KEY='cv-lang';
  function apply(l){
    if(l==='es') document.documentElement.setAttribute('data-lang','es'); else document.documentElement.removeAttribute('data-lang');
    document.querySelectorAll('[data-lang]').forEach(function(el){el.classList.toggle('active',el.getAttribute('data-lang')===l);});
  }
  var saved='en'; try{saved=localStorage.getItem(KEY)||'en';}catch(e){}
  apply(saved);
  document.querySelectorAll('[data-lang]').forEach(function(el){
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


/* Dark / light toggle from the header; the choice is remembered in localStorage */
(function(){
  var KEY='cv-theme';
  function apply(t){
    if(t==='light') document.documentElement.setAttribute('data-theme','light'); else document.documentElement.removeAttribute('data-theme');
    document.querySelectorAll('[data-set-theme]').forEach(function(el){el.classList.toggle('active',el.getAttribute('data-set-theme')===(t==='light'?'light':'dark'));});
  }
  var saved=null; try{saved=localStorage.getItem(KEY);}catch(e){}
  apply(saved||'dark');
  document.querySelectorAll('[data-set-theme]').forEach(function(el){
    el.addEventListener('click',function(){var t=el.getAttribute('data-set-theme');apply(t);try{localStorage.setItem(KEY,t);}catch(e){}});
  });
})();


/* ASCII skill bars sized to fill the column: [████████░░] with as many cells as fit */
(function(){
  function draw(){
    document.querySelectorAll('.sk-dots').forEach(function(el){
      var lvl=+el.parentElement.getAttribute('data-lvl')||0;
      var probe=document.createElement('span'); probe.textContent='██████████'; probe.style.cssText='position:absolute;visibility:hidden;white-space:pre;font:inherit;';
      el.appendChild(probe); var cw=probe.getBoundingClientRect().width/10; probe.remove();
      var w=el.getBoundingClientRect().width;   // same (zoomed) units as the probe
      if(!cw||!w) return;
      var n=Math.min(80,Math.floor(w/cw)-2), f=Math.round(n*lvl/5);
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
