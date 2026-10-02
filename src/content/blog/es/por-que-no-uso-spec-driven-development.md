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

Usar Spec driven development o SDD, es la opcion mas popular  que puedes ver en redes, cuando explore facebook, encuentro publicidad de cursos que te dicen que no te quedes atras aprende SDD, tratando de meter miedo y FOMO para vender, pero eso es otra historia, aqui lo que me llama la atencion es como las redes se han inundado de una metodologia que a mi parecer no esta lo suficientemente probada, simplemente aparece como una opcion popular .

Yo en lo personal, prefiero crear prompts lo mejor definido sposibles, con metas claras y ejecutar un plan mode o refinar el primot inicial usando un chat. Esto me ha funcionado mejor, avanzo mas rapido. al final mientras el codigo funcione y este bien estructurado los modelos actuales (de forntera y no frontera) pueden leer el codigo y entenderlo. El proceso de hacer el spec y que el spec viva en el code base, es similar a la idea de tener todo el codigo extensamente comentado antes d ela era de la IA, al final el codigo cambia y dejamos los comentarios olvidados, si quieres tener los comentarios actualizados, tienes que hacer mas trabajo adicional para manterner las dos piezas distintas. tal vez por eso en ningun empresa a lo que he trabajado, se oblig aa documentar todo el codigo, al final hacia mas lento el proceso, y creo que es lo mismo para el SDD.

Pero para contrastar un poco, creo que en proyectos de alta complejidad donde hay mucha interdependencia entre servicios, y esta bien tomarse su tiempo para crear el spec al inicio y tratar de cubir todos los edge cases que se puedan desde el inicio.

## Mi experiencia

En las ultimas empresas en las que he trabajado este año, en ninguna se hacia SDD, en ellas, cada quien hacia como pudiera usando claude code, no training no best practices, por lo menos tengo la suerte que estoy recibiendo training de mi empleador mas el timepo que le dedico de mi tiempo persoanl, se un poco como va la cosa en como usar de manera correcta el harness.

En cambio en proyectos personales, u nvideo jeugo y mi proyecto de codigo abierto "Agent Q", lo implemente, en el videojeugo me rendí rapidamente, ya que el videojuego lo estoy vibe codeando, en realidad no tengo claro los specs , pero en mi proyecto Agent Q al ser un proyecto mas pequeño y menos ambicioso, parecia buena idea usar SDD ya que el hype estaba por los cielos en internet. Empece con OpenSpec, fue la primera herramienta que encontre y aparte en mi empresa habian dado una charla sobre él. Al inicio me parecio mu bueno, sentia que todos mis specs estaban quedando implementados a la primera oportunidad con muy poco retrabajo. Pero note un detalle que me dejo helado, empece a acumular una candidad que me parecia absurda de spec files, eran alreadedor de 200 archivos en tan solo 2 dias de trabajo.

Mis compañeros que dieron una platica sobre eso en el trabajo, mencionaron que era una forma de evitar alucinaciones, pero creo que estaban equivocados en su declaracion, ya que las alucionaciones seguian apareciendo normalmente, el modelo me agregaba u omitia cosas , sin distincion de si utilizba o no SDD.

Por eso queria escribir esto, queria exponer lo spuntos malos que exiten en esta metodologia, y especialmente poder quejarme un poco del hype y fomo el cual venden los vende humo de internet con sus cursos de SDD.

## Que es SDD entonces?

No soy el mejor para decir que es SDD y acer la mejor definicion del mudno, dejara que cada quienb lo investigue, esta no es la finalidad de este post, pero hare un mini resumen.

SDD implica antes de escribir codigo, primero tienes que definir el spec, luego ese spec se utiliza como fuente de para la implementacion del codigo, esto es para que lo agentes de IA puedan codificar de manera mas certera, y evitar implementaciones flojas que despues necesiten refactorizacion.

La idea es hacer un plan -> tareas -> codificar.

Openspec te ayuda redactando lso specs, lo cual puede ser malo o bueno porque a veces lo hace muy bien y a veces inventa cosas, lo mejor es pasarle el mayor contexto y requerimientos por tu cuenta para que openspec lo mejore y lo convierta en un plan.


## Desmintiendo lo designios de SDD

De los features de SDD podemos sacar unos designios, estos nso dicen las ventajsa de SDD y por que es bueno, para mi es una espada de doble file, ahora explico por que cada designio.

| Designio | Mi punto de vista |
|---|---|
| Ayuda a generar mejores requerimientos y encontrar edge cases desde antes de implementar | Esto es parte verdad, pero al final, si dejas que la IA genere lso requerimientos, estas generando requerimientos incompletos y que no necesitabas |
| Los specs quedan por escrito en archivos dentro del proyecto, lo que le ayuda a los agentes para tener mejor contexto | Los specs no son la fuente de la verdad, al final siempre el codigo gana en esa carrera, depender de specs desactualizados, puede darte mas problemas a largo plazo |
| Los specs permiten trazabilidad de las decisiones | ¡en realidad necesitas trazabilidad para cambios?, para eso esta git |
| Deja un rastro que se puede revisar y auditar | Git!! | 
| Otros agentes o humanos pueden retomar la tarea sin acoplarse a un modelo en especifico | De nuevo, depender de unos specs que son generados por IA puede generar codigo que no necesitas. Otro detalle, esto tambien lo puedes hacer si por ejemplo tienes el requerimiento en un ticket de jira, no necesitas en un spec en el codigo para poder continuar una tarea. |
 

## Por qué deje de usarlo en proyectos personales

Para mis proyectos personales, en definitiva, elimine todo los specs que se habian acumulado y continue trabajando de manera directa con claude, codex y opencode. Usando plan mode y goal cada ve que se necesitara y con mis skill spersonalizados de cada proeycto, avanzo mucho mas rápido.

Si tengo que enumerar las razanoes, seria algo asi:
- Me hace ir mas lento, plan mode y direct mode funcionan perfeco.
- Genera muchos Markdown files que en subsecuentes sessiones no se usan, el modelo prefiere ir al codigo (yo tambien)
- Las alucinaciones siguen apareciendo con la misma frecuancia
- Git es mi herramienta de hacer tracking de cambios, no necesito specs.

### Spec drift

Buscando en intenet pude encontrar el termino "Spec drift", este es el nombr eusado para cuando el spec queda desfasado o desactualizado cuando hay cambios en el codigo sin actualizacion del spec. 

Esto pasa incluso cuando intentas seguir el flujo correcto de SDD, aun asi hay fixes pequeños o cambios desde otras sesiones que no son detectados en su sesion y por tanto no quedan registrados en el spec. Incluso en OpenSpec, te dicen que si el cambio es trivial, no crees un spec para ello, ¿en serio? ellos mismso estan fomentando el spec drift, si el spec no puede ser la fuente de la verdad, ¿para que lo quieres en tu proyecto?.



A mi punto de vista, el código siempre será la verdadera fuente de verdad. Los modelos en la actualidad (al momento en que escribo esto) pueden leer el codigo y entender el intent facilmente. ¿Que pasara si el agente lee el spec ve una cosa y luego encuentra en el codigo una contradiccion? en realidad un modelo no sabe distinguir entre una cosa y la otra y simplemente elegira una "verdad" al azar, pasa algo parecido si en un archivo AGENTS.md pones instrucciones contradictorias, el modelo elege cuando seguir cada una.

> *Spec Drift*: el código cambia, el markdown no.

### 3. El spec no genera codigo determinista

El modelo nunca generara el mismo codigo si como entrada tiene un spec, creo que es algoq ue se esta tratando de ahcer pero no es posible ahora mismo.

### 4. Revisar markdown no es revisar software

Que pasa si necesito revisar un bug?

Poniendo un ejemplo, quiero resolver un bug, que hago? Lo primero es entender que esta fallando, hay muchos tipos de bugs , pero se me vienen 2 ejemplos a la cabeza de un mal funcinamiento, una excepción no capturada y un funcionamiento incorrecto.

Mal funcionamiento
para el funcionamiento incorrecto, el mismo bug report ya te dice que esta ocurriendo mal. Por ejemplo, “el calculo del total es incorrecto”, “no aparece el nuevo item en la lista” o “el item aparece dos veces”. En estos casos veo muy improbable que el bug se arregle agregandole una cláusula al spec, “lso items deben aparecer una sola vez” o en el caso del item que no es visible , probablemente el spec ya tiene una cláusula “nuevos items deben aparecer en la lista”. Aquí el spec no nos sirve de mucho para encontrar el error, lo mejor es ir directo al código , encontrar el código relacionado y arreglarlo. Revisar el spec es inecesario, al final se tiene que ir al código de todo modos para buscar el error.

Excepciones/Crashes
Aqui en definitiva , creo un spec no es de utilidad al buscar una excepción o un crash, aquí es ir directo al código encontrar la error y aplicar el fix, ya sea que el fix sea solo un pequeño cambio o un refactor completo, el spec no ayuda a el mantenimiento de productos en producción.

## Mi propia forma de trabajar

al final cada proyecto es diferente, pero en general lo que yo hago y me funciona bien, es simple, le doy a mmi agente un objetivo y e indicaciones de como actuar, le digo como verificar que la tarea ha sido terminada, y si l atarea lo amerita, hago plan mod eprimero para verificar que si se v a a hace rlo que quiero. 

Todo esto es lo normal, lo que te dicen todo el mundo al iniciar a programar con estas herramientas, pero poco a poco uno va encontrando la forma de refinar los prompts y sacarles mejor probecho.

Lo resumire el promt en las siguientes secciones
- Objetivo claro y bien definido
- Criterio de aceptacion/validacion (que debe pasar para considerar terminada la tarea)
- Steering, cualquier instruccion adicional para ayudar al modelo a ir el camino que yo quiero.
- Guadrails, restricciones, cosas que no debe tocar, o comandso que no quiero que ejecute.

Con este esquema sencillo logro trabar rapido , los modelos entienden la tarea y la implementan, si hay un error sensillo se corrige en esa misma sesion, si hay un problema mas gordo, abro nueva session y paso un promt completo igual al mencionado arriba.

Tambien me he ayudado de abrir sesione ssolamente para refinar mi prompt, si lo haces dentro del mismo proyecto con claude code o codex, los modelos ex´plorarn el proeyecto para definir un mejor prompt. En post posterior explicare mas a fondo este formato preferido que tengo un skill par refinar prompts, no tiene nada de extraordinario, simplemente me ahorro unas cuantas teclas para refinar mi prompt.

## Conclusión

Mi conclusion es contundente y sencilla, SDD te alenta y hace que el trabajo de progrmar con agentes se sienta como redactar un documento pero sin ninguna ventaja. 

Creo que SDD se volvio muy popular por el hype de la IA, pero en realidad no es una metodología madura sin el respaldo de varios años que ayuden a garantizar que seguirla ayuda en algo.

Mejor mantenr los prompts consizos, bien estructurados y tener en cuenta que la IA sigue siendo hasta el momento , no determinista, agregar uan capa de markdowns no la hace determinista, aunque le duela a los aferrados  de SDD.

Invito a los que leyeron esto a reflexionar sobre SDD y sobre que cosas le ven que funcionan y que no.

