Clase 5 - 10/4 - ICS

      Estimaciones ágiles

Relacionado con el ciclo de vida Iterativo.
Trabajamos sobre → Dogmático vs pragmático
Dogmático: predecir cuantos recursos me va a llevar construir un software
Pragmático: desde la experiencia, tratar de adaptarnos en cada iteración en base a la experiencia 
Las estimaciones varían según la persona, distintos factores que no son iguales para todos y terminan incidiendo 
Conceptualmente: asumimos que hay sesgos propios del proceso y las personas que imposibilitan estimar en términos absolutos → Surgen estimaciones ágiles
La estimación es una herramienta de entrada para construir un plan (gestión tradicional). En ágil es una herramienta para el equipo. Sirve para verificar 
Nos pueden anticipar la factibilidad de un proyecto 
La estimación nos permite medir si podemos asumir un compromiso 
En ágil las estimaciones son relativas, estamos comparando entre distintos valores. La comparación nos libera de medidas absolutas. Se trabaja en equipo para poder realizar las estimaciones, además toman menos tiempo realizarlas. 
Tiene que estimar la persona que lo hace , el equipo consensua el valor
La unidad de medida van a ser los Story Points, cada equipo las define de acuerdo a las habilidad, conocimientos, experiencias, etc. 
Para determinar el tamaño vemos: Esfuerzo (cantidad de hs.), Complejidad (dificultad que tiene el código), Incertidumbre (parte de SP). 
La Story Point es una combinación de estas 3 medidas (siempre relativo para cada equipo) 
Si el nivel de duda es tan alto que no puedo plantear Story Point la planteo como Spike. Las SP se se plantean cuando tengo la certeza suficiente. Estimo las User que están por entrar 
La complejidad crece de manera Exponencial, para poder estimar se usa la serie de Fibonacci para modelar ese crecimiento
SP es relativo a la comparación y al equipo que lo define 
Las estimaciones se logran por consenso → Todos los miembros del equipo (que van a ejecutar la tarea!) deben estar de acuerdo
Planning Poker:
Asignar historia canónica, la user más sencilla que se va a trabajar 
Tomamos una de las User que van a entrar en la iteración
Cada integrante elije una carta de acuerdo a la complejidad que le supone realizarla
Revisamos si los valores convergen en complejidad
Si no, los extremos explican sus puntos de vista
Recordar modelo invest: las US deben cumplir para poder estimar (y también entrar en el PB)
Por lo general trabajamos con valores del 1 al 8 
No estimamos tareas, estimamos US. En el PB no hay tareas 
Una épica es una US arriba de 8 puntos, no puedo llegar a estimar
Las primeras estimaciones que hace un equipo son en horas luego derivan a SP. Se traducen SP a hs. 
Velocity: cantidad de SP aceptadas por el PO al finalizar una Sprint. Este valor se estabiliza a medida que el equipo empieza a entenderse. Los SP se suman si la totalidad de la feature se implemento
Plan de realease: es una aproximación estimada para el cliente de cuando le voy a presentar el producto. No es exacto sino que puede ir variando. Se hace en base a la velocidad y la totalidad de SP del proyecto, me puede dar un estimado de la cantidad de iteraciones
En Ágil no hay cronograma → el plan de Realease puede llegar a ser un equivalente pero para darle al cliente un estimado de cuando le vamos a presentar el producto
     
      Gestión de Producto

Una vez que me aseguro que el producto que estoy construyendo le agrega valor al cliente voy a empezar a construir (fundamento para arrancar). Antes de empezar a construir software quiero validar una hipótesis poniendo el menor esfuerzo posible
Más recientemente: quiero generar lealtad en el usuario, que quiera elegir mi producto/valor.  
Lo más difícil es saber que es lo que voy a construir
Agregar valor no es entregar más funcionalidades, a lo largo de todo el ciclo de vida busco agregar
Usualmente siempre ponemos el foco en los requerimientos y las tareas, que el software funcione.
Poner el foco en la experiencia implica ir más allá, 
Método Lean: poder construir un producto para aprender lo antes posible sin perder recursos
MVP: producto mínimo que busca ser una introducción del producto sin llegar a producción con la finalidad de validar la idea (Previo a beta, alpha y cualquier cosa) //Alpha, Beta ya son versiones desarrollada, el MVP el algo pre-desarrollo
Puede ser que no haya que programar, el punto es con el menor esfuerzo posible validar una hipótesis 
MVP: tiene que verse como un producto terminado aunque no sea el objetivo desarrollar. Es transversal a todo
Lo que yo espero del feedback es que sea convergente con la idea, que haya una correlación entre lo que construyo originalmente y lo que me piden. Respuestas que apuntan a una misma necesidad
El MVP es el arranque de todo, luego empieza a aparecer nuevas partes (validar necesidades, método científico al Software). 
MMF: pieza más pequeña que puede ser liberada y puedo salir a vender. No implica validación de hipótesis sino ir a vender 
MVF: sirve para testear si una característica no desarrollada por completo vale la pena desarrollar 
MVP → MMP (primer Realease del producto) → MLP
MMF es algo completamente funcional, MVF son piezas que todavía corresponden a aprendizaje para evaluar si vale la pena seguir trabajando
Cada MMF es un “paquete” que voy sumando al producto de software, crece en base a estos paquetes
MMP el foco es lanzar al mercado, funcionar y tener alcance 
“La grieta de la experiencia”
Me quiero diferenciar como producto de la competencia 
MLP: mis usuarios eligen mi producto por distintas cosas (conexión emocional, diferencias, etc.). Voy más allá de simplemente ser un producto funcional (”identidad”)
