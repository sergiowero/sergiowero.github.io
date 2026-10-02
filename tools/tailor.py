#!/usr/bin/env python3
"""CVs tailored to a job description, published at /tailor-cv/<company>-<position>-<yyyymmdd>.html.

The master CV (tools/gen.py) stays the only source of truth. A tailored CV is a *spec*, tailor-cv/<name>.json, written
by the /tailor-cv skill (.claude/skills/tailor-cv/SKILL.md) from a job description. The spec picks and rewrites; it
never invents: every bullet names the records of /cv/{en,es}/tree.json it comes from, and `build` refuses a spec that
breaks a rule. The page is drawn by gen.py's own fill() and page() with the spec as the view (gen.master_view), so it
looks exactly like the master CV and keeps its three downloads (DOCX ATS, PDF ATS, PDF).

  tailor-cv/<name>.json          the spec (not published)
  public/tailor-cv/<name>.html   the CV                    → /tailor-cv/<name>.html
  public/tailor-cv/<name>.md     the job description it answers, next to it (same name)
  public/tailor-cv/index.html    the explorer: every CV in one list, with a live preview → /tailor-cv/

  python3 tools/tailor.py new <jd.md | -> --company "Acme" --position "Backend Engineer" [--lang es] [--url …]
  python3 tools/tailor.py analyze <name>     what the JD asks for and what the tree has, job by job
  python3 tools/tailor.py show <id> [<id>…]  records in both languages, to write from
  python3 tools/tailor.py build <name>       validate + write public/tailor-cv/<name>.html (and the explorer) + one-page check
  python3 tools/tailor.py check <page.html>  one-page check of any CV page (public/index.html is the baseline)
  python3 tools/tailor.py index              write the explorer, public/tailor-cv/index.html, from every spec
  python3 tools/tailor.py render-all         re-render every spec and the explorer with the current design (gen.py runs it)

The rules `build` enforces (the spec format is in the skill):
  - The 6 jobs of the master CV, in its order, each with at least one bullet. Contact, stats, the AI box, education
    and languages are the master's: a spec has no key for them.
  - A job with children (Wizeline's client projects). "tailored": only the relevant children, with one or more
    bullets each ("**Fox Corp:** …"). "fallback", when no child is relevant: every child's master bullet, rewritten
    toward the JD. Either way the job may add bullets from its own content (not a child's) that are relevant.
  - A job without children. "tailored": only relevant bullets, from any of its records. "fallback", when nothing is
    relevant: its master bullets, one for one, rewritten toward the JD.
  - Every bullet cites `sources` inside its job (a child bullet: inside that child). Its text may not name a
    technology, a tool or a number its sources don't back, nor one of the technologies that are nowhere in the tree.
  - Summary: may change a little; {years} stands for the years of experience. Roles: the master's, reordered or fewer.
  - Core skills, the tech chips and "Best skills" change only for what the JD strictly requires (jd.required, each
    with a quote from the JD) and the tree backs. Levels come from gen.CORE / gen.CORE_EXTRA, never from a spec.
  - <name> is <company>-<position>-<yyyymmdd>, slugged, and names all three files.
"""
import argparse
import difflib
import functools
import glob
import hashlib
import html as _html
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date

if sys.version_info < (3, 12):
    sys.exit("tools/tailor.py needs Python 3.12+, like tools/gen.py: try python3.12 (Windows: py -3.12)")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen  # noqa: E402  the master CV: its data, its tree of records and its renderer
from gen import T  # noqa: E402

SPECS = os.path.join(gen.ROOT, "tailor-cv")      # the specs, <name>.json
OUT = os.path.join(gen.PUBLIC, "tailor-cv")      # the CVs, <name>.html, each with its job description beside it, <name>.md
SCHEMA = "tailor-cv/1"
LANGS = gen.CV_LANGS
MODES = ("tailored", "fallback")
A4_PX = 297 / 25.4 * 96                          # the sheet's height in CSS px (1122.5)
CORE_CATEGORIES = {"language", "framework", "runtime", "engine", "cloud", "database"}   # what a core-skill meter measures

# Technologies that are nowhere in the timeline (not in gen.TECH_CATALOG). Naming one claims something the tree does
# not back — usually a keyword copied from the JD — so `build` refuses it. If you do have one, add it to the timeline
# in gen.py: it then enters TECH_CATALOG and stops counting here. Case-sensitive, as they are written.
UNBACKED = """
Kotlin Scala Rust Swift Elixir Erlang Haskell Clojure Perl Dart Groovy Solidity COBOL Fortran F# VB.NET Bash PowerShell
Angular AngularJS Vue Vue.js Nuxt Svelte SvelteKit Ember Redux NestJS Express.js Laravel Rails Symfony ASP.NET Blazor
WPF WinForms Xamarin MAUI Hibernate JPA Quarkus Micronaut Vert.x Gatsby Remix Astro Tailwind Bootstrap Sass SCSS
Webpack Vite Storybook Flutter Ionic Cordova Electron Unreal Godot CryEngine Cocos2d Phaser Three.js WebGL Vulkan
DirectX OpenXR ARKit ARCore Photon PlayFab Nakama GameLift HTML HTML5 CSS CSS3
Jest Mocha Cypress Selenium Playwright Puppeteer JUnit TestNG Mockito NUnit xUnit pytest RSpec Cucumber Swagger
GraphQL gRPC Protobuf WebSocket WebSockets SignalR Socket.IO MQTT AMQP Kafka RabbitMQ ActiveMQ NATS Pulsar
Redis Memcached MongoDB DynamoDB Cassandra CouchDB Couchbase Neo4j Elasticsearch OpenSearch Solr MySQL MSSQL Oracle
SQLite T-SQL PL/SQL Redshift BigQuery Aurora Firestore Firebase Supabase CockroachDB TimescaleDB InfluxDB ClickHouse
Kubernetes K8s k8s OpenShift Helm Istio Terraform Pulumi CloudFormation CDK Ansible Chef Puppet Vagrant Packer Jenkins
GitLab CircleCI Bitbucket ArgoCD Spinnaker Nginx Apache Tomcat IIS Linux Unix Ubuntu Debian CentOS RHEL
Azure GCP BigTable Heroku Vercel Netlify DigitalOcean Cloudflare EC2 S3 EKS AKS GKE Fargate RDS CloudFront IAM
Cognito Kinesis EventBridge Athena SageMaker Bedrock ElastiCache Datadog Prometheus Grafana Splunk Sentry Kibana
Logstash ELK Jaeger OpenTelemetry PagerDuty Jira Confluence OAuth OAuth2 OIDC SAML JWT Keycloak Okta Auth0
Pandas NumPy SciPy PyTorch TensorFlow Keras scikit-learn Spark PySpark Hadoop Hive Airflow dbt Databricks Flink
LlamaIndex OpenAI GPT Pinecone Weaviate pgvector RAG MLflow Kubeflow Streamlit MCP TDD BDD CQRS SRE MLOps NLP
""".split() + ["React Native", "Ruby on Rails", "Entity Framework", "Unreal Engine", "SQL Server", "Google Cloud",
               "GitHub Actions", "GitLab CI", "Azure DevOps", "API Gateway", "Step Functions", "Event Sourcing",
               "Hexagonal Architecture", "Hugging Face", "Deep Learning", "Computer Vision", "New Relic",
               "Travis CI", "Cloud Run", "Cloud Functions", "App Engine", "Elastic Beanstalk", "Route 53"]
# Ways of working the tree does not name either: a warning, not an error — say them only if a source backs them.
UNBACKED_SOFT = ["Agile", "agile", "Scrum", "scrum", "Kanban", "SAFe", "SOLID", "Machine Learning", "machine learning",
                 "Pair programming", "pair programming"]

NUM_WORDS = {"en": dict(two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9, ten=10, eleven=11, twelve=12),
             "es": dict(dos=2, tres=3, cuatro=4, cinco=5, seis=6, siete=7, ocho=8, nueve=9, diez=10, once=11, doce=12)}
# Aliases too common as plain words to match in any case ("go", "react to", "spring 2027"): only as the catalog writes them.
CASE_ONLY = {"go", "c", "flow", "rider", "cursor", "steam", "spring", "codex", "react", "flask", "git"}


# ------------------------------------------------------------------ text helpers
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def spec_name(company, position, day):
    """day: YYYY-MM-DD → acme-senior-backend-engineer-20260929"""
    return f"{slug(company)}-{slug(position)}-{day.replace('-', '')}"


def plain(md):
    """The spec's Markdown subset as plain text; {years} is spelled out."""
    return gen._plain(md or "").replace("{years}", str(gen.YEARS))


def md_html(md):
    """The spec's Markdown subset (**bold**, [text](url)) → the page's HTML; {years} counts in the browser, like the master."""
    return gen._md_html(md).replace("{years}", f"<span data-years>{gen.YEARS}</span>")


_NUM_RX = re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)*(?!\w)")


def numbers(md, lang):
    """The numbers a text states ("100,000", "5", "five"); digits inside a name (Unity3D, 9mm, 3D) don't count."""
    t = gen._plain(md or "").replace("{years}", " ")
    out = set()
    for s in _NUM_RX.findall(t):
        if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", s):
            s = re.sub(r"[.,]", "", s)
        out.add(s.replace(",", "."))
    for w, n in NUM_WORDS[lang].items():
        if re.search(rf"(?<!\w){w}(?!\w)", t, re.I):
            out.add(str(n))
    return out


PARENT = {tid: spec[2] for tid, spec in gen.TECH_CATALOG.items()}


def up(ids):
    """Technologies plus their parents: aws-lambda → aws, spring-boot → spring."""
    out = set()
    for t in ids:
        while t and t not in out:
            out.add(t)
            t = PARENT.get(t)
    return out


def tech_named(text):
    """Catalog technologies a (plain) text names, by the catalog's own case-sensitive patterns."""
    return {tid for tid, rx in gen._TECH_RX if rx.search(text)}


def _word_rx(term, flags=0):
    return re.compile(r"(?<![\w.#+-])" + re.escape(term) + r"(?![\w#+])", flags)


_KNOWN = {a.lower() for spec in gen.TECH_CATALOG.values() for a in [spec[0]] + spec[3]}
_UNBACKED_RX = [(t, _word_rx(t)) for t in UNBACKED if t.lower() not in _KNOWN]
_SOFT_RX = [(t, _word_rx(t)) for t in UNBACKED_SOFT]


def unbacked(text):
    """(technologies, ways of working) a text names that are nowhere in the tree."""
    soft = {t.capitalize() if t.islower() else t for t, rx in _SOFT_RX if rx.search(text)}
    hard = {t for t, rx in _UNBACKED_RX if rx.search(text)}
    hard = {t for t in hard if not any(t != u and t in u for u in hard)}   # "Unreal Engine", not also "Unreal"
    return sorted(hard), sorted(soft)


def detect(text):
    """(tech ids, tag ids) a text asks for: the catalog and TAGS patterns, plus names, aliases and labels in any case."""
    tech, tags = _detect(text)
    return set(tech), set(tags)


@functools.lru_cache(maxsize=None)
def _detect(text):
    low = text.lower()
    tech = tech_named(text)
    for tid, spec in gen.TECH_CATALOG.items():
        for a in [spec[0]] + spec[3]:
            if a.lower() not in CASE_ONLY and _word_rx(a.lower()).search(low):
                tech.add(tid)
    tags = {gid for gid, rx in gen._TAG_RX if rx.search(text)}
    for gid, spec in gen.TAGS.items():
        # labels in both languages; of the stack aliases only phrases ("Message queues"), not words ("REST", "Online")
        for a in [spec[1].en, spec[1].es] + [a for a in spec[3] if not a.isalpha()]:
            a = _html.unescape(a).lower()
            if len(a) > 3 and re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", low):
                tags.add(gid)
    return frozenset(tech), frozenset(tags)


def jd_asks(spec, jd, also=()):
    """(tech ids, tag ids) the JD asks for: what detect() finds, plus jd.terms — the ids you read in it that the
    patterns miss (they are English; a Spanish JD needs this) — and jd.required."""
    jt, jg = detect(jd)
    extra = list((spec.get("jd") or {}).get("terms") or []) + list(also)
    extra += [r["id"] for r in (spec.get("jd") or {}).get("required") or [] if isinstance(r, dict) and "id" in r]
    for x in extra:
        (jt if x in gen.TECH_CATALOG else jg if x in gen.TAGS else set()).add(x)
    return jt, jg


def jd_sentences(jd):
    return [s.strip(" \t-*•·") for s in re.split(r"(?<=[.!?;])\s+|\n+", jd) if s.strip(" \t-*•·")]


# words that mark a sentence as a requirement, so a quote comes from "Requirements" rather than from the title
REQ_CUES = re.compile(r"\b(experience|years?|strong|solid|proficien\w*|required|must|hands-on|knowledge|expert\w*|"
                      r"experiencia|años|sólid\w*|dominio|requisito\w*|indispensable|conocimiento\w*)\b", re.I)


def quote_for(sents, rid):
    """The JD sentence that asks for rid — a requirement if one does, else the first that names it."""
    named = [s for s in sents if rid in up(detect(s)[0]) | detect(s)[1]]
    return next((s for s in named if REQ_CUES.search(s)), named[0] if named else "")


def _norm(s):
    return re.sub(r"\s+", " ", _html.unescape(s)).strip().lower()


# ------------------------------------------------------------------ the master CV, as the rules see it
class Master:
    """The master CV's records in both languages (gen.cv_tree) plus what the rules need: the 6 jobs, each job's
    children (entries inside it) and master bullets, which child a master bullet is about, and every subtree."""

    def __init__(self):
        self.tree = {lang: gen.cv_tree(lang) for lang in LANGS}
        self.rec = {lang: {r["id"]: r for r in self.tree[lang]["records"]} for lang in LANGS}
        en = self.rec["en"]
        self.order = [r["id"] for r in self.tree["en"]["records"]]
        self.vtech = self.tree["en"]["vocabulary"]["tech"]
        self.vtags = self.tree["en"]["vocabulary"]["tags"]
        resume = self.tree["en"]["resume"]["experience"]
        self.jobs = [e["id"] for e in resume]
        self.bullets = {e["id"]: list(e["highlight_ids"]) for e in resume}
        self.job_src = {gen._job_entry(j)["slug"]: j for j in gen.JOBS}
        self.children = {j: [c for c in en[j]["children"] if en[c]["entry"]] for j in self.jobs}
        self.bullet_child = {}   # "**Fox Corp:** …" is the master bullet of the child whose organization is Fox Corp
        for j in self.jobs:
            for b in self.bullets[j]:
                for c in self.children[j]:
                    if en[b]["text"].startswith(f"**{en[c]['organization']}:**"):
                        self.bullet_child[b] = c
        self.sub = {}
        for r in en.values():
            for a in r["path"]:
                self.sub.setdefault(a, set()).add(r["id"])

    def r(self, rid, lang="en"):
        return self.rec[lang][rid]

    def scope(self, job, child=None):
        """The records a bullet may cite: a child's subtree (and its master bullet); a job's own content, which in a
        job with children is everything but the children and their master bullets."""
        mapped = {b for b in self.bullets[job] if self.bullet_child.get(b)}
        if child:
            return self.sub[child] | {b for b in mapped if self.bullet_child[b] == child}
        own = set(self.sub[job])
        for c in self.children[job]:
            own -= self.sub[c]
        return own - mapped

    def texts(self, rid, lang):
        r = self.r(rid, lang)
        out = [r["title"], r["subtitle"], r["text"], r["result"], r["role"], r["organization"]]
        out += [f["value"] for f in r["facts"]] + list(r["stack"])
        return [x for x in out if x]

    def backing(self, root, sources):
        """What a bullet's sources back: technologies (with parents), tags and numbers of the sources, the records
        between the scope's root and each source, and the root itself."""
        ids = {root}
        for s in sources:
            ids.add(s)
            ids.update(a for a in self.r(s)["path"] if a in self.sub[root])
        tech, tags, nums = set(), set(), set()
        for i in ids:
            tech.update(self.r(i)["tech"])
            tags.update(self.r(i)["tags"])
            for lang in LANGS:
                for t in self.texts(i, lang):
                    nums |= numbers(t, lang)
        job = self.r(root)["context"]["job"] or root
        for k in ("start", "end"):
            d = (self.r(job)["dates"] or {}).get(k)
            if d:
                nums.add(d[:4])
        return up(tech), tags, nums

    def describe(self, rid, lang="en"):
        r = self.r(rid, lang)
        if r["type"] == "highlight":
            return r["text"]
        if r["entry"]:
            return " — ".join(x for x in [r["title"], r["text"]] if x)
        head = " — ".join(x for x in [r["title"], r["subtitle"]] if x)
        if r["result"]:
            head += f" → {r['result_label']}: {r['result']}"
        return head


# ------------------------------------------------------------------ the spec
def paths(name):
    """name → (name, spec, job description, page): the job description sits next to the page, with its name."""
    name = os.path.splitext(os.path.basename(name))[0]
    return name, os.path.join(SPECS, name + ".json"), os.path.join(OUT, name + ".md"), os.path.join(OUT, name + ".html")


def jd_markdown(jd, spec):
    """The job description as saved next to its CV: a front matter saying what it is, then the text as given."""
    j = spec["jd"]
    meta = [("company", j["company"]), ("position", j["position"]), ("date", j["date"]), ("lang", j["lang"]),
            ("url", j.get("url") or ""), ("cv", f"/tailor-cv/{spec['name']}.html")]
    return "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in meta) + "---\n\n" + jd.strip() + "\n"


def read_jd(path):
    """The job description's text, without its front matter."""
    if not os.path.exists(path):
        return ""
    text = open(path, encoding="utf-8").read()
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S).strip() + "\n"


def load(name):
    name, spec_path, jd_path, _ = paths(name)
    if not os.path.exists(spec_path):
        sys.exit(f"no spec at {os.path.relpath(spec_path, gen.ROOT)}: create it with `tailor.py new`")
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    return name, spec, read_jd(jd_path)


def skills_of(required, drop):
    """Core skills, tech chips and "Best skills" for a JD's strict requirements (ids, in the JD's order): what the JD
    requires moves to the front; a core skill enters only from gen.CORE / CORE_EXTRA (its level is yours, not the
    spec's); a required technology with no chip gets one. No requirement → exactly the master's."""
    def ids(s):
        t, g = gen._resolve(s)
        return set(t) | set(g)

    def match(rid, s):
        have = ids(s)
        return rid in up(have) or bool(have & up({rid}))

    pool = gen.CORE + gen.CORE_EXTRA
    core = []
    for rid in required:
        core += [e for e in pool if e not in core and match(rid, e[0])]
    core = (core + [e for e in gen.CORE if e not in core])[:len(gen.CORE)]
    tech = []   # a chip is a keyword: "Amazon SQS" gets its own chip even though "AWS" is one already
    for rid in required:
        exact = [c for c in gen.TECH if rid in ids(c)]
        if exact:
            tech += [c for c in exact if c not in tech]
        elif rid in gen.TECH_CATALOG and gen.TECH_CATALOG[rid][0] not in tech:
            tech.append(gen.TECH_CATALOG[rid][0])
        elif rid in gen.TAGS and gen.TAGS[rid][0] in ("domain", "practice") and gen.TAGS[rid][1] not in tech:
            tech.append(gen.TAGS[rid][1])
    tech += [c for c in gen.TECH if c not in tech and gen.plain(c) not in drop]
    best = []
    for rid in required:
        best += [b for b in gen.BEST_SKILLS if b not in best and match(rid, b)]
    best += [b for b in gen.BEST_SKILLS if b not in best]
    return core, tech, best


def bullet_html(b, lang, m):
    s = md_html(b[lang])
    if b.get("child"):   # a child's bullet opens with its client, as on the master: "<b>Fox Corp:</b> …"
        s = f"<b>{_html.escape(m.r(b['child'])['organization'], quote=False)}:</b> {s}"
    if b.get("tech"):
        s += f' <span class="stack">Tech: {_html.escape(", ".join(b["tech"]), quote=False)}.</span>'
    return s


def file_base(spec):
    word = lambda s: re.sub(r"[^A-Za-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()).strip("-")
    return f"Sergio-Sanchez-CV-{word(spec['jd']['company'])}-{word(spec['jd']['position'])}"


def view_of(spec, m):
    """The spec as a gen view: what fill() draws instead of the master's roles, summary, bullets and skills."""
    roles = spec["profile"].get("roles")
    by_name = {gen.plain(r): r for r in gen.ROLES}
    s = spec["profile"]["summary"]
    jobs = []
    for e in spec["experience"]:
        pts = [T(bullet_html(b, "en", m), bullet_html(b, "es", m)) for b in e["bullets"]]
        jobs.append(dict(m.job_src[e["id"]], pts=pts))
    core, tech, best = skills_of([r["id"] for r in spec["jd"].get("required") or []], set((spec.get("skills") or {}).get("drop") or []))
    return dict(roles=[by_name[r] for r in roles] if roles else gen.ROLES, profile=T(md_html(s["en"]), md_html(s["es"])),
                jobs=jobs, core=core, tech=tech, best=best, file=file_base(spec))


# ------------------------------------------------------------------ validation
KEYS = {
    "spec": ({"schema", "name", "jd", "profile", "experience"}, {"skills", "notes"}),
    "jd": ({"company", "position", "date", "lang"}, {"url", "required", "gaps", "terms"}),
    "required": ({"id", "quote"}, set()),
    "profile": ({"summary"}, {"roles", "sources"}),
    "summary": ({"en", "es"}, set()),
    "job": ({"id", "mode", "bullets"}, {"why"}),
    "bullet": ({"en", "es", "sources"}, {"child", "tech"}),
    "skills": (set(), {"drop"}),
}


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def _keys(rep, where, obj, kind):
    need, extra = KEYS[kind]
    if not isinstance(obj, dict):
        rep.err(where, f"must be an object with {sorted(need)}")
        return False
    for k in sorted(need - set(obj)):
        rep.err(where, f"missing `{k}`")
    for k in sorted(set(obj) - need - extra):
        rep.err(where, f"unknown key `{k}` (allowed: {sorted(need | extra)}) — contact, stats, education and "
                       "languages are always the master's")
    return not (need - set(obj))


def _text(rep, where, md, lang, m, tech_ok, nums_ok, summary=False):
    """One text in one language: Markdown subset only, no technology / number / unbacked name its sources don't back."""
    if not isinstance(md, str) or not md.strip():
        rep.err(where, f"`{lang}` is empty")
        return
    if re.search(r"<[a-zA-Z/]", md):
        rep.err(where, f"`{lang}` has HTML: write **bold** and [text](url) only")
    if md.count("**") % 2:
        rep.err(where, f"`{lang}` has an unpaired **")
    if re.search(r"\bTech:\s", md):
        rep.err(where, f"`{lang}` ends in a stack line: put those technologies in `tech`")
    t = gen._plain(md).replace("{years}", "")
    if re.search(r"(?<!\w)(1\d|2\d)\+?\s*(years|yrs|años)", t):
        rep.err(where, f"`{lang}` spells out the years of experience: write {{years}}, the page counts them")
    named = up(tech_named(t))
    if summary:
        bad = sorted(x for x in named if not m.vtech[x]["usage"]["records"])
    else:
        bad = sorted(named - tech_ok)
    if bad:
        rep.err(where, f"`{lang}` names {', '.join(gen.TECH_CATALOG[x][0] for x in bad)}, which its sources don't back "
                       "— cite the record that does, or leave it out")
    hard, soft = unbacked(t)
    if hard:
        rep.err(where, f"`{lang}` names {', '.join(hard)}: nowhere in the tree — never write it (list it in jd.gaps)")
    if soft:
        rep.warn(where, f"`{lang}` says {', '.join(soft)}: the tree never does; keep it only if a source backs it")
    extra = sorted(numbers(md, lang) - nums_ok, key=lambda s: float(s))
    if extra:
        rep.err(where, f"`{lang}` states {', '.join(extra)}, which its sources don't — cite the record with it or drop it")


def validate(name, spec, jd, m):
    rep = Report()
    if not _keys(rep, "spec", spec, "spec"):
        return rep
    if spec["schema"] != SCHEMA:
        rep.err("schema", f"must be {SCHEMA!r}")
    if spec["name"] != name:
        rep.err("name", f"{spec['name']!r} but the file is {name}.json")
    jdx = spec["jd"] if isinstance(spec["jd"], dict) else {}
    if _keys(rep, "jd", spec["jd"], "jd"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(jdx["date"])):
            rep.err("jd.date", "must be YYYY-MM-DD")
        elif spec["name"] != spec_name(jdx["company"], jdx["position"], jdx["date"]):
            rep.err("name", f"must be {spec_name(jdx['company'], jdx['position'], jdx['date'])!r} (<company>-<position>-<yyyymmdd>)")
        if jdx["lang"] not in LANGS:
            rep.err("jd.lang", f"one of {LANGS}: the language the page opens in")
    if not jd.strip():
        rep.err("jd", f"no job description at public/tailor-cv/{name}.md")

    # -- skills: only what the JD strictly requires, quoted, and the tree backs
    required = []
    for i, req in enumerate(jdx.get("required") or []):
        w = f"jd.required[{i}]"
        if not _keys(rep, w, req, "required"):
            continue
        rid, quote = req["id"], req["quote"]
        if rid not in gen.TECH_CATALOG and rid not in gen.TAGS:
            rep.err(w, f"{rid!r} is neither a technology nor a tag of the vocabulary (tree.json → vocabulary)")
            continue
        have = m.vtech[rid]["usage"]["records"] if rid in gen.TECH_CATALOG else m.vtags[rid]["records"]
        if not have:
            rep.err(w, f"{rid!r}: the tree has no record with it — that is a gap (jd.gaps), not a requirement we meet")
        if not isinstance(quote, str) or _norm(quote) not in _norm(jd):
            rep.err(w, "`quote` must be copied from the job description, word for word")
        else:
            t, g = detect(quote)
            if rid not in up(t) | g and not (up({rid}) & up(t)):
                rep.warn(w, f"the quote does not name {rid!r} as the vocabulary writes it; make sure it really asks for it")
        required.append(rid)
        if rid in gen.TAGS and gen.TAGS[rid][0] not in ("domain", "practice"):
            rep.warn(w, f"{rid!r} is a {gen.TAGS[rid][0]}: it changes no skill (only technologies, domains and practices do)")
    for i, x in enumerate(jdx.get("terms") or []):
        if x not in gen.TECH_CATALOG and x not in gen.TAGS:
            rep.err(f"jd.terms[{i}]", f"{x!r} is neither a technology nor a tag id (tree.json → vocabulary)")
    drop = (spec.get("skills") or {}).get("drop") or []
    if spec.get("skills") is not None:
        _keys(rep, "skills", spec["skills"], "skills")
    names = {gen.plain(c): c for c in gen.TECH}
    for c in drop:
        if c not in names:
            rep.err("skills.drop", f"{c!r} is not a chip of the master CV ({', '.join(names)})")
        elif any(rid in up(set(gen._resolve(names[c])[0])) | set(gen._resolve(names[c])[1]) for rid in required):
            rep.err("skills.drop", f"{c!r} is required by the JD: it stays")
    for rid in required:   # a language, framework or engine the JD requires deserves a meter: only Sergio can give it a level
        if (rid in gen.TECH_CATALOG and gen.TECH_CATALOG[rid][1] in CORE_CATEGORIES
                and not any(rid in up(set(gen._resolve(n)[0])) or set(gen._resolve(n)[0]) & up({rid}) for n, _ in gen.CORE + gen.CORE_EXTRA)):
            rep.warn("skills", f"{gen.TECH_CATALOG[rid][0]} is required and in the tree, but has no level in gen.CORE / "
                               "CORE_EXTRA, so it can only be a chip: ask Sergio for a 1–10 level to make it a core skill")

    # -- profile
    prof = spec["profile"]
    if _keys(rep, "profile", prof, "profile") and isinstance(prof["summary"], dict):
        roles = prof.get("roles")
        master_roles = [gen.plain(r) for r in gen.ROLES]
        if roles is not None:
            if not roles or not all(r in master_roles for r in roles) or len(set(roles)) != len(roles):
                rep.err("profile.roles", f"the master's roles, reordered or fewer, none twice: {master_roles}")
        srcs = prof.get("sources") or []
        for s in srcs:
            if s not in m.rec["en"]:
                rep.err("profile.sources", f"no record {s!r}")
        nums = {"6"}   # "led teams of up to six people", the master's own stat
        for lang in LANGS:
            nums |= numbers(gen.ytext(gen.PROFILE, lang).replace(str(gen.YEARS), ""), lang)
            nums |= numbers(m.tree[lang]["profile"]["bio"], lang)
            for s in srcs:
                if s in m.rec["en"]:
                    for t in m.texts(s, lang):
                        nums |= numbers(t, lang)
        if _keys(rep, "profile.summary", prof["summary"], "summary"):
            for lang in LANGS:
                _text(rep, "profile.summary", prof["summary"][lang], lang, m, set(), nums, summary=True)
            words = lambda s: re.findall(r"\w+", s.lower())
            master = gen.plain(gen.PROFILE)
            ratio = difflib.SequenceMatcher(None, words(master), words(plain(prof["summary"]["en"]))).ratio()
            if ratio < 0.5:
                rep.warn("profile.summary", f"only {ratio:.0%} of the master's wording is left: the profile should change a little")
            if len(plain(prof["summary"]["en"])) > 1.2 * len(master):
                rep.warn("profile.summary", "longer than the master's by more than 20%: the page may not fit")

    # -- experience: the 6 jobs, in order
    exp = spec["experience"]
    if not isinstance(exp, list) or [e.get("id") if isinstance(e, dict) else None for e in exp] != m.jobs:
        rep.err("experience", f"must be the master's 6 jobs, in its order: {m.jobs}")
        return rep
    jt, jg = jd_asks(spec, jd)
    for e in exp:
        jid, wj = e["id"], f"experience[{e['id']}]"
        if not _keys(rep, wj, e, "job"):
            continue
        kids, master = m.children[jid], m.bullets[jid]
        if e["mode"] not in MODES:
            rep.err(wj, f"mode must be one of {MODES}")
            continue
        if not isinstance(e["bullets"], list) or not e["bullets"]:
            rep.err(wj, "needs at least one bullet")
            continue
        if not (e.get("why") or "").strip():
            rep.warn(wj, "no `why`: say which of its records are relevant to the JD (or that none is)")
        for i, b in enumerate(e["bullets"]):
            wb = f"{wj}.bullets[{i}]"
            if not _keys(rep, wb, b, "bullet"):
                continue
            child = b.get("child")
            if child is not None and child not in kids:
                rep.err(wb, f"`child` {child!r} is not one of {jid}'s children {kids or '(it has none)'}")
                continue
            srcs = b["sources"]
            if not isinstance(srcs, list) or not srcs:
                rep.err(wb, "`sources`: the ids of the records it comes from (tailor.py analyze / show)")
                continue
            unknown = [s for s in srcs if s not in m.rec["en"]]
            if unknown:
                rep.err(wb, f"no records {unknown}")
                continue
            scope = m.scope(jid, child)
            outside = [s for s in srcs if s not in scope]
            if outside:
                where = f"child {child}" if child else (f"{jid}'s own content (not a child's)" if kids else jid)
                rep.err(wb, f"sources {outside} are outside {where}" + ("" if child or not kids else
                        " — a bullet about a client needs `child`"))
                continue
            root = child or jid
            tech_ok, tags_ok, nums_ok = m.backing(root, srcs)
            for s in b.get("tech") or []:
                try:
                    t_ids, g_ids = gen._resolve(s)
                except ValueError:
                    rep.err(wb, f"`tech` {s!r} is not in the vocabulary: write it as tree.json names it")
                    continue
                if not set(t_ids) <= tech_ok or not set(g_ids) <= tags_ok:
                    rep.err(wb, f"`tech` {s!r}: its sources don't back it")
            for lang in LANGS:
                _text(rep, wb, b[lang], lang, m, tech_ok, nums_ok)
            if len(plain(b["en"])) > 300:
                rep.warn(wb, "over 300 characters: long bullets cost the page lines")
            if e["mode"] == "tailored":
                ts = up(set().union(*(m.r(s)["tech"] for s in srcs)))
                gs = set().union(*(m.r(s)["tags"] for s in srcs))
                if not (ts & up(jt)) and not (gs & jg):
                    rep.warn(wb, "none of its sources' technologies or tags appears in the JD: is it relevant?")
        # -- the mode's shape
        bl = [b for b in e["bullets"] if isinstance(b, dict) and isinstance(b.get("sources"), list)]
        derived = [b for b in bl if set(b["sources"]) & set(master)]
        if e["mode"] == "fallback":
            cited = [[s for s in b["sources"] if s in master] for b in derived]
            if any(len(c) > 1 for c in cited) or [c[0] for c in cited] != master:
                rep.err(wj, f"fallback keeps every master bullet, in order, one bullet each: {master}")
            extra = [b for b in bl if b not in derived]
            if extra and not kids:
                rep.err(wj, "fallback (nothing relevant) has only its master bullets, rewritten toward the JD")
            if any(b.get("child") for b in extra):
                rep.err(wj, "in fallback the children show only through their master bullets; extra bullets are the job's own")
        elif kids and not any(b.get("child") for b in bl):
            rep.err(wj, "tailored shows the relevant children (≥1); if none is relevant, use fallback")
        per = {}
        for b in bl:
            if b.get("child"):
                per[b["child"]] = per.get(b["child"], 0) + 1
        for c, n in per.items():
            if n > 2:
                rep.warn(wj, f"{n} bullets for {c}: two at most keeps the page to one sheet")
    return rep


# ------------------------------------------------------------------ rendering
def meta_of(spec, view):
    jdx = spec["jd"]
    lang = jdx["lang"]
    summary = gen.plain(view["profile"], lang)
    where = gen.CONTACT[0][1]
    m = dict(path=f"/tailor-cv/{spec['name']}.html", type="profile",
             title=f"{gen.SHORT_NAME} — {jdx['position']} · {jdx['company']} | CV",
             description=gen._sentences(summary, 2),
             labels=[("Experience" if lang == "en" else "Experiencia", f"{gen.YEARS}+ " + ("years" if lang == "en" else "años")),
                     ("Based in" if lang == "en" else "Ubicación", where)],
             image_alt=f"{gen.NAME}: {', '.join(gen.plain(r, lang) for r in view['roles'])}.")
    out = gen.meta_html("cv", m)   # "cv": the master CV's link-card image
    if lang == "es":
        out = (out.replace('"og:locale" content="en_US"', '"og:locale" content="@@"')
                  .replace('"og:locale:alternate" content="es_MX"', '"og:locale:alternate" content="en_US"')
                  .replace('"og:locale" content="@@"', '"og:locale" content="es_MX"'))
    # made for one reader: out of search engines, but the link card still works when it is shared
    return out + '\n<meta name="robots" content="noindex, nofollow">'


def render(spec, m):
    """The page, exactly as gen.py draws public/index.html, with the spec as the view."""
    view = view_of(spec, m)
    html = gen.cv_page(gen.VERSIONS[gen.LIVE[0]], meta_of(spec, view), view=view, lang=spec["jd"]["lang"])
    _, _, _, out = paths(spec["name"])
    os.makedirs(OUT, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return out, view


def render_all(quiet=False):
    """Every spec in tailor-cv/, with this run's design and master data (contact, dates, levels), and the explorer
    that lists them. No validation: a spec is checked when it is built; a later change to the timeline must not break
    an old CV's page."""
    specs = sorted(glob.glob(os.path.join(SPECS, "*.json")))
    if not specs and not os.path.isdir(OUT):
        return
    m = Master()
    for p in specs:
        name = os.path.splitext(os.path.basename(p))[0]
        try:
            with open(p, encoding="utf-8") as f:
                out, _ = render(json.load(f), m)
            if not quiet:
                print(f"wrote {os.path.relpath(out, gen.PUBLIC)}")
        except Exception as ex:   # an old spec the master no longer matches: keep its page, say so
            print(f"skipped tailor-cv/{name}.json: {type(ex).__name__}: {ex}")
    out, n = render_explorer(m)
    if not quiet:
        print(f"wrote {os.path.relpath(out, gen.PUBLIC)} (the explorer: {n} CV{'s' if n != 1 else ''})")


# ------------------------------------------------------------------ the explorer: /tailor-cv/, every tailored CV
# public/tailor-cv/index.html, written from the specs by `build`, `index` and `render-all` (so by gen.py too): one row
# per CV, newest first, filtered by the timeline's `grep -i` bar, and a panel with the selected CV — its links and a
# live copy of the page, scaled to fit. Same shell as every page of the site; noindex, like the CVs it lists.
EXPLORER = os.path.join(OUT, "index.html")

EXPLORER_TPL = """<div class="sheet tx-page">
  $NAV$
  <header class="top">
    <div>
      <div class="prompt mono"><span class="g">sergio</span>@<span class="c">sergiowero.github.io</span>:~$ ls <span class="f">tailor-cv/</span></div>
      <div class="name"><span id="typed">$TX_TITLE$</span><span class="cur"></span></div>
      <div class="hname">$NAME$</div>
      <div class="sub mono">$TX_SUB$</div>
    </div>
  </header>
  <div class="tx">
    <div class="tx-col">
      $TX_SEARCH$
      <ol class="tx-list" aria-label="Tailored CVs">$TX_ROWS$</ol>
      $TX_NONE$
    </div>
    $TX_PANEL$
  </div>
  <script type="application/json" id="tx-data">$TX_DATA$</script>
</div>"""

EXPLORER_CSS = """
  /* ---- /tailor-cv/: the explorer (tools/tailor.py) — the tailored CVs in a list, the selected one in the panel ---- */
  .sheet.tx-page{overflow:visible;}   /* as on /timeline/: overflow:hidden on the sheet would defeat the sticky panel */
  .tx{display:flex;gap:6mm;margin-top:8px;align-items:flex-start;}
  .tx-col{flex:0 0 72mm;min-width:0;}
  .tx-col .hq{margin:0 0 6px;padding:6px 0 7px;}   /* the timeline's grep bar, without the offset of its rail */
  .tx-list{list-style:none;display:grid;gap:5px;padding-bottom:10px;}
  .tx-row{position:relative;}
  .tx-row.dim{display:none;}
  .tx-sel{display:block;width:100%;text-align:left;font:inherit;color:inherit;cursor:pointer;background:var(--panel);
    border:1px solid var(--line);border-radius:8px;padding:6px 26px 7px 10px;transition:border-color .15s,box-shadow .15s;}
  .tx-sel:hover{border-color:var(--cyan);}
  .tx-sel:focus-visible{outline:2px solid var(--cyan);outline-offset:1px;}
  .tx-row.active .tx-sel{border-color:var(--green);box-shadow:0 0 0 3px rgba(61,220,132,.14);}
  .tx-top{display:flex;align-items:center;gap:6px;font-size:7.6px;color:var(--muted);}
  .tx-row.active .tx-date{color:var(--green);}
  .tx-lang{font-size:6.6px;font-weight:700;letter-spacing:1px;line-height:1.5;border:1px solid var(--line);border-radius:3px;padding:0 4px;}
  .tx-co{display:block;font-size:11px;font-weight:600;color:var(--fg);line-height:1.2;margin-top:3px;}
  .tx-pos{display:block;font-size:8.8px;color:var(--cyan);line-height:1.3;margin-top:1px;}
  .tx-req{margin-top:5px;gap:3px;} .tx-req .dchip{font-size:6.8px;padding:1px 5px;}
  .tx-kids{display:block;font-size:7.2px;color:var(--muted);line-height:1.35;margin-top:4px;}
  .tx-open{position:absolute;top:5px;right:6px;font-size:11px;line-height:1;color:var(--muted);padding:3px 4px;border-radius:4px;}
  .tx-open:hover,.tx-open:focus-visible{color:var(--green);}
  .tx-none{font-size:9px;color:var(--muted);margin-top:6px;}
  .tx-panel{flex:1 1 auto;min-width:0;position:sticky;top:12px;background:var(--panel);border:1px solid var(--line);
    border-radius:10px;padding:10px 11px 11px;}
  .tx-panel.off{display:none;}
  .tx-p-co{font-size:15px;font-weight:700;color:var(--fg);letter-spacing:-.3px;line-height:1.15;margin-top:7px;}
  .tx-p-pos{font-size:9.8px;font-weight:500;color:var(--cyan);margin-top:2px;}
  .tx-p-when{font-size:8px;color:var(--green);margin-top:5px;}
  .tx-links{display:flex;flex-wrap:wrap;gap:3px 12px;margin-top:6px;font-size:8px;}
  .tx-links a{color:var(--cyan);} .tx-links a:hover{color:var(--green);} .tx-links a[hidden]{display:none;}
  /* the preview: the CV page itself in an iframe (the explorer strips its header and fab, see EMBED in the script),
     A4-shaped until the CV loads and gives its own shape; the script shrinks it when the viewport is too short */
  .tx-frame{position:relative;width:100%;aspect-ratio:210/297;margin:10px auto 0;overflow:hidden;
    border:1px solid var(--line);border-radius:6px;background:var(--bg);}
  .tx-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0;opacity:0;transition:opacity .2s;}
  .tx-frame.ready iframe{opacity:1;}
  .tx-hit{position:absolute;inset:0;z-index:1;border-radius:inherit;}   /* the preview is a picture: a click opens the CV */
  .tx-hit:hover{box-shadow:inset 0 0 0 2px var(--green);}
  .tx-hit:focus-visible{outline:2px solid var(--cyan);outline-offset:2px;}
  @media print{.tx-panel,.tx-open{display:none !important;} .tx-row.dim{display:block;}}
"""

EXPLORER_JS = r"""<script>
/* /tailor-cv/, the explorer: a row shows its CV in the panel — its links and the page itself, scaled to fit.
   The grep bar filters the list: every word must match (company, position, date, language, required skills, the
   clients it shows), ignoring case and accents; a word of one or two letters only as a whole word, so `es` is the
   CVs that open in Spanish, not every "inglés". ?q= keeps the filter and #<name> the CV, so a link can open the explorer on one.
   ↑/↓ move through the list, Enter on the selected row (or a double click, or a click on the preview) opens it. */
(function(){
  var dataEl=document.getElementById('tx-data'), panel=document.getElementById('tx-panel'), box=document.querySelector('.tx-col .hq');
  if(!dataEl||!panel||!box) return;   // no CVs yet: no bar, nothing to preview
  var data=JSON.parse(dataEl.textContent), rows=[].slice.call(document.querySelectorAll('.tx-row'));
  var sheet=document.querySelector('.sheet'), frame=panel.querySelector('.tx-frame'), iframe=frame.querySelector('iframe'), hit=frame.querySelector('.tx-hit');
  var input=box.querySelector('.hq-in'), clearBtn=box.querySelector('.hq-x'),
      count=box.querySelector('.hq-count'), empty=box.querySelector('.hq-empty');
  var W={en:{opens:{en:'opens in English',es:'opens in Spanish'},clear:'Clear search',open:'Open the CV',preview:'Preview of the CV',list:'Tailored CVs'},
         es:{opens:{en:'abre en inglés',es:'abre en español'},clear:'Limpiar búsqueda',open:'Abrir el CV',preview:'Vista previa del CV',list:'CVs a la medida'}};
  function w(){return W[window.cvLang()];}
  function $(k){return panel.querySelector('[data-tx="'+k+'"]');}
  var current=-1;
  function fill(){
    var e=data[current]; if(!e) return;
    $('file').textContent=e.name+'.html'; $('co').textContent=e.company; $('pos').textContent=e.position;
    $('when').textContent=e.date+' · '+w().opens[e.lang];
    $('cv').href=e.cv; $('jd').href=e.jd; hit.href=e.cv;
    var post=$('post'); post.hidden=!e.url; if(e.url) post.href=e.url;
    size();
  }
  function relabel(){
    clearBtn.setAttribute('aria-label',w().clear); clearBtn.title=w().clear;
    hit.setAttribute('aria-label',w().open); iframe.title=w().preview; document.querySelector('.tx-list').setAttribute('aria-label',w().list);
    rows.forEach(function(r,i){ var a=r.querySelector('.tx-open'); a.title=w().open; a.setAttribute('aria-label',w().open+': '+data[i].company+' · '+data[i].position); });
  }
  /* ---- the preview: same-origin, so the explorer takes the site's header and the download fab out of the copy and
     keeps its language and theme in step with the explorer's (a file:// page can't reach into it: it shows as is) ---- */
  var EMBED='.site-nav,.dl-fab{display:none !important;} html{overflow:hidden !important;}'+
            'body{padding:0 !important;display:block !important;min-height:0 !important;background:none !important;}'+
            '.sheet{margin:0 !important;box-shadow:none !important;border:0 !important;border-radius:0 !important;}';
  function mirror(){
    try{
      var d=iframe.contentDocument; if(!d||!d.documentElement) return;
      var h=d.documentElement, p=document.documentElement, l=p.getAttribute('data-lang'), t=p.getAttribute('data-theme'), was=h.getAttribute('data-lang');
      if(l) h.setAttribute('data-lang',l); else h.removeAttribute('data-lang');
      if(t) h.setAttribute('data-theme',t); else h.removeAttribute('data-theme');
      if(was!==l) d.dispatchEvent(new iframe.contentWindow.CustomEvent('langchange',{detail:l==='es'?'es':'en'}));   // its dates redraw
    }catch(err){}
  }
  /* the preview's shape: A4 until the CV says otherwise — on screen its sheet also holds the prompt and the footer
     that printing drops, so it can run a little taller than a page, and the frame follows it to show all of it */
  var ratio=297/210;
  function measure(){
    try{
      var sh=iframe.contentDocument.querySelector('.sheet'), r=sh&&sh.getBoundingClientRect();
      if(r&&r.width){ ratio=r.height/r.width; frame.style.aspectRatio=r.width+' / '+r.height; size(); }
    }catch(err){}
  }
  iframe.addEventListener('load',function(){
    try{
      var d=iframe.contentDocument;
      if(d&&d.head&&!d.getElementById('tx-embed')){ var st=d.createElement('style'); st.id='tx-embed'; st.textContent=EMBED; d.head.appendChild(st); }
      mirror(); iframe.contentWindow.dispatchEvent(new iframe.contentWindow.Event('resize'));   // its sheet refits without the padding
      measure(); if(d.fonts&&d.fonts.ready) d.fonts.ready.then(measure);
    }catch(err){}
    frame.classList.add('ready');
  });
  new MutationObserver(mirror).observe(document.documentElement,{attributes:true,attributeFilter:['data-lang','data-theme']});
  /* The CV's shape at the panel's width; shorter (and narrower) when the viewport cannot show all of it next to the
     panel's head. Everything is measured on screen (the sheet is CSS-zoomed) and set back in the sheet's own px. */
  function size(){
    frame.style.width=''; frame.style.height='';
    if(window.matchMedia&&window.matchMedia('print').matches) return;
    var z=parseFloat(sheet.style.zoom)||1, pr=panel.getBoundingClientRect(), fr=frame.getBoundingClientRect(); if(!fr.height) return;
    var room=window.innerHeight-24*z-(pr.height-fr.height);
    if(room<fr.height){ var hh=Math.max(fr.height*0.55,room)/z; frame.style.height=hh+'px'; frame.style.width=(hh/ratio)+'px'; }
  }
  function select(i,how){   // how: {hash, focus} — only a choice the reader makes goes into the URL
    if(i<0||i>=rows.length) return;
    current=i;
    rows.forEach(function(r,k){ var on=k===i; r.classList.toggle('active',on); r.querySelector('.tx-sel').setAttribute('aria-pressed',on?'true':'false'); });
    if(iframe.getAttribute('src')!==data[i].cv){ frame.classList.remove('ready'); iframe.setAttribute('src',data[i].cv); }
    fill();
    if(how&&how.hash){ var u=new URL(location.href); u.hash=data[i].name; history.replaceState(null,'',u); }
    if(how&&how.focus) rows[i].querySelector('.tx-sel').focus();
  }
  function open(i){ location.href=data[i].cv; }
  rows.forEach(function(r,i){
    var b=r.querySelector('.tx-sel');
    b.addEventListener('click',function(ev){ if(i===current&&ev.detail===0){ open(i); return; } select(i,{hash:true}); });   // detail 0: Enter / Space
    b.addEventListener('dblclick',function(){ open(i); });
  });
  function visible(){ var out=[]; rows.forEach(function(r,i){ if(!r.classList.contains('dim')) out.push(i); }); return out; }
  document.querySelector('.tx-list').addEventListener('keydown',function(ev){
    if(ev.key!=='ArrowDown'&&ev.key!=='ArrowUp') return;
    var vis=visible(), k=vis.indexOf(current); if(!vis.length) return;
    ev.preventDefault();
    k=ev.key==='ArrowDown'?Math.min(vis.length-1,k+1):Math.max(0,k-1);
    select(vis[k],{hash:true,focus:true});
  });
  /* ---- the grep bar ---- */
  var DIA=new RegExp('['+String.fromCharCode(0x300)+'-'+String.fromCharCode(0x36f)+']','g');
  function fold(s){ return String(s).normalize('NFD').replace(DIA,'').toLowerCase(); }
  var TOK=/"([^"]*)"|(\S+)/g;
  function tokens(q){ var out=[], m; TOK.lastIndex=0; while((m=TOK.exec(q))){ var t=fold(m[1]!==undefined?m[1]:m[2]).trim(); if(t) out.push(t); } return out; }
  var idx=data.map(function(e){ return fold(e.text); }), q='';
  function has(text,t){   // a short token is a whole word (es, en, ai…); a longer one is found anywhere
    if(t.length>2) return text.indexOf(t)>=0;
    return new RegExp('(^|[^a-z0-9])'+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'($|[^a-z0-9])').test(text);
  }
  function apply(){
    var toks=tokens(input.value); q=input.value.trim();
    rows.forEach(function(r,i){ r.classList.toggle('dim',!toks.every(function(t){ return has(idx[i],t); })); });
    var vis=visible();
    clearBtn.hidden=!q;
    count.textContent=toks.length?vis.length+'/'+rows.length:'';
    empty.hidden=!(toks.length&&!vis.length);
    panel.classList.toggle('off',!vis.length);
    if(vis.length&&vis.indexOf(current)<0) select(vis[0]);
  }
  function sync(){ var u=new URL(location.href); if(q) u.searchParams.set('q',q); else u.searchParams.delete('q'); history.replaceState(null,'',u); }
  var syncT=null;
  input.addEventListener('input',function(){ apply(); clearTimeout(syncT); syncT=setTimeout(sync,150); });
  input.addEventListener('keydown',function(ev){
    if(ev.key==='Escape'){ if(input.value){ input.value=''; apply(); sync(); } else input.blur(); return; }
    if(ev.key==='ArrowDown'||ev.key==='Enter'){ var vis=visible(); if(vis.length){ ev.preventDefault(); select(vis.indexOf(current)>=0?current:vis[0],{hash:true,focus:true}); } }
  });
  clearBtn.addEventListener('click',function(){ input.value=''; apply(); sync(); input.focus(); });
  document.addEventListener('keydown',function(ev){   // `/` focuses the search, as on /timeline/
    if(ev.key!=='/'||ev.ctrlKey||ev.metaKey||ev.altKey) return;
    var a=document.activeElement; if(a&&(a.tagName==='INPUT'||a.tagName==='TEXTAREA'||a.isContentEditable)) return;
    ev.preventDefault(); input.focus(); input.select();
  });
  function byHash(){ var want=decodeURIComponent(location.hash.slice(1)), i=-1; data.forEach(function(e,k){ if(e.name===want) i=k; }); return i; }
  window.addEventListener('hashchange',function(){ var i=byHash(); if(i>=0&&!rows[i].classList.contains('dim')) select(i); });
  document.addEventListener('langchange',function(){ relabel(); fill(); });
  window.addEventListener('resize',size); window.addEventListener('load',size);
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(size);
  // after every inline script has run: the sheet's zoom (FIT_JS) is what size() measures against
  function boot(){
    var q0=new URL(location.href).searchParams.get('q'); if(q0) input.value=q0;
    relabel();
    current=byHash();   // the CV the URL names, if the filter keeps it; apply() falls back to the first row it keeps
    if(current>=0) select(current); else current=-1;
    apply();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot); else boot();
})();
</script>"""


def _names(ids):
    """Vocabulary ids → what the page shows: a technology's name, or a tag's label in both languages."""
    out = []
    for rid in ids:
        if rid in gen.TECH_CATALOG:
            out.append(gen.TECH_CATALOG[rid][0])
        elif rid in gen.TAGS:
            lab = gen.TAGS[rid][1]
            out.append(T(gen.plain(lab, "en"), gen.plain(lab, "es")) if isinstance(lab, T) else gen.plain(lab))
    return out


def explorer_entry(spec, m):
    """One tailored CV as the explorer lists it: from the spec, plus the master for its client names."""
    j, name = spec["jd"], spec["name"]
    required = _names([r["id"] for r in j.get("required") or [] if isinstance(r, dict) and "id" in r])
    clients = []   # per job with client projects, the ones the CV shows: all in fallback, those with bullets when tailored
    for e in spec["experience"]:
        kids = m.children.get(e["id"], [])
        shown = kids if e["mode"] == "fallback" else [c for c in kids if any(b.get("child") == c for b in e["bullets"])]
        if shown:
            clients.append(dict(job=m.r(e["id"])["organization"], kids=[m.r(c)["organization"] for c in shown]))
    lang = j["lang"]
    # what the grep bar searches; not the roles, which nearly every CV shares ("lead" would keep them all)
    url = j.get("url") or ""
    words = ([j["company"], j["position"], j["date"], lang, {"en": "english inglés", "es": "spanish español"}[lang], name]
             + [x for c in clients for x in [c["job"]] + c["kids"]]
             + [x for r in required for x in ((r.en, r.es) if isinstance(r, T) else (r,))])
    return dict(name=name, company=j["company"], position=j["position"], date=j["date"], lang=lang,
                url=url if re.match(r"https?://", url) else "", cv=f"/tailor-cv/{name}.html", jd=f"/tailor-cv/{name}.md",
                required=[gen.d(r) for r in required], clients=clients, text=" ".join(words))


EXPLORER_KEYS = ("name", "company", "position", "date", "lang", "url", "cv", "jd", "text")   # what the script reads


def _explorer_row(i, e):
    a = lambda s: _html.escape(str(s), quote=True)
    chip = lambda x: ('<span class="dchip">' + (a(x) if not isinstance(x, dict) else a(x["en"]) if x["en"] == x["es"]
                                                else gen.i18n(a(x["en"]), a(x["es"]))) + '</span>')
    req = "".join(chip(x) for x in e["required"])
    return (f'\n<li class="tx-row" data-i="{i}"><button type="button" class="tx-sel" aria-pressed="false" aria-controls="tx-panel">'
            f'<span class="tx-top mono"><span class="tx-date">{a(e["date"])}</span><span class="tx-lang">{a(e["lang"].upper())}</span></span>'
            f'<span class="tx-co">{a(e["company"])}</span><span class="tx-pos">{a(e["position"])}</span>'
            + (f'<span class="dchips tx-req">{req}</span>' if req else "")
            + "".join(f'<span class="tx-kids mono">{a(c["job"])} › {" · ".join(a(k) for k in c["kids"])}</span>' for c in e["clients"]) +
            f'</button><a class="tx-open mono" href="{a(e["cv"])}" title="Open the CV">↗</a></li>')


def _explorer_search():
    return ('<div class="hq" role="search"><div class="hq-row">'
            '<label class="hq-prompt mono" for="tx-q"><span class="g">➜</span> <span class="c">~</span> grep -i</label>'
            '<span class="hq-field"><input class="hq-in mono" id="tx-q" type="text" inputmode="search" enterkeyhint="search" '
            'autocomplete="off" spellcheck="false" placeholder="aws · java · 2026-09 · es…">'
            '<button type="button" class="hq-x mono" aria-label="Clear search" hidden>×</button></span>'
            '<span class="hq-count mono" aria-live="polite"></span></div>'
            f'<div class="hq-empty mono" hidden>// {gen.i18n("no matches", "sin coincidencias")}</div></div>')


def _explorer_panel(off):
    I = gen.i18n
    return (f'<aside class="tx-panel{" off" if off else ""}" id="tx-panel" aria-live="polite">'
            '<div class="sub-k mono"><span class="g">➜</span> <span class="c">~</span> open tailor-cv/<span class="f" data-tx="file"></span></div>'
            '<div class="tx-p-co" data-tx="co"></div><div class="tx-p-pos" data-tx="pos"></div>'
            '<div class="tx-p-when mono" data-tx="when"></div>'
            f'<div class="tx-links mono"><a data-tx="cv" href="#">{I("open the CV", "abrir el CV")} ↗</a>'
            f'<a data-tx="jd" href="#" target="_blank" rel="noopener">{I("job description (.md)", "vacante (.md)")} ↗</a>'
            f'<a data-tx="post" href="#" target="_blank" rel="noopener noreferrer" hidden>{I("original posting", "publicación original")} ↗</a></div>'
            '<div class="tx-frame"><iframe title="Preview of the CV" tabindex="-1" inert></iframe>'
            '<a class="tx-hit" href="#" aria-label="Open the CV"></a></div>'
            '</aside>')


def explorer_meta(n):
    m = dict(path="/tailor-cv/", type="website", title=f"Tailored CVs — {gen.SHORT_NAME}",
             description=(f"{n} CV{'s' if n != 1 else ''} of {gen.SHORT_NAME}, each tailored to one job description, "
                          "with the master CV's design and its PDF and DOCX downloads, in English and Spanish."),
             labels=[("CVs", str(n)), ("Based in", gen.CONTACT[0][1])],
             image_alt=f"{gen.NAME}: CVs tailored to job descriptions.")
    return gen.meta_html("cv", m) + '\n<meta name="robots" content="noindex, nofollow">'


def render_explorer(m, specs=None):
    """public/tailor-cv/index.html from every spec in tailor-cv/ (or `specs`); returns (path, number of CVs)."""
    if specs is None:
        specs = []
        for p in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
            try:
                with open(p, encoding="utf-8") as f:
                    specs.append(json.load(f))
            except Exception as ex:
                print(f"explorer: skipped {os.path.relpath(p, gen.ROOT)}: {type(ex).__name__}: {ex}")
    entries = []
    for s in specs:
        if not os.path.exists(paths(s.get("name", ""))[3]):
            print(f"explorer: skipped {s.get('name', '?')}: no page yet (tailor.py build writes it)")
            continue
        try:
            entries.append(explorer_entry(s, m))
        except Exception as ex:   # a spec the master no longer matches still has its page; it just is not listed
            print(f"explorer: skipped {s.get('name', '?')}: {type(ex).__name__}: {ex}")
    entries.sort(key=lambda e: e["company"].lower())
    entries.sort(key=lambda e: e["date"], reverse=True)   # newest first; same day: by company
    n = len(entries)
    cvs = f"{n} CV" + ("" if n == 1 else "s")
    body = (EXPLORER_TPL.replace("$NAV$", gen.nav_html("tailor-cv")).replace("$NAME$", gen.NAME)
            .replace("$TX_TITLE$", gen.i18n("Tailored CVs", "CVs a la medida"))
            .replace("$TX_SUB$", gen.i18n(f"{cvs}, each tailored to one job description, newest first — pick one to preview it, open it to download it.",
                                          f"{cvs}, cada uno adaptado a una vacante, del más reciente al más antiguo — elige uno para verlo, ábrelo para descargarlo."))
            .replace("$TX_SEARCH$", _explorer_search() if n else "")
            .replace("$TX_ROWS$", "".join(_explorer_row(i, e) for i, e in enumerate(entries)))
            .replace("$TX_NONE$", "" if n else f'<p class="tx-none mono">// {gen.i18n("no tailored CVs yet: /tailor-cv with a job description makes the first one", "aún no hay CVs a la medida: /tailor-cv con una vacante hace el primero")}</p>')
            .replace("$TX_PANEL$", _explorer_panel(off=not n))
            .replace("$TX_DATA$", json.dumps([{k: e[k] for k in EXPLORER_KEYS} for e in entries], ensure_ascii=False).replace("</", "<\\/")))
    v = gen.VERSIONS[gen.LIVE[0]]
    body = gen.finish_body(body, v) + "\n" + v.get("extra_js", "") + "\n" + EXPLORER_JS
    html = gen.page(v["title"], v["fonts"], gen.version_css(v) + EXPLORER_CSS, body, explorer_meta(n))
    os.makedirs(OUT, exist_ok=True)
    with open(EXPLORER, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return EXPLORER, n


# ------------------------------------------------------------------ one-page check (headless Chromium)
def find_chrome():
    env = os.environ.get("TAILOR_CHROME") or os.environ.get("CHROME")
    if env and os.path.exists(env):
        return env
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge", "microsoft-edge"):
        if shutil.which(n):
            return shutil.which(n)
    pw = os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or os.path.expanduser("~/.cache/ms-playwright")
    cands = []
    for pat in ("chromium-*/chrome-linux/chrome", "chromium-*/chrome-win/chrome.exe",
                "chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium"):
        cands += sorted(glob.glob(os.path.join(pw, pat)), reverse=True)
    for base in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")):
        if base:
            cands += [os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"),
                      os.path.join(base, "Microsoft", "Edge", "Application", "msedge.exe")]
    cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium",
              "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    return next((c for c in cands if os.path.exists(c)), None)


FONT_CACHE = os.path.join(tempfile.gettempdir(), "sergiowero-cv-fonts")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"


def _fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()


def local_fonts(css_url):
    """The page's Google Fonts stylesheet with its font files downloaded next to it, so the check measures with the
    real typefaces even where the browser can't reach Google Fonts itself. None when offline."""
    os.makedirs(FONT_CACHE, exist_ok=True)
    path = os.path.join(FONT_CACHE, hashlib.sha1(css_url.encode()).hexdigest()[:16] + ".css")
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    try:
        css = _fetch(css_url).decode("utf-8")

        def local(mt):
            fn = os.path.join(FONT_CACHE, hashlib.sha1(mt.group(1).encode()).hexdigest()[:16] + ".woff2")
            if not os.path.exists(fn):
                data = _fetch(mt.group(1))
                with open(fn, "wb") as f:
                    f.write(data)
            return f"url({pathlib.Path(fn).as_uri()})"
        css = re.sub(r"url\((https://[^)]+)\)", local, css)
    except Exception:
        return None
    with open(path, "w", encoding="utf-8") as f:
        f.write(css)
    return css


MEASURE = """<style>.sheet{zoom:1 !important;min-height:0 !important;} .cols{align-items:flex-start !important;}</style>
<script>(function(){
  function done(){
    var s=document.querySelector('.sheet'); if(!s) return;
    var H=function(sel){var e=document.querySelector(sel);return e?e.getBoundingClientRect().height:0;};
    var faces=0; if(document.fonts) document.fonts.forEach(function(f){ if(f.status==='loaded') faces++; });
    document.documentElement.setAttribute('data-fit',JSON.stringify({h:H('.sheet'),main:H('.main'),aside:H('.aside'),faces:faces}));
  }
  (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(function(){setTimeout(done,50);});
})();</script>"""


def _variant(html, lang, ats, fonts_css, measure):
    """A copy of the page as it prints: in one language, plain or ATS, with local fonts; `measure` also lays it out
    with the print stylesheet on screen, at natural height, and writes that height into <html data-fit>."""
    attrs = f' data-default-lang="{lang}"' + (' data-print="ats"' if ats else "")
    html = re.sub(r"<html([^>]*)>", lambda mt: "<html" + re.sub(r'\s+data-default-lang="[^"]*"', "", mt.group(1)) + attrs + ">", html, count=1)
    if fonts_css:
        html = re.sub(r'<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">', lambda _: f"<style>{fonts_css}</style>", html)
    if measure:
        html = html.replace("@media print{", "@media all{").replace("@media screen{", "@media not all{")
        html = html.replace("</body>", MEASURE + "\n</body>")
    return html


def _chrome(chrome, args, tmp):
    base = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--no-default-browser-check",
            "--allow-file-access-from-files", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=5000",
            f"--user-data-dir={tempfile.mkdtemp(dir=tmp)}", "--window-size=1280,2000"]
    if os.name == "posix" and hasattr(os, "geteuid") and os.geteuid() == 0:
        base.append("--no-sandbox")   # Chromium refuses to run as root with its sandbox (containers, CI)
    return subprocess.run(base + args, capture_output=True, timeout=120)


def check(page, langs=LANGS):
    """[{lang, mode, pages, height, faces}] for the page printed plain and ATS in each language: `pages` from a real
    PDF, `height` of the sheet's content with the print stylesheet (the page holds 1122.5 px). None without Chromium."""
    chrome = find_chrome()
    if not chrome:
        return None
    html = open(page, encoding="utf-8").read()
    link = re.search(r'<link href="(https://fonts\.googleapis\.com/css2[^"]*)" rel="stylesheet">', html)
    fonts_css = local_fonts(_html.unescape(link.group(1))) if link else None
    tmp = tempfile.mkdtemp(prefix="tailor-check-")
    jobs = []
    for lang in langs:
        for ats in (False, True):
            for measure in (False, True):
                p = os.path.join(tmp, f"{lang}-{'ats' if ats else 'plain'}-{'m' if measure else 'p'}.html")
                with open(p, "w", encoding="utf-8") as f:
                    f.write(_variant(html, lang, ats, fonts_css, measure))
                jobs.append((lang, ats, measure, p))

    def run(job):
        lang, ats, measure, p = job
        url = pathlib.Path(p).as_uri()
        if measure:
            out = _chrome(chrome, ["--dump-dom", url], tmp).stdout.decode("utf-8", "replace")
            mt = re.search(r"data-fit=\"([^\"]*)\"", out)
            return json.loads(_html.unescape(mt.group(1))) if mt else {}
        pdf = p[:-5] + ".pdf"
        _chrome(chrome, ["--no-pdf-header-footer", f"--print-to-pdf={pdf}", url], tmp)
        data = open(pdf, "rb").read() if os.path.exists(pdf) else b""
        return {"pages": len(re.findall(rb"/Type\s*/Page(?!s)", data))}

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, jobs))
    shutil.rmtree(tmp, ignore_errors=True)
    out = {}
    for (lang, ats, _, _), r in zip(jobs, results):
        out.setdefault((lang, ats), {"lang": lang, "mode": "ats" if ats else "plain"}).update(r)
    return [dict(v, fonts=fonts_css is not None) for v in out.values()]


def print_check(results, baseline=None):
    """Prints the check; returns False when the plain PDF (the design, one sheet) is over a page."""
    if results is None:
        print("one-page check: skipped — no Chrome, Chromium or Edge found (set TAILOR_CHROME to its path). "
              "Open the page, print it to PDF and make sure it is one sheet in EN and ES.")
        return True
    ok = True
    print("one-page check (headless Chromium, A4):")
    for r in results:
        label = "PDF    " if r["mode"] == "plain" else "PDF ATS"
        h = r.get("h")
        pages = r.get("pages", 0)
        line = f"  {r['lang']}  {label}  {pages} page{'s' if pages != 1 else ' '}"
        if r["mode"] == "plain" and h:
            # the taller column sets the sheet's height: the experience column also has whatever the aside is taller by
            free = A4_PX - h + max(0.0, r.get("aside", 0) - r.get("main", 0))
            line += (f"   sheet {h:.0f} of {A4_PX:.0f} px — experience column: "
                     + (f"{free:.0f} px free (~{int(free // 12.3)} lines)" if free >= 0 else f"{-free:.0f} px OVER (~{int(-free // 12.3) + 1} lines)"))
        if r["mode"] == "ats" and baseline:
            base = next((b.get("pages") for b in baseline if b["lang"] == r["lang"] and b["mode"] == "ats"), None)
            if base:
                line += f"   (master CV: {base})"
        if not r.get("faces"):
            line += "   [web fonts did not load: sizes are approximate]"
        print(line)
        if r["mode"] == "plain" and pages != 1:
            ok = False
    return ok


# ------------------------------------------------------------------ commands
def skeleton(m, company, position, day, lang, url):
    """A spec that reproduces the master CV: every job in fallback, the master's own bullets and summary."""
    exp = []
    for jid in m.jobs:
        bullets = []
        for bid, pt in zip(m.bullets[jid], m.job_src[jid]["pts"]):
            child, b, tech = m.bullet_child.get(bid), {}, None
            if child:
                b["child"] = child
            for lang_ in LANGS:
                src = getattr(pt, lang_) if isinstance(pt, T) else pt
                if child:   # "<b>Fox Corp:</b> text <span class="stack">Tech: a, b.</span>" → text + tech
                    mt = re.fullmatch(r'<b>[^<]+:</b>\s*(.*?)\s*(?:<span class="stack">Tech: (.*?)\.</span>)?', src, re.S)
                    src, tech = mt.group(1), mt.group(2)
                b[lang_] = gen.ytext(src, lang_)
            if tech:
                b["tech"] = [x.strip() for x in tech.split(",")]
            b["sources"] = [bid]
            bullets.append(b)
        exp.append({"id": jid, "mode": "fallback", "why": "", "bullets": bullets})
    summary = {lang_: gen.ytext(re.sub(r"<span data-years>\d+</span>", "{years}", getattr(gen.PROFILE, lang_)), lang_) for lang_ in LANGS}
    return {"schema": SCHEMA, "name": spec_name(company, position, day),
            "jd": {"company": company, "position": position, "date": day, "lang": lang, "url": url,
                   "terms": [], "required": [], "gaps": []},
            "profile": {"summary": summary, "roles": None, "sources": []},
            "experience": exp, "skills": {"drop": []}, "notes": ""}


def cmd_new(a):
    if a.jd == "-" and hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8-sig")   # a Windows console is not UTF-8 by default
    jd = sys.stdin.read() if a.jd == "-" else open(a.jd, encoding="utf-8-sig").read()
    if not jd.strip():
        sys.exit("the job description is empty")
    day = a.date or date.today().isoformat()
    m = Master()
    spec = skeleton(m, a.company.strip(), a.position.strip(), day, a.lang, a.url)
    name, spec_path, jd_path, _ = paths(spec["name"])
    if not a.force and (os.path.exists(spec_path) or os.path.exists(jd_path)):
        sys.exit(f"{name} already exists (--force to start it over)")
    os.makedirs(SPECS, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    with open(jd_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(jd_markdown(jd, spec))
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    print(f"{name}\n  spec             tailor-cv/{name}.json  (the master CV, every job in fallback)\n"
          f"  job description  public/tailor-cv/{name}.md\n  CV               public/tailor-cv/{name}.html  (after build)")


def _hits(m, rid, jt, jg):
    r = m.r(rid)
    t = sorted(up(r["tech"]) & up(jt))
    g = [x for x in r["tags"] if x in jg]
    score = 3 * len(t) + sum(2 if m.vtags[x]["facet"] in ("domain", "practice") else 1 for x in g)
    return score, t, g


def cmd_analyze(a):
    name, spec, jd = load(a.name)
    m = Master()
    also = [x for x in (a.also or "").replace(" ", "").split(",") if x]   # read in the JD, missed by the patterns
    for x in also:
        if x not in gen.TECH_CATALOG and x not in gen.TAGS:
            sys.exit(f"--also: {x!r} is neither a technology nor a tag id (tree.json → vocabulary)")
    jt, jg = jd_asks(spec, jd, also)
    hard, soft = unbacked(jd)
    sents = jd_sentences(jd)
    W = lambda s, n=150: s if len(s) <= n else s[:n - 1] + "…"
    jdx = spec["jd"]
    print(f"# {jdx['company']} — {jdx['position']}  (tailor-cv/{name}.json, page in {jdx['lang']})\n")
    print("## What the JD names, and whether the tree has it")
    have_t = [t for t in sorted(jt) if m.vtech[t]["usage"]["records"]]
    used = lambda t: (f"{m.vtech[t]['usage']['years']} y in {', '.join(m.vtech[t]['usage']['entries'])}"
                      if m.vtech[t]["usage"]["entries"] else "only in the master CV's skills: no job to cite")
    print("technologies we have: " + ("; ".join(f"{gen.TECH_CATALOG[t][0]} ({t}, {used(t)})" for t in have_t) or "none"))
    print("practices / domains we have: " + (", ".join(f"{gen.plain(gen.TAGS[g][1])} ({g})" for g in sorted(jg)
                                                        if gen.TAGS[g][0] in ('domain', 'practice') and m.vtags[g]['records']) or "none"))
    print("competencies / outcomes / industries we have: " + (", ".join(f"{gen.plain(gen.TAGS[g][1])} ({g})" for g in sorted(jg)
                                                 if gen.TAGS[g][0] not in ('domain', 'practice') and m.vtags[g]['records']) or "none"))
    print("named in the JD, nowhere in the tree (gaps — never write them): " + (", ".join(hard + soft) or "none"))
    print("\n## jd.required candidates — keep only what the JD strictly requires (must-have, not nice-to-have)")
    for rid in have_t + [g for g in sorted(jg) if gen.TAGS[g][0] in ("domain", "practice") and m.vtags[g]["records"]]:
        q = quote_for(sents, rid)
        if q:
            print(f'  {{"id": "{rid}", "quote": {json.dumps(W(q, 200), ensure_ascii=False)}}}')
    pool = [n for n, _ in gen.CORE + gen.CORE_EXTRA]
    print("core skills with a level: " + ", ".join(pool) + "  (a required skill outside this list can only be a chip)")

    for jid in m.jobs:
        job = m.r(jid)
        kids = m.children[jid]
        print(f"\n## {jid} — {job['title']} · {job['dates']['text']}" + (f"   [children: {', '.join(kids)}]" if kids else ""))
        print("master bullets (the fallback material):")
        for b in m.bullets[jid]:
            s, t, g = _hits(m, b, jt, jg)
            c = m.bullet_child.get(b)
            print(f"  [{s:2}] {b}" + (f" → {c}" if c else "") + f"  {W(m.describe(b), 170)}")
        scopes = [("own content" + (" (not a child's)" if kids else ""), m.scope(jid))] + [(f"child {c}: {m.r(c)['title']}", m.scope(jid, c)) for c in kids]
        for label, scope in scopes:
            ids = [i for i in m.order if i in scope and i not in m.bullets[jid]]
            scored = [(i, *_hits(m, i, jt, jg)) for i in ids]
            total = sum(s for _, s, _, _ in scored)
            print(f"\n### {label} — relevance {total}")
            top = sorted([x for x in scored if x[1]], key=lambda x: -x[1])[:a.top]
            if not top:
                print("  nothing in it names what the JD asks for")
            for i, s, t, g in top:
                print(f"  [{s:2}] {i}  ({', '.join(t + g)})\n        {W(m.describe(i), 220)}")
            if a.all:
                rest = [i for i, s, _, _ in scored if not s]
                if rest:
                    print("  -- no JD term: " + ", ".join(rest))
    print("\nNext: `tailor.py show <ids>` for the records you will write from (both languages), then edit the spec and `build`.")


def cmd_show(a):
    m = Master()
    for rid in a.ids:
        if rid not in m.rec["en"]:
            print(f"### {rid}: no such record\n")
            continue
        r = m.r(rid)
        ctx = r["context"]
        where = " › ".join(x for x in [ctx["organization"], ctx["client"]] if x)
        print(f"### {rid}  ({r['type']} · {where})")
        print(f"tech: {', '.join(r['tech']) or '-'}   tags: {', '.join(r['tags']) or '-'}")
        for lang in LANGS:
            print(f"{lang.upper()}: {m.describe(rid, lang)}")
        print()


def cmd_build(a):
    name, spec, jd = load(a.name)
    m = Master()
    rep = validate(name, spec, jd, m)
    for w in rep.warnings:
        print(f"warning  {w}")
    for e in rep.errors:
        print(f"ERROR    {e}")
    if rep.errors:
        sys.exit(f"\n{len(rep.errors)} error(s): public/tailor-cv/{name}.html not written")
    out, view = render(spec, m)
    print(f"\nwrote {os.path.relpath(out, gen.ROOT)}  →  {gen.SITE}/tailor-cv/{name}.html")
    for e in spec["experience"]:
        kids = sorted({b["child"] for b in e["bullets"] if b.get("child")})
        print(f"  {e['id']:15} {e['mode']:9} {len(e['bullets'])} bullet(s)" + (f"  children: {', '.join(kids)}" if kids else ""))
    changed = lambda new, old: [gen.plain(x) if not isinstance(x, tuple) else x[0] for x in new] != [gen.plain(x) if not isinstance(x, tuple) else x[0] for x in old]
    print("  core skills   " + (" · ".join(n for n, _ in view["core"]) if changed(view["core"], gen.CORE) else "the master's"))
    print("  tech chips    " + (" · ".join(gen.plain(x) for x in view["tech"]) if changed(view["tech"], gen.TECH) else "the master's"))
    if spec["jd"].get("gaps"):
        print("  gaps (asked by the JD, not in the tree): " + ", ".join(spec["jd"]["gaps"]))
    idx, n = render_explorer(m)
    print(f"wrote {os.path.relpath(idx, gen.ROOT)}  →  {gen.SITE}/tailor-cv/  (the explorer: {n} CV{'s' if n != 1 else ''})")
    if a.no_check:
        return
    print()
    ok = print_check(check(out), check(os.path.join(gen.PUBLIC, "index.html")) if a.baseline else None)
    if not ok:
        sys.exit("\nthe page is over one sheet: drop the least relevant bullets or shorten them (EN and ES), then build again")


def cmd_check(a):
    print_check(check(a.page))


def cmd_render_all(_):
    render_all()


def cmd_index(_):
    out, n = render_explorer(Master())
    print(f"wrote {os.path.relpath(out, gen.ROOT)}  →  {gen.SITE}/tailor-cv/  ({n} CV{'s' if n != 1 else ''})")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="tailor.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="save a job description and start its spec from the master CV")
    n.add_argument("jd", help="the job description: a text/Markdown file, or - for stdin")
    n.add_argument("--company", required=True)
    n.add_argument("--position", required=True)
    n.add_argument("--lang", choices=LANGS, default="en", help="the JD's language: the page opens in it")
    n.add_argument("--url", default=None, help="where the JD was published")
    n.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    n.add_argument("--force", action="store_true", help="overwrite an existing spec")
    n.set_defaults(fn=cmd_new)
    an = sub.add_parser("analyze", help="what the JD asks for and what each job has")
    an.add_argument("name")
    an.add_argument("--top", type=int, default=8, help="records shown per job / child (default 8)")
    an.add_argument("--all", action="store_true", help="also list the records with no JD term")
    an.add_argument("--also", help="tech / tag ids the JD asks for that it missed, comma-separated (a Spanish JD: "
                                   "the tag patterns are English), e.g. game-dev,leadership,dependency-injection")
    an.set_defaults(fn=cmd_analyze)
    sh = sub.add_parser("show", help="records in both languages")
    sh.add_argument("ids", nargs="+")
    sh.set_defaults(fn=cmd_show)
    b = sub.add_parser("build", help="validate the spec, write the page, check it fits one sheet")
    b.add_argument("name")
    b.add_argument("--no-check", action="store_true", help="skip the one-page check")
    b.add_argument("--baseline", action="store_true", help="also check the master CV, to compare the ATS PDF")
    b.set_defaults(fn=cmd_build)
    c = sub.add_parser("check", help="one-page check of a CV page")
    c.add_argument("page")
    c.set_defaults(fn=cmd_check)
    r = sub.add_parser("render-all", help="re-render every spec with the current design, and the explorer")
    r.set_defaults(fn=cmd_render_all)
    x = sub.add_parser("index", help="write the explorer, /tailor-cv/: every tailored CV in one list")
    x.set_defaults(fn=cmd_index)
    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
