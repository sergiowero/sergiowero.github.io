/* Downloads the CV in whatever language is on screen, without the site header.
   PDF  — the browser's own print dialog (.site-nav is display:none when printing, so the header never lands in it).
   DOCX — written here from #cv-data (same source as the page), always on a light page so it stays editable.
   No dependencies: the zip container and the OOXML parts are built by hand. */
(function () {
  var dataEl = document.getElementById('cv-data');
  if (!dataEl) return;
  var CV = JSON.parse(dataEl.textContent);
  var START_YEAR = 2010;
  var INK = '0B1220', BODY = '3D444D', MUTED = '6E7781', GREEN = '1A7F37', LINK = '0969DA', RULE = 'D0D7DE';

  function lang() {
    return window.cvLang ? window.cvLang()
      : (document.documentElement.getAttribute('data-lang') === 'es' ? 'es' : 'en');
  }
  function L(v) { return (v && typeof v === 'object' && !Array.isArray(v)) ? (v[lang()] || v.en) : v; }
  function label(k) { return textOf(L(CV.labels[k])); }
  function years() { return new Date().getFullYear() - START_YEAR; }
  function fileBase() { return 'Sergio-Sanchez-CV-' + lang().toUpperCase(); }

  // ---------------------------------------------------------------- PDF (print dialog)
  /* Prints exactly what is on screen — current theme and language. The page sets
     print-color-adjust:exact on <html>, so the dark background survives the print dialog too. */
  function exportPDF() {
    var prev = document.title;
    document.title = fileBase();   // browsers propose the document title as the PDF file name
    window.addEventListener('afterprint', function restore() {
      document.title = prev;
      window.removeEventListener('afterprint', restore);
    });
    window.print();
  }

  // ---------------------------------------------------------------- zip (stored, no compression)
  var CRC_TABLE = (function () {
    var t = new Int32Array(256);
    for (var n = 0; n < 256; n++) {
      var c = n;
      for (var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[n] = c;
    }
    return t;
  })();

  function crc32(bytes) {
    var c = -1;
    for (var i = 0; i < bytes.length; i++) c = (c >>> 8) ^ CRC_TABLE[(c ^ bytes[i]) & 0xFF];
    return (c ^ -1) >>> 0;
  }

  function zip(files) {
    var enc = new TextEncoder(), parts = [], central = [], offset = 0, count = 0, cdSize = 0;
    files.forEach(function (f) {
      var name = enc.encode(f.name), bytes = enc.encode(f.xml), crc = crc32(bytes), size = bytes.length;
      var lh = new DataView(new ArrayBuffer(30));
      lh.setUint32(0, 0x04034b50, true);
      lh.setUint16(4, 20, true); lh.setUint16(6, 0x0800, true); lh.setUint16(8, 0, true);
      lh.setUint16(10, 0, true); lh.setUint16(12, 0x21, true);
      lh.setUint32(14, crc, true); lh.setUint32(18, size, true); lh.setUint32(22, size, true);
      lh.setUint16(26, name.length, true); lh.setUint16(28, 0, true);
      parts.push(new Uint8Array(lh.buffer), name, bytes);

      var ch = new DataView(new ArrayBuffer(46));
      ch.setUint32(0, 0x02014b50, true);
      ch.setUint16(4, 20, true); ch.setUint16(6, 20, true);
      ch.setUint16(8, 0x0800, true); ch.setUint16(10, 0, true);
      ch.setUint16(12, 0, true); ch.setUint16(14, 0x21, true);
      ch.setUint32(16, crc, true); ch.setUint32(20, size, true); ch.setUint32(24, size, true);
      ch.setUint16(28, name.length, true);
      ch.setUint32(42, offset, true);
      central.push(new Uint8Array(ch.buffer), name);
      offset += 30 + name.length + size;
      cdSize += 46 + name.length;
      count++;
    });
    var eocd = new DataView(new ArrayBuffer(22));
    eocd.setUint32(0, 0x06054b50, true);
    eocd.setUint16(8, count, true); eocd.setUint16(10, count, true);
    eocd.setUint32(12, cdSize, true); eocd.setUint32(16, offset, true);
    return new Blob(parts.concat(central, [new Uint8Array(eocd.buffer)]),
      { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
  }

  // ---------------------------------------------------------------- OOXML
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function textOf(html) {
    var t = document.createElement('template');
    t.innerHTML = html;
    return t.content.textContent;
  }

  var rels = [];   // hyperlink targets, in the order they appear
  function relId(href) {
    rels.push(href);
    return 'rIdL' + rels.length;
  }

  /* w:rPr children follow a fixed schema order: b, i, caps, color, spacing, sz, szCs, u */
  function rPr(o) {
    return '<w:rPr>' + (o.b ? '<w:b/>' : '') + (o.i ? '<w:i/>' : '') +
      (o.caps ? '<w:caps/>' : '') +
      (o.color ? '<w:color w:val="' + o.color + '"/>' : '') +
      (o.caps ? '<w:spacing w:val="20"/>' : '') +
      '<w:sz w:val="' + (o.sz || 19) + '"/><w:szCs w:val="' + (o.sz || 19) + '"/>' +
      (o.u ? '<w:u w:val="single"/>' : '') + '</w:rPr>';
  }
  function run(text, o) {
    o = o || {};
    var r = '<w:r>' + rPr(o) + '<w:t xml:space="preserve">' + esc(text) + '</w:t></w:r>';
    return o.href ? '<w:hyperlink r:id="' + relId(o.href) + '">' + r + '</w:hyperlink>' : r;
  }
  /* and w:pPr children: numPr, pBdr, spacing */
  function para(runs, o) {
    o = o || {};
    return '<w:p><w:pPr>' +
      (o.bullet ? '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>' : '') +
      (o.rule ? '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="3" w:color="' + RULE + '"/></w:pBdr>' : '') +
      '<w:spacing w:before="' + (o.before || 0) + '" w:after="' + (o.after == null ? 40 : o.after) +
      '" w:line="240" w:lineRule="auto"/>' +
      '</w:pPr>' + runs + '</w:p>';
  }
  function heading(text) {
    return para(run(text, { b: true, caps: true, color: GREEN, sz: 18 }), { before: 220, after: 80, rule: true });
  }

  /* The CV strings carry light HTML (<b>, <a>, <span class="stack">, <span data-years>) — turn it into runs. */
  function runsFrom(html, base) {
    var tpl = document.createElement('template');
    tpl.innerHTML = html;
    var out = '';
    (function walk(node, st) {
      Array.prototype.forEach.call(node.childNodes, function (n) {
        if (n.nodeType === 3) { if (n.nodeValue) out += run(n.nodeValue, st); return; }
        if (n.nodeType !== 1) return;
        var s = {}, key;
        for (key in st) s[key] = st[key];
        var tag = n.tagName.toLowerCase();
        if (tag === 'b' || tag === 'strong') s.b = true;
        if (tag === 'i' || tag === 'em') s.i = true;
        if (tag === 'a') { s.href = n.getAttribute('href'); s.color = LINK; s.u = true; }
        if (n.classList.contains('stack')) s.color = MUTED;
        if (n.hasAttribute('data-years')) { out += run(String(years()), s); return; }
        walk(n, s);
      });
    })(tpl.content, base || { color: BODY });
    return out;
  }

  function period(job) {
    var M = CV.months[lang()], now = new Date();
    function ym(s) { var p = s.split('-'); return { y: +p[0], m: +p[1] }; }
    function fmt(d) { return M[d.m - 1] + ' ' + d.y; }
    var a = ym(job.frm), b = job.to ? ym(job.to) : { y: now.getFullYear(), m: now.getMonth() + 1 };
    var months = (b.y - a.y) * 12 + (b.m - a.m) + 1;
    var y = Math.floor(months / 12), m = months % 12, parts = [];
    if (y) parts.push(y + label(y === 1 ? 'yr' : 'yrs'));
    if (m) parts.push(m + label(m === 1 ? 'mo' : 'mos'));
    return fmt(a) + ' — ' + (job.to ? fmt(b) : label('present')) + ' · ' + parts.join(' ');
  }

  function documentXml() {
    rels = [];
    var body = '';

    body += para(run(CV.name, { b: true, color: INK, sz: 40 }), { after: 30 });
    body += para(run(textOf(L(CV.role)), { color: MUTED, sz: 19 }), { after: 60 });

    var contact = '';
    CV.contact.forEach(function (c, i) {
      if (i) contact += run('  ·  ', { color: RULE, sz: 17 });
      contact += run(c.text, c.href ? { href: c.href, color: LINK, sz: 17 } : { color: BODY, sz: 17 });
    });
    body += para(contact, { after: 60, rule: true });

    body += heading(label('profile'));
    body += para(runsFrom(L(CV.profile)), { after: 60 });

    body += heading(label('experience'));
    CV.jobs.forEach(function (job) {
      body += para(run(textOf(L(job.role)), { b: true, color: INK, sz: 21 }) +
        run('  ·  ' + job.co, { b: true, color: LINK, sz: 21 }), { before: 120, after: 0 });
      var meta = period(job) + '  ·  ' + textOf(L(job.loc));
      var inds = L(job.inds).map(function (x) { return textOf(L(x)); }).join(', ');
      if (inds) meta += '  ·  ' + inds;
      body += para(run(meta, { color: MUTED, sz: 17 }), { after: 40 });
      L(job.pts).forEach(function (pt) { body += para(runsFrom(L(pt)), { bullet: true }); });
    });

    body += heading(label('core'));
    CV.core.forEach(function (sk) {
      body += para(run(sk.name, { b: true, color: INK }) + run('  —  ' + L(sk.word), { color: MUTED }), { after: 20 });
    });

    body += heading(label('tech'));
    body += para(run(CV.tech.map(function (x) { return textOf(L(x)); }).join('  ·  '), { color: BODY }));

    body += heading(textOf(L(CV.ai.head)));
    body += para(run(textOf(L(CV.ai.text)), { color: BODY }), { after: 30 });
    body += para(run(CV.ai.chips.join('  ·  '), { color: GREEN, b: true, sz: 17 }));

    body += heading(label('titles'));
    L(CV.titles).forEach(function (t) { body += para(runsFrom(L(t)), { bullet: true }); });

    body += heading(label('education'));
    CV.edu.forEach(function (e) {
      body += para(run(textOf(L(e.deg)), { b: true, color: INK }) +
        run('  ·  ' + textOf(L(e.meta)), { color: MUTED, sz: 17 }), { after: 20 });
    });

    body += '<w:p><w:pPr><w:spacing w:before="200"/></w:pPr>' +
      run(CV.site, { color: MUTED, sz: 16 }) + '</w:p>';

    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"' +
      ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>' + body +
      '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>' +
      '<w:pgMar w:top="850" w:right="850" w:bottom="850" w:left="850" w:header="0" w:footer="0" w:gutter="0"/>' +
      '</w:sectPr></w:body></w:document>';
  }

  var STYLES_XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">' +
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>' +
    '<w:color w:val="' + BODY + '"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr></w:rPrDefault>' +
    '<w:pPrDefault><w:pPr><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>' +
    '</w:docDefaults>' +
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>' +
    '</w:styles>';

  var NUMBERING_XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">' +
    '<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/>' +
    '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/>' +
    '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="340" w:hanging="220"/></w:pPr>' +
    '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:hint="default"/><w:color w:val="' + GREEN + '"/></w:rPr>' +
    '</w:lvl></w:abstractNum>' +
    '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>';

  var CONTENT_TYPES =
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
    '<Default Extension="xml" ContentType="application/xml"/>' +
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>' +
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>' +
    '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>' +
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>' +
    '</Types>';

  var ROOT_RELS =
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>' +
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>' +
    '</Relationships>';

  function documentRels() {
    var out = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
      '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' +
      '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>';
    rels.forEach(function (href, i) {
      out += '<Relationship Id="rIdL' + (i + 1) + '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"' +
        ' Target="' + esc(href) + '" TargetMode="External"/>';
    });
    return out + '</Relationships>';
  }

  function coreXml() {
    var now = new Date().toISOString().replace(/\.\d+Z$/, 'Z');
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"' +
      ' xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"' +
      ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
      '<dc:title>' + esc(CV.name) + ' — CV</dc:title>' +
      '<dc:creator>' + esc(CV.name) + '</dc:creator>' +
      '<cp:lastModifiedBy>' + esc(CV.name) + '</cp:lastModifiedBy>' +
      '<dcterms:created xsi:type="dcterms:W3CDTF">' + now + '</dcterms:created>' +
      '<dcterms:modified xsi:type="dcterms:W3CDTF">' + now + '</dcterms:modified>' +
      '</cp:coreProperties>';
  }

  function exportDOCX() {
    var doc = documentXml();   // fills `rels` as it walks the links
    var blob = zip([
      { name: '[Content_Types].xml', xml: CONTENT_TYPES },
      { name: '_rels/.rels', xml: ROOT_RELS },
      { name: 'docProps/core.xml', xml: coreXml() },
      { name: 'word/document.xml', xml: doc },
      { name: 'word/_rels/document.xml.rels', xml: documentRels() },
      { name: 'word/styles.xml', xml: STYLES_XML },
      { name: 'word/numbering.xml', xml: NUMBERING_XML }
    ]);
    var url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url;
    a.download = fileBase() + '.docx';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  }

  document.querySelectorAll('[data-export]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (btn.getAttribute('data-export') === 'pdf') exportPDF(); else exportDOCX();
    });
  });
})();
