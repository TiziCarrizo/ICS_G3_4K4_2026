# Nota Clase Practica Testing

**Fecha:** 12-05
**Recordatorio:** Scrum TP => Martes 26-05

## Conceptos Generales de Testing
* **Defectos $\neq$ Errores**
* **Tipos de Test:**
  * Unitarios
  * Aceptación (de sistemas, de usuario)
  * Integración

* **Pre-condición:** Armar el ambiente para llevar a cabo la prueba.
* A mayor cantidad de C.E. (Clases de Equivalencia) que puedas probar con menor cantidad de casos de prueba.

* **Clase de Equivalencia $\Rightarrow$** Independiente entre sí.
* **Condiciones externas $\rightarrow$** Entrada (usuario) $\rightarrow$ Salida

---

## Caso Práctico: Taxi Mobile (TP 8)

### 1. Tabla de Clases de Equivalencia (C.E.)

#### Entradas

| Condición Externa | C.E. Válidas | C.E. Inválidas |
| :--- | :--- | :--- |
| **Estados del taxi** | `1` Libre <br> `2` Solicitado <br> `3` Ocupado <br> `4` Fuera de Servicio | `5` Cualquier otro estado |
| **Sist. geolocalización** | `6` Sist. geolocalizacion habilitado | `7` Sist. geolocalizacion no habilitado |
| **Posicionamiento del mouse** | `8` Posición del mouse | *(Ninguna)* |
| **Barrio** | `9` Barrio existente | `10` Barrio no existente |
| **Patente** | `11` Patente reg. con formato XX-000-XX <br> `12` Patente reg. con formato XXX-000 | `13` Patente con formato incorrecto <br> `14` Patente inexistente |
| **Usuario** | `15` Usuario logeado con permisos admin | `16` Usuario no logeado <br> `17` Usuario logeado con otros permisos |

#### Salidas / Errores

| Condición Externa | C.E. Válidas | C.E. Inválidas / Errores |
| :--- | :--- | :--- |
| **Taxi ocupado** | **`18` Muestra:** Infor. del pasajero, Estado del taxi, Precio, fecha, hora inicio | |
| **Colores estado** | `19` Amarillo, Rojo, Verde, Negro | |
| **Taxi solicitado** | **`20` Muestra:** Datos del pasajero | |
| **Taxi Libre** | `25` Inf. del taxi | |
| **Errores de Sistema**| | **`21`** Sist. geolocalización inhabilitado <br> **`22`** Usuario log. con otro rol |

*(Nota: Se asume el número 25 para "Inf. del taxi" y el 31 para "Barrio inexistente").*

---

### 2. Casos de Prueba

En lugar de una tabla extensa que dificulta la lectura, los casos de prueba se detallan en formato de fichas.

#### Caso de Prueba #1
* **Prioridad:** Alta
* **Nombre:** Ver taxi con estado "libre" en un barrio existente con su información
* **Clases de Equivalencia (C.E.):** `1`, `6`, `8`, `9`, `11`, `15`, `18`, `25`

**Pre-condiciones:**
* El usuario "Maria Casan" está logeado con permisos de admin.
* Sistema de localización encendido y configurado en la ciudad de CBA.
* Barrio "Alberdi" cargado en el sistema.
* Taxi Libre cargado en el sistema con patente `AA-000-AA` conectado en el sistema de localización "Alberdi".
* Estado Libre cargado en B.D.

**Pasos:**
1. El usuario "Maria Casan" selecciona ver mapa filtrado.
2. M.C. selecciona el barrio "Alberdi".
3. M.C. selecciona el estado Libre.
4. M.C. confirma la búsqueda.

**Resultado Esperado:**
* **`5`** El sistema muestra el mapa indicando el taxi Libre con un ícono verde y su información:
  * Patente = `AA-000-AA`
  * Color = Amarillo
  * Modelo = Fluence
  * Marca = Autox

---

#### Caso de Prueba #2
* **Prioridad:** Baja
* **Nombre:** Visualizar taxi en un barrio inexistente
* **Clases de Equivalencia (C.E.):** `2`, `6`, `10`, `17`, `15`, `31`

**Pre-condiciones:**
* El usuario "Maria Casan" está logeado con permisos de admin.
* Sistema de localización encendido y configurado en la ciudad de CBA.
* Barrio "Alberdi" cargado en B.D.
* Taxi con chapa `AA-000-AA` está en estado solicitado.
* Pasajero "Sebas" solicitó el taxi `AA-000-AA`.

**Pasos:**
1. El usuario Maria Casan selecciona ver mapa de taxi.
2. M.C. ingresa el barrio "Jardin".
3. M.C. filtra por estado.
4. M.C. confirma la búsqueda.

**Resultado Esperado:**
* **`1`** Sistema muestra el formulario de búsqueda.
* **`4`** El sistema muestra el mensaje de error: *"Barrio ingresado inexistente"*.