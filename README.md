# Gestión de Configuración del Software — ICS G3 4K4 2026

> **Versión:** 1.0.4 | **Fecha:** 24/03/2026 | **Fecha última modificación:** 13/06/2026  
> **Materia:** Ingeniería y Calidad de Software  
> **Repositorio:**

---

## Integrantes del equipo

| Apellido y Nombre | Legajo |
|---|---|
| Carrizo Tiziana | 94506 |
| Crespo Santiago | 85516 |
| Reartes Facundo | 90208 |
| Felippa Alexis | 90843|
| Genesir Mauro | 90090 |
| Ledesma Theo | 95968 |
| Truenow Leonardo | 93109 |
| Tavella Valentino | 78973 |
| Linares Julián | 97088 |
| Sacco Juan | 89319 |

## Introducción

### Propósito del Documento

Establecer las convenciones, criterios de nombrado, organización de carpetas y lineamientos de versionado aplicables a todos los ítems de configuración del curso. Garantiza la trazabilidad y el orden de los artefactos generados durante la cursada.

### Alcance

El presente plan cubre los siguientes elementos:

- Documentación de planificación y materiales de cursada.
- Evaluaciones parciales, ejercicios resueltos y resúmenes.
- Trabajos prácticos y sus artefactos asociados (diagramas, código, resoluciones).
- Material bibliográfico de referencia.

---

## Organización del Repositorio

A continuación se describe la estructura de directorios del repositorio:

```text
ICS_G3_4K4_2026/
├── Bibliografia/
│   ├── Libros_Catedra/
│   └── Libros_Adicionales/
├── Herramientas_Cursado/
│   ├── Cronograma/
│   ├── Informacion_Catedra/
│   └── Material_de_Apoyo/
│── Parciales/
│   └── Parcial_<N>/
│       ├── Ejercicios/
│       ├── Elementos_de_Clase/
│       │   └── Clase_<N>_<FECHA>/
│       └── Resumenes/
└── Trabajos_Practicos/
    ├── Practico_<N>/
    │    └── Artefactos/
    └── Trabajo_Investigacion_<N>/    
         └── Artefactos/
```

> [!NOTE]
> `<N>` representa el número secuencial del parcial, trabajo práctico, clase u otro ítem.  
> `<FECHA>` utiliza el formato `YYYYMMDD` (ejemplo: `20260324`).

---

## Convenciones de Nombrado

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Cronograma de clases | `HC_CRON_<Año>_v<N>.pdf` | `Herramientas_Cursado/Cronograma/` |
| Programa | `HC_PROG_<Año>_v<N>.pdf` | `Herramientas_Cursado/Informacion_Catedra/` |
| Material de Apoyo | `HC_APO<N>_<Nombre>.pdf` | `Herramientas_Cursado/Material_de_Apoyo/` |

### Ítems de Parciales

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Template de Parcial | `P<N>_TEMPLATE_<Nombre>.<ext>` | `Parciales/Parcial_<N>/` |
| Ejercicio Resuelto | `P<N>_EJ<N>_<Nombre>.<ext>` | `Parciales/Parcial_<N>/Ejercicios/` |
| Resumen de Parcial | `P<N>_RES<N>_<Autor>.pdf` | `Parciales/Parcial_<N>/Resumenes/` |

### Elementos de Clase

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Presentación de Clase | `P<N>_C<N>_PRES_<Titulo>.ppt` | `Parciales/Parcial_<N>/Elementos_de_Clase/Clase_<N>_<FECHA>/` |
| Nota de Clase | `P<N>_C<N>_NOTA_<Titulo>.<formato>` | `Parciales/Parcial_<N>/Elementos_de_Clase/Clase_<N>_<FECHA>/` |

### Trabajos Prácticos

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Enunciado del TP | `TP<N>_ENUNCIADO_<Titulo>.pdf` | `Trabajos_Practicos/Practico_<N>/` |
| Artefacto del TP | `TP<N>_ART<N>_<Nombre>.<ext>` | `Trabajos_Practicos/Practico_<N>/Artefactos/` |
| Resolución del TP | `TP<N>_RESOLUCION_ITEM<N>.<ext>` | `Trabajos_Practicos/Practico_<N>/` |
| Enunciado del TI | `TI<N>_ENUNCIADO_<Titulo>.pdf` | `Trabajos_Practicos/Trabajo_Investigacion_<N>/` |
| Artefacto del TI | `TI<N>_ART<N>_<Nombre>.<ext>` | `Trabajos_Practicos/Trabajo_Investigacion_<N>/Artefactos/` |
| Resolución del TI | `TI<N>_RESOLUCION_ITEM<N>.<ext>` | `Trabajos_Practicos/Trabajo_Investigacion_<N>/` |

### Bibliografía

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Material Bibliográfico | `BIB<N>_<Tema>_<Nombre>.<formato>` | `Bibliografia/Libros_Catedra/` o `Bibliografia/Libros_Adicionales/` |

---

## Convención de Mensajes de Commit

Para mantener trazabilidad del autor y consistencia entre aportes, los mensajes de commit deben respetar el siguiente formato:

`<Legajo>: <descripcion breve del cambio>`

---

## Glosario de Abreviaturas

| Abreviatura | Significado |
|---|---|
| `P` | Parcial |
| `TP` | Trabajo Práctico |
| `BIB` | Bibliografía |
| `N` | Número secuencial (parcial, TP, ítem, etc.) |
| `EJ` | Ejercicio |
| `C` | Clase |
| `RES` | Resumen |
| `ART` | Artefacto |
| `PRES` | Presentación |
| `ICS` | Ingeniería y Calidad de Software |

## Criterios de Línea Base

Definimos como críterios de línea base del repositorio, que la misma se establezca luego de la correción de dos trabajos prácticos considerando únicamente los prácticos evaluables. Esto lo decidimos ya que consideramos que es el momento correcto ya que contamos con los ítems de configuración validos y estables. Como equipo decidimos identificar a cada versión de la línea base, con nombres de planetas. Para garantizar el orden cronológico y la trazabilidad de las versiones, utilizaremos el formato `LB_v<Numero>_<Planeta>`, donde el número indicará la secuencia de la versión y los nombres de los planetas se asignarán según su orden de proximidad al Sol.

Ejemplo:
LB_v1.0_Mercurio (Línea Base 1),
LB_v2.0_Venus (Línea Base 2),
LB_v3.0_Tierra (Línea Base 3)