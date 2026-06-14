# TDD

Invierte la lógica de desarrollo partiendo primero de las pruebas y luego desarrollar el código

TDD es proactivo: busco diseñar pruebas unitarias antes de escribir el código. Me basare en las pruebas para desarrollar

La idea es plantear lo que debo hacer antes de desarrollar

Como beneficios se genera un código mucho más robusto frente al desarrollo tradicional y asegura la cobertura de las pruebas

Corazón TDD: Ciclo Red-Green-Refactor

Primero escribimos los test sin código funcional, obligando a que las pruebas fallen (funciones vacías). Luego desarrollamos la mínima implementación para que que la prueba pase y finalmente refactorizamos para mejorar el código aplicando distintos métodos (patrones, lineamientos de diseños, etc)

 3 Leyes: 

- No escribir nada sin que se haya hecho una prueba antes, si un test no justifica una función esta no debe existir
- Con un test que falle es suficiente, no hace falta saturarse de pruebas sino hacer las necesesarias
- No escribir más código que el necesario para que la prueba pase

Los patrones de TDD nos permiten ir pasando de una parte del ciclo de desarrollo a la siguiente 

Refactoring: se busca que los cambios en el código afecten lo menos posible al código que ya validamos, “Limpiar desorden”

Para empezar con el refactoring debemos tener todas las pruebas en Green
Luego vamos a buscar partes que no sean muy claras 
Refactorizamos y ejecutamos nuevamente las pruebas hasta que queden en Green

Aplicar o no TDD depende del equipo

Siempre busco tratar de probar la mayor cantidad de código posible con la menor cantidad de casos de prueba 

Mínimamente un test por cada historia de usuario

PRACTICO: Validaciones de entrada son datos que pone el usuario. Validaciones de salida son las que hace el sistema con lógica de programación

Mensajes de éxito son clases válidas todo lo que cumpla el objetivo, mensajes de error inválidas
