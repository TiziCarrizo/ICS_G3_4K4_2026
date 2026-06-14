# Clase 31/3 ICS

# Introducción Ágil

## Valores Ágiles

Priorizar procesos donde se relacionan individuos
No podés dedicar más tiempo a la construcción que a la entrega
Nuestros contratos van a ser FLEXIBLES, priorizando la relación con el cliente
Dejar de lado dificultades para responder a los cambios

Definición de Proceso vs. definición de ciclo de vida: 

## Principios manifiesto ágil

El agilismo no es para cualquier contexto ni cualquier equipo, se deben cumplir los valores. 

 NO es una metodología ni un proceso, es una ideología 

Compromiso entre nada de proceso y demasiado proceso, sacar la burocracia de los procesos definidos y el anarquismo de nada definido

Son orientados a la gente en lugar de al proceso 

Se tiene un plan y una arquitectura. 

No se trabaja en pedazos sino en algo que funcione, que devuelva valor funcional

## Requerimientos Ágiles

Los requerimientos ágiles son guiados por los principios y valores, luego los describimos. 

Voy a centrarme en el valor de una feature, trabajar con lo suficiente, charlar con el cliente

Trabajar fuertemente en los requerimientos que se usan siempre, a menudo y a veces, el 80/20 

1er aspecto: Responder de manera eficiente ante el cambio, para ello trabajar priorizando requerimientos de acuerdo a EL VALOR DE NEGOCIO QUE APORTAN 
Trabajar con requerimientos que están en la parte superior, estos pueden ir cambiando
Analizo cuando lo necesito, el momento justo

2do aspecto: mecanismo de comunicación, ideal cara a cara en un pizarrón. Contraste mandar en papel CU al cliente, al olvido

En requerimientos ágil nos enfocamos en requerimientos de usuario y de negocio, pensamos más en el dominio del problema

Importante: Tradicional vs. Ágil. Planteamos iteraciones cuya salida tiene que ser un producto desplegable en producción.
En tradicional decimos cuantos requisitos hacemos por iteración variando el tiempo y los recursos. En ágil defino el tiempo y recursos (una sprint de 2 semanas y 5 personas) en base a eso defino las features que implemento.
En ágil quiero tener una cadencia de entregas fijas donde en todas se da una funcionalidad 
    Los requerimientos en tradicional pueden cambiar y las implementaciones se dan en periodos de tiempo disparejos

## Principios ágiles relacionados a los requerimientos

## User Stories

Están dentro de los requerimientos ágiles. Lo importante es el valor que aportan   

Card, Conversation, Confirmation → Conversación es lo más importante, sin embargo, deben estar escritas. Ahí determino el valor que deben tener

Son multipropósito:

- Identifico necesidad de usuario
- Mecanismo para diferir una conversación
- Ítem de planificación

El PO prioriza las historias de acuerdo a su valor de negocio. Más arriba, más detalle; de acuerdo a su posición varía el detalle debido a la implementación inminente 

Posiciones verticales: todo debe ser tenido en cuenta de forma transversal para dar una implementación certera. DESARROLLO TODO LO NECESARIO PARA DESPLEGAR, CADA ASPECTO

Modelado de Roles: el rol define el valor de negocio, de acuerdo a un rol puede ser mayor o menor. 

Criterios de aceptación: define lo que el PO va a ver cuando le entreguemos la historia. 

- Definen límites para la User
- Ayuda a definir lo que aporta valor
- Ayuda a definir las pruebas

De manera ideal se plantea que el PO sea quien defina las User Stories

## DOR

Arriba en el PB historias con suficiente detalle para estar en una iteración

Cada equipo define el nivel de preparación que debe tener una User para entrar en iteración

Sin embargo, el modelo INVEST define el piso que deberían tener 

- I → Independientes, cada una debe funcionar de manera independiente a las demás
- N Negociables
- V Valor para el cliente
- E debo decir el esfuerzo que tiene
- S debe poder implementar en una iteración
- T demostrar que cumple con las pruebas de aceptación

CUANDO PUEDE SER INCLUÍDA PARA EMPEZAR A DESARROLLAR

## DONE

Definición del equipo donde se plantean los requisitos para poder agregar al incremento   

CUANDO PUEDE SER DEPLEGADA EN PRODUCCIÓN 

Si el PO acepta la incluyo en el incremento (producción finalizada)

DoR es que la US esté bien definida y DoD una vez que fue desarrollada exitosamente desde el lado técnico

## SPIKE

 Tipo especial de US

Incertidumbre tan grande que no se puede estimar el esfuerzo que va a llevar la user (ej: API no sé como funciona) (o ej funcional: no puedo interpretar lo que el usuario definió)

En este caso estimamos el esfuerzo que nos puede llevar realizar la investigación
