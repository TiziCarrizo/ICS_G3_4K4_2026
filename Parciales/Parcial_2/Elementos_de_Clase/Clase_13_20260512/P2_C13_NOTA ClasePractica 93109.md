# Clase 13 12/5 (ICS)

El testing es para detectar defectos no errores

Niveles: 

- Unitario
- Integración
- De usuario
- De aceptación de sistema

Pruebas de caja negra: no miramos código para hacer las pruebas
Comparamos en base a las entradas las salidas esperadas para validar un resultado, de ser erróneos se ajusta y vuelve a probar

Clases de equivalencia: subconjuntos de valores que tomamos para realizar una prueba. Las clases deben ser independientes entre sí. Ej.: venta de alcohol; válido: usuario mayor a 18, inválido usuario menor o igual a 17. Los resultados deben dar distintos, lógica de programación

Valores límites: testeamos en el límite del valor que me interesa  

Para identificar condiciones y clases válidas usamos los criterios de aceptación

Para identificar casos de prueba las pruebas unitarias, por lo menos un caso de prueba por cada una 

Maximización: con la menor cantidad de casos de prueba probar la mayor cantidad de clases de equivalencia 

Clases de equivalencia de Entrada

| Condición Externa  | Clase eq válidas | Clase eq inválidas |
| --- | --- | --- |
| Estados  | 3) Libre 
4) Ocupada 
5) Solicitado
6) Fuera de servicio
***Las separamos según el comportamiento que tengan después***  | 5) Cualquier otro estado
 |
| Sistema Localización | 6) Sistema habilitado | 7) Taxi no pasa ubicación |
| Posición del mouse | 8) Posición del mouse sobre taxi | No |
| Barrio | 9) Barrio existente | 10) Barrio inexistente |
| Chapa  | 11) Patente registrada con formato xx-000-xx
12) Patente refistrada con formato xxx-000 | 12) Patente con formato incorrecto
13) Patente inexistente  |
| Usuario | 15) Usuario con permisos de admin | 16) Usuario con cualquier otro perfil |

    Separamos las clases de acuerdo al comportamiento que tengan, si me generan distintas salidas seguramente sean clases distintas

    En este caso la posición del mouse me va a dar las salidas que debo mostrar, va a ser una entrada. Donde vos posicionas el mouse (entrada) te va a dar una salida (datos del taxi y si tiene pasajero)

     La patente son dos clases distintas porque me va a dar dos salidas distintas, también por las validaciones ¿?

Clases de equivalencia de Salida

| Condición Externa | CEV | CEI |
| --- | --- | --- |
| Taxi Ocupado | 17) Muestra: 
  • Información del pasajero
  • Estado del Taxi
  • Precio,
  • Fecha y hora |  |
| Colores estado | 18) Verde, amarillo, rojo, negro |  |
| Taxi Solicitado | 19) Muestra datos del pasajero |  |
| Errores |  | 20) Sistema Localización desactivado
21) Taxi inexistente
22) …
25) Información del taxi
22) Barrio inexistente |
|  |  |  |

    Las salidas dependen de lo que muestro, si tengo un excel o un mail de salida son dos clases distintas

    Asociamos las clases inválidas a mensajes de error 

    Vamos a probar cada clase de equivalencia según el estado. La información de salida la dividimos por el estado del taxi

    Por lo menos un error por cada clase de equivalencia de entrada inválida, puede haber más

    Mensajes de confirmación y mails son clases de salidas 

    Siempre que sean los esperados, mientras más datos concretos mejor

# Casos de prueba

    Para los casos de pruebas se colocan datos concretos y se necesitan precondiociones

    Nombre tiene que ser descriptivo (tener en cuenta pruebas unitarias)

    Vamos a tener un caso de prueba por cada prueba de la User

| Número | Prioridad | Nombre | Clase de eq. | Precondiciones | Pasos  | Resultado esperado |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Alta | Ver taxis con estado “libre” para un barrio existente con su información  | 1, 6, 8, 9, 12, 15, 18, 25 |   • Usuario logueado “Moria Casan” con permisos de administrador 
  • Sistema de localización encendido y configurado en la Ciudad de Córdoba
  • El taxi Libre cargado en el sistema con patente AAA-000
  • Barrio “Alberdi” cargado en el sistema
  • Estado Libre cargado en BD |   1. El usuario Moria Casan selecciona “Ver Mapa”
  2. Moria Casan selecciona barrio “Alberdi”
  3. Moria Casan selecciona el estado Libre
  4. Moria Casan selecciona “Confirmar”
 |   5. El sistema muestra el mapa indicando el taxi libre con un ícono verde y su información 
  • Patente: AAA-000
  • Pintura: Amarillo 
  • Modelo: Fluence
  • Marca: Renault |
| 2 | Baja | Visualizar taxi en un barrio inexistente | 2, 6, 10, 11, 15, 22 |   • El usuario Moria Casan logueado con permisos de de Administrador
  • Geolocalización activa y configurada en Córdoba
  • Barrio “Alberdi” cargado en la BD
  • Taxi con chapa AA-000-AA en estado Solicitado cargado en el sistema
  • Pasajero “Salva” Solicitó el taxi: AA-000-AA
  • Estado Solicitado cargado en BD |   1. Ek usuario Moria Casan selecciona “Ver Mapa de Taxis”
  2. MC ingresa “Barrio Jardín”
  3. MC filtra por estado Solicitado
  4. MC confirma la búsqueda | 1 El sistema muestra el formulario de búsqueda
4 El mensaje muestra el mensaje de error 
”Barrio ingresado inexistente” |

    Casos de prueba de éxito [Pasa] son prioridad alta, aquellos que sean falla van a depender del impacto que tengan para el usuario van a ser media o baja.

    Datos concretos, la precondición es todo lo del taxi en conjunto

    Las opciones del desplegable deben estar cargadas en el sistema ej: estado libre

    Para casos nuevos tratar de probar clases que no probé

Tratar de maximizar, no se puede probar todo 

Para valores límites siempre pruebo en el LIMITE si me dice. Ej si puede ser 0 o 1000 pruebo con 1000, si tiene 235 no cumple. En el límite (rangos, fechas válidas). Ej 2: si el usuario puede tener 10 caracteres pruebo un nombre así 

Lógica: probas con el 1000 pero cualquier valor de ese rango cumple
