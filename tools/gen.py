#!/usr/bin/env python3
import re
"""Generates the A4-sheet CV variants (v2-v4, v6-v9) from shared data.
v1 and v5 are hand-written and left untouched."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")        # static files, copied as-is by Astro
OUT = os.path.join(PUBLIC, "Backups")        # all variants
LIVE = ("v3-dark-terminal.html", os.path.join(PUBLIC, "index.html"))   # the chosen design, published at the root
SHELL_DIR = os.path.join(ROOT, "src", "shell")   # the v3 shell exported for the Astro blog pages


def i18n(en, es):
    """Both languages in the markup; CSS (html[data-lang]) shows one."""
    return f'<span class="i18n-en">{en}</span><span class="i18n-es">{es}</span>'


class T:
    """A bilingual string. .html() renders both languages (CSS shows one); .data() feeds the export JSON."""
    __slots__ = ("en", "es")

    def __init__(self, en, es=None):
        self.en, self.es = en, en if es is None else es

    def html(self):
        return self.en if self.en == self.es else i18n(self.en, self.es)

    def data(self):
        return {"en": self.en, "es": self.es}


def h(v):
    return v.html() if isinstance(v, T) else v


def d(v):
    if isinstance(v, T):
        return v.data()
    if isinstance(v, (list, tuple)):
        return [d(x) for x in v]
    return v

# The other site sections share the v3 shell (same background, sheet, header and theme/language state).
ABOUT_BIO_EN = ("I'm Sergio Sánchez, a software engineer with over 15 years of experience across gaming, media, and "
                "enterprise. I move between backend architecture, game systems, and developer tooling — wherever a "
                "good idea needs to become something that actually ships. I've led teams of up to six engineers, "
                "and lately spend a good part of my time figuring out how AI agents fit into that process without "
                "losing rigor.")
ABOUT_BIO_ES = ("Soy Sergio Sánchez, ingeniero de software con más de 15 años de experiencia en gaming, medios y "
                "empresa. Me muevo entre arquitectura backend, sistemas de videojuegos y herramientas de "
                "desarrollo — donde una buena idea necesita convertirse en algo que realmente funcione. He "
                "liderado equipos de hasta seis ingenieros y, últimamente, dedico buena parte de mi tiempo a "
                "integrar agentes de IA en ese proceso sin perder rigor.")

TOOLBOX = [
    ("VS Code", "General-purpose editor for scripts and web work.", "Editor de uso general para scripts y web."),
    ("IntelliJ IDEA", "IDE for Java / Spring backends.", "IDE para backends en Java / Spring."),
    ("Rider", ".NET and Unity3D IDE.", "IDE para .NET y Unity3D."),
    ("Unity3D", "Game engine for the titles I've shipped.", "Motor de juego de los títulos que he lanzado."),
    ("PostgreSQL", "Go-to relational database.", "Base de datos relacional de cabecera."),
    ("AWS", "Cloud infrastructure for backend services.", "Infraestructura cloud para servicios backend."),
    ("Git", "Version control, every day.", "Control de versiones, todos los días."),
]

def toolbox_html():
    cards = "".join(
        f'<div class="toolcard"><div class="tt">{name}</div><div class="td">{i18n(en, es)}</div></div>'
        for name, en, es in TOOLBOX)
    return f'<div class="toolgrid">{cards}</div>'

SITE_PAGES = {
    "about/index.html": ("about", """<div class="sheet">
  $NAV$
  <header class="top">
    <div>
      <div class="prompt mono"><span class="g">sergio</span>@<span class="c">sergiowero.github.io</span>:~$ whoami</div>
      <div class="name"><span id="typed">$NAME$</span><span class="cur"></span></div>
      <div class="sub mono">$L_SUB$</div>
    </div>
  </header>
  <div class="cols">
    <main class="main">
      <section><h2 class="sh">$L_ABOUT$</h2><p class="profile">$ABOUT_BIO$</p></section>
      <section>$AI$</section>
      <section><h2 class="sh">$L_TOOLBOX$</h2>$TOOLBOX$</section>
      <section><h2 class="sh">$L_CONTACT$</h2><div class="contact">$CONTACT$</div></section>
    </main>
    <aside class="aside">
      <img class="avatar" src="/about/photo.jpg" alt="Sergio Sánchez at the Golden Gate Bridge" width="800" height="800">
    </aside>
  </div>
</div>"""),
    "timeline/index.html": ("history", """<div class="sheet hist-page">
  $NAV$
  <header class="top">
    <div>
      <div class="prompt mono"><span class="g">sergio</span>@<span class="c">sergiowero.github.io</span>:~$ cat <span class="f">$L_HISTFILE$</span></div>
      <div class="name"><span id="typed">$I18N_HISTORY_TITLE$</span><span class="cur"></span></div>
      <div class="hname">$NAME$</div>
      <div class="sub mono">$I18N_HISTORY_SUB$</div>
    </div>
  </header>
  <div class="hist">
    <div class="hcol">
      $HSEARCH$
      <main class="htl">$HISTORY$</main>
    </div>
    <aside class="subject" aria-live="polite">
      <div class="sub-k mono"><span class="g">➜</span> <span class="c">~</span> cat timeline/<span class="f" data-sub="slug"></span>.md</div>
      <div class="sub-kind mono" data-sub="kind"></div>
      <div class="sub-parent" data-sub="parent"></div>
      <div class="sub-co" data-sub="co"></div>
      <div class="sub-role" data-sub="role"></div>
      <div class="sub-when mono" data-sub="when"></div>
      <div class="sub-loc" data-sub="loc"></div>
      <div class="dchips" data-sub="inds"></div>
      <div class="sub-h mono">// tech</div>
      <div class="dchips" data-sub="tech"></div>
      <div class="sub-h mono">// timeline</div>
      <ol class="sub-nav" data-sub="nav"></ol>
      <div class="sub-progress"><i></i></div>
    </aside>
  </div>
  <script type="application/json" id="history-data">$HISTORY_JSON$</script>
</div>"""),
}
# old /cv/ and /history/ links keep working
REDIRECTS = {"cv/index.html": "/", "history/index.html": "/timeline/"}

# ------------------------------------------------------------------ DATA
NAME = "Sergio de Jesús Sánchez Robles"
ROLE = "Senior Software Engineer · Tech Lead"
TAG = "Backend &amp; Full-Stack · Game Development · AI-Assisted Engineering"

PROFILE = T(
    "Software developer with <b><span data-years>15</span> years of experience</b> across the gaming, media, and enterprise sectors, "
    "collaborating with major global companies. As an <b>AI enthusiast</b>, I actively leverage AI-assisted tools in my "
    "daily workflow to optimize backend development and accelerate project delivery. I am a rapid learner, highly "
    "adaptable to new technology stacks. Having previously <b>led teams of up to six people</b>, I consistently deliver "
    "high-quality, scalable software solutions on time and within budget.",
    "Desarrollador de software con <b><span data-years>15</span> años de experiencia</b> en videojuegos, medios y empresa, "
    "con compañías globales de primer nivel. Como <b>entusiasta de la IA</b>, uso herramientas asistidas por IA en mi día a "
    "día para optimizar el backend y acelerar la entrega de proyectos. Aprendo rápido y me adapto a nuevos stacks "
    "tecnológicos. Habiendo <b>liderado equipos de hasta seis personas</b>, entrego soluciones escalables y de alta calidad, "
    "a tiempo y en presupuesto.")

STEAM = "https://store.steampowered.com/app/2493180/The_Lullaby_of_Life/"
YT_VR = "https://www.youtube.com/watch?v=dyOfO0sYyp8&amp;t=446s"
YT_REEL = "https://www.youtube.com/watch?v=PWaarVatoEU"
CERBY = "https://www.cerby.com/"
INDITEX = "https://www.inditex.com/"

def ext(href, text):
    return f'<a href="{href}" target="_blank" rel="noopener noreferrer">{text}</a>'

MX = T("Guadalajara, México")
REMOTE = T("Remote", "Remoto")

JOBS = [
    dict(role=T("Senior Software Engineer / Tech Lead", "Ingeniero de Software Senior / Tech Lead"), co="Wizeline",
         tech=[".NET", "Java", "Spring", "Node.js", "Python", "React", "AWS", "PostgreSQL", "MariaDB", "Claude Code"],
         history_children=[   # second level on the History page (dates optional; add frm/to when known)
             dict(kind="project", slug="wizeline-global-news", role="", co="Dow Jones", loc=REMOTE, inds=[T("News", "Noticias")],
                  facts=[(T("Product", "Producto"), T("Gas-price SaaS", "SaaS de precios de gasolina")),
                         (T("Architecture", "Arquitectura"), "DDD"),
                         (T("Cloud"), "AWS"),
                         (T("Data", "Datos"), "PostgreSQL")],
                  tech=[".NET", "C#", "PostgreSQL", "AWS", "DDD", T("Domain events", "Eventos de dominio"),
                        T("Message queues", "Colas de mensajes"), T("Outbox pattern", "Patrón Outbox"),
                        T("Unit tests", "Pruebas unitarias"), "Claude Code"],
                  lede=T("Wizeline's engagement with Dow Jones, on a <b>gas-price SaaS</b>: a platform that helps gas station owners "
                         "keep a history of their prices, see what competitors are charging and set their own prices automatically "
                         "with strategies they define. Built in <b>.NET</b> on <b>PostgreSQL</b>, designed with <b>Domain-Driven Design</b>, "
                         "and split into many services that talk to each other through message queues.",
                         "El proyecto de Wizeline con Dow Jones, sobre un <b>SaaS de precios de gasolina</b>: una plataforma que ayuda a los "
                         "dueños de gasolineras a llevar un histórico de sus precios, ver los de la competencia y fijar los suyos de forma "
                         "automática con estrategias que ellos mismos definen. Hecha en <b>.NET</b> sobre <b>PostgreSQL</b>, diseñada con "
                         "<b>Domain-Driven Design</b> y dividida en muchos servicios que se comunican entre sí por colas de mensajes."),
                  pts=[],
                  groups=[
                      dict(h=T("The product", "El producto"), pts=[
                          T("<b>Price history:</b> every price a station has had is kept, so owners can look back at how their prices and the market moved.",
                            "<b>Histórico de precios:</b> se guarda cada precio que ha tenido una gasolinera, para que los dueños puedan ver cómo se movieron sus precios y el mercado."),
                          T("<b>Competitor prices:</b> the platform shows what the competition around each station is charging.",
                            "<b>Precios de la competencia:</b> la plataforma muestra lo que cobra la competencia alrededor de cada gasolinera."),
                          T("<b>Automatic pricing:</b> owners define their own strategies and the system sets the station's prices by following them.",
                            "<b>Precios automáticos:</b> los dueños definen sus propias estrategias y el sistema fija los precios de la gasolinera siguiéndolas."),
                          T("Clients use the tool to keep their stations up to date with the market and to protect the business' revenue.",
                            "Los clientes usan la herramienta para mantener sus gasolineras al día con el mercado y cuidar los ingresos del negocio."),
                      ]),
                      dict(h=T(".NET, PostgreSQL and Domain-Driven Design", ".NET, PostgreSQL y Domain-Driven Design"), pts=[
                          T("Services written in <b>.NET</b>, with the platform's data in <b>PostgreSQL</b>.",
                            "Servicios escritos en <b>.NET</b>, con los datos de la plataforma en <b>PostgreSQL</b>."),
                          T("The system was designed with <b>DDD</b>: the business rules lived in a domain model, and what happened in it was expressed as domain events.",
                            "El sistema estaba diseñado con <b>DDD</b>: las reglas de negocio vivían en un modelo de dominio, y lo que pasaba en él se expresaba como eventos de dominio."),
                      ]),
                      dict(h=T("Many services, domain events and the Outbox pattern", "Muchos servicios, eventos de dominio y el patrón Outbox"), pts=[
                          T("There were many services, and they communicated with each other through <b>message queues</b> carrying <b>domain events</b> instead of calling each other directly.",
                            "Había muchos servicios, y se comunicaban entre sí por <b>colas de mensajes</b> que llevaban <b>eventos de dominio</b>, en vez de llamarse directamente."),
                          T("Publishing followed the <b>Outbox pattern</b>: an event was saved to the database in the same transaction as the change that produced it, and sent to the queue from there — so no change went out without its event, and no event went out for a change that was rolled back.",
                            "La publicación seguía el <b>patrón Outbox</b>: el evento se guardaba en la base de datos en la misma transacción que el cambio que lo produjo, y desde ahí se enviaba a la cola; así ningún cambio salía sin su evento, ni salía un evento de un cambio que se revirtió."),
                      ]),
                      dict(h=T("Unit tests as part of \"done\"", "Pruebas unitarias como parte de \"terminado\""), pts=[
                          T("The project with the <b>most unit tests</b> I have seen in my career.",
                            "El proyecto con <b>más pruebas unitarias</b> que he visto en mi carrera."),
                          T("A feature was not complete until it shipped with extensive unit tests covering all of it — the tests were part of the deliverable, not an afterthought.",
                            "Un feature no estaba completo hasta que se entregaba con pruebas unitarias extensas que lo cubrieran todo: las pruebas eran parte de la entrega, no algo posterior."),
                      ]),
                      dict(h=T("Day to day", "Día a día"), pts=[
                          T("Engineered new features and resolved production issues in a high-velocity environment.",
                            "Desarrollé nuevas funcionalidades y resolví incidentes en producción en un entorno de alta velocidad."),
                          T("Leveraged AI tooling to accelerate development cycles and enhance code quality.",
                            "Usé herramientas de IA para acelerar los ciclos de desarrollo y elevar la calidad del código."),
                      ]),
                  ],
                  deliverables=[
                      dict(kind="milestone",
                           title=T("Feature set delivered for Costco", "Set de funcionalidades entregado para Costco"),
                           role=T("A set of features built for one client of the platform: Costco",
                                  "Un conjunto de funcionalidades hecho para un cliente de la plataforma: Costco"),
                           tech=[".NET", "PostgreSQL", "DDD", T("Unit tests", "Pruebas unitarias")],
                           pts=[T("Completed the full set of features Costco needed, each one delivered with the extensive unit tests the project required.",
                                  "Completé el set completo de funcionalidades que Costco necesitaba, cada una entregada con las pruebas unitarias extensas que el proyecto exigía.")],
                           result=T("Delivered in full, earning the <b>client's satisfaction</b>.",
                                    "Entregado por completo, logrando la <b>satisfacción del cliente</b>.")),
                  ]),
             dict(kind="project", slug="wizeline-media", role=T("Tech Lead"), co="Fox Corp", loc=REMOTE, inds=[T("Media &amp; Entertainment", "Medios y Entretenimiento")],
                  facts=[(T("Team", "Equipo"), T("5 engineers", "5 ingenieros")),
                         (T("Cloud"), "AWS"),
                         (T("Data", "Datos"), "PostgreSQL")],
                  tech=["Java 8", "Java 11", "Spring Boot", "JavaScript", "Node.js", "AWS Lambda", "Amazon SNS",
                        "Amazon SQS", "Amazon ECS", "CloudWatch", "PostgreSQL"],
                  lede=T("Wizeline's engagement with Fox Corp, where I was Tech Lead of a squad of five engineers. "
                         "Two kinds of services shared one AWS messaging layer: serverless workers written in JavaScript, "
                         "and Java applications running on containers.",
                         "El proyecto de Wizeline con Fox Corp, donde fui Tech Lead de un equipo de cinco ingenieros. "
                         "Dos tipos de servicios compartían una misma capa de mensajería en AWS: workers serverless escritos en "
                         "JavaScript y aplicaciones Java corriendo en contenedores."),
                  pts=[],
                  groups=[
                      dict(h=T("AWS &amp; service-to-service messaging", "AWS y mensajería entre servicios"), pts=[
                          T("<b>SNS</b> and <b>SQS</b> were the connective tissue of the platform: services published and consumed messages instead of calling each other directly.",
                            "<b>SNS</b> y <b>SQS</b> eran el tejido conectivo de la plataforma: los servicios publicaban y consumían mensajes en vez de llamarse directamente entre sí."),
                          T("The same messaging layer carried the integrations with <b>external systems</b> — services owned by clients and by other companies we worked with.",
                            "Esa misma capa de mensajería llevaba las integraciones con <b>sistemas externos</b>: servicios de clientes y de otras empresas con las que trabajábamos."),
                          T("Anything that could be processed asynchronously was modelled as a queue, so producers and consumers could move at their own pace.",
                            "Todo lo que podía procesarse de forma asíncrona se modelaba como una cola, de modo que productores y consumidores avanzaran a su propio ritmo."),
                      ]),
                      dict(h=T("Serverless services in JavaScript", "Servicios serverless en JavaScript"), pts=[
                          T("<b>AWS Lambda</b> ran a good part of the platform — some services, not all of them.",
                            "<b>AWS Lambda</b> corría buena parte de la plataforma: algunos servicios, no todos."),
                          T("<b>JavaScript</b> was the language of every Lambda, and the one I used most heavily on this engagement.",
                            "<b>JavaScript</b> era el lenguaje de todas las lambdas, y el que más usé en este proyecto."),
                          T("Those functions handled <b>queue-based tasks</b>; the main one was dispatching the calls that transcoded video.",
                            "Esas funciones resolvían <b>tareas basadas en colas</b>; la principal era lanzar las llamadas que transcodificaban video."),
                      ]),
                      dict(h=T("Java services on containers", "Servicios Java en contenedores"), pts=[
                          T("Every Java-based service was a <b>Spring Boot</b> application.",
                            "Todos los servicios basados en Java eran aplicaciones <b>Spring Boot</b>."),
                          T("They were deployed on <b>Amazon ECS</b>, AWS's own container orchestrator — its in-house counterpart to Kubernetes.",
                            "Se desplegaban en <b>Amazon ECS</b>, el orquestador de contenedores propio de AWS: su contraparte interna de Kubernetes."),
                          T("Those services talked to a <b>PostgreSQL</b> database, where the platform's data lived.",
                            "Esos servicios se conectaban a una base de datos <b>PostgreSQL</b>, donde vivían los datos de la plataforma."),
                          T("Two runtimes coexisted: <b>Java 8</b> on some services and <b>Java 11</b> on others.",
                            "Convivían dos runtimes: <b>Java 8</b> en algunos servicios y <b>Java 11</b> en otros."),
                      ]),
                      dict(h=T("Observability &amp; debugging", "Observabilidad y depuración"), pts=[
                          T("<b>CloudWatch</b> was where we read the logs — following what a message actually did across services and debugging the problems that turned up.",
                            "<b>CloudWatch</b> era donde leíamos los logs: seguir qué hizo realmente un mensaje entre servicios y depurar los problemas que aparecían."),
                      ]),
                  ],
                  deliverables=[dict(kind="milestone",
                      title=T("Tech Lead"),
                      role=T("A squad of five engineers, for the whole engagement",
                             "Un equipo de cinco ingenieros, durante todo el proyecto"),
                      pts=[T("Directed a team of 5 engineers as Tech Lead, designing and implementing customized, scalable software solutions for internal stakeholders.",
                             "Dirigí un equipo de 5 ingenieros como Tech Lead, diseñando e implementando soluciones escalables y a la medida para stakeholders internos."),
                           T("<b>Pull request reviews</b> for everything the squad shipped.",
                             "<b>Revisión de pull requests</b> de todo lo que entregaba el equipo."),
                           T("<b>Solution design</b> done together with the team members, not handed down to them.",
                             "<b>Diseño de las soluciones</b> en conjunto con los integrantes del equipo, no impuesto desde arriba."),
                           T("<b>Requirements refinement</b> directly with the business side, before the work reached the team.",
                             "<b>Refinamiento de requerimientos</b> directamente con negocio, antes de que el trabajo llegara al equipo.")],
                      result=T("Within <b>3 months</b> every member of the team could work independently, and our results earned us the <b>trust of the stakeholders</b>.",
                               "En <b>3 meses</b> cada integrante del equipo podía trabajar de forma independiente, y nuestros resultados nos ganaron la <b>confianza de los stakeholders</b>.")),
                  dict(kind="milestone",
                      title=T("Legacy → Media Cloud video migration service",
                              "Servicio de migración de video de legacy a Media Cloud"),
                      role=T("Mine end to end — designed, built and shipped to production on my own",
                             "Mío de principio a fin: lo diseñé, lo construí y lo llevé a producción yo solo"),
                      tech=["Java 11", "Spring Boot", "Amazon SQS", "PostgreSQL", T("Inbox pattern", "Patrón Inbox")],
                      pts=[
                          T("A service that moved video out of Fox's legacy system and into <b>Media Cloud</b>, the new platform the team was building on.",
                            "Un servicio que sacaba el video del sistema legacy de Fox y lo llevaba a <b>Media Cloud</b>, la nueva plataforma sobre la que trabajaba el equipo."),
                          T("Built in <b>Java 11</b> with <b>Spring Boot</b>, taking its work from an <b>SQS</b> queue and keeping its state in <b>PostgreSQL</b>.",
                            "Hecho en <b>Java 11</b> con <b>Spring Boot</b>, tomando el trabajo de una cola de <b>SQS</b> y guardando su estado en <b>PostgreSQL</b>."),
                          T("Processing followed the <b>Inbox pattern</b>: every incoming message was written to the database before being acted on, so a redelivered message never migrated the same video twice.",
                            "El procesamiento seguía el <b>patrón Inbox</b>: cada mensaje entrante se escribía en la base de datos antes de actuar sobre él, de modo que un mensaje reentregado nunca migraba dos veces el mismo video."),
                      ],
                      result=T("Shipped to production and migrated <b>over 100,000 legacy videos</b>, metadata included, into Fox's new system.",
                               "Entregado en producción y migró <b>más de 100,000 videos legacy</b>, metadatos incluidos, al nuevo sistema de Fox."))]),
             dict(kind="project", slug="wizeline-retail", role="", co="Inditex", loc=REMOTE, inds=[T("Retail")],
                  facts=[(T("Product", "Producto"), T("Factory audit viewer", "Visor de auditorías de fábricas")),
                         (T("Focus", "Enfoque"), "Backend"),
                         (T("Architecture", "Arquitectura"), T("Microservices · Clean Architecture", "Microservicios · Clean Architecture")),
                         (T("Workflow", "Flujo de trabajo"), "API first · OpenAPI")],
                  tech=["Java 11", "Spring", "Spring Batch", "MariaDB", "OpenAPI", "Clean Architecture",
                        T("Microservices", "Microservicios"), "Snowflake"],
                  lede=T("Wizeline's engagement with <b>Inditex</b>, the retail group behind Zara. The project was a "
                         "<b>viewer for the audits of the company's factories</b>: a set of <b>Java 11</b> microservices built with "
                         "<b>Clean Architecture</b> and an <b>API-first</b> workflow, backed by <b>MariaDB</b>. I architected the backend "
                         "services, modelled the relational database and built the service that migrated the audit data out of "
                         "<b>Snowflake</b> with <b>Spring Batch</b>.",
                         "El proyecto de Wizeline con <b>Inditex</b>, el grupo de retail detrás de Zara. El proyecto era un "
                         "<b>visualizador de las auditorías de las fábricas de la empresa</b>: un conjunto de microservicios en <b>Java 11</b> "
                         "hechos con <b>Clean Architecture</b> y un flujo de trabajo <b>API first</b>, sobre <b>MariaDB</b>. Diseñé la "
                         "arquitectura de los servicios backend, modelé la base de datos relacional y construí el servicio que migró los "
                         "datos de auditorías desde <b>Snowflake</b> con <b>Spring Batch</b>."),
                  pts=[],
                  groups=[
                      dict(h=T("The product", "El producto"), pts=[
                          T("A <b>viewer for the audits</b> Inditex runs on its <b>factories</b>: the audit data brought into one system where it could be looked at.",
                            "Un <b>visualizador de las auditorías</b> que Inditex hace a sus <b>fábricas</b>: los datos de las auditorías reunidos en un sistema donde se pudieran consultar."),
                          T("I architected the <b>backend services</b> behind it.",
                            "Diseñé la arquitectura de los <b>servicios backend</b> que lo sostenían."),
                      ]),
                      dict(h=T("API first, with OpenAPI", "API first, con OpenAPI"), pts=[
                          T("We worked <b>API first</b>: before any change started, its API was defined in an <b>OpenAPI</b> spec and agreed on; only then did the implementation begin.",
                            "Trabajábamos <b>API first</b>: antes de empezar cualquier cambio, su API se definía en una especificación <b>OpenAPI</b> y se acordaba; solo entonces empezaba la implementación."),
                          T("The contract came first and the code followed it, so what a service exposed was never a surprise.",
                            "El contrato iba primero y el código lo seguía, de modo que lo que exponía un servicio nunca era una sorpresa."),
                      ]),
                      dict(h=T("Microservices in Java 11, with Clean Architecture", "Microservicios en Java 11, con Clean Architecture"), pts=[
                          T("The backend was a set of <b>microservices</b> written in <b>Java 11</b> with <b>Spring</b>.",
                            "El backend era un conjunto de <b>microservicios</b> escritos en <b>Java 11</b> con <b>Spring</b>."),
                          T("Each one followed <b>Clean Architecture</b>: the domain and use cases at the centre; framework, database and HTTP at the edges, depending inward.",
                            "Cada uno seguía <b>Clean Architecture</b>: el dominio y los casos de uso al centro; framework, base de datos y HTTP en los bordes, dependiendo hacia adentro."),
                      ]),
                      dict(h=T("Data", "Datos"), pts=[
                          T("The data lived in <b>MariaDB</b>; I modelled the relational schema the services worked against.",
                            "Los datos vivían en <b>MariaDB</b>; modelé el esquema relacional sobre el que trabajaban los servicios."),
                      ]),
                  ],
                  deliverables=[
                      dict(kind="milestone",
                           title=T("Snowflake → MariaDB audit migration service",
                                   "Servicio de migración de auditorías de Snowflake a MariaDB"),
                           role=T("Built it — a long-running import on Spring Batch", "Lo construí: una importación de larga duración sobre Spring Batch"),
                           tech=["Java 11", "Spring Batch", "Snowflake", "MariaDB"],
                           pts=[T("A service that moved the audit data from <b>Snowflake</b>, where Inditex kept it, into the project's <b>MariaDB</b> database.",
                                  "Un servicio que llevaba los datos de auditorías desde <b>Snowflake</b>, donde Inditex los guardaba, a la base de datos <b>MariaDB</b> del proyecto."),
                                T("Built on <b>Spring Batch</b>, made for exactly this kind of long-running, chunked import.",
                                  "Hecho sobre <b>Spring Batch</b>, pensado justo para este tipo de importaciones largas y por lotes.")],
                           result=T("Delivered: the audits landed in <b>MariaDB</b>, and the viewer had its data.",
                                    "Entregado: las auditorías quedaron en <b>MariaDB</b> y el visualizador tuvo sus datos.")),
                  ],
                  links=[("inditex.com", INDITEX)]),
             dict(kind="project", slug="wizeline-cybersecurity", role="", co="Cerby", loc=REMOTE, inds=[T("Cybersecurity", "Ciberseguridad")],
                  facts=[(T("Product", "Producto"), T("Credential management", "Gestión de credenciales")),
                         (T("Team", "Equipo"), T("Founding project team", "Equipo inicial del proyecto")),
                         (T("Focus", "Enfoque"), "Backend"),
                         (T("Architecture", "Arquitectura"), T("Modular monolith · DDD", "Monolito modular · DDD"))],
                  tech=["Python", "Flask", "DDD", T("Modular monolith", "Monolito modular"), "SQLAlchemy", "Alembic",
                        T("Chrome extension", "Extensión de Chrome"), "Next.js", "React"],
                  lede=T("Wizeline's engagement with <b>Cerby</b>, a cybersecurity company whose software manages the "
                         "<b>credentials of a business</b> — the accounts and passwords its teams share for the apps they use. "
                         "I was part of the <b>initial project team</b>, on the backend: I led the first version of the backend, "
                         "modelled the initial database and built the company's first Chrome extension.",
                         "El proyecto de Wizeline con <b>Cerby</b>, una empresa de ciberseguridad cuyo software gestiona las "
                         "<b>credenciales de una empresa</b>: las cuentas y contraseñas que sus equipos comparten para las apps que usan. "
                         "Fui parte del <b>equipo inicial del proyecto</b>, en el backend: lideré la primera versión del backend, "
                         "modelé la base de datos inicial y construí la primera extensión de Chrome de la empresa."),
                  pts=[],
                  groups=[
                      dict(h=T("The product", "El producto"), pts=[
                          T("<b>Cerby</b> is cybersecurity software for managing a company's credentials: the logins its people share for the applications they work with, kept under control instead of in spreadsheets and chats.",
                            "<b>Cerby</b> es un software de ciberseguridad para gestionar las credenciales de una empresa: los accesos que su gente comparte para las aplicaciones con las que trabaja, bajo control en vez de en hojas de cálculo y chats."),
                          T("I joined as part of the <b>initial project team</b>, before there was a platform to build on — my part was the <b>backend</b>.",
                            "Entré como parte del <b>equipo inicial del proyecto</b>, antes de que existiera una plataforma sobre la cual construir; mi parte fue el <b>backend</b>."),
                      ]),
                      dict(h=T("Backend in Python with Flask, designed with DDD", "Backend en Python con Flask, diseñado con DDD"), pts=[
                          T("Led the <b>first version of the backend</b>, written in <b>Python</b> with <b>Flask</b>.",
                            "Lideré la <b>primera versión del backend</b>, escrita en <b>Python</b> con <b>Flask</b>."),
                          T("It was my <b>first time working with Domain-Driven Design</b>: the domain modelled first, the framework kept at the edges.",
                            "Fue mi <b>primera vez trabajando con Domain-Driven Design</b>: el dominio modelado primero y el framework en los bordes."),
                          T("The project was a <b>modular monolith</b> — one deployable, split into modules with clear boundaries, so it could grow without becoming a tangle or forcing microservices too early.",
                            "El proyecto fue un <b>monolito modular</b>: un solo desplegable, dividido en módulos con fronteras claras, para que pudiera crecer sin enredarse ni forzar microservicios antes de tiempo."),
                      ]),
                      dict(h=T("Data model &amp; migrations", "Modelo de datos y migraciones"), pts=[
                          T("For the backend MVP I <b>modelled the initial database</b>.",
                            "Para el MVP del backend <b>modelé la base de datos inicial</b>."),
                          T("Schema changes went through a <b>migration system</b> built on <b>SQLAlchemy</b> (with Alembic), so every change to the model was versioned and repeatable across environments.",
                            "Los cambios de esquema pasaban por un <b>sistema de migraciones</b> hecho sobre <b>SQLAlchemy</b> (con Alembic), de modo que cada cambio al modelo quedaba versionado y era repetible entre entornos."),
                      ]),
                      dict(h=T("Frontend, in support", "Frontend, como apoyo"), pts=[
                          T("Worked as an <b>auxiliary hand on the frontend</b>, built in <b>Next.js</b>, whenever the web side needed it.",
                            "Trabajé como <b>apoyo en el frontend</b>, hecho en <b>Next.js</b>, cuando el lado web lo necesitaba."),
                      ]),
                  ],
                  deliverables=[
                      dict(kind="milestone",
                           title=T("The MVP, delivered", "El MVP, entregado"),
                           role=T("The initial platform Cerby launched with", "La plataforma inicial con la que Cerby se lanzó"),
                           tech=["Python", "Flask", "Next.js", T("Chrome extension", "Extensión de Chrome")],
                           pts=[T("The whole MVP — backend, web frontend and Chrome extension — shipped as the product's first version.",
                                  "El MVP completo, backend, frontend web y extensión de Chrome, entregado como la primera versión del producto.")],
                           result=T("A <b>success</b>: it is what allowed Cerby to keep going — the company is <b>still alive today</b>, built on what that MVP started.",
                                    "Un <b>éxito</b>: fue lo que permitió que Cerby siguiera adelante; la empresa <b>sigue viva hasta hoy</b>, construida sobre lo que ese MVP inició.")),
                      dict(kind="milestone",
                           title=T("First version of the backend", "Primera versión del backend"),
                           role=T("Led it — Python, Flask, DDD, modular monolith", "La lideré: Python, Flask, DDD, monolito modular"),
                           tech=["Python", "Flask", "DDD", T("Modular monolith", "Monolito modular"), "SQLAlchemy", "Alembic"],
                           pts=[T("The MVP's backend, from the initial data model and its migrations to the service the product launched with.",
                                  "El backend del MVP, desde el modelo de datos inicial y sus migraciones hasta el servicio con el que se lanzó el producto.")],
                           result=T("The <b>initial platform launched</b> on it.",
                                    "La <b>plataforma inicial se lanzó</b> sobre él.")),
                      dict(kind="release",
                           title=T("Cerby's first Chrome extension", "La primera extensión de Chrome de Cerby"),
                           role=T("Built the first version", "Construí la primera versión"),
                           tech=[T("Chrome extension", "Extensión de Chrome")],
                           pts=[T("The company's <b>first browser extension</b>: the piece that brings the managed credentials into the browser, where people actually log in.",
                                  "La <b>primera extensión de navegador</b> de la empresa: la pieza que lleva las credenciales gestionadas al navegador, donde la gente realmente inicia sesión.")],
                           result=T("Shipped as Cerby's first Chrome extension.",
                                    "Entregada como la primera extensión de Chrome de Cerby.")),
                  ],
                  links=[("cerby.com", CERBY)]),
         ], period=T("Mar 2020 - Present", "Mar 2020 - Actualidad"), frm="2020-03", to=None,
         inds=[T("News", "Noticias"), T("Media &amp; Entertainment", "Medios y Entretenimiento"), T("Retail"), T("Cybersecurity", "Ciberseguridad")], loc=MX, cur=True, pts=[
        T('<b>Dow Jones:</b> Engineered new features and resolved production issues in a high-velocity environment. Leveraged AI tooling to accelerate development cycles and enhance code quality. <span class="stack">Tech: .NET, AWS, PostgreSQL, Claude Code.</span>',
          '<b>Dow Jones:</b> Desarrollé funcionalidades y resolví incidentes en producción en un entorno de alta velocidad. Usé herramientas de IA para acelerar los ciclos de desarrollo y elevar la calidad del código. <span class="stack">Tech: .NET, AWS, PostgreSQL, Claude Code.</span>'),
        T('<b>Fox Corp:</b> Directed a team of 5 engineers as Tech Lead, designing and implementing customized, scalable software solutions for internal stakeholders. <span class="stack">Tech: Java, Spring, Node.js, AWS, PostgreSQL.</span>',
          '<b>Fox Corp:</b> Dirigí un equipo de 5 ingenieros como Tech Lead, diseñando e implementando soluciones escalables y a la medida para stakeholders internos. <span class="stack">Tech: Java, Spring, Node.js, AWS, PostgreSQL.</span>'),
        T('<b>Inditex:</b> Architected backend services for a complex audit system. Designed relational databases, implemented microservices, and built migration services for long-running data imports. <span class="stack">Tech: Java, Spring, MariaDB.</span>',
          '<b>Inditex:</b> Diseñé la arquitectura backend de un sistema de auditoría complejo. Modelé bases de datos relacionales, implementé microservicios y construí servicios de migración para importaciones de larga duración. <span class="stack">Tech: Java, Spring, MariaDB.</span>'),
        T('<b>Cerby:</b> Spearheaded the full-stack development of an MVP as a contingent engineer to successfully launch the initial platform. <span class="stack">Tech: Python, React.</span>',
          '<b>Cerby:</b> Lideré el desarrollo full-stack de un MVP como ingeniero externo para lanzar con éxito la plataforma inicial. <span class="stack">Tech: Python, React.</span>'),
    ], history=dict(   # the full story for /timeline/; the Resume keeps the bullets above
        tech=[".NET", "Java", "Spring", "Node.js", "Python", "React", "AWS", "PostgreSQL", "MariaDB", "Claude Code",
              "Codex", "LangChain", "Claude SDK"],
        facts=[(T("Company", "Empresa"), T("Software consultancy", "Consultora de software")),
               (T("Role", "Rol"), T("Senior Software Engineer / Tech Lead", "Ingeniero de Software Senior / Tech Lead")),
               (T("Clients", "Clientes"), "Dow Jones · Fox Corp · Inditex · Cerby"),
               (T("Now", "Ahora"), T("Training as an AI engineer", "Formándome como AI engineer"))],
        lede=T("Wizeline is a <b>software consultancy</b> with many clients: its engineers are placed on client engagements, "
               "and every entry below is a client I have worked for since joining in March 2020 — Dow Jones, Fox Corp, "
               "Inditex and Cerby. My role is <b>Senior Software Engineer / Tech Lead</b>: I join the client's team, build and "
               "run their backend services, and lead when the engagement calls for it. Alongside the client work there is "
               "<b>constant training</b> — including on AI tools such as <b>Claude Code</b> and <b>Codex</b> — and right now it is "
               "aimed at becoming an <b>AI engineer</b>: building agents, mainly in <b>Python</b> with <b>LangChain</b> and the "
               "<b>Claude SDK</b>.",
               "Wizeline es una <b>consultora de software</b> con muchos clientes: sus ingenieros se asignan a proyectos de "
               "cliente, y cada entrada de abajo es un cliente para el que he trabajado desde que entré en marzo de 2020: "
               "Dow Jones, Fox Corp, Inditex y Cerby. Mi rol es <b>Ingeniero de Software Senior / Tech Lead</b>: me integro al "
               "equipo del cliente, construyo y opero sus servicios backend, y lidero cuando el proyecto lo requiere. Junto al "
               "trabajo con clientes hay <b>capacitación constante</b> —incluida en herramientas de IA como <b>Claude Code</b> y "
               "<b>Codex</b>— y ahora mismo está enfocada en convertirme en <b>AI engineer</b>: crear agentes, principalmente en "
               "<b>Python</b> con <b>LangChain</b> y el <b>Claude SDK</b>."),
        groups=[
            dict(h=T("The role", "El rol"), pts=[
                T("Wizeline is a consultancy: it has many clients, and its engineers work embedded in those clients' teams. "
                  "Since March 2020 I have gone through four of them — each has its own entry below.",
                  "Wizeline es una consultora: tiene muchos clientes, y sus ingenieros trabajan integrados en los equipos de esos "
                  "clientes. Desde marzo de 2020 he pasado por cuatro; cada uno tiene su propia entrada abajo."),
                T("Mostly backend: designing services, data models and integrations, and taking features from design to "
                  "production in whatever stack the client runs — <b>.NET</b>, <b>Java / Spring</b>, <b>Node.js</b> or "
                  "<b>Python</b>, on <b>AWS</b>, <b>PostgreSQL</b> and <b>MariaDB</b>.",
                  "Sobre todo backend: diseñar servicios, modelos de datos e integraciones, y llevar funcionalidades de diseño a "
                  "producción en el stack que use el cliente: <b>.NET</b>, <b>Java / Spring</b>, <b>Node.js</b> o "
                  "<b>Python</b>, sobre <b>AWS</b>, <b>PostgreSQL</b> y <b>MariaDB</b>."),
                T("<b>Tech Lead</b> when the engagement calls for it: at Fox Corp I led a squad of five engineers for the three "
                  "years of the engagement.",
                  "<b>Tech Lead</b> cuando el proyecto lo requiere: en Fox Corp lideré un equipo de cinco ingenieros durante los "
                  "tres años del proyecto."),
            ]),
        ],
        deliverables=[
            dict(kind="training",
                 title=T("Constant training &amp; AI at work", "Capacitación constante e IA en el trabajo"),
                 role=T("Ongoing since 2020 · alongside the client work, not between projects",
                        "Continua desde 2020 · en paralelo al trabajo con clientes, no entre proyectos"),
                 tech=["Claude Code", "Codex", "Python", "LangChain", "Claude SDK"],
                 pts=[
                     T("Training is a constant part of the job at Wizeline: there is always a track running next to the client work.",
                       "La capacitación es parte constante del trabajo en Wizeline: siempre hay una ruta corriendo junto al trabajo con clientes."),
                     T("<b>AI tooling</b>: trained to work with coding agents such as <b>Claude Code</b> and <b>Codex</b>, "
                       "which I now use day to day on client work.",
                       "<b>Herramientas de IA</b>: capacitado para trabajar con agentes de programación como <b>Claude Code</b> y "
                       "<b>Codex</b>, que hoy uso a diario en el trabajo con clientes."),
                     T("<b>AI engineering</b>: the current track — being trained to build agents, mainly in <b>Python</b> "
                       "with <b>LangChain</b> and the <b>Claude SDK</b>.",
                       "<b>AI engineering</b>: la ruta actual; me están formando para crear agentes, principalmente en <b>Python</b> "
                       "con <b>LangChain</b> y el <b>Claude SDK</b>."),
                 ],
                 result=T("In training to become an <b>AI engineer</b>: agents in Python, LangChain and the Claude SDK.",
                          "En formación para ser <b>AI engineer</b>: agentes en Python, LangChain y el Claude SDK.")),
        ],
    )),
    dict(role=T("Lead Software Engineer", "Ingeniero de Software Líder"), co="1 Simple Idea", tech=["C#", "Unity3D", "iOS", "IoC / DI"], period=T("Jul 2019 - Mar 2020"), frm="2019-07", to="2020-03", inds=[T("Gaming · Mobile", "Videojuegos · Móvil")], loc=MX, cur=False, pts=[
        T('Led a small programming team in the development of a mobile iOS game, taking ownership of the <b>core game architecture</b>.',
          'Lideré un equipo pequeño de programación en un juego móvil para iOS, a cargo de la <b>arquitectura central del juego</b>.'),
        T('Architected and implemented an Inversion of Control (IoC), Dependency Injection (DI), and a robust event-driven system.',
          'Diseñé e implementé Inversión de Control (IoC), Inyección de Dependencias (DI) y un sistema robusto orientado a eventos.'),
        T('Accelerated the development cycle and reduced bug rates by establishing a modular paradigm, which significantly decreased art asset integration time for art teams.',
          'Aceleré el ciclo de desarrollo y reduje los bugs con un paradigma modular que recortó de forma notable el tiempo de integración de assets para los equipos de arte.'),
        T(f'Released on <b>Apple Arcade</b>, now on Steam: {ext(STEAM, "The Lullaby of Life")}.',
          f'Publicado en <b>Apple Arcade</b> y ahora en Steam: {ext(STEAM, "The Lullaby of Life")}.'),
    ], history=dict(   # the full story for /timeline/; the Resume keeps the bullets above
        tech=["C#", "Unity3D", "iOS", "Apple Arcade", "IoC / DI", T("Unit tests", "Pruebas unitarias"), "Flow"],
        facts=[(T("Game", "Juego"), "The Lullaby of Life"),
               (T("Engine", "Motor"), "Unity3D"),
               (T("Platform", "Plataforma"), "iOS · Apple Arcade"),
               (T("Built in", "Hecho en"), T("9 months", "9 meses"))],
        lede=T("Nine months at 1 Simple Idea on <b>The Lullaby of Life</b>, a mobile game for iOS built in <b>Unity3D</b>. "
               "The game was split in two — the visual and gameplay side, and a logic layer covered by unit tests — and held "
               "together by two systems written specifically for it: a hand-made IoC / DI container and <b>Flow</b>, a "
               "data-connection system.",
               "Nueve meses en 1 Simple Idea trabajando en <b>The Lullaby of Life</b>, un juego móvil para iOS hecho en <b>Unity3D</b>. "
               "El juego se dividió en dos —la parte visual y de gameplay, y una capa de lógica cubierta por pruebas unitarias— y "
               "se sostenía sobre dos sistemas escritos específicamente para él: un contenedor de IoC / DI hecho a mano y <b>Flow</b>, "
               "un sistema de conexión de datos."),
        pts=[],
        groups=[
            dict(h=T("Inversion of Control &amp; Dependency Injection", "Inversión de Control e Inyección de Dependencias"), pts=[
                T("A hand-made <b>IoC / DI</b> system, written specifically for this game instead of taken from a library.",
                  "Un sistema de <b>IoC / DI</b> hecho a mano, escrito específicamente para este juego en lugar de tomarlo de una librería."),
                T("Game components declared what they needed and the container supplied it, so no component depended directly on another.",
                  "Los componentes del juego declaraban lo que necesitaban y el contenedor lo proveía, de modo que ningún componente dependía directamente de otro."),
            ]),
            dict(h=T("Two layers: visual + gameplay, and logic", "Dos capas: visual + gameplay, y lógica"), pts=[
                T("The game was divided in two parts: the <b>visual and gameplay</b> layer, and the <b>logic</b> layer.",
                  "El juego se dividió en dos partes: la capa <b>visual y de gameplay</b>, y la capa de <b>lógica</b>."),
                T("Keeping the logic apart from the visuals is what made it testable: the whole logic layer had <b>unit tests</b>.",
                  "Separar la lógica de lo visual es lo que la hizo testeable: toda la capa de lógica tenía <b>pruebas unitarias</b>."),
            ]),
            dict(h=T("Flow — connecting data between components", "Flow: conexión de datos entre componentes"), pts=[
                T("<b>Flow</b>, a data-connection system built specially for the game: a variable in one component could be connected to a variable in another transparently, without the two components knowing about each other.",
                  "<b>Flow</b>, un sistema de conexión de datos hecho especialmente para el juego: una variable de un componente se podía conectar a la de otro de forma transparente, sin que los dos componentes se conocieran entre sí."),
                T("Together with the DI container it gave the project a modular paradigm that cut bug rates and the time art teams spent integrating assets.",
                  "Junto con el contenedor de DI, dio al proyecto un paradigma modular que redujo los bugs y el tiempo que los equipos de arte pasaban integrando assets."),
            ]),
        ],
        deliverables=[
            dict(kind="milestone", title=T("Lead Programmer", "Programador Líder"),
                 role=T("Led the small programming team that built the game", "Lideré el equipo pequeño de programación que construyó el juego"),
                 pts=[T('Led a small programming team in the development of a mobile iOS game, taking ownership of the <b>core game architecture</b>.',
                        'Lideré un equipo pequeño de programación en un juego móvil para iOS, a cargo de la <b>arquitectura central del juego</b>.')]),
            dict(kind="pace", title=T("Finished in nine months", "Terminado en nueve meses"),
                 role=T("Fast and well organized — with some overtime along the way", "Rápido y bien organizado, con algo de tiempo extra en el camino"),
                 pts=[T("The game went from start to finish in <b>nine months</b>. The whole team worked fast and in a very organized way, and that is what made the timeline possible.",
                        "El juego pasó de inicio a fin en <b>nueve meses</b>. Todo el equipo trabajó rápido y de forma muy organizada, y eso es lo que hizo posible el plazo."),
                      T("It did not come for free, though: there was some extra time in the day-to-day, and a few Saturdays went into getting the project finished.",
                        "Eso sí, no salió gratis: hubo algo de tiempo extra en el día a día, y algunos sábados se fueron en terminar el proyecto.")],
                 result=T("Shipped fast — but the overtime was the price of the schedule, not something anyone wanted to repeat.",
                          "Salió rápido, pero las horas extra fueron el precio del calendario, no algo que nadie quisiera repetir.")),
            dict(kind="release", title=T("Published on Apple Arcade", "Publicado en Apple Arcade"), tech=["iOS", "Apple TV", "Apple Arcade"],
                 pts=[T("<b>The Lullaby of Life</b> shipped on <b>Apple Arcade</b>, Apple's subscription game service, for iOS and Apple TV.",
                        "<b>The Lullaby of Life</b> salió en <b>Apple Arcade</b>, el servicio de juegos por suscripción de Apple, para iOS y Apple TV.")]),
            dict(kind="release", title=T("Published on Steam", "Publicado en Steam"), tech=["Steam"],
                 pts=[T(f"The game later reached Steam: {ext(STEAM, 'The Lullaby of Life on Steam')}.",
                        f"El juego llegó después a Steam: {ext(STEAM, 'The Lullaby of Life en Steam')}.")]),
        ],
        links=[(T("The Lullaby of Life on Steam", "The Lullaby of Life en Steam"), STEAM)],
    )),
    dict(role=T("Senior Software Engineer", "Ingeniero de Software Senior"), co="Virtually Live", tech=["C#", "Unity3D", "VR", "Python", "Django", "Go", "REST"], period=T("Feb 2017 - Jan 2020", "Feb 2017 - Ene 2020"), frm="2017-02", to="2020-01", inds=[T("Gaming · VR", "Videojuegos · VR")], loc=T("Málaga, Spain", "Málaga, España"), cur=False, pts=[
        T('Developed <b>racing games</b> for HTC Vive, Oculus, and Gear VR platforms.',
          'Desarrollé <b>juegos de carreras</b> para HTC Vive, Oculus y Gear VR.'),
        T('Engineered a core abstraction layer for game modules, encompassing VR controllers, Social APIs, and database access, utilizing JSON for configuration management.',
          'Construí una capa de abstracción para los módulos del juego —controles VR, APIs sociales y acceso a datos— con JSON para la gestión de configuración.'),
        T('Ported the VR title to iOS by developing core gameplay mechanics in C# and architecting the supporting backend RESTful services with Python, Django, and Go.',
          'Porté el título de VR a iOS desarrollando las mecánicas principales en C# y diseñando los servicios backend RESTful con Python, Django y Go.'),
        T(f'Contributed to the successful release of the iOS adaptation ({ext(YT_VR, "gameplay")}).',
          f'Contribuí al lanzamiento de la adaptación para iOS ({ext(YT_VR, "gameplay")}).'),
    ], history=dict(   # the full story for /timeline/; the Resume keeps the bullets above
        tech=["C#", "Unity3D", "VR", "Steam", "HTC Vive", "Oculus", "Gear VR", "iOS", "Python", "Django", ".NET", "Go", "REST",
              T("Live race data", "Datos de carrera en vivo"), T("Game modes", "Modos de juego"), T("Prototyping", "Prototipado")],
        facts=[(T("Data", "Datos"), T("Formula E live race feed", "Datos en vivo de las carreras de Fórmula E")),
               (T("Products", "Productos"), T("Steam VR app → mobile app (iOS)", "App de VR en Steam → app móvil (iOS)")),
               (T("Engine", "Motor"), T("Unity3D (C#)")),
               (T("Backend"), T("Python · Django (first version in .NET)", "Python · Django (primera versión en .NET)")),
               (T("Shown at", "Mostrado en"), T("Official Formula E events", "Eventos oficiales de Fórmula E"))],
        lede=T("Three years working remotely for Virtually Live, a studio based in Málaga. Everything rested on one thing: the <b>input data from the Formula E "
               "races</b>, which let us <b>simulate the race that was happening live</b>, in a virtual world, only a few minutes "
               "behind. On that base we built two products. First a <b>Steam app</b>, so that people with a <b>VR</b> headset could "
               "<b>watch the race as if they were there</b> — and even <b>ride along with the drivers</b>; the <b>pool</b> and "
               "<b>trivia (Jeopardy)</b> prototypes were meant to live inside it. Then the project <b>dropped VR</b> and became a "
               "<b>mobile app</b> where people watched the race and <b>competed against the drivers</b>: that is where we programmed "
               "the <b>game modes</b>, the <b>UI</b> and rules such as the <b>safety car</b>. Underneath, a <b>backend in Python "
               "and Django</b> for accounts and friends — after a first version I wrote in .NET. It went <b>live on iOS</b>, and "
               "during a race the <b>Formula E commentators mentioned the players competing in the app</b>. Alongside, a <b>VR "
               "showroom</b> of the racing cars' components, used at the official Formula E events.",
               "Tres años trabajando en remoto para Virtually Live, un estudio de Málaga. Todo se apoyaba en una cosa: los <b>datos de entrada de las carreras de "
               "Fórmula E</b>, que nos permitían <b>simular la carrera que estaba en vivo</b>, en un mundo virtual, con solo unos "
               "minutos de retraso. Sobre esa base hicimos dos productos. Primero una <b>app de Steam</b>, para que la gente con "
               "<b>VR</b> pudiera <b>ver la carrera como si estuviera ahí</b> —e incluso <b>subirse con los pilotos</b>—; los "
               "prototipos de <b>pool</b> y <b>trivia (Jeopardy)</b> se querían usar dentro de ella. Luego el proyecto <b>descartó el "
               "VR</b> y se convirtió en una <b>app de móviles</b> donde la gente veía la carrera y <b>competía con los corredores</b>: "
               "ahí es donde programamos los <b>modos de juego</b>, la <b>UI</b> y reglas como el <b>safety car</b>. Debajo, un "
               "<b>backend en Python con Django</b> para cuentas y amigos, después de una primera versión que hice en .NET. Salió "
               "<b>live en iOS</b>, y durante una carrera los <b>locutores de la Fórmula E mencionaron a los jugadores que competían "
               "en la app</b>. Aparte, un <b>showroom de VR</b> con los componentes de los autos de carreras, usado en los eventos "
               "oficiales de Fórmula E."),
        pts=[],
        groups=[
            dict(h=T("The base: Formula E's live race data, simulated in a virtual world", "La base: los datos en vivo de la Fórmula E, simulados en un mundo virtual"), pts=[
                T("We had the <b>input data from the Formula E races</b>.",
                  "Teníamos los <b>datos de entrada de las carreras de Fórmula E</b>."),
                T("With it we could <b>simulate the race that was running live</b> in a <b>virtual world</b>, with only <b>a few minutes of delay</b>. The two products below were both built on this same base.",
                  "Con ellos podíamos <b>simular la carrera que estaba en vivo</b> en un <b>mundo virtual</b>, con solo <b>unos minutos de retraso</b>. Los dos productos de abajo se construyeron sobre esta misma base."),
            ]),
            dict(h=T("First product: a Steam app to watch the race in VR", "Primer producto: una app de Steam para ver la carrera en VR"), pts=[
                T("An app on <b>Steam</b> so that people with a <b>VR</b> headset — <b>HTC Vive</b>, <b>Oculus</b>, <b>Gear VR</b> — could <b>watch the race as if they were there</b>, and even <b>ride along with the drivers</b>.",
                  "Una app en <b>Steam</b> para que la gente con <b>VR</b> —<b>HTC Vive</b>, <b>Oculus</b>, <b>Gear VR</b>— pudiera <b>ver la carrera como si estuviera ahí</b>, e incluso <b>subirse con los pilotos</b>."),
                T("Engineered a <b>core abstraction layer</b> for the game modules — <b>VR controllers</b>, <b>social APIs</b> and <b>database access</b> — with <b>JSON</b> for configuration management.",
                  "Construí una <b>capa de abstracción</b> para los módulos del juego —<b>controles VR</b>, <b>APIs sociales</b> y <b>acceso a datos</b>— con <b>JSON</b> para la gestión de configuración."),
                T("This is where the <b>online pool</b> and <b>trivia (Jeopardy)</b> games were meant to be used: things to play inside the VR app, around the race. Both stayed prototypes and <b>never saw the light</b>.",
                  "Aquí es donde se querían usar los juegos de <b>pool online</b> y <b>trivia (Jeopardy)</b>: cosas para jugar dentro de la app de VR, alrededor de la carrera. Los dos se quedaron en prototipo y <b>nunca salieron a la luz</b>."),
            ]),
            dict(h=T("The pivot: VR dropped, a mobile app to compete against the drivers", "El giro: se descarta el VR, una app móvil para competir con los corredores"), pts=[
                T("The project then <b>dropped VR</b> and became a <b>mobile app</b> where people could <b>watch the race</b> and <b>compete against the drivers</b>.",
                  "Luego el proyecto <b>descartó el VR</b> y se convirtió en una <b>app de móviles</b> donde la gente podía <b>ver la carrera</b> y <b>competir con los corredores</b>."),
                T("This is the part of the project where we programmed the <b>game modes</b> and the <b>UI</b>, and added rules such as the <b>safety car</b>, among others.",
                  "En esa parte del proyecto es donde programamos los <b>modos de juego</b> y la <b>UI</b>, y agregamos reglas como el <b>safety car</b>, entre otras."),
                T("The core gameplay mechanics in <b>C#</b>, on <b>iOS</b>.",
                  "Las mecánicas principales en <b>C#</b>, en <b>iOS</b>."),
            ]),
            dict(h=T("Backend: accounts and friends, in Python with Django", "Backend: cuentas y amigos, en Python con Django"), pts=[
                T("Implemented the <b>backend</b> so that users could <b>have an account</b> and <b>add friends</b>.",
                  "Implementé el <b>backend</b> para que los usuarios pudieran <b>tener cuenta</b> y <b>agregar amigos</b>."),
                T("Written in <b>Python</b> with <b>Django</b>, as <b>RESTful services</b>, with <b>Go</b> alongside.",
                  "Escrito en <b>Python</b> con <b>Django</b>, como <b>servicios RESTful</b>, con <b>Go</b> al lado."),
                T("<b>An interesting detail:</b> I implemented a first version of the backend in <b>.NET</b>. Then the company hired a new lead, and everything moved to <b>Python</b>.",
                  "<b>Un detalle interesante:</b> implementé una versión inicial del backend en <b>.NET</b>. Después la empresa contrató a un nuevo líder y cambió todo a <b>Python</b>."),
            ]),
            dict(h=T("A VR showroom for Formula E", "Un showroom de VR para Fórmula E"), pts=[
                T("Separately, a <b>showroom</b>: an application to show, in <b>virtual reality</b>, the <b>components of the racing cars</b>.",
                  "Aparte, un <b>showroom</b>: una aplicación para mostrar, en <b>realidad virtual</b>, los <b>componentes de los autos de carreras</b>."),
                T("This one did ship — it was <b>used at the official Formula E events</b>.",
                  "Este sí salió: <b>se usó en los eventos oficiales de Fórmula E</b>."),
            ]),
        ],
        deliverables=[
            dict(kind="prototype", title=T("Online pool in VR", "Pool online en VR"), tech=["Unity3D", "C#", "VR", T("Online")],
                 role=T("Mini-game for the Steam VR app · prototype", "Minijuego para la app de VR en Steam · prototipo"),
                 pts=[T("A <b>pool game</b>, <b>online</b>, in <b>virtual reality</b> — meant to be played inside the Steam app, around the live race.",
                        "Un <b>juego de pool</b>, <b>online</b>, en <b>realidad virtual</b>: pensado para jugarse dentro de la app de Steam, alrededor de la carrera en vivo.")],
                 result=T("Stayed a prototype; it was never released.", "Se quedó en prototipo; nunca salió a la luz.")),
            dict(kind="prototype", title=T("Trivia (Jeopardy) in VR", "Trivia (Jeopardy) en VR"), tech=["Unity3D", "C#", "VR"],
                 role=T("Mini-game for the Steam VR app · prototype", "Minijuego para la app de VR en Steam · prototipo"),
                 pts=[T("The <b>Jeopardy</b> quiz show as a game in <b>virtual reality</b> — meant for the same Steam app, alongside the pool game.",
                        "El concurso <b>Jeopardy</b> como juego en <b>realidad virtual</b>: pensado para la misma app de Steam, junto al juego de pool.")],
                 result=T("Stayed a prototype; it was never released.", "Se quedó en prototipo; nunca salió a la luz.")),
            dict(kind="milestone", title=T("Live on iOS — real users racing during a Formula E race", "Live en iOS: usuarios compitiendo durante una carrera de Fórmula E"),
                 role=T("Mobile app · game modes, UI, race rules and backend", "App móvil · modos de juego, UI, reglas de carrera y backend"),
                 tech=["Unity3D", "C#", "iOS", "Python", "Django"],
                 pts=[T("The project went <b>live on iOS only</b>.",
                        "El proyecto salió <b>live solamente en iOS</b>."),
                      T("There was a <b>race with users playing</b> in the app, competing against the drivers as the real race ran.",
                        "Se pudo tener una <b>carrera con usuarios jugando</b> en la app, compitiendo con los corredores mientras corría la carrera real."),
                      T("The <b>Formula E commentators</b>, live on air, <b>mentioned the players who were competing in the app</b>.",
                        "Los <b>locutores de la Fórmula E</b>, en vivo, <b>mencionaban a los jugadores que estaban compitiendo en la app</b>."),
                      T(f"Gameplay of the iOS app: {ext(YT_VR, 'video')}.",
                        f"Gameplay de la app de iOS: {ext(YT_VR, 'video')}.")],
                 result=T("A live Formula E race with people racing in the app, and the broadcast commentators mentioning them.",
                          "Una carrera de Fórmula E en vivo con gente compitiendo en la app, y los locutores de la transmisión mencionándolos.")),
            dict(kind="release", title=T("VR showroom for Formula E", "Showroom de VR para Fórmula E"), tech=["Unity3D", "C#", "VR"],
                 role=T("VR application · racing-car components", "Aplicación de VR · componentes de los autos de carreras"),
                 pts=[T("A <b>showroom</b> in <b>virtual reality</b>: an application to show the <b>components of the racing cars</b>.",
                        "Un <b>showroom</b> en <b>realidad virtual</b>: una aplicación para mostrar los <b>componentes de los autos de carreras</b>.")],
                 result=T("Used at the official Formula E events.", "Usado en los eventos oficiales de Fórmula E.")),
        ],
        links=[(T("iOS app — gameplay", "App de iOS: gameplay"), YT_VR)],
    )),
    dict(role=T("Software Engineer", "Ingeniero de Software"), co="Intel", tech=["Ruby", "XML", "Automation"], period=T("Feb 2015 - Feb 2017"), frm="2015-02", to="2017-02", inds=[T("Semiconductors", "Semiconductores")], loc=MX, cur=False, pts=[
        T('Engineered <b>APIs in Ruby</b> to support hardware validation teams and streamline testing workflows.',
          'Desarrollé <b>APIs en Ruby</b> para los equipos de validación de hardware y para agilizar los flujos de pruebas.'),
        T('Created automation tools and scripts to synchronize API deployments with client environments across multiple global Intel sites.',
          'Creé herramientas y scripts de automatización para sincronizar despliegues de APIs con los entornos cliente en varias sedes globales de Intel.'),
        T('Leveraged Ruby metaprogramming to parse XML-formatted design documents and dynamically generate executable files.',
          'Usé metaprogramación en Ruby para interpretar documentos de diseño en XML y generar ejecutables de forma dinámica.'),
    ], history=dict(   # the full story for /timeline/; the Resume keeps the bullets above
        tech=["Ruby", T("Ruby metaprogramming", "Metaprogramación en Ruby"), "XML", T("Custom libraries", "Librerías personalizadas"),
              T("Hardware validation", "Validación de hardware"), T("Automation", "Automatización"), "Git", "CI/CD"],
        facts=[(T("Area", "Área"), T("Hardware validation", "Validación de hardware")),
               (T("Language", "Lenguaje"), "Ruby"),
               (T("Input", "Entrada"), T("XML design documents", "Documentos de diseño en XML")),
               (T("Reach", "Alcance"), T("Intel sites worldwide", "Sedes de Intel en el mundo"))],
        lede=T("Two years at Intel writing <b>custom Ruby libraries</b> for the hardware validation teams. The libraries are what "
               "the teams use to <b>validate all of their chip designs before sending them to real simulation</b>: a design "
               "document in XML goes in, and the executable that checks it comes out, generated on the fly with Ruby "
               "metaprogramming. Around the libraries, the automation that kept them deployed and in sync across Intel's sites "
               "around the world.",
               "Dos años en Intel escribiendo <b>librerías personalizadas en Ruby</b> para los equipos de validación de hardware. "
               "Las librerías son lo que los equipos usan para <b>validar todos sus diseños de chip antes de mandarlos a simulación "
               "real</b>: entra un documento de diseño en XML y sale el ejecutable que lo revisa, generado al vuelo con "
               "metaprogramación en Ruby. Alrededor de las librerías, la automatización que las mantenía desplegadas y sincronizadas "
               "en las sedes de Intel en el mundo."),
        pts=[],
        groups=[
            dict(h=T("Custom Ruby libraries for validation", "Librerías personalizadas en Ruby para validación"), pts=[
                T("The core of the job: <b>libraries written specifically for validation</b>, in Ruby, made for the hardware validation teams rather than taken off the shelf.",
                  "El centro del trabajo: <b>librerías escritas específicamente para validación</b>, en Ruby, hechas para los equipos de validación de hardware y no tomadas de fuera."),
                T("The teams use the library to <b>validate every chip design</b> they produce <b>before it goes to real simulation</b> — a design does not reach the simulator until the library has checked it.",
                  "Los equipos usan la librería para <b>validar todos los diseños de chip</b> que producen <b>antes de mandarlos a simulación real</b>: un diseño no llega al simulador hasta que la librería lo ha revisado."),
                T("Catching a problem at this stage is what makes the library worth it: real simulation is the expensive step, and a design that fails there costs far more than one that fails a check in Ruby.",
                  "Detectar un problema en esta etapa es lo que hace que la librería valga la pena: la simulación real es el paso caro, y un diseño que falla ahí cuesta mucho más que uno que falla una revisión en Ruby."),
                T("Exposed as <b>APIs in Ruby</b> so each team could plug the validation into its own testing workflow.",
                  "Expuestas como <b>APIs en Ruby</b> para que cada equipo pudiera integrar la validación en su propio flujo de pruebas."),
            ]),
            dict(h=T("From XML design documents to executables, with metaprogramming", "De documentos de diseño en XML a ejecutables, con metaprogramación"), pts=[
                T("The chip designs arrived as <b>design documents in XML</b>.",
                  "Los diseños de chip llegaban como <b>documentos de diseño en XML</b>."),
                T("The library parsed those documents and, using <b>Ruby metaprogramming</b>, <b>generated the executable files dynamically</b> from what the document described — the code that validated a design was built from the design itself, not written by hand for each one.",
                  "La librería interpretaba esos documentos y, con <b>metaprogramación en Ruby</b>, <b>generaba los ejecutables de forma dinámica</b> a partir de lo que describía el documento: el código que validaba un diseño se construía desde el diseño mismo, no se escribía a mano para cada uno."),
            ]),
            dict(h=T("Deployment automation across Intel sites", "Automatización de despliegues entre sedes de Intel"), pts=[
                T("The validation teams were spread over <b>several Intel sites around the world</b>, each with its own client environment.",
                  "Los equipos de validación estaban repartidos en <b>varias sedes de Intel en el mundo</b>, cada una con su propio entorno cliente."),
                T("Wrote the <b>automation tools and scripts</b> that synchronized the API deployments with those environments, so every site was running the same version of the libraries.",
                  "Escribí las <b>herramientas y scripts de automatización</b> que sincronizaban los despliegues de las APIs con esos entornos, para que todas las sedes corrieran la misma versión de las librerías."),
            ]),
        ],
        deliverables=[
            dict(kind="milestone", title=T("Moved the project from SVN to Git", "Migración del proyecto de SVN a Git"),
                 role=T("My own initiative — proposed it and carried it through", "Iniciativa mía: la propuse y la llevé a cabo"),
                 tech=["SVN", "Git", "CI/CD"],
                 pts=[T("The project lived in <b>SVN</b>. I put forward the initiative to move it to <b>Git</b> and led the change.",
                        "El proyecto vivía en <b>SVN</b>. Propuse la iniciativa de pasarlo a <b>Git</b> y llevé el cambio."),
                      T("With Git branches, each person could <b>work on several features at the same time</b>, and working together on the same codebase got easier.",
                        "Con las ramas de Git, cada persona podía <b>trabajar en varias funcionalidades al mismo tiempo</b>, y trabajar en conjunto sobre el mismo código se volvió más fácil."),
                      T("The <b>CI/CD</b> built on top of it was <b>simpler and more modern</b> than what SVN allowed.",
                        "El <b>CI/CD</b> construido encima quedó <b>más simple y más moderno</b> que lo que SVN permitía.")],
                 result=T("Easier collaboration on parallel features, and a simplified, modernized CI/CD.",
                          "Colaboración más fácil en funcionalidades en paralelo, y un CI/CD simplificado y modernizado.")),
        ],
    )),
    dict(role=T("3D &amp; Online Programmer", "Programador 3D y Online"), co="Gameloft", tech=["C++", "JavaScript", "jQuery", "Objective-C", "Android", "iOS"], period=T("May 2011 - Jan 2015", "May 2011 - Ene 2015"), frm="2011-05", to="2015-01", inds=[T("Gaming · Mobile", "Videojuegos · Móvil")], loc=MX, cur=False, pts=[
        T('Programmed 3D games and internal development tools using portable <b>C++, JavaScript (jQuery), and Objective-C</b> to ensure seamless cross-platform compatibility across Android and iOS.',
          'Programé juegos 3D y herramientas internas con <b>C++, JavaScript (jQuery) y Objective-C</b> portables, garantizando compatibilidad entre Android e iOS.'),
        T('Integrated proprietary REST-based online services into multiple Android titles.',
          'Integré servicios online propietarios basados en REST en varios títulos de Android.'),
        T('Contributed to the development and release of major mobile titles, including <b>The Oregon Trail: American Settler</b> and <b>9mm</b>.',
          'Participé en el desarrollo y lanzamiento de títulos móviles importantes, entre ellos <b>The Oregon Trail: American Settler</b> y <b>9mm</b>.'),
    ], history=dict(   # /timeline/ only: every shipped project as its own card; the Resume keeps the bullets above
        tech=["C++", "Objective-C", "OpenGL", "Android", "iOS", "Mac OS", "BlackBerry PlayBook", "Unity",
              "JavaScript", "PHP", "jQuery", T("Game servers", "Servidores de juego")],
        deliverables=[
            dict(kind="release", title="The Oregon Trail: American Settler", tech=["C++", "iOS"],
                 role=T("iOS · new features, a Travel mode and community events", "iOS · nuevas funcionalidades, un modo Travel y eventos comunitarios"),
                 pts=[T("Published on <b>iOS</b>. We added new features and a <b>Travel mode</b>.",
                        "Publicado en <b>iOS</b>. Agregamos nuevas funcionalidades y un <b>modo Travel</b>."),
                      T("Added <b>community events</b>: many players take part in a <b>harvest competition</b>, with a <b>leaderboard</b> and prizes.",
                        "Agregamos <b>eventos comunitarios</b>: muchos usuarios participan en una <b>competencia de cosecha</b>, con <b>leaderboard</b> y premios.")],
                 result=T("The community events increased the game's revenue over the following months.",
                          "Los eventos comunitarios incrementaron el revenue del juego en los meses siguientes.")),
            dict(kind="milestone", title=T("Event configuration tool for The Oregon Trail", "Herramienta de configuración de eventos para The Oregon Trail"),
                 tech=["JavaScript", "PHP", "jQuery"],
                 role=T("Internal tool, built by me", "Herramienta interna, hecha por mí"),
                 pts=[T("Built a <b>specialised tool</b> to configure the game's events, in <b>JavaScript</b>, <b>PHP</b> and <b>jQuery</b>.",
                        "Creé una <b>herramienta especializada</b> para configurar los eventos del juego, en <b>JavaScript</b>, <b>PHP</b> y <b>jQuery</b>.")]),
            dict(kind="release", title=T("Spider-Man on the BlackBerry PlayBook", "Spider-Man en la BlackBerry PlayBook"),
                 tech=["C++", "OpenGL", "Android", "BlackBerry PlayBook"],
                 role=T("Port · iOS → Android for the PlayBook", "Port · iOS → Android para la PlayBook"),
                 pts=[T("Took the <b>iOS</b> game and ported it to <b>Android</b> for the <b>PlayBook</b>, in the <b>C++ / OpenGL</b> codebase.",
                        "Tomé el juego de <b>iOS</b> e hice el port a <b>Android</b> para la <b>PlayBook</b>, en el código base de <b>C++ / OpenGL</b>.")]),
            dict(kind="release", title=T("Zombiewood — multiplayer mode", "Zombiewood: modo multijugador"),
                 tech=[T("Game server", "Servidor de juego"), T("Multiplayer", "Multijugador")],
                 role=T("Game server · cooperative play", "Servidor de juego · juego cooperativo"),
                 pts=[T("Implemented a <b>game server</b> for Zombiewood where players fought zombies <b>cooperatively</b>.",
                        "Implementé un <b>game server</b> para Zombiewood donde los jugadores jugaban de manera <b>cooperativa</b> derrotando zombies.")],
                 result=T("Published, and it kept the game alive for one more year.",
                          "Publicado, y mantuvo el juego vivo un año más.")),
            dict(kind="release", title=T("9mm on Mac OS", "9mm en Mac OS"), tech=["C++", "OpenGL", "Mac OS"],
                 role=T("Port · iOS → Mac OS", "Port · iOS → Mac OS"),
                 pts=[T("Ported in <b>C++ / OpenGL</b>; implemented <b>mouse and keyboard</b> controls, <b>joystick</b> support and a new <b>quick-time events</b> system.",
                        "Port en <b>C++ / OpenGL</b>; implementé los controles de <b>mouse y teclado</b>, <b>joystick</b> y un nuevo sistema de <b>quick-time events</b>."),
                      T("Released.", "Publicado.")]),
            dict(kind="release", title=T("Texas Poker — multiplayer server", "Texas Poker: servidor multijugador"),
                 tech=["C++", "Unity", T("Multiplayer", "Multijugador")],
                 role=T("Game server in C++ · Unity client integration", "Servidor de juego en C++ · integración con el cliente en Unity"),
                 pts=[T("Built the <b>multiplayer server</b> in <b>C++</b>. The game was made in <b>Unity</b>; on that side I only integrated the <b>communication with the server</b> for multiplayer.",
                        "Creé el <b>servidor multijugador</b> en <b>C++</b>. El juego estaba hecho en <b>Unity</b>; de ese lado sólo integré la <b>comunicación con el servidor</b> para el multijugador."),
                      T("Released.", "Publicado.")]),
            dict(kind="release", title=T("Disney Cars on Android", "Cars de Disney en Android"), tech=["C++", "Android"],
                 role=T("Port · iOS → Android", "Port · iOS → Android"),
                 pts=[T("Took the <b>iOS</b> Disney Cars game and ported it to <b>Android</b>, in <b>C++</b>. Released.",
                        "Tomé el juego de Cars de Disney de <b>iOS</b> e hice el port a <b>Android</b>, en <b>C++</b>. Publicado.")]),
        ],
    )),
    dict(role=T("Game Developer", "Desarrollador de Videojuegos"), co="Kaxan Games", tech=["C#", "Unity3D", "iOS", "Nintendo Wii"], period=T("Aug 2009 - May 2011", "Ago 2009 - May 2011"), frm="2009-08", to="2011-05", inds=[T("Gaming · Mobile &amp; Console", "Videojuegos · Móvil y Consola")], loc=MX, cur=False, pts=[
        T('Developed and published <b>over five mobile games</b> for iPhone and iPad utilizing C# and Unity3D.',
          'Desarrollé y publiqué <b>más de cinco juegos móviles</b> para iPhone y iPad con C# y Unity3D.'),
        T('Contributed as an additional programmer to a released <b>Nintendo Wii</b> title.',
          'Participé como programador adicional en un título lanzado para <b>Nintendo Wii</b>.'),
        T(f'Showcased development work in a demo reel of five released iOS games ({ext(YT_REEL, "gameplay")}).',
          f'Mostré mi trabajo en un demo reel con cinco juegos de iOS publicados ({ext(YT_REEL, "gameplay")}).'),
    ], history=dict(   # the full story for /timeline/; the Resume keeps the bullets above
        tech=["C#", "Unity 3", "iOS", "Nintendo Wii", "Gamebryo", "Lua", T("Mobile games", "Juegos móviles"), T("Console", "Consola")],
        facts=[(T("Platforms", "Plataformas"), T("iOS · Nintendo Wii")),
               (T("Engines", "Motores"), T("Unity 3 (C#) · Gamebryo (Lua)")),
               (T("Team", "Equipo"), T("Two programmers + a team of artists", "Dos programadores + un equipo de artistas")),
               (T("Shipped", "Publicados"), T("4 iOS games · 1 Wii game", "4 juegos de iOS · 1 juego de Wii"))],
        lede=T("My first job in games, and my first shipped projects. Almost two years at Kaxan Games programming <b>mobile games in "
               "Unity</b> — <b>Taco Master</b>, <b>Bread Boy</b>, <b>Mosca Gogo</b> and <b>Armadillo</b>, all published on <b>iOS</b> — "
               "with one other programmer and a team of artists, on the old Unity 3 and C#. In between, an additional-programmer "
               "credit on a <b>Nintendo Wii</b> title from the <b>El Chavo del 8</b> franchise, and a first stretch on the "
               "<b>Gamebryo</b> engine, scripted in Lua, before the studio moved to Unity.",
               "Mi primer trabajo en videojuegos, y mis primeros proyectos publicados. Casi dos años en Kaxan Games programando "
               "<b>juegos móviles en Unity</b> —<b>Taco Master</b>, <b>Bread Boy</b>, <b>Mosca Gogo</b> y <b>Armadillo</b>, todos "
               "publicados en <b>iOS</b>— con otro programador y un equipo de artistas, en el viejo Unity 3 y C#. En medio, un "
               "crédito como programador adicional en un título de <b>Nintendo Wii</b> de la franquicia de <b>El Chavo del 8</b>, y "
               "una primera etapa con el motor <b>Gamebryo</b>, programado en Lua, antes de que el estudio pasara a Unity."),
        pts=[],
        groups=[
            dict(h=T("Mobile games in Unity", "Juegos móviles en Unity"), pts=[
                T("Programmed <b>mobile games in Unity</b> with <b>C#</b>, on the versions of the time — <b>Unity 3</b> — long before the engine looked the way it does now.",
                  "Programé <b>juegos móviles en Unity</b> con <b>C#</b>, en las versiones de entonces —<b>Unity 3</b>—, mucho antes de que el motor se viera como se ve hoy."),
                T("Each game was built by <b>two programmers</b> — me and one other team member — working with a <b>team of artists</b>.",
                  "Cada juego lo hicimos <b>dos programadores</b> —yo y otro miembro del equipo— trabajando con un <b>equipo de artistas</b>."),
                T("They were my <b>first projects</b>, and it shows: they were not particularly flashy. But every one of them made it through to publication on <b>iOS</b>, and that was the point.",
                  "Fueron mis <b>primeros proyectos</b>, y se nota: no eran especialmente vistosos. Pero todos llegaron a publicarse en <b>iOS</b>, y de eso se trataba."),
                T(f"The five iOS games are in a short demo reel ({ext(YT_REEL, 'gameplay')}).",
                  f"Los cinco juegos de iOS están en un demo reel corto ({ext(YT_REEL, 'gameplay')})."),
            ]),
            dict(h=T("Gamebryo and Lua, before Unity", "Gamebryo y Lua, antes de Unity"), pts=[
                T("The studio started out experimenting with <b>Gamebryo</b>, an engine scripted in <b>Lua</b>, and we received training on it.",
                  "El estudio empezó experimentando con <b>Gamebryo</b>, un motor que se programaba en <b>Lua</b>, y recibimos training para usarlo."),
                T("That was the beginning; the studio then moved to <b>Unity</b>, and the games above were all made there.",
                  "Eso fue el inicio; después el estudio pasó a <b>Unity</b>, y todos los juegos de arriba se hicieron ahí."),
            ]),
            dict(h=T("Training from animation and programming experts", "Training con expertos en animación y programación"), pts=[
                T("Throughout my time at Kaxan we received <b>training from several experts</b> in <b>animation</b> and <b>programming</b> — a big part of how a first job in games turned into a foundation.",
                  "Durante mi estancia en Kaxan recibimos <b>training de varios expertos</b> en <b>animación</b> y <b>programación</b>: una parte importante de cómo un primer trabajo en videojuegos se volvió una base."),
            ]),
        ],
        deliverables=[
            dict(kind="release", title="Taco Master", tech=["Unity 3", "C#", "iOS"],
                 role=T("Mobile game · programmer, one of two", "Juego móvil · programador, uno de dos"),
                 pts=[T("Built in <b>Unity 3</b> with C# by two programmers and a team of artists, and published on <b>iOS</b>.",
                        "Hecho en <b>Unity 3</b> con C# por dos programadores y un equipo de artistas, y publicado en <b>iOS</b>.")]),
            dict(kind="release", title="Bread Boy", tech=["Unity 3", "C#", "iOS"],
                 role=T("Mobile game · programmer, one of two", "Juego móvil · programador, uno de dos"),
                 pts=[T("Built in <b>Unity 3</b> with C# by two programmers and a team of artists, and published on <b>iOS</b>.",
                        "Hecho en <b>Unity 3</b> con C# por dos programadores y un equipo de artistas, y publicado en <b>iOS</b>.")]),
            dict(kind="release", title="Mosca Gogo", tech=["Unity 3", "C#", "iOS"],
                 role=T("Mobile game · programmer, one of two", "Juego móvil · programador, uno de dos"),
                 pts=[T("Built in <b>Unity 3</b> with C# by two programmers and a team of artists, and published on <b>iOS</b>.",
                        "Hecho en <b>Unity 3</b> con C# por dos programadores y un equipo de artistas, y publicado en <b>iOS</b>.")]),
            dict(kind="release", title="Armadillo", tech=["Unity 3", "C#", "iOS"],
                 role=T("Mobile game · programmer, one of two", "Juego móvil · programador, uno de dos"),
                 pts=[T("Built in <b>Unity 3</b> with C# by two programmers and a team of artists, and published on <b>iOS</b>.",
                        "Hecho en <b>Unity 3</b> con C# por dos programadores y un equipo de artistas, y publicado en <b>iOS</b>.")]),
            dict(kind="release", title=T("El Chavo del 8 for Nintendo Wii", "El Chavo del 8 para Nintendo Wii"), tech=["Unity", "C#", "Nintendo Wii"],
                 role=T("Console game · additional programmer", "Juego de consola · programador adicional"),
                 pts=[T("A <b>Nintendo Wii</b> game from the <b>El Chavo del 8</b> franchise, also made in <b>Unity</b>. I contributed as an additional programmer.",
                        "Un juego de <b>Nintendo Wii</b> de la franquicia de <b>El Chavo del 8</b>, hecho también en <b>Unity</b>. Participé como programador adicional."),
                      T("It was published, and it is still playable today if you have a Wii.",
                        "Sí se publicó, y hoy en día se puede jugar si tienes un Wii.")],
                 result=T("A shipped console title, on a franchise everyone in México knows.",
                          "Un título de consola publicado, de una franquicia que todo México conoce.")),
        ],
        links=[(T("Demo reel — five iOS games", "Demo reel: cinco juegos de iOS"), YT_REEL)],
    )),
]

# Core skills on a 1–10 scale: the number drives the bar/percent, the word comes from the band it falls in.
CORE = [("C# / .NET", 10), ("Java / Spring", 9), ("Python / FastAPI", 8), ("JavaScript / Node.js", 6),
        ("AWS", 7), ("SQL / Postgres", 8)]
CORE_MAX = 10
LEVEL_WORDS = [(9, T("Expert", "Experto")), (7, T("Advanced", "Avanzado")), (0, T("Proficient", "Competente"))]
def level(lvl):
    """(word, pct) for a 1–10 level."""
    word = next(w for lo, w in LEVEL_WORDS if lvl >= lo)
    return word, f"{round(100 * lvl / CORE_MAX)}%"
TECH = ["C#", ".NET", "Java", "Spring", "Python", "FastAPI", "JavaScript", "Node.js", "React", "AWS",
        "PostgreSQL", T("Microservices", "Microservicios"), T("RESTful APIs", "APIs RESTful"), T("Unit Testing", "Pruebas unitarias"),
        T("OOP", "POO"), "Unity3D", "Git", "Full-Stack", "Typescript", "Docker"]
AI_HEAD = T("AI-Assisted Dev", "Desarrollo asistido por IA")
AI_TEXT = T("AI-assisted tools in my daily workflow to optimize backend development and accelerate project delivery.",
            "Herramientas asistidas por IA en mi trabajo diario para optimizar el desarrollo backend y acelerar la entrega de proyectos.")
AI_CHIPS = ["Claude Code", "opencode", "Codex"]
TITLES = [
    T(f'<b>The Lullaby of Life</b> — Apple Arcade &amp; {ext(STEAM, "Steam")}'),
    T(f'<b>VR racing games</b> — HTC Vive, Oculus, Gear VR &amp; {ext(YT_VR, "iOS")}',
      f'<b>Juegos de carreras VR</b> — HTC Vive, Oculus, Gear VR e {ext(YT_VR, "iOS")}'),
    T('<b>The Oregon Trail: American Settler</b>, <b>9mm</b> — Gameloft'),
    T(f'<b>5+ iOS games</b> &amp; a Nintendo Wii title — {ext(YT_REEL, "demo reel")}',
      f'<b>5+ juegos de iOS</b> y un título de Nintendo Wii — {ext(YT_REEL, "demo reel")}'),
]
EDU = [(T("Master in Computer Science", "Maestría en Ciencias Computacionales"), T("Universidad Autónoma de Guadalajara · Aug 2018", "Universidad Autónoma de Guadalajara · Ago 2018")),
       (T("Computer Science", "Ciencias Computacionales"), T("Universidad de Guadalajara · Dec 2010", "Universidad de Guadalajara · Dic 2010"))]
STATS = [('<span data-years>15</span>', "+", T("Years building software", "Años de experiencia")),
         ("6", "", T("Max engineers led", "Ingenieros a cargo"))]

# ---- Extended History: newest first, up to TWO levels (an entry may carry `children`: jobs, projects, milestones inside it).
#   This page is meant to be long: unlike the CV sheet, nothing here is trimmed to fit. Give an entry as much
#   structure as the work deserves — a lede, a spec row, and as many titled groups of bullets as it takes.
#   kind:  "job" | "project" | "education" | "milestone" | "release" | "award" | "talk"   (changes the marker on the timeline)
#   frm/to: "YYYY-MM"  (to=None → present; omit `to` for a single-date event; children may omit `frm` entirely)
#   dur:   how long it lasted when there are no exact dates, e.g. T("3 yrs", "3 años") — shown where the date would go
#   facts: [(label, value)] spec row under the title, e.g. [(T("Team", "Equipo"), T("5 engineers", "5 ingenieros"))]
#   lede:  one intro paragraph, the context a reader needs before the bullets
#   pts:   headline bullets (HTML allowed)
#   groups: [dict(h=<section title>, pts=[...])] — the long-form body, one titled group per area of work
#   role:  the position; "" on a child that keeps the parent's (headline is then just the company)
#   tech:  chips, shown inline on the timeline and in the subject panel     inds: industry chips
#   deliverables: [dict(kind="milestone"|"release"|"award"|"pace"|"prototype"|"training", title=…, role=…, pts=[…], result=…, tech=[…])]
#          — a highlighted card for something that stands on its own and can feed the CV later;
#            "pace" is the yellow one: how long it took and the overtime it cost (fast, but not a pace to repeat);
#            "prototype" is the grey dashed one: built, but it never shipped;
#            "training" is the pink one: learning that runs alongside the work (footer reads Now, not Result)
#   links: [(label, href)] external links     children: list of the same dicts (one level only)
#   On a JOBS dict, put all of the above under `history=dict(...)` — the Resume keeps its own pts/tech untouched.
def _job_entry(j):
    e = dict(kind="job", slug=j["co"].lower().replace(" ", "-").replace("&amp;", "and"), role=j["role"], co=j["co"],
             frm=j["frm"], to=j["to"], loc=j["loc"], inds=j["inds"], tech=j.get("tech", []),
             pts=[] if j.get("history_children") else j["pts"], children=j.get("history_children", []))
    e.update(j.get("history", {}))   # long-form fields for /timeline/ only; may also override pts/tech
    return e

def _sorted(entries):
    # newest first; entries without a date keep their written order, after the dated ones
    return sorted(entries, key=lambda e: e.get("frm") or "", reverse=True)

def history_entries():
    """Top-level entries (each may have `children`), newest first."""
    entries = [_job_entry(j) for j in JOBS]
    entries += [
        dict(kind="education", slug="uag-msc", role=EDU[0][0], co="Universidad Autónoma de Guadalajara",
             frm="2018-08", loc=MX, inds=[T("Education", "Educación")],
             tech=["Java", "C++", "JavaScript", "SQL", "C#"],   # what the course projects were written in
             lede=T("Master's degree in Computer Science at the Universidad Autónoma de Guadalajara, completed in August 2018. "
                    "The programme ran from the low level — embedded systems and operating systems — through data, "
                    "mathematics and artificial intelligence, up to mobile programming, systems design and project management; "
                    "the projects delivered along the way were written in <b>Java</b>, <b>C++</b>, <b>JavaScript</b>, <b>SQL</b> and <b>C#</b>.",
                    "Maestría en Ciencias Computacionales en la Universidad Autónoma de Guadalajara, concluida en agosto de 2018. "
                    "El programa fue desde el bajo nivel —sistemas embebidos y sistemas operativos— pasando por datos, "
                    "matemáticas e inteligencia artificial, hasta programación para móviles, diseño de sistemas y gestión de proyectos; "
                    "los proyectos entregados en el camino se escribieron en <b>Java</b>, <b>C++</b>, <b>JavaScript</b>, <b>SQL</b> y <b>C#</b>."),
             pts=[],
             groups=[
                 dict(h=T("Coursework", "Materias"), pts=[
                     T("<b>Embedded systems</b>, <b>operating systems</b> and <b>low-level</b> systems programming.",
                       "<b>Sistemas embebidos</b>, <b>sistemas operativos</b> y programación de sistemas a <b>bajo nivel</b>."),
                     T("<b>Advanced databases</b>.",
                       "<b>Bases de datos avanzadas</b>."),
                     T("<b>Data mining</b>.",
                       "<b>Minería de datos</b>."),
                     T("<b>Mathematics and statistics</b>.",
                       "<b>Matemáticas y estadística</b>."),
                     T("<b>Artificial intelligence</b>.",
                       "<b>Inteligencia artificial</b>."),
                     T("<b>Mobile programming</b>.",
                       "<b>Programación para móviles</b>."),
                     T("<b>Systems design</b>.",
                       "<b>Diseño de sistemas</b>."),
                     T("<b>Project management</b>.",
                       "<b>Gestión de proyectos</b>."),
                 ]),
                 dict(h=T("Course projects", "Proyectos de los cursos"), pts=[
                     T("The projects delivered during the courses were built in <b>Java</b>, <b>C++</b>, <b>JavaScript</b>, <b>SQL</b> and <b>C#</b> — the stack below is theirs.",
                       "Los proyectos entregados durante los cursos se hicieron en <b>Java</b>, <b>C++</b>, <b>JavaScript</b>, <b>SQL</b> y <b>C#</b>; el stack de abajo es el de esos proyectos."),
                 ]),
             ]),
        dict(kind="education", slug="udg-cs", role=EDU[1][0], co="Universidad de Guadalajara",
             frm="2010-12", loc=MX, inds=[T("Education", "Educación")],
             tech=["C", "Java", "C#"],   # the languages the courses were taught in
             lede=T("Computer Science degree at the Universidad de Guadalajara, completed in December 2010. "
                    "The programme started from the ground up — programming in <b>C</b>, data structures, operating systems "
                    "and compilers — and went on to object-oriented programming in <b>Java</b>, software architecture in <b>C#</b> "
                    "and computer graphics, again in <b>C</b>.",
                    "Carrera de Ciencias Computacionales en la Universidad de Guadalajara, concluida en diciembre de 2010. "
                    "El programa partió desde la base —programación en <b>C</b>, estructuras de datos, sistemas operativos "
                    "y compiladores— y siguió con programación orientada a objetos en <b>Java</b>, arquitectura de software en <b>C#</b> "
                    "y gráficos por computadora, de nuevo en <b>C</b>."),
             pts=[],
             groups=[
                 dict(h=T("Coursework", "Materias"), pts=[
                     T("<b>Introduction to programming</b>, in <b>C</b>.",
                       "<b>Introducción a la programación</b>, en <b>C</b>."),
                     T("<b>Object-oriented programming</b>, in <b>Java</b>.",
                       "<b>Programación orientada a objetos</b>, en <b>Java</b>."),
                     T("<b>Software architecture</b>, in <b>C#</b>.",
                       "<b>Arquitectura de software</b>, en <b>C#</b>."),
                     T("<b>Computer graphics</b>, in <b>C</b>.",
                       "<b>Gráficos por computadora</b>, en <b>C</b>."),
                     T("<b>Data structures</b>.",
                       "<b>Estructuras de datos</b>."),
                     T("<b>Operating systems</b>.",
                       "<b>Sistemas operativos</b>."),
                     T("<b>Compilers</b>.",
                       "<b>Compiladores</b>."),
                     T("Among others.",
                       "Entre otras."),
                 ]),
             ]),
    ]
    entries += EXTRA_HISTORY
    for e in entries:
        e["children"] = _sorted(e.get("children", []))
    return _sorted(entries)

def history_flat():
    """Depth-first list used by the page: (index, level, parent_index, entry)."""
    flat = []
    for e in history_entries():
        pi = len(flat); flat.append((pi, 0, None, e))
        for c in e["children"]:
            flat.append((len(flat), 1, pi, c))
    return flat

EXTRA_HISTORY = [
    # dict(kind="milestone", slug="my-talk", role="Speaker at …", co="Conference", frm="2023-05", loc="…", inds=["Community"], tech=[], pts=["…"],
    #      children=[dict(kind="project", slug="my-talk-demo", role="Live demo", co="…", loc="…", inds=[], tech=["Unity"], pts=["…"])]),
]

ICON = {
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "in": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M11 17v-4a2 2 0 0 1 4 0v4"/></svg>',
    "gh": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M9 19c-4.5 1.5-4.5-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/></svg>',
    "ai": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M6 6l2 2M16 16l2 2M18 6l-2 2M8 16l-2 2"/><circle cx="12" cy="12" r="3.5"/></svg>',
}
CONTACT = [
    ("pin", "Zapopan, Jalisco, México", None),
    ("phone", "+52 1 33 1799 1812", "tel:+5213317991812"),
    ("mail", "sergioj.sanchezr@gmail.com", "mailto:sergioj.sanchezr@gmail.com"),
    ("in", "linkedin.com/in/sergiojsanchez", "https://www.linkedin.com/in/sergiojsanchez/"),
    ("gh", "github.com/sergiowero", "https://github.com/sergiowero"),
]

# ------------------------------------------------------------------ BLOCKS
def contact_html():
    out = []
    for ic, text, href in CONTACT:
        inner = f'<a href="{href}"{" target=\"_blank\" rel=\"noopener noreferrer\"" if href and href.startswith("http") else ""}>{text}</a>' if href else text
        out.append(f'<div class="cline">{ICON[ic]}{inner}</div>')
    return "\n".join(out)

def core_html():
    # one markup, many looks: each version shows the bar (.sk-track), the dots (.sk-dots), the word or the percent
    out = []
    for name, lvl in CORE:
        word, pct = level(lvl)
        dots = "".join('<i class="on"></i>' if i < lvl else '<i></i>' for i in range(CORE_MAX))
        out.append(f'<div class="cskill" data-lvl="{lvl}" data-max="{CORE_MAX}"><div class="sk-top"><span class="sk-name">{name}</span>'
                   f'<span class="sk-word">{h(word)}</span><span class="sk-pct">{pct}</span></div>'
                   f'<div class="sk-track"><div class="sk-fill" style="width:{pct}"></div></div><div class="sk-dots">{dots}</div></div>')
    return "\n".join(out)

def chips_html(items, cls="dchip"):
    return '<div class="dchips">' + "".join(f'<span class="{cls}">{h(s)}</span>' for s in items) + '</div>'

def ai_html(with_icon=True):
    ic = ICON["ai"] if with_icon else ""
    return (f'<div class="ai"><div class="h">{ic}{h(AI_HEAD)}</div><p>{h(AI_TEXT)}</p>{chips_html(AI_CHIPS)}</div>')

def titles_html():
    return "\n".join(f'<div class="award">{h(t)}</div>' for t in TITLES)

def edu_html():
    return "\n".join(f'<div class="edu"><div class="d">{h(deg)}</div><div class="m">{h(meta)}</div></div>' for deg, meta in EDU)

BEST_SKILLS = [".NET", "Spring", "Python", "Node.js"]
BEST_LABEL = T("Best skills", "Fortalezas")
BEST_STAT = ('<div class="stat best"><div class="n">' + "".join(f'<span class="bs">{b}</span>' for b in BEST_SKILLS)
             + f'</div><div class="l">{h(BEST_LABEL)}</div></div>')

INDUSTRIES = [T("Gaming", "Videojuegos"), T("Media", "Medios"), T("Enterprise", "Empresa")]
INDUSTRIES_LABEL = T("Industries", "Industrias")
INDUSTRIES_STAT = ('<div class="stat best"><div class="n">' + "".join(f'<span class="bs">{h(b)}</span>' for b in INDUSTRIES)
             + f'</div><div class="l">{h(INDUSTRIES_LABEL)}</div></div>')

def stats_html():
    stat = lambda n, u, l: f'<div class="stat"><div class="n">{n}<span class="u">{u}</span></div><div class="l">{h(l)}</div></div>'
    return '<div class="stats">' + stat(*STATS[0]) + INDUSTRIES_STAT + stat(*STATS[1]) + BEST_STAT + '</div>'

def profile_html():
    return f'<p class="profile">{h(PROFILE)}</p>'

def experience_html():
    out = ['<div class="tl">']
    for j in JOBS:
        out.append(f'<div class="job{" cur" if j["cur"] else ""}">')
        out.append(f'<div class="job-head"><div class="r">{h(j["role"])} · <span class="c">{j["co"]}</span></div><div class="p" data-from="{j["frm"]}"{f' data-to="{j["to"]}"' if j["to"] else ""}>{h(j["period"])}</div></div>')
        inds = "".join(f'<span class="ind">{h(i)}</span>' for i in j["inds"])
        out.append(f'<div class="loc">{h(j["loc"])}<span class="inds">{inds}</span></div>')
        out.append('<ul class="pts">' + "".join(f'<li>{h(p)}</li>' for p in j["pts"]) + '</ul>')
        out.append('</div>')
    out.append('</div>')
    return "\n".join(out)

import json

_MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def _bullets(pts, cls="pts", attrs=""):
    return f'<ul class="{cls}"{attrs}>' + "".join(f"<li>{h(p)}</li>" for p in pts) + "</ul>"

# Every block of an entry (spec row, lede, bullets, each group, each deliverable card, stack, links) is an `.hblock`
# with a bilingual label: the search on /timeline/ folds the blocks a query does not touch into a one-line
# `▸ // label` row (CSS attr()). Groups and cards use their own title; the headless ones use these.
BLOCK_LABELS = {"facts": T("specs", "datos"), "lede": T("summary", "resumen"), "pts": T("highlights", "puntos"),
                "stack": T("stack"), "links": T("links", "enlaces")}
KIND_LABELS = {"job": T("job", "empleo"), "project": T("project", "proyecto"), "education": T("education", "educación"),
               "milestone": T("milestone", "hito"), "release": T("release", "lanzamiento"), "award": T("award", "reconocimiento"),
               "talk": T("talk", "charla")}

def _blk(label):
    """The class + label attributes that make an element a foldable block (see BLOCK_LABELS)."""
    label = label if isinstance(label, T) else T(label)
    attr = lambda s: re.sub(r"<[^>]+>", "", s).replace('"', "&quot;")   # plain text, safe inside the quotes
    return f' data-label-en="{attr(label.en)}" data-label-es="{attr(label.es)}"'

def _hfacts(e):
    """Spec row under the title: key/value pairs, e.g. Team 5 engineers · Cloud AWS."""
    facts = e.get("facts") or []
    return (f'<div class="hfacts mono hblock"{_blk(BLOCK_LABELS["facts"])}>'
            + "".join(f'<span class="hfact"><b>{h(k)}</b>{h(v)}</span>' for k, v in facts)
            + "</div>") if facts else ""

def _hgroups(e):
    """Bullets split into titled sections, so a long entry stays readable."""
    out = [f'<section class="hgroup hblock"{_blk(g["h"])}><h4 class="hg-h mono">{h(g["h"])}</h4>{_bullets(g["pts"])}</section>'
           for g in (e.get("groups") or [])]
    return f'<div class="hgroups">{"".join(out)}</div>' if out else ""

DELIV_BADGE = {"milestone": T("Milestone", "Hito"), "release": T("Release", "Lanzamiento"),
               "award": T("Award", "Reconocimiento"), "pace": T("Pace", "Ritmo"), "prototype": T("Prototype", "Prototipo"),
               "training": T("Training", "Capacitación")}
DELIV_RESULT = T("Result", "Resultado")
DELIV_FOOT = {"training": T("Now", "Ahora")}   # footer label per kind; the rest say Result

def _hdelivs(e):
    """Highlighted cards for the things worth pulling out of an entry: a shipped deliverable, a release, an award —
    or `pace`, the yellow one: how fast it got done and what that cost (overtime), a fact worth showing but not bragging about —
    or `prototype`, the grey dashed one: something built that never shipped —
    or `training`, the pink one: learning that runs alongside the work (its footer says Now instead of Result)."""
    out = []
    for dv in e.get("deliverables") or []:
        kind = dv.get("kind", "milestone")
        role = f'<div class="hd-role">{h(dv["role"])}</div>' if dv.get("role") else ""
        result = (f'<div class="hd-result"><b class="mono">{h(DELIV_FOOT.get(kind, DELIV_RESULT))}</b> {h(dv["result"])}</div>'
                  if dv.get("result") else "")
        chips = ("".join(f'<span class="dchip">{h(t)}</span>' for t in dv.get("tech", [])))
        chips = f'<div class="dchips">{chips}</div>' if chips else ""
        out.append(f'<section class="hdeliv {kind} hblock"{_blk(dv["title"])}><div class="hd-badge mono">{h(DELIV_BADGE[kind])}</div>'
                   f'<h4 class="hd-t">{h(dv["title"])}</h4>{role}{_bullets(dv["pts"])}{result}{chips}</section>')
    return "".join(out)

def _hstack(e):
    """The entry's own tech chips, inline on the timeline (the sticky panel shows them too)."""
    tech = e.get("tech") or []
    return (f'<div class="hstack hblock"{_blk(BLOCK_LABELS["stack"])}><span class="hs-h mono">stack</span><div class="dchips">'
            + "".join(f'<span class="dchip">{h(t)}</span>' for t in tech) + "</div></div>") if tech else ""

def _hlinks(e):
    links = e.get("links") or []
    return (f'<div class="hlinks mono hblock"{_blk(BLOCK_LABELS["links"])}>' + "".join(ext(href, h(label)) for label, href in links) + "</div>") if links else ""

def _hentry_html(i, level, e):
    frm = e.get("frm")
    if not frm:
        when = f'<div class="hdate mono">{h(e["dur"])}</div>' if e.get("dur") else ""
    elif "to" not in e:
        y, m = frm.split("-"); when = f'<div class="hdate mono">{_MONTHS[int(m)-1]} {y}</div>'
    else:
        dur = f'<span class="hdur">{h(e["dur"])}</span>' if e.get("dur") else ""
        when = f'<div class="hdate mono" data-from="{frm}"{f" data-to=\"{e["to"]}\"" if e["to"] else ""}>{frm}</div>{dur}'
    inds = "".join(f'<span class="ind">{h(x)}</span>' for x in e.get("inds", []))
    lede = f'<p class="hlede hblock"{_blk(BLOCK_LABELS["lede"])}>{h(e["lede"])}</p>' if e.get("lede") else ""
    pts = _bullets(e["pts"], "pts hblock", _blk(BLOCK_LABELS["pts"])) if e.get("pts") else ""
    children = ""
    if level == 0 and e.get("children"):
        # indices of children follow the parent in history_flat()
        kids = "".join(_hentry_html(i + 1 + k, 1, c) for k, c in enumerate(e["children"]))
        children = f'<div class="hchildren">{kids}</div>'
    # .hhead is all that stays when the search dims an entry; .hbody holds the foldable blocks; children sit outside both
    return (f'<section class="hentry {e["kind"]}{" child" if level else ""}" id="h-{e["slug"]}" data-i="{i}" data-kind="{e["kind"]}">'
            f'<div class="hhead">{when}<h3>{_htitle(e)}</h3>'
            f'<div class="loc">{h(e.get("loc", ""))}<span class="inds">{inds}</span></div></div>'
            f'<div class="hbody">{_hfacts(e)}{lede}{pts}{_hgroups(e)}{_hdelivs(e)}{_hstack(e)}{_hlinks(e)}</div>{children}</section>')

def _htitle(e):
    """Entry headline: `{role} · {company}`, or the company alone when the role is the parent's (role="")."""
    co = f'<span class="c">{e["co"]}</span>'
    return f'{h(e["role"])} · {co}' if e.get("role") else co

def history_html():
    return "\n".join(_hentry_html(i, 0, e) for i, lvl, parent, e in history_flat() if lvl == 0)

# ---- /timeline/ search: a sticky `grep -i` bar over the timeline column, plus optional facet chips.
# A facet chip only adds its word to the query (or removes it) — the query is the only state, so a link is just ?q=…
SEARCH_LABELS = dict(   # the clear button's label and the placeholder live in the JS (attributes cannot hold both languages)
    filters=T("filters", "filtros"),
    empty=T("no matches", "sin coincidencias"),
    more=T("more", "más"),
    tech=T("tech"), industry=T("industry", "industria"), kind=T("kind", "tipo"),
)
FACET_MIN = 2   # a tech chip is shown up front when this many entries carry it; the rest sit behind "+N more"

def _facet_chips(items, folded=()):
    """`items`: [(T label, count)] → chip buttons carrying the term in both languages (the JS picks the visible one)."""
    def chip(t, hidden):
        t = t if isinstance(t, T) else T(t)
        term = lambda s: re.sub(r"<[^>]+>", "", s).replace('"', "&quot;")
        return (f'<button type="button" class="dchip{" extra" if hidden else ""}" data-term-en="{term(t.en)}" data-term-es="{term(t.es)}">'
                f'{h(t)}</button>')
    return "".join(chip(t, False) for t in items) + "".join(chip(t, True) for t in folded)

def history_search_html():
    flat = history_flat()
    key = lambda t: t.en if isinstance(t, T) else t
    # tech: how many entries carry each chip; the common ones up front, the long tail folded
    seen, count = {}, {}
    for _, _, _, e in flat:
        for t in e.get("tech") or []:
            seen.setdefault(key(t), t); count[key(t)] = count.get(key(t), 0) + 1
    order = sorted(seen, key=lambda k: (-count[k], k.lower()))
    top = [seen[k] for k in order if count[k] >= FACET_MIN]
    rest = [seen[k] for k in order if count[k] < FACET_MIN]
    # industry: "Gaming · Mobile" is two atoms, each searchable on its own
    inds = {}
    for _, _, _, e in flat:
        for t in e.get("inds") or []:
            t = t if isinstance(t, T) else T(t)
            for en, es in zip(t.en.split(" · "), t.es.split(" · ")):
                inds.setdefault(en, T(en, es))
    kinds = []
    for _, _, _, e in flat:
        if KIND_LABELS[e["kind"]] not in kinds: kinds.append(KIND_LABELS[e["kind"]])
    L = {k: h(v) for k, v in SEARCH_LABELS.items()}
    more = f'<button type="button" class="hq-morechips mono">+{len(rest)} {L["more"]}</button>' if rest else ""
    facet = lambda name, chips: f'<div class="hq-facet"><span class="hq-fh mono">// {L[name]}</span><div class="dchips">{chips}</div></div>'
    return (f'<div class="hq" role="search">'
            f'<div class="hq-row">'
            f'<label class="hq-prompt mono" for="hq-in"><span class="g">➜</span> <span class="c">~</span> grep -i</label>'
            f'<span class="hq-field"><input class="hq-in mono" id="hq-in" type="text" inputmode="search" enterkeyhint="search" autocomplete="off" spellcheck="false" placeholder="lead · aws · 2021 · unity…">'
            f'<button type="button" class="hq-x mono" aria-label="Clear search" hidden>×</button></span>'
            f'<span class="hq-count mono" aria-live="polite"></span>'
            f'<button type="button" class="hq-more mono" aria-expanded="false" aria-controls="hq-facets">// {L["filters"]} <i>▸</i></button>'
            f'</div>'
            f'<div class="hq-facets" id="hq-facets" hidden>{facet("tech", _facet_chips(top, rest) + more)}{facet("industry", _facet_chips(inds.values()))}{facet("kind", _facet_chips(kinds))}</div>'
            f'<div class="hq-empty mono" hidden>// {L["empty"]}</div>'
            f'</div>')

ROLE_PLAIN = T("Senior Software Engineer / Tech Lead / Backend &amp; Full-Stack / Game Dev / AI-Assisted",
               "Ingeniero de Software Senior / Tech Lead / Backend y Full-Stack / Videojuegos / Asistido por IA")
# The headings the DOCX uses and that @media print swaps in for the shell commands (see sh_label).
# Wording is deliberately the canonical one resume parsers look for — "Professional Summary",
# "Work Experience", "Skills", "Projects", "Education" — not the site's own section names.
DOC_LABELS = {
    "profile": T("Professional Summary", "Resumen profesional"),
    "experience": T("Work Experience", "Experiencia laboral"),
    "core": T("Skills", "Habilidades"),
    "tech": T("Technical Skills", "Habilidades técnicas"),
    "titles": T("Projects", "Proyectos"),
    "education": T("Education", "Educación"),
    "present": T("Present", "Actualidad"),
    "yr": T(" yr", " año"), "yrs": T(" yrs", " años"), "mo": T(" mo", " mes"), "mos": T(" mos", " meses"),
}

def cv_data_json():
    """Everything the in-browser DOCX writer needs, in both languages. Same source as the page itself."""
    data = dict(
        name=NAME, role=d(ROLE_PLAIN), site="sergiowero.github.io",
        contact=[dict(text=text, href=href) for _, text, href in CONTACT],
        profile=d(PROFILE),
        jobs=[dict(role=d(j["role"]), co=j["co"], frm=j["frm"], to=j["to"],
                   loc=d(j["loc"]), inds=d(j["inds"]), pts=d(j["pts"])) for j in JOBS],
        core=[dict(name=name, word=d(level(lvl)[0]), pct=level(lvl)[1]) for name, lvl in CORE],
        tech=d(TECH), titles=d(TITLES),
        ai=dict(head=d(AI_HEAD), text=d(AI_TEXT), chips=AI_CHIPS),
        edu=[dict(deg=d(deg), meta=d(meta)) for deg, meta in EDU],
        labels={k: d(v) for k, v in DOC_LABELS.items()},
        months=dict(en=_MONTHS, es=["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]),
    )
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

def cv_data_html():
    return (f'<script type="application/json" id="cv-data">{cv_data_json()}</script>\n'
            '<script src="/cv-export.js" defer></script>')

def history_json():
    data = [dict(kind=e["kind"], kind_label=d(KIND_LABELS[e["kind"]]), slug=e["slug"], role=d(e["role"]), co=e["co"], frm=e.get("frm"), dur=d(e.get("dur")),
                 to=("single" if "to" not in e else e["to"]), loc=d(e.get("loc", "")), inds=d(e.get("inds", [])), tech=d(e.get("tech", [])),
                 level=lvl, parent=parent) for i, lvl, parent, e in history_flat()]
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

FIT_JS = """<script>
/* window.cvLang() is defined in <head>; anything rendered from JS redraws on the 'langchange' event below */
/* Years of experience, computed from the year I started working */
(function(){
  var START_YEAR=2010;
  var years=new Date().getFullYear()-START_YEAR;
  document.querySelectorAll('[data-years]').forEach(function(el){el.textContent=years;});
})();
/* Job dates rendered from data-from / data-to (YYYY-MM; no data-to = present): "Mar 2020 - Present · 6 yrs 8 mos" */
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
    el.textContent=label(a)+' - '+(toAttr?label(b):w.present);   // plain hyphen: resume parsers' date regexes expect it
    var d=document.createElement('span'); d.className='dur'; d.textContent=' \u00b7 '+parts.join(' ');
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
</script>"""

BASE_CSS = """*{margin:0;padding:0;box-sizing:border-box;}
  html{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  @page{size:A4;margin:0;}
  a{text-decoration:none;color:inherit;}
  .sheet{width:210mm;min-height:297mm;margin:0 auto;position:relative;overflow:hidden;}
  .cline svg,.ai .h svg{width:13px;height:13px;flex:none;}
  .p .dur{font-weight:400;opacity:.85;}
  .sk-top{display:flex;justify-content:space-between;align-items:baseline;gap:6px;}
  .stat.best{flex:1.35;}
  .stat.best .n{font-size:10.5px;line-height:1.25;letter-spacing:0;}
  .stat.best .bs+.bs::before{content:" · ";}
  .inds{display:inline-flex;flex-wrap:wrap;gap:3px;margin-left:6px;vertical-align:middle;}
  .ind{display:inline-block;font-size:7.3px;line-height:1.35;padding:1px 6px;border-radius:3px;font-weight:600;white-space:nowrap;}
  .sk-pct,.sk-dots{display:none;}
  @media screen{
    body{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;padding:clamp(12px,3vw,44px);}
    .sheet{flex:none;box-shadow:0 30px 80px -22px rgba(0,0,0,.6),0 10px 26px rgba(0,0,0,.35);border-radius:14px;}
  }
  /* site header, embedded as the top strip of the sheet (visual only for now) */
  .site-nav{display:flex;align-items:center;justify-content:flex-end;gap:8px;padding:7px 12mm;color:var(--nav-fg);font-family:var(--nav-font,inherit);}
  .site-nav .tabs{display:flex;gap:2px;}
  .site-nav .tab{padding:4px 7px;border-radius:6px;font-size:8.4px;font-weight:500;color:var(--nav-muted);cursor:default;user-select:none;letter-spacing:.2px;white-space:nowrap;}
  .site-nav .tab.active{background:var(--nav-active-bg);color:var(--nav-active-fg);font-weight:700;}
  .site-nav a.tab{cursor:pointer;} .site-nav .tab:hover:not(.active){color:var(--nav-fg);}
  html[data-lang="es"] .i18n-en{display:none !important;} html:not([data-lang="es"]) .i18n-es{display:none !important;}
  .site-nav .grp{display:flex;align-items:center;gap:1px;}
  .site-nav .grp .tab{padding:4px 6px;cursor:pointer;}
  .site-nav .grp .slash{color:var(--nav-muted);font-size:8.6px;opacity:.6;padding:0 1px;}
  .site-nav .grp .tab svg{width:10px;height:10px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;vertical-align:-1.5px;margin-right:3px;}
  .site-nav .theme .tab{padding:4px 5px;} .site-nav .theme .tab svg{width:11px;height:11px;margin-right:0;vertical-align:-2px;}
  /* one button: the sun in light mode, the moon in dark mode (html[data-theme] is set before paint, see <head>) */
  .site-nav .theme button.tab{background:none;border:0;font:inherit;line-height:inherit;color:var(--nav-muted);}
  .site-nav .theme .moon{display:none;} :root[data-theme="dark"] .site-nav .theme .sun{display:none;} :root[data-theme="dark"] .site-nav .theme .moon{display:inline;}
  /* download the CV: fixed to the viewport so it never shrinks with the sheet (see public/cv-export.js) */
  .dl-fab{position:fixed;right:18px;bottom:18px;z-index:40;display:flex;align-items:center;gap:8px;font-family:var(--nav-font,inherit);}
  .dl-fab .dl-k{font-size:11px;color:var(--nav-muted);margin-right:2px;}
  .dl-fab .dl-k::before{content:"// ";opacity:.7;}
  .dl-fab button{display:inline-flex;align-items:center;gap:6px;font:inherit;font-size:12.5px;font-weight:700;letter-spacing:.3px;
    padding:11px 15px;border-radius:999px;border:0;cursor:pointer;background:var(--nav-active-bg);color:var(--nav-active-fg);
    box-shadow:0 12px 28px -8px rgba(0,0,0,.6),0 2px 6px rgba(0,0,0,.25);transition:transform .12s,filter .12s;}
  .dl-fab button.alt{background:transparent;color:var(--nav-active-bg);box-shadow:none;
    border:1.5px solid var(--nav-active-bg);padding:9.5px 13.5px;}
  .dl-fab button:hover{transform:translateY(-1px);filter:brightness(1.08);}
  .dl-fab button svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;}
  @media (max-width:600px){.dl-fab{right:12px;bottom:12px;} .dl-fab .dl-k{display:none;}}
  /* section headings carry both skins (see sh_label): the shell command for the screen, a plain heading for print */
  h2.sh .ats{display:none;}
  @media print{
    .sheet{zoom:1 !important;box-shadow:none !important;border-radius:0 !important;}
    .site-nav,.dl-fab{display:none !important;}
    /* ATS pass: no shell decoration reaches the PDF — plain headings, no prompts, no ASCII meters */
    h2.sh .cmd{display:none;} h2.sh .ats{display:inline;}
    h2.sh::before,h2.sh::after{content:none !important;}
    .prompt,.foot{display:none !important;}
    .name .cur{display:none;}
  }"""

FLAG_MX = '<svg viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M8.7 5v14M15.3 5v14"/><circle cx="12" cy="12" r="1.6"/></svg>'
FLAG_US = '<svg viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 12h20M11 8.5h11M11 15.5H2M2 12v7"/><path d="M2 12h9V5"/></svg>'
SECTIONS = [("cv", "/", "Resume", "Currículum"), ("history", "/timeline/", "Timeline", "Mi línea de tiempo"),
            ("blog", "/blog/", "Blog", "Blog"), ("about", "/about/", "About me", "Sobre mí")]

HL = '<span class="hl">/</span>'

def sh_label(cmd, ats):
    """A section heading in two skins: the shell command on screen, a plain heading when printing.
       CSS swaps them in @media print, so a PDF (and any ATS reading it) never sees `cat profile.md`."""
    return f'<span class="cmd">{h(cmd)}</span><span class="ats">{h(ats)}</span>'

LABELS = {
    # the first role is the headline one: it gets the green, the rest stay muted
    "$L_SUB$": T(f'<span class="r0">Senior Software Engineer</span> {HL} Tech Lead {HL} Backend &amp; Full-Stack {HL} Game Dev {HL} AI-Assisted',
                 f'<span class="r0">Ingeniero de Software Senior</span> {HL} Tech Lead {HL} Backend y Full-Stack {HL} Videojuegos {HL} Asistido por IA'),
    "$L_PROFILE$": sh_label(T("cat profile.md", "cat perfil.md"), DOC_LABELS["profile"]),
    "$L_EXP$": sh_label(T("cat experience.log", "cat experiencia.log"), DOC_LABELS["experience"]),
    "$L_CORE$": sh_label(T("ls core-skills/", "ls habilidades/"), DOC_LABELS["core"]),
    "$L_TECH$": sh_label(T("ls tech/"), DOC_LABELS["tech"]),
    "$L_SHIPPED$": sh_label(T("cat shipped.txt", "cat lanzamientos.txt"), DOC_LABELS["titles"]),
    "$L_EDU$": sh_label(T("cat education.txt", "cat educacion.txt"), DOC_LABELS["education"]),
    "$L_ABOUT$": sh_label(T("cat about.md", "cat sobre-mi.md"), T("About", "Sobre mí")),
    "$L_TOOLBOX$": sh_label(T("ls toolbox/", "ls herramientas/"), T("Toolbox", "Herramientas")),
    "$L_CONTACT$": sh_label(T("cat contact.md", "cat contacto.md"), T("Contact", "Contacto")),
    "$L_CVFILE$": T("cv.md"),
    "$L_HISTFILE$": T("timeline.md"),
}

DL_ICON = '<svg viewBox="0 0 24 24"><path d="M12 3v11M7.5 10.5 12 15l4.5-4.5M4 20h16"/></svg>'
# Fixed to the viewport, outside the sheet, so it keeps its size on every screen (the sheet is CSS-zoomed);
# display:none when printing, so it never reaches the PDF.
# DOCX leads and PDF is the outlined secondary: the Word file is one column with plain headings,
# real bullets and live hyperlinks, so it is the one that survives an applicant tracking system intact.
DOWNLOAD_TPL = ('<div class="dl-fab" role="group" aria-label="Download CV / Descargar CV">'
                f'<span class="dl-k">{i18n("download", "descargar")}</span>'
                f'<button type="button" data-export="docx">{DL_ICON}DOCX</button>'
                f'<button type="button" class="alt" data-export="pdf">{DL_ICON}PDF</button></div>')

def nav_html(active="cv"):
    tabs = "".join(
        f'\n    <a class="tab{" active" if key == active else ""}" href="{href}"{" aria-current=\"page\"" if key == active else ""}>{i18n(en, es)}</a>'
        for key, href, en, es in SECTIONS)
    return NAV_TPL.replace("$TABS$", tabs)

NAV_TPL = """<header class="site-nav" aria-label="Site sections">
  <nav class="tabs">$TABS$
  </nav>
  <div class="grp lang" aria-label="Language (visual only)"><span class="tab" data-lang="es">$FLAG_ES$ES</span><span class="slash">/</span><span class="tab active" data-lang="en">$FLAG_EN$EN</span></div>
  <div class="grp theme" aria-label="Theme"><button class="tab" type="button" data-toggle-theme title="Toggle theme" aria-label="Toggle theme"><svg class="sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><svg class="moon" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button></div>
</header>"""

def page(title, fonts, css, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>(function(){{try{{var d=document.documentElement;if(localStorage.getItem('cv-theme')==='dark')d.setAttribute('data-theme','dark');if(localStorage.getItem('cv-lang')==='es')d.setAttribute('data-lang','es');}}catch(e){{}}}})();
window.cvLang=function(){{return document.documentElement.getAttribute('data-lang')==='es'?'es':'en';}};</script>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>{title}</title>
<meta name="description" content="Sergio de Jesús Sánchez Robles — Senior Software Engineer / Tech Lead. 15 years across gaming, media and enterprise.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
<style>
  {BASE_CSS}
{css}
</style>
</head>
<body>
{body}
{FIT_JS}
</body>
</html>
"""

def fill(tpl, active="cv"):
    for key, label in LABELS.items():
        tpl = tpl.replace(key, h(label))
    return (tpl.replace("$NAV$", nav_html(active)).replace("$CVDATA$", cv_data_html())
            .replace("$DOWNLOAD$", DOWNLOAD_TPL if active == "cv" else "").replace("$HISTORY_JSON$", history_json()).replace("$HISTORY$", history_html()).replace("$HSEARCH$", history_search_html())
            .replace("$I18N_HISTORY_TITLE$", i18n("Timeline", "Mi línea de tiempo"))
            .replace("$I18N_HISTORY_SUB$", i18n("All the projects I have worked on so far, newest first — scroll and the panel on the right follows.", "Todos los proyectos en los que he trabajado hasta ahora, de lo más reciente a lo más antiguo — al hacer scroll, el panel derecho te sigue.")).replace("$CONTACT$", contact_html()).replace("$CORE$", core_html())
            .replace("$TECH$", chips_html(TECH)).replace("$AI$", ai_html()).replace("$AI_NOICON$", ai_html(False))
            .replace("$TITLES$", titles_html()).replace("$EDU$", edu_html()).replace("$STATS$", stats_html())
            .replace("$PROFILE$", profile_html()).replace("$EXP$", experience_html())
            .replace("$ABOUT_BIO$", i18n(ABOUT_BIO_EN, ABOUT_BIO_ES)).replace("$TOOLBOX$", toolbox_html())
            .replace("$NAME$", NAME).replace("$ROLE$", ROLE).replace("$TAG$", TAG))

VERSIONS = {}

# =================================================================== v2 EDITORIAL SERIF (A4)
VERSIONS["v2-editorial-serif.html"] = dict(
    nav="--nav-bg:#f2ede3;--nav-line:#dcd5c7;--nav-fg:#1c1a17;--nav-muted:#8a847a;--nav-active-bg:#b8321f;--nav-active-fg:#fff;",
    title="Sergio Sanchez CV",
    fonts="family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600",
    css="""
  :root{--paper:#faf7f1;--ink:#1c1a17;--body:#4a463f;--muted:#8a847a;--line:#dcd5c7;--accent:#b8321f;--accent-soft:#f3dcd6;}
  body{font-family:'Inter',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:var(--paper);}
  .serif{font-family:'Fraunces','Iowan Old Style',Georgia,serif;}
  .sheet{background:var(--paper);padding:12mm 13mm 8mm;display:flex;flex-direction:column;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#3b2a25 0%,#1f1613 50%,#120d0b 100%);}}

  .site-nav{margin:-12mm -13mm 7mm;padding-left:13mm;padding-right:13mm;}
  .top{display:flex;justify-content:space-between;align-items:flex-end;gap:10mm;border-bottom:1.5px solid var(--ink);padding-bottom:8px;}
  .kicker{font-size:8px;letter-spacing:2.2px;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:6px;}
  .name{font-family:'Fraunces',Georgia,serif;font-size:31px;font-weight:600;letter-spacing:-.8px;line-height:1;color:var(--ink);}
  .name em{font-style:italic;font-weight:400;color:var(--accent);}
  .tag{font-size:9px;color:var(--muted);margin-top:6px;}
  .contact{display:grid;gap:4px;flex:none;}
  .cline{display:flex;align-items:center;gap:6px;font-size:8.6px;color:var(--body);}
  .cline svg{stroke:var(--accent);width:11px;height:11px;}

  .stats{display:flex;margin:6px 0 8px;border-bottom:1px solid var(--line);}
  .stat{flex:1;padding:6px 10px 8px 0;border-right:1px solid var(--line);margin-right:10px;}
  .stat:last-child{border-right:0;margin-right:0;}
  .stat .n{font-family:'Fraunces',Georgia,serif;font-size:22px;font-weight:600;color:var(--ink);line-height:1;letter-spacing:-.5px;}
  .stat .n .u{color:var(--accent);}
  .stat .l{font-size:7.6px;text-transform:uppercase;letter-spacing:1.1px;color:var(--muted);margin-top:4px;font-weight:500;}

  .cols{display:flex;gap:8mm;flex:1;}
  .main{flex:1 1 auto;min-width:0;}
  .aside{flex:0 0 52mm;}
  h2.sh{font-size:8.6px;letter-spacing:2px;text-transform:uppercase;color:var(--ink);font-weight:600;margin-bottom:7px;display:flex;align-items:center;gap:8px;}
  h2.sh::after{content:"";flex:1;height:1px;background:var(--line);}
  section{margin-bottom:9px;}

  .profile{font-size:9.6px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--ink);font-weight:600;}

  .job{display:grid;grid-template-columns:1fr;padding:5px 0 3px;border-top:1px solid var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-family:'Fraunces',Georgia,serif;font-size:12px;font-weight:600;color:var(--ink);}
  .job .c{color:var(--accent);font-style:italic;font-weight:400;}
  .job .p{font-size:8.2px;color:var(--muted);font-weight:500;white-space:nowrap;flex:none;}
  .job.cur .p::after{content:"· Current";color:var(--accent);margin-left:4px;font-weight:600;}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"—";position:absolute;left:0;color:var(--accent);}
  .ind{font-size:6.8px;letter-spacing:1px;text-transform:uppercase;font-weight:600;color:var(--accent);border:1px solid var(--accent-soft);background:#fff;border-radius:2px;padding:1px 5px;}
  ul.pts li b{color:var(--ink);font-weight:600;}
  ul.pts li a{color:var(--accent);font-weight:600;}
  .stack{color:var(--muted);}

  .cskill{padding:3px 0 5px;}
  .sk-top{font-size:9.3px;color:var(--ink);}
  .sk-word{font-family:'Fraunces',Georgia,serif;font-style:italic;color:var(--accent);font-size:8.6px;}
  .sk-track{height:1px;background:var(--line);margin-top:5px;}
  .sk-fill{height:2px;margin-top:-.5px;background:var(--ink);position:relative;}
  .sk-fill::after{content:"";position:absolute;right:-2px;top:-2px;width:6px;height:6px;border-radius:50%;background:var(--accent);}
  .ai{background:var(--ink);color:var(--paper);padding:10px 11px;border-radius:3px;}
  .ai .h{font-size:8px;letter-spacing:1.6px;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:var(--accent);}
  .ai p{font-size:8.8px;line-height:1.45;color:#d9d3c7;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:500;padding:2px 7px;border-radius:20px;border:1px solid var(--line);color:var(--ink);background:#fff;}
  .ai .dchip{background:transparent;border-color:rgba(255,255,255,.3);color:var(--paper);}
  .award{font-size:8.8px;color:var(--body);padding:3px 0;border-bottom:1px dotted var(--line);line-height:1.35;}
  .award:last-child{border-bottom:0;}
  .award b{color:var(--ink);font-weight:600;}
  .award a{color:var(--accent);}
  .edu{padding:3px 0;border-bottom:1px dotted var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-family:'Fraunces',Georgia,serif;font-size:10.5px;font-weight:600;color:var(--ink);}
  .edu .m{font-size:8.4px;color:var(--muted);}
  .foot{margin-top:auto;padding-top:6px;border-top:1px solid var(--line);font-size:7.6px;color:var(--muted);display:flex;justify-content:space-between;}
""",
    body="""<div class="sheet">
  $NAV$
  <header class="top">
    <div>
      <div class="kicker">$ROLE$ · Zapopan, México</div>
      <div class="name">Sergio de Jesús Sánchez <em>Robles</em></div>
      <div class="tag">$TAG$</div>
    </div>
    <div class="contact">$CONTACT$</div>
  </header>
  $STATS$
  <div class="cols">
    <main class="main">
      <section><h2 class="sh">Profile</h2>$PROFILE$</section>
      <section><h2 class="sh">Experience</h2>$EXP$</section>
    </main>
    <aside class="aside">
      <section>$AI$</section>
      <section><h2 class="sh">Core Skills</h2>$CORE$</section>
      <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
      <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
      <section><h2 class="sh">Education</h2>$EDU$</section>
    </aside>
  </div>
  <div class="foot"><span>$NAME$</span><span>sergiowero.github.io</span></div>
</div>""")

# =================================================================== v3 DARK TERMINAL (A4)
VERSIONS["v3-dark-terminal.html"] = dict(
    flags=True,
    nav="--nav-bg:transparent;--nav-line:transparent;--nav-fg:#1f2328;--nav-muted:#6e7781;--nav-active-bg:#1a7f37;--nav-active-fg:#fff;--nav-font:'JetBrains Mono',Menlo,monospace;",
    title="Sergio Sanchez CV",
    extra_js="""<script>
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
    return label(e.frm)+' - '+(e.to?label(e.to):w().present)+' · '+parts.join(' ');
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
  var TOK=/"([^"]*)"|(\\S+)/g, YEAR=/^([0-9]{4})(?:-([0-9]{4}))?$/;
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
  function textOf(el){ return textNodes(el).map(function(n){return n.nodeValue;}).join(' ').replace(/\\s+/g,' '); }
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
    if(!found) parts.push(/\\s/.test(t)?'"'+t+'"':t);
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
</script>
<script>
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
</script>
<script>
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
</script>
<script>
/* Typewriter effect on the name (skipped when the user prefers reduced motion or when printing) */
(function(){
  var el=document.getElementById('typed'); if(!el) return;
  if(window.matchMedia&&(window.matchMedia('(prefers-reduced-motion: reduce)').matches||window.matchMedia('print').matches)) return;
  /* a bilingual title holds one span per language (CSS shows one): type each on its own */
  var els=el.querySelectorAll('.i18n-en,.i18n-es'); if(!els.length) els=[el];
  var done=[];
  Array.prototype.forEach.call(els,function(t){
    var full=t.textContent; t.textContent=''; var i=0;
    done.push(function(){ t.textContent=full; });
    (function tick(){ if(i<=full.length){ t.textContent=full.slice(0,i++); setTimeout(tick,i<8?90:45);} })();
  });
  /* printing mid-animation would put a half-typed name in the PDF: finish it first */
  window.addEventListener('beforeprint',function(){ done.forEach(function(f){f();}); });
})();
</script>""",
    fonts="family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700",
    css="""
  /* light mode is the default */
  :root{--bg:#f6f8fa;--panel:#fff;--line:#d0d7de;--text:#1f2328;--muted:#6e7781;--green:#1a7f37;--cyan:#0969da;--amber:#9a6700;--pink:#bf3989;--fg:#0b1220;--body-text:#3d444d;--empty:#d8dee4;}
  /* dark mode (toggled from the header) */
  :root[data-theme="dark"]{--bg:#0b0f14;--panel:#141b23;--line:#1f2a35;--text:#d6dde6;--muted:#7d8a99;--green:#3ddc84;--cyan:#4cc9f0;--amber:#ffb454;--pink:#ff6b9d;--fg:#fff;--body-text:#b9c3cf;--empty:#33414f;
    --nav-fg:#d6dde6;--nav-muted:#7d8a99;--nav-active-bg:#3ddc84;--nav-active-fg:#06130c;}
  @media screen{:root[data-theme="dark"] body{background:radial-gradient(900px 500px at 50% -10%,#0f1f1a 0%,#070a0d 55%,#000 100%);}}
  /* ---- Extended History: timeline + sticky "subject" panel ---- */
  .sheet.hist-page{overflow:visible;}   /* overflow:hidden on the sheet would defeat position:sticky */
  .hist{display:flex;gap:7mm;margin-top:8px;align-items:flex-start;}
  .hcol{flex:1 1 auto;min-width:0;}
  .htl{position:relative;padding-left:16px;padding-bottom:22vh;}
  .htl::before{content:"";position:absolute;left:4px;top:6px;bottom:6px;width:2px;background:var(--line);border-radius:2px;}
  .hentry{position:relative;padding:6px 0 10px;scroll-margin-top:60px;}
  .htl .hentry.job{border-top:0;}
  /* Markers sit centred on the rail. The rail's centre is 11px left of an entry's content edge
     (.htl padding 16px, line at 4px + 1px) and 14.5px left of a child's (.hchildren border 1px + padding 14px).
     `*{box-sizing}` does not reach pseudo-elements, so each marker sets border-box and its outer size in --mk;
     `left` is then derived from --mk, which keeps every kind on the rail. */
  .hentry::before{content:"";position:absolute;box-sizing:border-box;--mk:14px;width:var(--mk);height:var(--mk);left:calc(-11px - var(--mk) / 2);top:9px;
    border-radius:50%;background:var(--bg);border:2px solid var(--muted);transition:.25s;}
  .hentry.active::before{border-color:var(--green);background:var(--green);box-shadow:0 0 0 4px rgba(61,220,132,.18);}
  .hentry.education::before{border-radius:2px;transform:rotate(45deg);}
  .hentry.project::before{border-radius:2px;--mk:12px;top:10px;}
  .hentry.milestone::before{border-radius:50% 50% 50% 0;transform:rotate(-45deg);}
  .hentry.release::before{border-radius:2px;--mk:16px;height:11px;top:11px;}
  .hentry.award::before{border:0;--mk:10px;background:var(--muted);clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);}
  .hentry.award.active::before{background:var(--green);box-shadow:none;}
  .hentry.talk::before{border-radius:4px 4px 4px 0;}
  .hchildren{margin:4px 0 0;padding-left:14px;border-left:1px dashed var(--line);}
  .hentry.child{padding:5px 0 6px;}
  .hentry.child::before{--mk:11px;left:calc(-14.5px - var(--mk) / 2);top:9px;}
  .hentry.child.project::before{--mk:10px;top:10px;}
  .hentry.child.award::before{--mk:7px;}
  .hentry.child h3{font-size:10.5px;}
  .hentry.child .hdate{font-size:7.6px;}
  .hentry.parent-active > .hhead h3 .c{color:var(--green);}
  .sub-parent{font-size:8px;color:var(--muted);margin-top:6px;} .sub-parent:empty{display:none;}
  .sub-parent b{color:var(--cyan);font-weight:600;}
  .sub-nav ol{list-style:none;margin:0;padding-left:10px;border-left:1px dashed var(--line);}
  .sub-nav ol li{font-size:7.9px;padding:1px 0 1px 10px;}
  .sub-nav ol li::before{width:4px;height:4px;top:6px;}
  .hdate{font-size:8px;color:var(--muted);}
  .hentry.active .hdate{color:var(--green);}
  .hdur{font-family:'JetBrains Mono',monospace;font-size:7.6px;color:var(--muted);}
  /* the long-form blocks of an entry: spec row, lede, titled groups, stack chips, links */
  .hfacts{display:flex;flex-wrap:wrap;gap:3px 10px;margin-top:4px;font-size:7.6px;color:var(--text);}
  .hfact b{color:var(--muted);font-weight:500;text-transform:uppercase;letter-spacing:1px;margin-right:5px;}
  .hfact+.hfact{padding-left:10px;border-left:1px solid var(--line);}
  .hlede{font-size:9.1px;line-height:1.45;color:var(--body-text);margin-top:5px;}
  .hgroups{margin-top:6px;display:grid;gap:6px;}
  .hgroup{position:relative;padding-left:9px;}
  .hgroup::before{content:"";position:absolute;left:0;top:3px;bottom:2px;width:2px;border-radius:2px;background:var(--line);}
  .hentry.active .hgroup::before{background:rgba(61,220,132,.35);}
  .hg-h{font-size:7.6px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:var(--cyan);}
  .hg-h::before{content:"// ";color:var(--muted);font-weight:400;}
  .hgroup ul.pts{margin-top:2px;}
  /* deliverable card: the achievement pulled out of an entry */
  .hdeliv{position:relative;margin-top:8px;padding:8px 10px 9px;border-radius:9px;
    border:1px solid rgba(61,220,132,.38);background:linear-gradient(160deg,rgba(61,220,132,.10),rgba(76,201,240,.06));}
  .hdeliv.release{border-color:rgba(76,201,240,.4);background:linear-gradient(160deg,rgba(76,201,240,.10),rgba(61,220,132,.05));}
  .hdeliv.award{border-color:rgba(255,180,84,.45);background:linear-gradient(160deg,rgba(255,180,84,.12),rgba(255,107,157,.05));}
  .hdeliv.pace{border-color:rgba(255,214,0,.6);background:linear-gradient(160deg,rgba(255,214,0,.17),rgba(255,180,84,.05));}
  .hdeliv.prototype{border-style:dashed;border-color:rgba(125,138,153,.55);background:linear-gradient(160deg,rgba(125,138,153,.10),rgba(125,138,153,.03));}
  .hdeliv.training{border-color:rgba(255,107,157,.5);background:linear-gradient(160deg,rgba(255,107,157,.13),rgba(124,77,255,.06));}
  .hd-badge{display:inline-block;font-size:6.8px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;
    color:var(--green);border:1px solid rgba(61,220,132,.45);border-radius:3px;padding:1px 5px;}
  .hdeliv.release .hd-badge{color:var(--cyan);border-color:rgba(76,201,240,.5);}
  .hdeliv.award .hd-badge{color:var(--amber);border-color:rgba(255,180,84,.55);}
  .hdeliv.pace .hd-badge{color:var(--amber);border-color:rgba(255,214,0,.75);}
  .hdeliv.prototype .hd-badge{color:var(--muted);border-color:rgba(125,138,153,.7);}
  .hdeliv.training .hd-badge{color:var(--pink);border-color:rgba(255,107,157,.6);}
  .hd-t{font-size:10px;font-weight:700;color:var(--fg);margin-top:4px;line-height:1.25;}
  .hd-role{font-size:8.2px;color:var(--muted);margin-top:1px;}
  .hdeliv ul.pts{margin-top:4px;}
  .hd-result{font-size:8.8px;line-height:1.4;color:var(--fg);margin-top:5px;padding-top:5px;border-top:1px dashed rgba(61,220,132,.35);}
  .hd-result b{color:var(--fg);font-weight:600;}
  .hd-result b.mono{font-size:6.8px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:var(--green);margin-right:6px;}
  .hdeliv.pace .hd-result{border-top-color:rgba(255,214,0,.55);} .hdeliv.pace .hd-result b.mono{color:var(--amber);}
  .hdeliv.prototype .hd-result{border-top-color:rgba(125,138,153,.5);} .hdeliv.prototype .hd-result b.mono{color:var(--muted);}
  .hdeliv.training .hd-result{border-top-color:rgba(255,107,157,.5);} .hdeliv.training .hd-result b.mono{color:var(--pink);}
  .hdeliv .dchips{margin-top:6px;}
  .hstack{display:flex;align-items:baseline;gap:6px;margin-top:6px;}
  .hs-h{font-size:7.2px;letter-spacing:1.4px;text-transform:uppercase;color:var(--muted);flex:0 0 auto;padding-top:2px;}
  .hstack .dchips{font-size:7.4px;}
  .hlinks{display:flex;flex-wrap:wrap;gap:10px;margin-top:5px;font-size:8px;}
  .hlinks a{color:var(--cyan);}
  .hlinks a::before{content:"↗ ";color:var(--muted);}
  .hentry h3{font-size:11.5px;font-weight:600;color:var(--fg);margin-top:2px;}
  .hentry h3 .c{color:var(--cyan);}
  .hentry .loc{font-size:8.2px;color:var(--muted);}
  .hentry ul.pts{margin-top:3px;}
  .subject{flex:0 0 56mm;position:sticky;top:12px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 11px;transition:opacity .18s;}
  .subject.swap{opacity:.35;}
  .sub-k{font-size:8px;color:var(--muted);} .sub-k .g{color:var(--green);} .sub-k .c{color:var(--cyan);} .sub-k .f{color:var(--amber);}
  .sub-kind{font-size:7.4px;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-top:8px;}
  .sub-co{font-size:15px;font-weight:700;color:var(--fg);letter-spacing:-.3px;line-height:1.15;margin-top:2px;}
  .sub-role{font-size:9.6px;font-weight:500;color:var(--cyan);margin-top:2px;} .sub-role:empty{display:none;}
  .sub-when{font-size:8px;color:var(--green);margin-top:5px;}
  .sub-loc{font-size:8.2px;color:var(--muted);margin-bottom:6px;}
  .sub-h{font-size:8px;color:var(--muted);margin:9px 0 4px;}
  .subject .dchips:empty::after{content:"—";color:var(--muted);font-size:8px;}
  .sub-nav{list-style:none;margin:0;}
  .sub-nav li{font-size:8.4px;color:var(--muted);padding:2px 0 2px 12px;position:relative;cursor:pointer;line-height:1.35;}
  .sub-nav li::before{content:"";position:absolute;left:0;top:7px;width:5px;height:5px;border-radius:50%;background:var(--line);}
  .sub-nav li.active{color:var(--fg);font-weight:600;} .sub-nav li.active::before{background:var(--green);}
  .sub-nav li:hover{color:var(--cyan);}
  .sub-progress{height:3px;border-radius:2px;background:var(--line);margin-top:9px;overflow:hidden;}
  .sub-progress i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--green),var(--cyan));transition:width .3s;}
  /* ---- /timeline/ search: a `grep -i` bar that sticks to the top of the timeline column ---- */
  .hq{position:sticky;top:0;z-index:5;margin:0 0 6px -16px;padding:6px 0 7px 16px;
    background:color-mix(in srgb,var(--bg) 90%,transparent);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);}
  .hq-row{display:flex;align-items:center;gap:8px;}
  .hq-prompt{font-size:8.6px;color:var(--muted);white-space:nowrap;cursor:text;} .hq-prompt .g{color:var(--green);} .hq-prompt .c{color:var(--cyan);}
  .hq-field{flex:1 1 auto;min-width:0;display:flex;align-items:center;border-bottom:1px solid var(--line);transition:border-color .15s;}
  .hq-field:focus-within{border-color:var(--green);}
  .hq-in{flex:1 1 auto;min-width:0;background:none;border:0;outline:0;font:inherit;font-size:9.4px;color:var(--fg);padding:3px 0;caret-color:var(--green);}
  .hq-in::placeholder{color:var(--muted);opacity:.7;}
  .hq-x{background:none;border:0;cursor:pointer;font:inherit;font-size:12px;line-height:1;color:var(--muted);padding:0 3px;} .hq-x:hover{color:var(--pink);}
  .hq-count{font-size:8px;color:var(--muted);white-space:nowrap;} .hq-count:empty{display:none;}
  .hq-more{background:none;border:0;cursor:pointer;font:inherit;font-size:8px;color:var(--muted);white-space:nowrap;padding:2px 0;}
  .hq-more:hover,.hq-more[aria-expanded="true"]{color:var(--cyan);} .hq-more i{font-style:normal;display:inline-block;transition:transform .15s;} .hq-more[aria-expanded="true"] i{transform:rotate(90deg);}
  .hq-facets{display:grid;gap:5px;margin-top:6px;padding-top:6px;border-top:1px dashed var(--line);} .hq-facets[hidden]{display:none;}
  .hq-facet{display:flex;align-items:flex-start;gap:8px;}
  .hq-fh{font-size:7.4px;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);flex:0 0 58px;padding-top:3px;}
  .hq-facet .dchips{gap:3px;}
  .hq-facet .dchip{cursor:pointer;font:inherit;font-size:7.6px;padding:1px 6px;} .hq-facet .dchip:hover{border-color:var(--cyan);color:var(--cyan);}
  .hq-facet .dchip.on{border-color:var(--green);color:var(--green);background:rgba(61,220,132,.10);}
  .hq-facet .dchip.extra{display:none;} .hq-facet.all .dchip.extra{display:inline-block;} .hq-facet.all .hq-morechips{display:none;}
  .hq-morechips{background:none;border:0;cursor:pointer;font:inherit;font-size:7.4px;color:var(--cyan);padding:1px 4px;}
  .hq-empty{font-size:8.6px;color:var(--amber);margin-top:6px;}
  /* filter states: a dimmed entry keeps only its head; an untouched block folds into its label; hits are marked */
  .hentry.dim .hbody,.hentry.dim .loc{display:none;}
  .hentry.dim .hhead{opacity:.5;}
  .hentry.dim > .hhead h3,.hentry.dim > .hhead h3 .c,.hentry.dim > .hhead .hdate{color:var(--muted);}
  .hentry.dim::before{border-color:var(--line);background:var(--bg);box-shadow:none;}
  .hblock.fold{cursor:pointer;margin-top:4px;padding:1px 0 1px 9px;position:relative;font-family:'JetBrains Mono',monospace;font-size:7.6px;color:var(--muted);}
  .hblock.fold::after{content:"";position:absolute;left:0;top:3px;bottom:2px;width:2px;border-radius:2px;border-left:2px dotted var(--line);}
  .hblock.fold > *{display:none !important;}
  /* (.hgroup::before is normally its absolute 2px bar — here it becomes the label, so every box property is reset) */
  .hentry .hblock.fold::before{content:"▸ // " attr(data-label-en);position:static;display:inline;width:auto;height:auto;background:none;border:0;border-radius:0;}
  html[data-lang="es"] .hentry .hblock.fold::before{content:"▸ // " attr(data-label-es);}
  .hblock.fold:hover{color:var(--cyan);}
  .hgroups .hblock.fold{margin-top:0;} .hlede.hblock.fold{margin-top:5px;}
  .hdeliv.hblock.fold,.hgroup.hblock.fold{border:0;background:none;border-radius:0;padding:1px 0 1px 9px;}
  mark.hm{background:rgba(255,180,84,.30);color:inherit;border-radius:2px;padding:0 1px;box-decoration-break:clone;-webkit-box-decoration-break:clone;}
  .hentry.dim mark.hm{background:none;}
  .sub-nav li.dim{opacity:.4;pointer-events:none;}
  .hq-in:focus{outline:0;}
  @view-transition{navigation:auto;}   /* smooth cross-fade between the site's pages (same shell everywhere) */
  .empty{font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--muted);margin-top:10px;}
  body{font-family:'Inter',system-ui,sans-serif;color:var(--text);font-size:10px;line-height:1.5;background:var(--bg);}
  .mono{font-family:'JetBrains Mono',Menlo,Consolas,monospace;}
  .sheet{background:var(--bg);padding:11mm 12mm 4mm;display:flex;flex-direction:column;
    background-image:radial-gradient(500px 260px at 90% -5%,rgba(76,201,240,.10),transparent 60%),radial-gradient(420px 220px at 0% 8%,rgba(61,220,132,.09),transparent 60%);}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#e6ecf2 0%,#cfd8e1 55%,#bcc7d2 100%);} .sheet{border:1px solid var(--line);}}

  .site-nav{margin:-11mm -12mm 6mm;}
  .prompt{font-size:8.6px;color:var(--muted);}
  .prompt .g{color:var(--green);} .prompt .c{color:var(--cyan);} .prompt .f{color:var(--amber);}
  .name{font-size:29px;font-weight:700;letter-spacing:-1px;line-height:1;color:var(--fg);margin-top:5px;}
  .name .cur{display:inline-block;width:.45em;height:.9em;background:var(--green);vertical-align:-.08em;margin-left:3px;animation:blink 1s steps(1) infinite;}
  @keyframes blink{50%{opacity:0;}}
  .hname{font-size:11px;font-weight:600;color:var(--cyan);letter-spacing:-.1px;margin-top:6px;}   /* /timeline/: the name, secondary to the title */
  .sub{font-size:9px;color:var(--muted);margin-top:5px;}
  .sub .hl{color:var(--amber);}
  .sub .r0{color:var(--green);font-weight:600;font-size:10px;letter-spacing:-.1px;}  /* the headline role, ahead of the rest */
  .top{display:flex;justify-content:space-between;align-items:flex-end;gap:8mm;}
  .contact{display:grid;gap:3px;flex:none;}
  .cline{display:flex;align-items:center;gap:6px;font-size:8.4px;color:var(--muted);}
  .cline a{color:var(--text);}
  .cline svg{stroke:var(--green);width:11px;height:11px;}

  .stats{display:flex;gap:6px;margin:5px 0 5px;}
  .stat{flex:1;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:5px 8px;}
  /* stat cards read like a terminal: a "// comment" label on top, then the value */
  .stat{display:flex;flex-direction:column-reverse;justify-content:flex-end;gap:4px;padding:6px 8px;}
  .stat .l{font-family:'JetBrains Mono',monospace;font-size:7.6px;color:var(--muted);margin:0;text-transform:lowercase;letter-spacing:0;}
  .stat .l::before{content:"// ";}
  .stat .n{font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:700;color:var(--fg);line-height:1;letter-spacing:-.5px;}
  .stat .n .u{color:var(--green);}
  .stat.best .n{display:flex;flex-wrap:wrap;gap:3px;}
  .stat.best .bs{font-family:'JetBrains Mono',monospace;font-size:7.6px;font-weight:700;color:var(--green);background:rgba(61,220,132,.10);border:1px solid rgba(61,220,132,.45);border-radius:4px;padding:1px 6px;line-height:1.5;}
  .stat.best .bs+.bs::before{content:none;}

  .cols{display:flex;gap:7mm;flex:1;}
  .main{flex:1 1 auto;min-width:0;}
  .aside{flex:0 0 54mm;}
  h2.sh{font-family:'JetBrains Mono',monospace;font-size:8.6px;color:var(--muted);font-weight:500;margin-bottom:6px;}
  h2.sh::before{content:"➜ ~ ";color:var(--green);}
  h2.sh::after{content:"";}
  section{margin-bottom:8px;}

  .profile{font-size:9.5px;line-height:1.5;color:var(--body-text);}
  .profile b{color:var(--fg);font-weight:600;}

  .job{padding:6px 0 4px;border-top:1px dashed var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:600;color:var(--fg);}
  .job .c{color:var(--cyan);}
  .job .p{font-family:'JetBrains Mono',monospace;font-size:7.8px;color:var(--muted);white-space:nowrap;flex:none;}
  .job.cur .p{color:var(--green);}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:12px;margin-bottom:2.5px;line-height:1.35;font-size:9.1px;color:var(--body-text);}
  .ind{font-family:'JetBrains Mono',monospace;font-size:7.4px;font-weight:700;color:var(--cyan);background:rgba(76,201,240,.12);border:1px solid rgba(76,201,240,.45);padding:1px 6px;border-radius:4px;}
  .ind::before{content:"#";color:rgba(76,201,240,.6);margin-right:1px;}
  ul.pts li::before{content:">";position:absolute;left:0;color:var(--green);font-family:'JetBrains Mono',monospace;font-weight:700;}
  ul.pts li b{color:var(--fg);font-weight:600;}
  ul.pts li a{color:var(--cyan);}
  .stack{color:var(--muted);}

  .cskill{padding:2px 0 3px;}
  .sk-top{font-size:9px;color:var(--text);font-weight:500;}
  .sk-word,.sk-track{display:none;}
  .sk-pct{display:inline;font-family:'JetBrains Mono',monospace;font-size:8.4px;color:var(--green);}
  .sk-dots{display:block;font-family:'JetBrains Mono',monospace;font-size:8.6px;line-height:1.25;margin-top:1px;white-space:nowrap;overflow:hidden;}
  .sk-dots::before{content:"[";color:var(--muted);} .sk-dots::after{content:"]";color:var(--muted);}
  .sk-dots i::before{content:"░";color:var(--empty);} .sk-dots i.on::before{content:"█";color:var(--green);}
  .sk-dots.ascii::before,.sk-dots.ascii::after{content:none;}
  .sk-dots .b{color:var(--muted);} .sk-dots .f{color:var(--green);} .sk-dots .e{color:var(--empty);}
  .ai{background:linear-gradient(160deg,rgba(61,220,132,.10),rgba(76,201,240,.07));border:1px solid rgba(61,220,132,.35);border-radius:9px;padding:9px 10px;}
  .ai .h{font-family:'JetBrains Mono',monospace;font-size:8.4px;color:var(--green);margin-bottom:4px;display:flex;align-items:center;gap:6px;}
  .ai .h::before{content:"// ";color:var(--muted);}
  .ai .h svg{display:none;}
  .ai p{font-size:8.8px;color:var(--body-text);line-height:1.45;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-family:'JetBrains Mono',monospace;font-size:7.6px;padding:2px 6px;border-radius:4px;background:var(--panel);border:1px solid var(--line);color:var(--text);}
  .ai .dchip{border-color:rgba(61,220,132,.4);color:var(--green);background:transparent;}
  .award{font-size:8.7px;color:var(--body-text);padding:2.5px 0;border-bottom:1px dashed var(--line);line-height:1.35;}
  .award:last-child{border-bottom:0;}
  .award b{color:var(--fg);font-weight:600;}
  .award a{color:var(--cyan);}
  .edu{padding:3px 0;border-bottom:1px dashed var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.5px;font-weight:600;color:var(--fg);}
  .edu .m{font-size:8.2px;color:var(--muted);}
  .foot{margin-top:auto;padding-top:5px;border-top:1px solid var(--line);font-family:'JetBrains Mono',monospace;font-size:7.6px;color:var(--muted);display:flex;justify-content:space-between;}
  .foot .g{color:var(--green);}

  .toolgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:6px;}
  .toolcard{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:7px 9px;}
  .toolcard .tt{font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:700;color:var(--fg);}
  .toolcard .tt::before{content:"> ";color:var(--green);}
  .toolcard .td{font-size:8.4px;color:var(--body-text);margin-top:2px;line-height:1.4;}

  /* profile photo — 4:5 portrait like the reference page; the square source is cropped, keeping the face on the left */
  .avatar{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:35% 50%;
    border:1px solid var(--line);border-radius:10px;background:var(--panel);}

  /* ---------------------------------------------------------------- printing / ATS
     The terminal skin is screen-only. When the page is printed (that is what the PDF button does),
     everything that reads as a shell command is dropped, so a resume parser gets plain text:
     the `sergio@…:~$ cat cv.md` prompt, the `➜ ~ ` and `// ` prefixes, the `#` on industry tags,
     the `[████░░]` skill meters (replaced by the word: Expert / Advanced …) and the `exit 0` footer. */
  @media print{
    .hq{display:none !important;}
    .name .cur{display:none;}            /* the blinking caret is screen decoration */
    h2.sh{font-family:'Inter',system-ui,sans-serif;font-size:9.4px;font-weight:700;color:var(--fg);
      text-transform:uppercase;letter-spacing:.7px;border-bottom:1px solid var(--line);padding-bottom:3px;}
    .stat .l::before,.ai .h::before,.hg-h::before{content:none;}
    .stat .l{font-family:'Inter',system-ui,sans-serif;text-transform:none;}
    ul.pts li::before{content:"•";font-weight:400;}   /* a bullet every parser knows, instead of ">" */
    .ind::before{content:none;} .ind{padding-left:2px;}
    .sk-dots{display:none !important;}                            /* the ASCII bar carries no text worth parsing */
    .sk-word{display:inline;color:var(--muted);}                  /* the level as a word instead: Expert / Avanzado */
    .toolcard .tt::before{content:none;}
    .hlinks a::before{content:none;}
  }
""",
    body="""<div class="sheet">
  $NAV$
  <header class="top">
    <div>
      <div class="prompt mono"><span class="g">sergio</span>@<span class="c">sergiowero.github.io</span>:~$ cat <span class="f">$L_CVFILE$</span></div>
      <div class="name"><span id="typed">$NAME$</span><span class="cur"></span></div>
      <div class="sub mono">$L_SUB$</div>
    </div>
    <div class="contact">$CONTACT$</div>
  </header>
  $STATS$
  <div class="cols">
    <main class="main">
      <section><h2 class="sh">$L_PROFILE$</h2>$PROFILE$</section>
      <section><h2 class="sh">$L_EXP$</h2>$EXP$</section>
    </main>
    <aside class="aside">
      <section>$AI$</section>
      <section><h2 class="sh">$L_CORE$</h2>$CORE$</section>
      <section><h2 class="sh">$L_TECH$</h2>$TECH$</section>
      <section><h2 class="sh">$L_SHIPPED$</h2>$TITLES$</section>
      <section><h2 class="sh">$L_EDU$</h2>$EDU$</section>
    </aside>
  </div>
  <div class="foot"><span><span class="g">➜</span> exit 0 · $NAME$</span><span>sergiowero.github.io</span></div>
  $CVDATA$
</div>
$DOWNLOAD$""")

# =================================================================== v4 BENTO GRID (A4)
VERSIONS["v4-bento-grid.html"] = dict(
    nav="--nav-bg:#fff;--nav-line:#e6e8ef;--nav-fg:#0f1222;--nav-muted:#7c8196;--nav-active-bg:#2f5bff;--nav-active-fg:#fff;",
    title="Sergio Sanchez CV",
    fonts="family=Plus+Jakarta+Sans:wght@400;500;600;700;800",
    css="""
  :root{--bg:#f3f4f8;--card:#fff;--ink:#0f1222;--body:#3f4458;--muted:#7c8196;--line:#e6e8ef;--blue:#2f5bff;--blue-soft:#e8edff;--orange:#ff7a1a;--mint:#12b886;--mint-soft:#e3f8f0;--violet:#7c4dff;--violet-soft:#efe9ff;}
  body{font-family:'Plus Jakarta Sans',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:var(--bg);}
  .sheet{background:var(--bg);padding:7mm;display:grid;grid-template-columns:1fr 54mm;grid-auto-rows:min-content;gap:6px;align-content:start;
    background-image:radial-gradient(500px 300px at 5% -5%,rgba(47,91,255,.10),transparent 60%),radial-gradient(400px 240px at 100% 0%,rgba(255,122,26,.10),transparent 60%);}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#2a3a8a 0%,#151a3a 50%,#0b0d1e 100%);}}
  .site-nav{grid-column:1/-1;margin:-7mm -7mm 0;padding-left:7mm;padding-right:7mm;}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:9px 11px;}
  .span2{grid-column:1/-1;}
  .stack-col{display:grid;gap:6px;align-content:start;}
  h2.sh{font-size:7.8px;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:6px;}
  h2.sh::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--blue);}
  .c-or h2.sh::before{background:var(--orange);} .c-mint h2.sh::before{background:var(--mint);} .c-vio h2.sh::before{background:var(--violet);}

  .hero{background:linear-gradient(135deg,#101635 0%,#1a2352 60%,#2f5bff 140%);color:#fff;border:0;position:relative;overflow:hidden;display:flex;justify-content:space-between;gap:8mm;align-items:flex-end;padding:12px 14px;}
  .hero::after{content:"";position:absolute;right:-60px;top:-60px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(255,122,26,.55),transparent 65%);}
  .hero>*{position:relative;z-index:1;}
  .mono{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,var(--orange),#ffb066);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;color:#fff;margin-bottom:8px;}
  .name{font-size:26px;font-weight:800;letter-spacing:-.8px;line-height:1.02;}
  .role{font-size:9.5px;color:#c9d2ff;margin-top:5px;font-weight:500;}
  .role b{color:#ffb066;font-weight:700;}
  .contact{display:grid;gap:3px;flex:none;}
  .cline{display:flex;align-items:center;gap:6px;font-size:8.2px;color:#c9d2ff;}
  .cline svg{stroke:#ffb066;width:11px;height:11px;}

  .stats{display:grid;grid-template-columns:1fr 1fr 1fr 1.3fr;gap:6px;grid-column:1/-1;}
  .stat{border-radius:12px;padding:8px 11px;display:flex;align-items:baseline;gap:8px;}
  .stat:nth-child(1){background:var(--blue-soft);} .stat:nth-child(1) .n{color:var(--blue);}
  .stat:nth-child(2){background:var(--mint-soft);} .stat:nth-child(2) .n{color:var(--mint);}
  .stat:nth-child(3){background:var(--violet-soft);} .stat:nth-child(3) .n{color:var(--violet);}
  .stat.best{background:#fff0e4;flex-direction:column;align-items:flex-start;gap:2px;} .stat.best .n{color:var(--orange);}
  .stat .n{font-size:20px;font-weight:800;letter-spacing:-1px;line-height:1;}
  .stat .n .u{color:var(--orange);}
  .stat .l{font-size:8px;color:var(--muted);font-weight:600;line-height:1.2;}

  .profile{font-size:9.4px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--ink);font-weight:700;}

  .job{padding:4px 0 3px;border-top:1px solid var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:10.8px;font-weight:700;color:var(--ink);letter-spacing:-.1px;}
  .job .c{color:var(--blue);}
  .job .p{font-size:7.8px;color:var(--muted);font-weight:700;white-space:nowrap;flex:none;background:var(--bg);padding:1px 6px;border-radius:5px;}
  .job.cur .p{background:var(--mint-soft);color:var(--mint);}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9px;}
  .ind{border-radius:20px;background:var(--blue-soft);color:var(--blue);}
  .ind:nth-child(4n+2){background:var(--mint-soft);color:var(--mint);} .ind:nth-child(4n+3){background:var(--violet-soft);color:var(--violet);} .ind:nth-child(4n){background:#fff0e4;color:var(--orange);}
  ul.pts li::before{content:"";position:absolute;left:0;top:5.5px;width:4px;height:4px;border-radius:1px;background:var(--orange);transform:rotate(45deg);}
  ul.pts li b{color:var(--ink);font-weight:700;}
  ul.pts li a{color:var(--blue);font-weight:600;}
  .stack{color:var(--muted);}

  .ai{background:linear-gradient(135deg,var(--orange) 0%,#ff9a4a 100%);color:#fff;border-radius:12px;padding:9px 11px;}
  .ai .h{font-size:7.8px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;color:rgba(255,255,255,.9);margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:#fff;}
  .ai p{font-size:8.8px;line-height:1.45;font-weight:500;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:600;padding:2px 7px;border-radius:20px;background:var(--bg);color:var(--ink);border:1px solid var(--line);}
  .ai .dchip{background:rgba(255,255,255,.18);border-color:rgba(255,255,255,.35);color:#fff;}
  .cskill{padding:2.5px 0 4px;}
  .sk-top{align-items:center;font-size:9.2px;font-weight:600;color:var(--ink);}
  .sk-word{display:none;}
  .sk-pct{display:inline;font-size:7.4px;font-weight:700;color:var(--blue);background:var(--blue-soft);padding:1px 6px;border-radius:20px;}
  .sk-track{height:6px;border-radius:6px;background:var(--bg);margin-top:3px;overflow:hidden;}
  .sk-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--blue),var(--violet));}
  .award{font-size:8.6px;color:var(--body);background:var(--bg);border-radius:8px;padding:5px 8px;margin-bottom:4px;line-height:1.35;}
  .award:last-child{margin-bottom:0;}
  .award b{color:var(--ink);font-weight:700;}
  .award a{color:var(--blue);font-weight:600;}
  .edu{padding:3px 0;border-bottom:1px solid var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.4px;font-weight:700;color:var(--ink);}
  .edu .m{font-size:8.2px;color:var(--muted);}
""",
    body="""<div class="sheet">
  $NAV$
  <header class="card hero span2">
    <div>
      <div class="mono">SS</div>
      <div class="name">$NAME$</div>
      <div class="role">$ROLE$ · <b>AI-Assisted Engineering</b> · Zapopan, México</div>
    </div>
    <div class="contact">$CONTACT$</div>
  </header>
  $STATS$
  <main class="stack-col">
    <section class="card"><h2 class="sh">About</h2>$PROFILE$</section>
    <section class="card"><h2 class="sh">Experience</h2>$EXP$</section>
  </main>
  <aside class="stack-col">
    <section class="ai"><div class="h">AI-Assisted Dev</div><p>$AI_TEXT$</p>$AI_CHIPS$</section>
    <section class="card"><h2 class="sh">Core Skills</h2>$CORE$</section>
    <section class="card c-vio"><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
    <section class="card c-or"><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
    <section class="card c-mint"><h2 class="sh">Education</h2>$EDU$</section>
  </aside>
</div>""")

# =================================================================== v6 SPLIT PANEL (A4, sidebar right)
VERSIONS["v6-split-panel.html"] = dict(
    nav="--nav-bg:transparent;--nav-line:transparent;--nav-fg:#161616;--nav-muted:#8a8a85;--nav-active-bg:#c8f135;--nav-active-fg:#111;",
    title="Sergio Sanchez CV",
    fonts="family=Space+Grotesk:wght@400;500;600;700",
    css="""
  :root{--char:#151515;--paper:#f6f5f0;--ink:#161616;--body:#444;--muted:#8a8a85;--line:#e2e0d8;--lime:#c8f135;--lime-dark:#6f8c00;--on-dark:#f2f2ee;--on-dark-mute:#9c9c95;}
  body{font-family:'Space Grotesk',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:var(--paper);}
  .sheet{background:var(--paper);display:flex;flex-direction:column;}
  .cols{display:flex;flex:1;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#2a2f14 0%,#141510 50%,#0a0a08 100%);}}
  .main{flex:1 1 auto;min-width:0;padding:7mm 9mm 6mm 12mm;}
  .panel{flex:0 0 64mm;background:var(--char);color:var(--on-dark);padding:7mm 8mm 6mm;position:relative;overflow:hidden;}
  .panel::before{content:"";position:absolute;left:-90px;bottom:-90px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(200,241,53,.22),transparent 65%);pointer-events:none;}
  .panel>*{position:relative;z-index:1;}

  .site-nav{padding:0;margin:0 0 4mm;}
  .badge{display:inline-flex;align-items:center;gap:6px;font-size:8px;letter-spacing:1.6px;text-transform:uppercase;color:var(--lime-dark);font-weight:600;}
  .badge i{width:7px;height:7px;border-radius:50%;background:var(--lime);box-shadow:0 0 0 3px rgba(200,241,53,.3);}
  .name{font-size:36px;font-weight:700;letter-spacing:-1.8px;line-height:.95;color:var(--ink);margin-top:8px;}
  .name span{color:var(--lime-dark);}
  .tag{font-size:9px;color:var(--muted);margin-top:6px;}

  .stats{display:flex;gap:7px;margin:8px 0 8px;}
  .stat{flex:1;background:#fff;border:1px solid var(--line);border-radius:10px;padding:6px 10px;}
  .stat .n{font-size:19px;font-weight:700;letter-spacing:-1px;line-height:1;color:var(--ink);}
  .stat .n .u{color:var(--lime-dark);}
  .stat .l{font-size:7.8px;color:var(--muted);margin-top:3px;}

  h2.sh{font-size:8.4px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);font-weight:600;margin-bottom:7px;display:flex;align-items:center;gap:7px;}
  h2.sh::before{content:"";width:7px;height:7px;background:var(--lime);border-radius:2px;}
  .panel h2.sh{color:var(--on-dark-mute);}
  section{margin-bottom:9px;}
  .panel section{margin-bottom:12px;}

  .profile{font-size:10px;line-height:1.5;color:var(--ink);font-weight:500;}
  .profile b{font-weight:600;background:linear-gradient(transparent 62%,var(--lime) 62%);}

  .job{padding:4px 0 3px;border-top:1px dashed var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:600;color:var(--ink);letter-spacing:-.2px;}
  .job .c{color:var(--lime-dark);}
  .job .p{font-size:8px;color:var(--muted);font-weight:500;white-space:nowrap;flex:none;}
  .job.cur .p{background:var(--lime);color:#111;padding:1px 6px;border-radius:3px;font-weight:600;}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"";position:absolute;left:0;top:5.5px;width:5px;height:5px;background:var(--lime);border-radius:1px;}
  .ind{border:1px solid var(--ink);color:var(--ink);border-radius:999px;background:transparent;font-weight:500;}
  ul.pts li b{color:var(--ink);font-weight:600;}
  ul.pts li a{color:var(--lime-dark);font-weight:600;}
  .stack{color:var(--muted);}

  .cline{display:flex;align-items:center;gap:7px;font-size:8.6px;color:var(--on-dark-mute);margin-bottom:5px;}
  .cline a{color:var(--on-dark);}
  .cline svg{stroke:var(--lime);}
  .cskill{padding:3px 0;display:flex;align-items:center;justify-content:space-between;gap:8px;}
  .sk-top{font-size:9.4px;color:#fff;font-weight:500;}
  .sk-word,.sk-track{display:none;}
  .sk-dots{display:flex;gap:2px;flex:none;}
  .sk-dots i{width:6px;height:6px;border:1px solid rgba(200,241,53,.45);border-radius:1px;}
  .sk-dots i.on{background:var(--lime);border-color:var(--lime);}
  .ai{border:1px solid rgba(200,241,53,.4);border-radius:9px;padding:9px 10px;background:rgba(200,241,53,.06);}
  .ai .h{font-size:8px;letter-spacing:1.6px;text-transform:uppercase;color:var(--lime);font-weight:600;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:var(--lime);}
  .ai p{font-size:8.6px;color:var(--on-dark-mute);line-height:1.45;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.6px;font-weight:500;padding:2px 7px;border-radius:20px;border:1px solid rgba(255,255,255,.2);color:var(--on-dark);}
  .ai .dchip{border-color:rgba(200,241,53,.5);color:var(--lime);}
  .award{font-size:8.6px;color:var(--on-dark-mute);padding:2.5px 0;line-height:1.35;border-bottom:1px dotted rgba(255,255,255,.14);}
  .award:last-child{border-bottom:0;}
  .award b{color:#fff;font-weight:600;}
  .award a{color:var(--lime);}
  .edu{padding:3px 0;border-bottom:1px dotted rgba(255,255,255,.14);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.4px;font-weight:600;color:#fff;}
  .edu .m{font-size:8.2px;color:var(--on-dark-mute);}
""",
    body="""<div class="sheet">
  <div class="cols">
  <main class="main">
    $NAV$
    <div class="badge"><i></i>$ROLE$</div>
    <div class="name">Sergio de Jesús<br>Sánchez Robles<span>.</span></div>
    <div class="tag">$TAG$ · Zapopan, México</div>
    $STATS$
    <section><h2 class="sh">About</h2>$PROFILE$</section>
    <section><h2 class="sh">Experience</h2>$EXP$</section>
  </main>
  <aside class="panel">
    <section><h2 class="sh">Contact</h2>$CONTACT$</section>
    <section>$AI$</section>
    <section><h2 class="sh">Core Skills</h2>$CORE$</section>
    <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
    <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
    <section><h2 class="sh">Education</h2>$EDU$</section>
  </aside>
  </div>
</div>""")

# =================================================================== v7 SWISS BLACK / YELLOW (A4, new)
VERSIONS["v7-swiss-yellow.html"] = dict(
    nav="--nav-bg:#fff;--nav-line:#111;--nav-fg:#111;--nav-muted:#7a7a7a;--nav-active-bg:#ffd500;--nav-active-fg:#111;",
    title="Sergio Sanchez CV",
    fonts="family=Archivo:wght@400;500;600;700;800;900",
    css="""
  :root{--ink:#111;--body:#3a3a3a;--muted:#7a7a7a;--line:#e3e3e3;--rail:#f4f4f4;--yellow:#ffd500;}
  body{font-family:'Archivo',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:#fff;}
  .sheet{background:#fff;display:flex;flex-direction:column;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#3a3a3a 0%,#1a1a1a 50%,#0a0a0a 100%);}}

  .head{padding:7mm 12mm 0;}
  .head .in{display:flex;justify-content:space-between;align-items:flex-end;gap:8mm;padding-bottom:9px;border-bottom:4px solid var(--ink);}
  .kicker{display:inline-block;background:var(--yellow);color:var(--ink);font-size:8px;font-weight:800;letter-spacing:1.8px;text-transform:uppercase;padding:2px 7px;margin-bottom:8px;}
  .name{font-size:34px;font-weight:900;letter-spacing:-1.6px;line-height:.95;color:var(--ink);text-transform:uppercase;}
  .tag{font-size:9px;color:var(--muted);margin-top:6px;font-weight:500;}
  .contact{display:grid;gap:3px;flex:none;text-align:right;}
  .cline{display:flex;align-items:center;justify-content:flex-end;gap:6px;font-size:8.4px;color:var(--ink);font-weight:500;}
  .cline svg{stroke:var(--ink);width:11px;height:11px;order:2;}

  .stats{display:flex;background:var(--ink);color:#fff;margin:0 12mm;}
  .stat{flex:1;padding:7px 12px;border-right:1px solid rgba(255,255,255,.15);display:flex;align-items:baseline;gap:8px;}
  .stat:last-child{border-right:0;}
  .stat .n{font-size:20px;font-weight:900;letter-spacing:-1px;line-height:1;}
  .stat.best{flex-direction:column;align-items:flex-start;gap:2px;} .stat.best .n{color:var(--yellow);}
  .stat .n .u{color:var(--yellow);}
  .stat .l{font-size:7.6px;text-transform:uppercase;letter-spacing:1px;color:#bdbdbd;font-weight:600;line-height:1.2;}

  .cols{display:flex;flex:1;margin-top:7mm;}
  .rail{flex:0 0 58mm;background:var(--rail);padding:7mm 7mm 8mm 12mm;}
  .main{flex:1 1 auto;min-width:0;padding:0 12mm 8mm 8mm;}
  h2.sh{font-size:8.4px;letter-spacing:2px;text-transform:uppercase;color:var(--ink);font-weight:800;margin-bottom:6px;padding-bottom:3px;border-bottom:2px solid var(--ink);}
  section{margin-bottom:8px;}

  .profile{font-size:9.6px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--ink);font-weight:700;background:linear-gradient(transparent 60%,var(--yellow) 60%);}

  .job{padding:4px 0 3px;border-top:1px solid var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:800;color:var(--ink);letter-spacing:-.2px;}
  .job .c{font-weight:600;color:var(--ink);background:linear-gradient(transparent 60%,var(--yellow) 60%);}
  .job .p{font-size:8px;color:var(--muted);font-weight:700;white-space:nowrap;flex:none;letter-spacing:.3px;}
  .job.cur .p{color:var(--ink);}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"";position:absolute;left:0;top:6px;width:5px;height:2px;background:var(--ink);}
  .ind{background:var(--yellow);color:var(--ink);border-radius:0;text-transform:uppercase;letter-spacing:.6px;font-size:6.8px;font-weight:800;}
  ul.pts li b{color:var(--ink);font-weight:700;}
  ul.pts li a{color:var(--ink);font-weight:700;text-decoration:underline;text-decoration-color:var(--yellow);text-decoration-thickness:2px;}
  .stack{color:var(--muted);}

  .cskill{padding:1.5px 0 2.5px;}
  .sk-top{font-size:8.6px;font-weight:800;color:var(--ink);text-transform:uppercase;letter-spacing:.3px;line-height:1.3;}
  .sk-word{font-weight:500;text-transform:none;letter-spacing:0;color:var(--muted);font-size:8.2px;}
  .sk-track{height:5px;background:#e3e3e3;margin-top:2px;}
  .sk-fill{height:100%;background:var(--ink);position:relative;}
  .sk-fill::after{content:"";position:absolute;right:0;top:0;width:6px;height:100%;background:var(--yellow);}
  .ai{background:var(--ink);color:#fff;padding:10px 11px;}
  .ai .h{font-size:8px;letter-spacing:1.8px;text-transform:uppercase;color:var(--yellow);font-weight:800;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:var(--yellow);}
  .ai p{font-size:8.8px;line-height:1.45;color:#cfcfcf;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:700;padding:2px 7px;border:1.5px solid var(--ink);color:var(--ink);background:#fff;}
  .ai .dchip{background:var(--yellow);border-color:var(--yellow);color:var(--ink);}
  .award{font-size:8.7px;color:var(--body);padding:2.5px 0;border-bottom:1px solid var(--line);line-height:1.35;}
  .award:last-child{border-bottom:0;}
  .award b{color:var(--ink);font-weight:700;}
  .award a{color:var(--ink);font-weight:700;text-decoration:underline;text-decoration-color:var(--yellow);text-decoration-thickness:2px;}
  .edu{padding:3px 0;border-bottom:1px solid var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.5px;font-weight:800;color:var(--ink);}
  .edu .m{font-size:8.2px;color:var(--muted);}
""",
    body="""<div class="sheet">
  $NAV$
  <header class="head">
    <div class="in">
      <div>
        <div class="kicker">$ROLE$</div>
        <div class="name">Sergio de Jesús<br>Sánchez Robles</div>
        <div class="tag">$TAG$ · Zapopan, México</div>
      </div>
      <div class="contact">$CONTACT$</div>
    </div>
  </header>
  $STATS$
  <div class="cols">
    <aside class="rail">
      <section>$AI$</section>
      <section><h2 class="sh">Core Skills</h2>$CORE$</section>
      <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
      <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
      <section><h2 class="sh">Education</h2>$EDU$</section>
    </aside>
    <main class="main">
      <section><h2 class="sh">Profile</h2>$PROFILE$</section>
      <section><h2 class="sh">Experience</h2>$EXP$</section>
    </main>
  </div>
</div>""")

# =================================================================== v8 CORPORATE NAVY / EMERALD (A4, new)
VERSIONS["v8-navy-emerald.html"] = dict(
    nav="--nav-bg:transparent;--nav-line:transparent;--nav-fg:#0b2545;--nav-muted:#7a8595;--nav-active-bg:#13a97a;--nav-active-fg:#fff;",
    title="Sergio Sanchez CV",
    fonts="family=IBM+Plex+Sans:wght@400;500;600;700",
    css="""
  :root{--navy:#0b2545;--navy-2:#13315c;--ink:#0b2545;--body:#3b4656;--muted:#7a8595;--line:#dfe5ee;--side:#eef2f7;--em:#13a97a;--em-soft:#dff5ec;}
  body{font-family:'IBM Plex Sans',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:#fff;}
  .sheet{background:#fff;display:flex;flex-direction:column;}
  .cols{display:flex;flex:1;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#1b4f8a 0%,#0b2545 50%,#061426 100%);}}
  .side{flex:0 0 60mm;background:var(--side);padding:7mm 7mm 8mm 10mm;border-right:1px solid var(--line);}
  .main{flex:1 1 auto;min-width:0;padding:7mm 11mm 8mm 9mm;}

  .mono{width:40px;height:40px;border-radius:10px;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;margin-bottom:12px;position:relative;}
  .mono::after{content:"";position:absolute;right:-4px;bottom:-4px;width:12px;height:12px;border-radius:50%;background:var(--em);border:2px solid var(--side);}
  h2.sh{font-size:8.4px;letter-spacing:1.8px;text-transform:uppercase;color:var(--navy);font-weight:700;margin-bottom:7px;display:flex;align-items:center;gap:7px;}
  h2.sh::before{content:"";width:12px;height:3px;background:var(--em);border-radius:2px;}
  section{margin-bottom:10px;}

  .cline{display:flex;align-items:center;gap:7px;font-size:8.6px;color:var(--body);margin-bottom:5px;}
  .cline svg{stroke:var(--em);}
  .cskill{padding:3px 0;border-bottom:1px solid var(--line);display:flex;align-items:flex-end;justify-content:space-between;gap:8px;}
  .cskill:last-child{border-bottom:0;}
  .sk-top{font-size:9.3px;color:var(--ink);font-weight:500;}
  .sk-word,.sk-track{display:none;}
  .sk-dots{display:flex;gap:2px;align-items:flex-end;height:11px;flex:none;}
  .sk-dots i{width:3px;background:var(--line);border-radius:1px;}
  .sk-dots i:nth-child(1){height:2px;} .sk-dots i:nth-child(2){height:3px;} .sk-dots i:nth-child(3){height:4px;} .sk-dots i:nth-child(4){height:5px;} .sk-dots i:nth-child(5){height:6px;} .sk-dots i:nth-child(6){height:7px;} .sk-dots i:nth-child(7){height:8px;} .sk-dots i:nth-child(8){height:9px;} .sk-dots i:nth-child(9){height:10px;} .sk-dots i:nth-child(10){height:11px;}
  .sk-dots i.on{background:var(--em);}
  .ai{background:var(--navy);color:#fff;border-radius:9px;padding:10px 11px;}
  .ai .h{font-size:8px;letter-spacing:1.5px;text-transform:uppercase;color:#8fe3c5;font-weight:700;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:#8fe3c5;}
  .ai p{font-size:8.8px;line-height:1.45;color:#c8d3e3;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:600;padding:2px 7px;border-radius:5px;background:#fff;border:1px solid var(--line);color:var(--navy);}
  .ai .dchip{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.25);color:#fff;}
  .award{font-size:8.7px;color:var(--body);padding:2.5px 0 2.5px 10px;position:relative;line-height:1.35;}
  .award::before{content:"";position:absolute;left:0;top:7px;width:4px;height:4px;border-radius:50%;background:var(--em);}
  .award b{color:var(--ink);font-weight:600;}
  .award a{color:var(--em);font-weight:600;}
  .edu{padding:3px 0;border-bottom:1px solid var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.5px;font-weight:600;color:var(--ink);}
  .edu .m{font-size:8.2px;color:var(--muted);}

  .site-nav{padding:0;margin:0 0 4mm;}
  .kicker{font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--em);font-weight:700;margin-bottom:6px;}
  .name{font-size:29px;font-weight:700;letter-spacing:-.8px;line-height:1;color:var(--navy);}
  .role{font-size:12px;font-weight:600;color:var(--navy-2);margin-top:6px;}
  .tag{font-size:9px;color:var(--muted);margin-top:3px;}
  .stats{display:flex;gap:8px;margin:11px 0 11px;}
  .stat{flex:1;border:1px solid var(--line);border-left:3px solid var(--em);border-radius:8px;padding:6px 10px;}
  .stat .n{font-size:19px;font-weight:700;color:var(--navy);line-height:1;letter-spacing:-.5px;}
  .stat .n .u{color:var(--em);}
  .stat .l{font-size:7.8px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;font-weight:600;margin-top:3px;line-height:1.2;}
  .profile{font-size:9.6px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--navy);font-weight:600;}

  .tl{position:relative;padding-left:16px;}
  .tl::before{content:"";position:absolute;left:4px;top:4px;bottom:4px;width:2px;background:var(--line);}
  .job{position:relative;margin-bottom:6px;}
  .job::before{content:"";position:absolute;left:-16px;top:3px;width:10px;height:10px;border-radius:50%;background:#fff;border:2.5px solid var(--em);}
  .job.cur::before{background:var(--em);box-shadow:0 0 0 3px var(--em-soft);}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:700;color:var(--navy);}
  .job .c{color:var(--em);font-weight:600;}
  .job .p{font-size:8.2px;color:var(--muted);font-weight:600;white-space:nowrap;flex:none;}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"";position:absolute;left:0;top:6px;width:4px;height:4px;border-radius:50%;background:var(--navy);}
  .ind{background:var(--em-soft);color:#0f7a58;border-radius:4px;}
  ul.pts li b{color:var(--navy);font-weight:600;}
  ul.pts li a{color:var(--em);font-weight:600;}
  .stack{color:var(--muted);}
""",
    body="""<div class="sheet">
  <div class="cols">
  <aside class="side">
    <div class="mono">SS</div>
    <section><h2 class="sh">Contact</h2>$CONTACT$</section>
    <section><h2 class="sh">Core Skills</h2>$CORE$</section>
    <section>$AI$</section>
    <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
    <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
    <section><h2 class="sh">Education</h2>$EDU$</section>
  </aside>
  <main class="main">
    $NAV$
    <div class="kicker">Curriculum Vitae · 2026</div>
    <div class="name">$NAME$</div>
    <div class="role">$ROLE$</div>
    <div class="tag">$TAG$</div>
    $STATS$
    <section><h2 class="sh">Profile</h2>$PROFILE$</section>
    <section><h2 class="sh">Experience</h2>$EXP$</section>
  </main>
  </div>
</div>""")

# =================================================================== v9 GRADIENT HERO PURPLE→PINK (A4, new)
VERSIONS["v9-gradient-hero.html"] = dict(
    nav="--nav-bg:transparent;--nav-line:transparent;--nav-fg:#fff;--nav-muted:rgba(255,255,255,.75);--nav-active-bg:#fff;--nav-active-fg:#5b21b6;",
    title="Sergio Sanchez CV",
    fonts="family=Sora:wght@400;500;600;700;800",
    css="""
  :root{--p1:#5b21b6;--p2:#ec4899;--ink:#1e1b2e;--body:#463f5c;--muted:#8b85a3;--line:#ebe7f3;--tint:#f7f4fc;}
  body{font-family:'Sora',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:#fff;}
  .sheet{background:#fff;display:flex;flex-direction:column;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#4c1d95 0%,#2a1052 50%,#120726 100%);}}

  .band{background:linear-gradient(120deg,var(--p1) 0%,#9333ea 55%,var(--p2) 100%);color:#fff;padding:6mm 12mm 8mm;position:relative;overflow:hidden;}
  .band::before{content:"";position:absolute;right:-30mm;top:-45mm;width:90mm;height:90mm;border-radius:50%;background:rgba(255,255,255,.08);}
  .band::after{content:"";position:absolute;left:40%;bottom:-40mm;width:60mm;height:60mm;border-radius:50%;background:rgba(255,255,255,.06);}
  .band .in{position:relative;z-index:1;display:flex;justify-content:space-between;align-items:flex-end;gap:8mm;}
  .band .site-nav{position:relative;z-index:1;padding:0;margin:0 0 3mm;}
  .kicker{font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.8);font-weight:600;margin-bottom:6px;}
  .name{font-size:28px;font-weight:800;letter-spacing:-.9px;line-height:1.02;}
  .role{font-size:11px;font-weight:600;margin-top:6px;}
  .tag{font-size:8.8px;color:rgba(255,255,255,.8);margin-top:3px;}
  .contact{display:grid;gap:3px;flex:none;}
  .cline{display:flex;align-items:center;gap:6px;font-size:8.2px;color:rgba(255,255,255,.9);background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);padding:2px 8px 2px 6px;border-radius:20px;width:fit-content;}
  .cline svg{stroke:#fff;width:10px;height:10px;}
  .stats{position:relative;z-index:1;display:flex;gap:7px;margin-top:8px;}
  .stat{flex:1;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);border-radius:10px;padding:6px 10px;backdrop-filter:blur(4px);display:flex;align-items:baseline;gap:8px;}
  .stat .n{font-size:19px;font-weight:800;line-height:1;letter-spacing:-.5px;}
  .stat.best{flex-direction:column;align-items:flex-start;gap:2px;}
  .stat .n .u{color:#fbcfe8;}
  .stat .l{font-size:7.6px;text-transform:uppercase;letter-spacing:.8px;color:rgba(255,255,255,.85);font-weight:600;line-height:1.2;}

  .cols{display:flex;gap:8mm;padding:5mm 12mm 7mm;flex:1;}
  .main{flex:1 1 auto;min-width:0;}
  .aside{flex:0 0 55mm;}
  h2.sh{font-size:8.4px;letter-spacing:1.8px;text-transform:uppercase;font-weight:700;margin-bottom:7px;display:flex;align-items:center;gap:7px;
    background:linear-gradient(90deg,var(--p1),var(--p2));-webkit-background-clip:text;background-clip:text;color:transparent;}
  h2.sh::after{content:"";flex:1;height:1px;background:var(--line);}
  section{margin-bottom:9px;}

  .profile{font-size:9.6px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--ink);font-weight:600;}

  .tl{position:relative;padding-left:16px;}
  .tl::before{content:"";position:absolute;left:4px;top:4px;bottom:4px;width:2px;border-radius:2px;background:linear-gradient(180deg,var(--p1),var(--p2),var(--line));}
  .job{position:relative;margin-bottom:6px;}
  .job::before{content:"";position:absolute;left:-16px;top:3px;width:10px;height:10px;border-radius:50%;background:#fff;border:2.5px solid var(--p2);}
  .job.cur::before{background:linear-gradient(135deg,var(--p1),var(--p2));border-color:transparent;box-shadow:0 0 0 3px rgba(236,72,153,.18);}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:700;color:var(--ink);}
  .job .c{color:var(--p1);font-weight:600;}
  .job .p{font-size:8px;color:var(--muted);font-weight:600;white-space:nowrap;flex:none;}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"";position:absolute;left:0;top:6px;width:4px;height:4px;border-radius:1px;background:var(--p2);transform:rotate(45deg);}
  .ind{background:var(--tint);color:var(--p1);border:1px solid #e3d9f7;border-radius:20px;}
  ul.pts li b{color:var(--ink);font-weight:600;}
  ul.pts li a{color:var(--p1);font-weight:600;}
  .stack{color:var(--muted);}

  .cskill{padding:2.5px 6px 5px 0;}
  .sk-top{font-size:9.2px;font-weight:600;color:var(--ink);}
  .sk-word{font-size:8px;color:var(--muted);font-weight:500;}
  .sk-track{height:4px;border-radius:4px;background:var(--line);margin-top:5px;}
  .sk-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--p1),var(--p2));position:relative;}
  .sk-fill::after{content:"";position:absolute;right:-4px;top:-3px;width:10px;height:10px;border-radius:50%;background:#fff;border:2.5px solid var(--p2);box-shadow:0 0 0 3px rgba(236,72,153,.18);}
  .ai{background:var(--tint);border:1px solid var(--line);border-radius:10px;padding:10px 11px;position:relative;overflow:hidden;}
  .ai::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,var(--p1),var(--p2));}
  .ai .h{font-size:8px;letter-spacing:1.5px;text-transform:uppercase;color:var(--p1);font-weight:700;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:var(--p2);}
  .ai p{font-size:8.8px;line-height:1.45;color:var(--body);margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:600;padding:2px 7px;border-radius:20px;background:var(--tint);border:1px solid var(--line);color:var(--ink);}
  .ai .dchip{background:linear-gradient(90deg,var(--p1),var(--p2));border-color:transparent;color:#fff;}
  .award{font-size:8.7px;color:var(--body);padding:2.5px 0;border-bottom:1px solid var(--line);line-height:1.35;}
  .award:last-child{border-bottom:0;}
  .award b{color:var(--ink);font-weight:600;}
  .award a{color:var(--p2);font-weight:600;}
  .edu{padding:3px 0;border-bottom:1px solid var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.5px;font-weight:700;color:var(--ink);}
  .edu .m{font-size:8.2px;color:var(--muted);}
""",
    body="""<div class="sheet">
  <header class="band">
    $NAV$
    <div class="in">
      <div>
        <div class="kicker">Curriculum Vitae · 2026</div>
        <div class="name">$NAME$</div>
        <div class="role">$ROLE$</div>
        <div class="tag">$TAG$ · Zapopan, México</div>
      </div>
      <div class="contact">$CONTACT$</div>
    </div>
    $STATS$
  </header>
  <div class="cols">
    <main class="main">
      <section><h2 class="sh">Profile</h2>$PROFILE$</section>
      <section><h2 class="sh">Experience</h2>$EXP$</section>
    </main>
    <aside class="aside">
      <section>$AI$</section>
      <section><h2 class="sh">Core Skills</h2>$CORE$</section>
      <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
      <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
      <section><h2 class="sh">Education</h2>$EDU$</section>
    </aside>
  </div>
</div>""")

def finish_body(body, v):
    """Per-version header state: flag icons on ES / EN (v3 only)."""
    flags = v.get("flags", False)
    return body.replace("$FLAG_ES$", FLAG_MX if flags else "").replace("$FLAG_EN$", FLAG_US if flags else "")

# ------------------------------------------------------------------ BUILD
if __name__ == "__main__":
    for fname, v in VERSIONS.items():
        body = fill(v["body"]).replace("$AI_TEXT$", h(AI_TEXT)).replace("$AI_CHIPS$", chips_html(AI_CHIPS))
        body = finish_body(body, v)
        css = "  :root{" + v["nav"] + "}\n" + v["css"]
        html = page(v["title"], v["fonts"], css, body + "\n" + v.get("extra_js", ""))
        path = os.path.join(OUT, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote {fname} ({len(html)//1024} KB)")
        if fname == LIVE[0]:
            os.makedirs(os.path.dirname(LIVE[1]), exist_ok=True)
            with open(LIVE[1], "w", encoding="utf-8") as f:
                f.write(html)
            print(f"wrote index.html (from {fname})")
            # shell pieces for the Astro blog pages (same look, same header, same scripts)
            os.makedirs(SHELL_DIR, exist_ok=True)
            head = page("", v["fonts"], "", "")
            head = head[head.index('<script>'):head.index('<style>')]   # pre-paint theme/lang script, favicons, fonts
            head = re.sub(r"<title></title>\n|<meta name=\"description\"[^>]*>\n", "", head)   # the layout sets those per page
            scripts = re.sub(r"</?script>", "", FIT_JS + "\n" + v.get("extra_js", ""))
            for name, content in {"shell.css": BASE_CSS + "\n" + css, "head.html": head, "header.html": finish_body(nav_html("blog"), v), "shell.js": scripts}.items():
                with open(os.path.join(SHELL_DIR, name), "w", encoding="utf-8") as f:
                    f.write(content)
            print("wrote src/shell/{shell.css,head.html,header.html,shell.js}")
            # the other sections, same shell
            for rel, (active, tpl) in SITE_PAGES.items():
                body = finish_body(fill(tpl, active=active), v) + "\n" + v.get("extra_js", "")
                page_html = page(v["title"], v["fonts"], css, body)
                path = os.path.join(PUBLIC, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(page_html)
                print(f"wrote {rel} ({active})")
            for rel, target in REDIRECTS.items():
                path = os.path.join(PUBLIC, rel); os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f'<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="https://sergiowero.github.io{target}"><title>Redirecting…</title><a href="{target}">{target}</a>')
                print(f"wrote {rel} → {target}")
