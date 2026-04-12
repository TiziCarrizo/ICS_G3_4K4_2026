# Gestión de Configuración del Software — ICS G3 4K4 2026

> **Versión:** 1.0.3 | **Fecha:** 24/03/2026 | **Fecha última modificación:** 07/04/2026  
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

```
ICS_G3_4K4_2026/
├── Parciales/
│   └── Parcial_<N>/
│       ├── Ejercicios/
│       ├── Elementos de clase/
│       │   └── Clase_<N>_<FECHA>/
│       ├── Parciales Viejos/
│       └── Resúmenes/
├── TrabajosPracticos/
│   └── Practico_<N>/
│       └── Artefactos/
└── Bibliografia/
    ├── Ignenieria de Software/
    ├── SCM
    ├── Testing de software
    ├── TDD
    ├── Agilismo
    ├── Lean y Kanban
```

> [!NOTE]
> `<N>` representa el número secuencial del parcial, trabajo práctico, clase u otro ítem.  
> `<FECHA>` utiliza el formato `YYYYMMDD` (ejemplo: `20260324`).

---

## Convenciones de Nombrado

### Ítems de Parciales

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Template de Parcial | `P<N>_TEMPLATE_<Nombre>.pdf` | `Parciales/Parcial_<N>/` |
| Ejercicio Resuelto | `P<N>_EJ<N>_<Nombre>.<ext>` | `Parciales/Parcial_<N>/Ejercicios/` |
| Parcial de Año Anterior | `P<N>_<Año>_<Tema>.pdf` | `Parciales/Parcial_<N>/Parciales Viejos/` |
| Resumen de Parcial | `P<N>_RES<N>_<Autor>.pdf` | `Parciales/Parcial_<N>/Resúmenes/` |

### Elementos de Clase

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Presentación de Clase | `P<N>_C<N>_PRES_<Titulo>.ppt` | `Parciales/Parcial_<N>/Elementos de clase/Clase_<N>_<FECHA>/` |
| Nota de Clase | `P<N>_C<N>_NOTA_<Titulo>.<formato>` | `Parciales/Parcial_<N>/Elementos de clase/Clase_<N>_<FECHA>/` |

### Trabajos Prácticos

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Enunciado del TP | `TP<N>_ENUNCIADO_<Titulo>.pdf` | `TrabajosPracticos/Practico_<N>/` |
| Artefacto del TP | `TP<N>_ART<N>_<Nombre>.<ext>` | `TrabajosPracticos/Practico_<N>/Artefactos/` |
| Resolución del TP | `TP<N>_RESOLUCION_ITEM<N>.<ext>` | `TrabajosPracticos/Practico_<N>/` |

### Bibliografía

| Ítem | Formato del Nombre | Ubicación |
|---|---|---|
| Material Bibliográfico | `BIB<N>_<Nombre>.<formato>` | `Bibliografia/` |

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
Definimos como críterios de línea base del repositorio, que la misma se establezca luego de la correción de dos trabajos prácticos considerando únicamente los prácticos evaluables. Esto lo decidimos ya que consideramos que es el momento correcto ya que contamos con los ítems de configuración validos y estables. Como equipo decidimos identificar a cada versión de la línea base, con nombres de planetas.
