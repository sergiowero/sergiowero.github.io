---
title: "Por qué no uso Spec-Driven Development y tú tampoco deberías"
description: "SDD promete poner orden en la programación con agentes de IA. En la práctica, prefiero iterar sobre código y tests."
pubDate: 2026-09-27
tags: ["ia", "spec-driven-development", "ingeniería de software", "opinión"]
draft: false
---

## TL;DR

Usar Spec-Driven Development, o SDD, es probablemente la opción más popular que puedes ver en redes. Cuando exploré Facebook, me encontré con publicidad de cursos que te dicen que no te quedes atrás, que aprendas SDD, tratando de meter miedo y FOMO para venderte la idea. Eso es otra historia. Lo que más me llama la atención es cómo las redes se han inundado de una metodología que, a mi parecer, no está suficientemente probada y que simplemente aparece como una opción “popular”.

Yo, en lo personal, prefiero crear prompts lo más bien definidos posible, con metas claras, y ejecutar un plan mode o refinar el prompt inicial usando un chat. Eso me ha funcionado mejor y me permite avanzar más rápido. Al final, mientras el código funcione y esté bien estructurado, los modelos actuales —de frontera y no frontera— pueden leer el código y entenderlo. El proceso de crear un spec y hacer que ese spec viva en el codebase es similar a la idea de tener todo el código extensamente comentado antes de la era de la IA: al final, el código cambia y dejamos los comentarios olvidados. Si quieres mantenerlos actualizados, tienes que hacer trabajo adicional para mantener dos piezas distintas sincronizadas. Tal vez por eso, en ninguna empresa en la que he trabajado, se ha obligado a documentar todo el código. Al final, eso hace más lento el proceso, y creo que pasa lo mismo con SDD.

Eso sí, para contrastar un poco, creo que en proyectos de alta complejidad, con mucha interdependencia entre servicios, sí puede valer la pena tomarse su tiempo para crear el spec al inicio y tratar de cubrir todos los edge cases posibles desde el principio.

## Mi experiencia

En las últimas empresas en las que he trabajado este año, ninguna usaba SDD. En ellas, cada quien hacía como podía usando Claude Code, sin entrenamiento ni best practices claros. Por lo menos tengo la suerte de que mi empleador me da training para aprender a menajr estos harnesses.

En cambio, en proyectos personales —un videojuego y mi proyecto de código abierto Agent Q— lo implementé. En el videojuego me rendí rápido, porque lo estoy haciendo con vibe coding y, en realidad, no tengo claro los specs. Pero en Agent Q, al ser un proyecto más pequeño y menos ambicioso, parecía buena idea usar SDD, ya que el hype estaba por los cielos en internet. Empecé con OpenSpec; fue la primera herramienta que encontré y además, en mi empresa, habían dado una charla sobre ella. Al inicio me pareció muy bueno: sentía que todos mis specs estaban quedando implementados a la primera con muy poco retrabajo.

Pero noté un detalle que me dejó helado: empecé a acumular una cantidad que me parecía absurda de spec files. Eran alrededor de 200 archivos en solo 2 días de trabajo.

Mis compañeros que dieron una charla sobre eso en el trabajo mencionaron que era una forma de evitar alucinaciones, pero creo que estaban equivocados. Las alucinaciones seguían apareciendo normalmente: el modelo me agregaba o omitía cosas, sin distinción de si usaba o no SDD.

Por eso quería escribir esto: quería exponer los puntos malos que existen en esta metodología, y sobre todo quejarme un poco del hype y del FOMO que venden los “vendedores de humo” de internet con sus cursos de SDD.

## ¿Qué es SDD entonces?

No soy el mejor para decir qué es SDD ni para dar la mejor definición del mundo, así que dejaré que cada quien lo investigue; esa no es la finalidad de este post. Pero haré un mini resumen.

SDD implica que, antes de escribir código, primero debes definir el spec. Luego, ese spec se usa como fuente para la implementación del código con la idea de que los agentes de IA puedan codificar de manera más certera y evitar implementaciones flojas que después necesiten refactorización.

La idea es: plan -> tareas -> codificar.

OpenSpec te ayuda a redactar los specs, lo cual puede ser bueno o malo. A veces lo hace muy bien y a veces inventa cosas. Lo mejor es pasarle el mayor contexto y los requisitos por tu cuenta para que OpenSpec lo mejore y lo convierta en un plan.

## Desmintiendo los designios de SDD

De las promesas de SDD se pueden sacar varios designios: son los argumentos que normalmente dicen por qué SDD es bueno. Para mí, es una espada de doble filo, y ahora explico por qué cada uno.

| Designio | Mi punto de vista |
|---|---|
| Ayuda a generar mejores requerimientos y encontrar edge cases antes de implementar | Esto tiene parte de verdad, pero al final, si dejas que la IA genere los requisitos, estás generando requerimientos incompletos y que no necesitabas |
| Los specs quedan por escrito en archivos dentro del proyecto, lo que ayuda a los agentes a tener mejor contexto | Los specs no son la fuente de la verdad; al final, siempre el código gana esa carrera. Depender de specs desactualizados puede darte más problemas a largo plazo |
| Los specs permiten trazabilidad de las decisiones | ¿En realidad necesitas trazabilidad para cambios? Para eso está Git |
| Dejan un rastro que se puede revisar y auditar | Git, otra vez |
| Otros agentes o humanos pueden retomar la tarea sin acoplarse a un modelo en específico | De nuevo, depender de specs generados por IA puede producir código que no necesitas. Además, esto también puedes hacerlo con un ticket de Jira o un issue bien escrito. No necesitas un spec en el código para continuar una tarea |

## Por qué dejé de usarlo en proyectos personales

En mis proyectos personales, eliminé casi todos los specs que se habían acumulado y continué trabajando directamente con Claude, Codex y OpenCode. Usando plan mode y goal mode cada vez que hacía falta, y con mis skills personalizados por proyecto, avanzo mucho más rápido.

Si tengo que enumerar las razones, sería algo así:

- Me hace ir más lento; plan mode y direct mode funcionan mejor.
- Genera muchos archivos Markdown que, en sesiones posteriores, no se usan. El modelo prefiere ir directamente al código, y yo también.
- Las alucinaciones siguen apareciendo con la misma frecuencia.
- Git es mi herramienta de tracking de cambios; no necesito specs.

### Spec drift

Buscando en internet pude encontrar el término “spec drift”. Es el nombre que se usa cuando el spec queda desfasado o desactualizado porque el código cambia sin que el spec se actualice.

Esto pasa incluso cuando intentas seguir el flujo correcto de SDD. Aun así, hay fixes pequeños o cambios desde otras sesiones que no son detectados en la sesión actual y, por tanto, no quedan registrados en el spec. Incluso en OpenSpec te dicen que, si el cambio es trivial, no crees un spec para ello. ¿En serio? Ellos mismos están fomentando el spec drift. Si el spec no puede ser la fuente de la verdad, ¿para qué lo quieres en tu proyecto?

A mi punto de vista, el código siempre será la verdadera fuente de verdad. Los modelos actuales pueden leer el código y entender muy bien la intención. ¿Qué pasa si el agente lee el spec, ve una cosa, y luego encuentra en el código una contradicción? En realidad, un modelo no sabe distinguir entre una cosa y la otra y simplemente elegirá una “verdad” al azar. Pasa algo parecido si en un archivo AGENTS.md pones instrucciones contradictorias: el modelo elige qué seguir.

> *Spec Drift*: el código cambia, el markdown no.

### El spec no genera código determinista

El modelo nunca generará el mismo código si como entrada tiene un spec. Creo que es algo que se está intentando hacer, pero no es posible ahora mismo.

### Revisar markdown no es revisar software

¿Qué pasa si necesito revisar un bug?

Pongamos un ejemplo: quiero resolver un bug. ¿Qué hago? Lo primero es entender qué está fallando. Hay muchos tipos de bugs, pero se me vienen dos ejemplos a la cabeza: una excepción no capturada y un mal funcionamiento.

#### Mal funcionamiento

En el caso de un funcionamiento incorrecto, el mismo bug report ya te dice qué está ocurriendo mal. Por ejemplo: “el cálculo del total es incorrecto”, “no aparece el nuevo item en la lista” o “el item aparece dos veces”. En estos casos, veo muy improbable que el bug se arregle agregándole una cláusula al spec: “los items deben aparecer una sola vez”, o en el caso del item que no es visible, probablemente el spec ya tiene una cláusula que dice “los nuevos items deben aparecer en la lista”. Aquí el spec no nos sirve de mucho para encontrar el error. Lo mejor es ir directo al código, localizar la parte relacionada y arreglarla. Revisar el spec es innecesario; al final, de todos modos hay que ir al código para buscar la causa.

#### Excepciones / crashes

Aquí, en definitiva, un spec no sirve para nada a la hora de buscar una excepción o un crash. Lo correcto es ir directo al código, encontrar el error y aplicar el fix, ya sea un pequeño cambio o un refactor completo. El spec no ayuda al mantenimiento de productos en producción.

## Mi propia forma de trabajar

Al final, cada proyecto es diferente, pero en general lo que yo hago y me funciona bien es simple: le doy a mi agente un objetivo claro y unas indicaciones de cómo actuar. Le digo cómo verificar que la tarea ha sido terminada, y si la tarea lo amerita, hago plan mode primero para confirmar que realmente va a hacer lo que quiero.

Todo esto es lo normal, lo que te dicen todos al empezar a programar con estas herramientas. Pero poco a poco uno va encontrando la forma de refinar los prompts y sacarles mejor provecho.

Para resumir, mis prompts tienen lo siguiente:

- Objetivo claro y bien definido.
- Criterios de aceptación / validación: qué debe pasar para considerar la tarea terminada.
- Steering: cualquier instrucción adicional que ayude al modelo a ir por el camino deseado.
- Guardrails: restricciones, cosas que no debe tocar y comandos que no quiero que ejecute.

Con este esquema sencillo logro trabajar rápido. Los modelos entienden la tarea y la implementan. Si hay un error sencillo, se corrige en esa misma sesión. Si hay un problema más gordo, abro una nueva sesión y paso un prompt completo igual al de arriba.

También me ha ayudado abrir sesiones solo para refinar mi prompt. Si lo haces dentro del mismo proyecto con Claude Code o Codex, los modelos exploran el proyecto para definir un mejor prompt. En un post posterior explicaré más a fondo este formato preferido que tengo para refinar prompts; no tiene nada de extraordinario, simplemente me ahorro unas cuantas teclas.

## Conclusión

Mi conclusión es contundente y sencilla: SDD te alienta y hace que el trabajo de programar con agentes se sienta como redactar un documento, pero sin ninguna ventaja real.

Creo que SDD se volvió muy popular por el hype de la IA, pero en realidad no es una metodología madura ni tiene el respaldo de años de evidencia que garanticen que seguirla ayuda en algo.

Mejor mantener los prompts claros, bien estructurados y tener en cuenta que la IA sigue siendo, hasta el momento, no determinista. Agregar una capa de markdown no la vuelve determinista, aunque a los más aferrados a SDD les duela.

Invito a los que leyeron esto a reflexionar sobre SDD y a cuestionar qué cosas le ven que funcionan y cuáles no.

