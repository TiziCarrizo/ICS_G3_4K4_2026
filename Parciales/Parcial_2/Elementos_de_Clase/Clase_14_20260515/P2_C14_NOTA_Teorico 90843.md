# Clase 15-05 ISW: Filosofía Lean y Kanban

## Filosofía Lean
* **Origen**: Surge en la industria de fabricación automotriz con el fin de competir con otras empresas del sector.
* **Enfoque central**: Su premisa es hacer **"mejor con menos"**, donde la entrega al cliente es la clave absoluta y el objetivo principal es **eliminar el desperdicio**.
* **Valor**: Está orientada a entregar exclusivamente aquello que le aporta valor real al cliente.
* **Continuidad**: Se concibe como un enfoque continuo y evolutivo, no como un proceso con un final cerrado.

### Los 7 Principios de Lean
1. **Eliminar desperdicio**: Solo se produce lo que se necesita, manteniendo un stock mínimo. Es crucial minimizar las esperas, el stock, las búsquedas y los defectos.
2. **Amplificar el aprendizaje**.
3. **Tomar decisiones diarias**: Pensar activamente en el desarrollo; por ejemplo, la arquitectura de software se empieza a definir desde el primer día.
4. **Diferir compromisos**: Ayuda directamente a minimizar el desperdicio.
5. **Dar poder al equipo**.
6. **Ver el todo**: Es necesario analizar el sistema de forma holística y no por partes aisladas; la mejora de una sección nunca debe perjudicar a otra.
7. **Entregar lo antes posible**.

---

## Desperdicios (Wastes)

### Desperdicios Generales
* Talento no utilizado.
* Inventario.
* Movimientos.
* Espera.
* Transportación.
* Otros.

### Desperdicios Basados en Conocimiento (Desarrollo de Software)
* **Trabajo terminado parcialmente**: Se corresponde con el concepto de *inventario*.
* **Características extra**: Se traduce en *sobreproducción*.
* **Proceso extra**.
* **Cambio de tareas de conocimiento**: Se asocia con el *transporte*.
* **Esperas / demoras**.
* **Cambio de contexto**: Se vincula con los *movimientos*. Implica una pérdida de tiempo por no enfocarse en una sola cosa a la vez. La regla clave es: *focalizate en terminar, no en seguir empezando cosas*.
* *(Nota: En los apuntes originales se indica que faltan algunos desperdicios en esta lista)*.

---

## Kanban

### Definición y Enfoque
* Es un método (marco de trabajo) que sirve para definir, gestionar y mejorar servicios encargados de entregar trabajo del conocimiento.
* Está diseñado para la **mejora de procesos**, NO para la gestión de proyectos.
* Se centra en la optimización de un proceso continuo y sin fin.
* No define roles ni actividades específicas; provee prácticas para evolucionar a partir del aprendizaje.
* Su origen metodológico se remonta a Japón, utilizado para estudiar técnicas bajo el concepto de **JUST IN TIME** (Justo a Tiempo).

### Flujo y Capacidad
* Su meta es gestionar el flujo del proceso de forma eficiente. **Dato clave**: No hay manera de hacer que un proceso fluya si todo el equipo está operando al 100% de su capacidad.
* Los valores nos guían, mientras que las prácticas son la ejecución real de los principios.

### Valores de Kanban
* **Gestión de cambios**: Comenzar exactamente con lo que hacés ahora, identificando las actividades actuales sin modificarlas de golpe. Se busca la mejora a través de un camino evolutivo, localizando dónde están los impedimentos y cuellos de botella para resolverlos.
* **Entrega de servicios**: Enfocarse en las necesidades del cliente, promover equipos autoorganizados y establecer esquemas de revisión periódica.

### Prácticas Generales de Kanban
1. **Visualizar**: Ver las tareas a realizar y priorizarlas mediante un modelo visual que exponga claramente el flujo.
2. **Limitar el trabajo en curso (WIP)**: Evitar la multitarea; las personas no pueden estar haciendo varias cosas al mismo tiempo.
3. **Gestionar el flujo**: Lograr que las piezas de trabajo fluyan sin interrupciones.
4. **Hacer las políticas explícitas**: Definir normas y reglas de trabajo conocidas por todos. *Ejemplo: Si ingresa una pieza de trabajo crítica, se prioriza de inmediato sin importar los pendientes del tablero.*
5. **Establecer ciclos de retroalimentación**: Instancia similar a la retrospectiva de Scrum (Retrospective).
6. **Mejorar colaborativamente**: Fomentar la evolución y el crecimiento mutuo del equipo.

---

## Dinámica del Tablero y Gestión de Colas

### Modelado del Tablero y el WIP (Work in Progress)
* Se toma el proceso actual y se traslada a un tablero con tareas "en curso" y "en espera".
* Entre las distintas etapas de actividad se utilizan columnas de espera o de acumulación.
* Las tareas avanzan de columna en columna respetando los límites asignados.
* Permite detectar visualmente los **cuellos de botella** (cuando se acumulan demasiadas tareas en una etapa específica).
* **Limitar el WIP**: Restringir el trabajo en curso fomenta la conversación y la mejora continua. El WIP no es estático; se va adaptando según la dinámica del proceso.
  * *Buena práctica inicial*: Si tenés 3 testers, podés fijar un WIP de 2 (aplicando la regla general de: `cantidad de integrantes - 1`) en la primera etapa, para luego ir calibrándolo según los cuellos de botella detectados.
* **Flexibilidad**: Los miembros del equipo pueden rotar y moverse según las necesidades urgentes de cada etapa.
* **La paradoja de la capacidad**: Trabajar al 100% reduce el rendimiento general al mínimo, ya que no deja margen (holgura) para resolver impedimentos o reasignar colaboradores. Los sistemas eficaces operan con trabajadores menos saturados; se necesita holgura para maniobrar ante estancamientos. El límite de WIP asigna esta holgura de manera implícita.

### Administración de Colas
* Coordina el flujo, destrabándolo ante impedimentos y moviendo piezas para corregir cuellos de botella.
* **Regla estricta**: Nunca se deja una tarea a la mitad, siempre se termina antes de tomar otra.
* Funciona mediante un sistema **Pull** (tirar/atraer el trabajo) en lugar de **Push** (empujar el trabajo).

### División y Tipos de Trabajo
La forma de fragmentar las asignaciones varía según la definición del proceso con el que se esté trabajando. Se deben tipificar las tareas, por ejemplo:
* Requerimientos (`*reque.`)
* Bugs / Errores (`*bug`)
* Historias de usuario (`*usr`)
* *(Depende de las necesidades de modelado del equipo)*.

---

## Políticas Explícitas y Clases de Servicio

* Todas las políticas operativas deben ser consensuadas y acordadas entre las partes (equipo, clientes, stakeholders, etc.).
* Deben ser: pocas, bien definidas, visibles, aplicables en todo momento y fáciles de modificar.
* **Clases de Servicio**: Cada ítem o pieza de trabajo debe estar catalogado bajo una clase de servicio específica:
  * **Expresso**: Tareas de máxima prioridad y urgencia inmediata.
  * **Fecha fija**: Tareas con compromisos de entrega y plazos temporales estrictos.
  * **Estándar**: Sigue la regla FIFO (*First In, First Out* - Primero en entrar, primero en salir).
  * **Intangible**: Tareas destinadas a absorber variaciones de capacidad, cubrir las tipo *expresso* y resolver la holgura del sistema.

---

## Cadencias (Reuniones)
El equipo establece intervalos de tiempo fijos y regulares (cadencias) para sus eventos (pueden ser diarios, mensuales, a demanda, etc.). Las principales reuniones del flujo son:
* **Team kanban meeting**
* **Team retrospective**
* **Team replenishment meeting**

---

## Métricas Claves
Son fundamentales para la toma de decisiones y sirven como base técnica para definir los SLA (*Service Level Agreements*).

* **Lead time (LT)** Mide el tiempo total que transcurre desde que el cliente solicita el requerimiento hasta que se le entrega en mano (perspectiva del cliente).
* **Cycle time (CT)**: Mide el tiempo transcurrido entre dos puntos específicos del tablero; representa la duración de una pieza desde que inicia formalmente su proceso hasta que concluye.
* **Touch time (TT)**: Es el tiempo neto y efectivo de trabajo real invertido sobre la pieza.

### Relación Jerárquica de Tiempos
En términos de magnitud, estas métricas siempre se comportan bajo la siguiente inecuación:

$$LT \ge CT \ge TT$$