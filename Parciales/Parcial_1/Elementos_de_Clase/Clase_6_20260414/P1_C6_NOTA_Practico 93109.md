# Clase 6 - 14/04 - ICS

Idea de estimar es tratar de ver el tamaño de lo que queremos hacer

Que los equipos puedan ver y debatir el tamaño

Story Point es la medida relativa para estimar en un equipo el esfuerzo para implementar una feature

Ágil NO ES UNA METODOLOGÍA 

Pilares: 

- Transparencia
- Inspección
- Adaptación

 Todo el equipo conoce en que trabajamos, constantemente estamos bajo la inspección del cliente y si surge algún cambio nos adaptamos

4 Valores:

- Adaptación sobre el plan
- Software funcional sobre documentación
- Charla con el cliente sobre
- Individuos contentos sobre procesos y herramientas (equipos autogestionados)

12 Principios: priorizar el valor, las entregas, la comunicación en resumen. Todo se relaciona con los valores y pilares

Cuando hablamos de requerimientos nos paramos del lado de la solución (qué tiene que hacer), ágil desde el problema (cómo) ¿?

Los requerimientos en ágil los detallan los usuarios (o en su defecto algún actor interesado en usar el sistema)

US: Debería poder terminarla en una única Sprint.
El desarrollador debería poder tomar una US y no tener dudas con respecto 

- Frase verbal
- Descripción
    - Como  ***rol***  quiero  ***frase verbal***   para  ***valor de negocio***
    - Lo más importante es el valor de negocio, ***responde a lo que quiero***
    - Si no tiene para, no tiene sentido
    - El rol se relaciona con quien va a usar la funcionalidad
- Criterios de aceptación: son escritos por el Product Owner
    - Detalles que debe tener la funcionalidad para que ***el cliente la apruebe (Ej. “Generar factura en formato PDF”, relacionado con el como sin datos específicos)***
    - Puede referirse a funcional o no funcional
    - Generalmente lleva un “Debe” o “Puede” dependiendo de la obligatoriedad
    - Las condiciones previas no forman parte de los criterios. Cada US es independiente (INVEST). Si está bien aclarado el rol no va
    - Para el práctico: van a estar en el dominio. Sino, se charla con el cliente
- Pruebas de usuario: las debe poder realizar el usuario (cuestiones como si se da la conexión con la base de dato van para otro lado)
    - Permiten probar que los criterios están implementados
    - Es una ***VERIFICACIÓN***, la validación la hace el cliente
    - “Probar <frase verbal>”. Ej. Probar inscribirme a materia en horario válido - PASA
    - Se deberían escribir todos los caminos empezando con el PASA y luego desglosar todos los FALLA
    - Si uno no se cumple no se realiza nada, no se cumple el valor
    - No tienen relación 1 a 1 con criterios, pueden variar

Tanto los criterios como las pruebas están en un nivel de abstracción genérico, no completo con datos concretos sino que ***completo el campo*** de manera genérica

Tiene que quedar claro que es lo válido y que lo inválido (si uso formato inválido)

La estimación va en la tarjeta, para desarrollar siempre debe ser 13 o menos. Más que eso implica que no es del todo concreto

3 puntos claves de estimación: esfuerzo, complejidad (cuestiones funcionales ej. conexiones, muchos datos), incertidumbre. 

Incertidumbre: que no sabemos respecto a lo que tenemos que desarrollar (técnica: conexión con nube de Google o funcional: pautas sobre como debe ser una contraseña)

Esfuerzo y complejidad no van de la mano. Esfuerzo → Horas de trabajo. Complejidad → Manejo/experiencia que tengo sobre el desarrollo/tema 

De Sprint a Sprint puedo revisar la estimación

DONE es una aceptación de la US que puede ir un poco más allá de los criterios. Cuestiones particulares de producción 

Nuestra forma de priorizar es con el Product Backlog. En la tarjeta sólo pueden estar a modo de referencia. Siempre trabajamos con lo que esta más arriba en el PB (está listo para ser programado).

Spike: US con demasiada incertidumbre  

Ágil: flexibilidad en cualquier aspecto del equipo pudiendo asignarse tareas entre los miembros incluso en medio de una Sprint (che termine, te ayudo)

# Trabajo Práctico 1 - US

 Rol: 

Titular de gastos 

US: Para poder definirla tengo que ver el valor que me esta aportando como usuario.

- Registrar Usuario/Cuenta
- Cargar datos de gasto
- Consultar/Visualizar datos de gasto (en singular porque veo de a uno)
- Registrar tipo de gasto
- Modificar gasto (pensar en valor de negocio no sólo funcionalidades específicas. Me sirve más poder modificar todos los datos. Si el valor es uno solo es una sola US)
- Iniciar Sesión
- Filtrar gasto
- Registrar responsable

Diferencia entre Visualizar y Consultar: consultar puede tener filtros y visualizar muestra todo. Por esa diferencia puede o no incluir las cuestiones de los filtros

No volverse loco con iniciar sesión, cerrar o registrar usuario

***El valor de negocios es único.*** Cualquier y implica dividir en 2 US

Para el parcial quedarnos con el enunciado. Poner todas las pruebas necesarias

US: Registrar Gasto

Como Titular quiero Registrar Gasto para mantener un control sobre mis gastos

Criterios de aceptación:

- Se debe incluir Monto, tipo de gasto, fecha, si es gasto propio o no,
- Se puede modificar fecha por una anterior a la actual
- Se debe autocompletar con los datos del usuario logueado
- Se puede modificar el responsable del gasto
- Se debe autocompletar con la fecha actual

PU: 

- [ ]  Probar registrar Gasto indicando monto positivo, tipo de gasto válido, fecha, responsable - PASA
- [ ]  Probar registrar Gasto indicando monto positivo, tipo de gasto válido, responsable modificando Fecha Actual - PASA
- [ ]  Probar registrar Gasto modificando responsable
- [x]  Probar registrar Gasto indicando monto negativo - FALLA
- [ ]  Probar registrar Gasto indicando Fecha Futura - FALLA

Tener en cuenta la lógica de las fallas para no ser redundantes (si pruebo dejar vacío un campo aplica a todas las que tenga que llenar campo) ***Veo el mensaje de error que tengo que mostrar***

US 2: Consultar

Como titular quiero ***consultar*** los gastos para saber en que gasté este mes

CA: 

- Puede filtrar por: responsable, tipo de fecha, gasto
- Puede ordenar por: fecha, tipo, responsable
- Debe mostrar los campos: Fecha, Gasto, Tipo de Gasto,… (estamos permitiendo una consulta con filtros)
