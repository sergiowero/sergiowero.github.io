---
title: "Por qué no uso Spec-Driven Development y tú tampoco deberías"
description: "SDD promete poner orden en la programación con agentes de IA. Por qué, en la práctica, prefiero iterar sobre código y tests."
pubDate: 2026-09-27
tags: ["ia", "spec-driven-development", "ingeniería de software", "opinión"]
draft: true   # esqueleto: cambia a false cuando esté escrita
---

<!--
  ESQUELETO. Cada sección trae los temas a desarrollar como viñetas; reemplázalas con tu texto.
  Los bloques de código y las tablas son ejemplos de formato: adáptalos, muévelos o bórralos.
  Los comentarios HTML como este no se ven en la página, pero sí en el código fuente: bórralos antes de publicar.

  Bloques de código (se abren con tres backticks + lenguaje):
    bash        comandos para copiar y pegar, sin prompt
    console     sesión de terminal: las líneas con "$ " son comandos, el resto es salida
    powershell  lo mismo para Windows
    diff        líneas con + / - en verde / rojo
    text        sin colores (árboles de carpetas, logs)

  Tablas: la fila de guiones define la alineación
    |---|  izquierda   |:---:|  centro   |---:|  derecha (números)
-->

## TL;DR

- La tesis en una línea.
- Qué hago en su lugar.
- El caso en el que sí lo usaría.

## Contexto: de dónde sale esta opinión

- Tu experiencia: proyectos en empresa vs. proyectos personales (juegos).
- Qué herramientas probaste, en qué proyecto y durante cuánto tiempo.
- Por qué escribirlo ahora: el hype de SDD en 2025–2026.

## Qué es Spec-Driven Development (la versión justa)

- Definición: spec en lenguaje natural → plan → tareas → código generado por un agente.
- Los tres niveles: *spec-first*, *spec-anchored* y *spec-as-source*.
- Las herramientas más conocidas y qué artefactos producen.

<!-- Ejemplo de tabla simple (alineación por defecto: izquierda). Verifica los niveles antes de publicar. -->

| Herramienta | Artefactos que genera | Nivel |
|---|---|---|
| GitHub Spec Kit | `constitution.md`, `spec.md`, `plan.md`, `tasks.md` | spec-first |
| Kiro | `requirements.md`, `design.md`, `tasks.md` | spec-first |
| Tessl | specs ligadas a cada archivo de código | spec-as-source |

<!-- Ejemplo de comandos para copiar y pegar: bloque "bash", sin "$". -->

```bash
# Instalar la CLI de Spec Kit e inicializar un proyecto para Claude Code
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify init mi-proyecto --ai claude
```

<!-- Ejemplo de estructura de carpetas: bloque "text". -->

```text
mi-proyecto/
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   ├── scripts/
│   └── templates/
└── specs/
    └── 001-login-con-sso/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        └── tasks.md
```

## Lo que SDD hace bien

- Obliga a pensar antes de pedirle código al agente.
- Le da al agente contexto que sobrevive entre sesiones.
- Deja un rastro que se puede revisar y auditar.

## Por qué no lo uso

### 1. Es waterfall con un prompt encima

- *Big design up front*: la spec se escribe cuando menos sabes del problema.
- El costo de cambiar de opinión a mitad de camino.

### 2. Dos fuentes de verdad: la spec se pudre

El código siempre será la verdadera fuente de verdad. Una lista de specs mal actualizadas solo agrega contexto innecesario y erróneo, y puede causar un efecto de bola de nieve donde, al final, la spec ya no podrá ser salvada.

- *Drift*: el código cambia, el markdown no.

<!-- Ejemplo de sesión de terminal: bloque "console". Las líneas con "$ " se pintan como comandos, el resto como salida.
     Los hashes y mensajes son de relleno: pon los de tu repo. -->

```console
$ git log --oneline -- specs/001-login-con-sso/spec.md
a1b2c3d spec: login con SSO

$ git log --oneline -- src/Auth/
f9e8d7c Sesión expira a los 15 min por auditoría
e6d5c4b Refresh token rotativo
b3a2918 Login con SSO
```

<!-- Ejemplo de diff: bloque "diff". -->

```diff
--- a/src/Auth/SessionOptions.cs
+++ b/src/Auth/SessionOptions.cs
@@ -8,7 +8,7 @@ public sealed class SessionOptions
-    public TimeSpan Expiration { get; init; } = TimeSpan.FromMinutes(30);
+    public TimeSpan Expiration { get; init; } = TimeSpan.FromMinutes(15);
```

### 3. El lenguaje natural no es una especificación

- La ambigüedad del lenguaje natural vs. la precisión del código y los tests.
- No determinismo: la misma spec produce código distinto en cada corrida.

### 4. Revisar markdown no es revisar software

- Cientos de líneas generadas que nadie lee con atención.
- La revisión se muda del diff al documento, y el diff queda sin revisar.

<!-- Ejemplo de conteo en Linux/macOS y en Windows. "NNN" es un marcador: pon tus números reales. -->

```console
$ wc -l specs/001-login-con-sso/*.md
  NNN specs/001-login-con-sso/data-model.md
  NNN specs/001-login-con-sso/plan.md
  NNN specs/001-login-con-sso/research.md
  NNN specs/001-login-con-sso/spec.md
  NNN specs/001-login-con-sso/tasks.md
  NNN total
```

```powershell
Get-ChildItem .\specs -Recurse -Filter *.md | Get-Content | Measure-Object -Line
```

### 5. La ceremonia no escala hacia abajo

- Un bug de tres líneas no necesita *requirements*, *design* y *tasks*.
- El tiempo y los tokens que se van en generar documentos.

<!-- Ejemplo de tabla con números alineados a la derecha ("---:"). Los "?" son marcadores: mide y reemplaza. -->

| Tipo de cambio | Archivos de spec | Tiempo con SDD | Tiempo sin SDD |
|---|---:|---:|---:|
| Bug fix de 3 líneas | ? | ? min | ? min |
| Endpoint nuevo | ? | ? min | ? min |
| Feature completa | ? | ? h | ? h |

### 6. Se aprende construyendo (y en juegos, todavía más)

- Descubrir el problema mientras lo resuelves.
- Prototipos desechables y *find the fun*: no se puede especificar lo que todavía no has jugado.

## Qué hago en su lugar

- Iteraciones cortas con el agente: plan efímero → diff pequeño → revisión.
- Tests como especificación ejecutable.
- Contexto persistente en `CLAUDE.md` / `AGENTS.md`, no una spec por feature.
- ADRs solo para las decisiones que sí deben sobrevivir.

<!-- Ejemplo de salida de tests: bloque "console". -->

```console
$ dotnet test
Passed!  - Failed:     0, Passed:    42, Skipped:     0, Total:    42, Duration: 1 s - Auth.Tests.dll (net8.0)

$ pytest -q
........................................                                 [100%]
40 passed in 0.84s
```

## Cuándo sí tiene sentido

- Contratos entre equipos o servicios (OpenAPI, protobuf).
- Dominios regulados donde el documento es un entregable.
- Migraciones grandes y mecánicas.
- Traspaso de trabajo entre personas o empresas.

<!-- Ejemplo de tabla con la columna central centrada (":---:"). -->

| Situación | ¿SDD? | Alternativa |
|---|:---:|---|
| Bug fix | no | Test que reproduce el bug + fix |
| Prototipo de un juego | no | Prototipo desechable |
| API pública entre equipos | sí | — |
| Dominio regulado | depende | ADR + tests de aceptación |

## Conclusión

- Retoma la tesis.
- Invita a la discusión: ¿dónde te ha funcionado a ti?

## Referencias

<!-- Verifica los links antes de publicar. -->

- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Kiro](https://kiro.dev)
- [Tessl](https://tessl.io)
- Birgitta Böckeler, [*Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl*](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
