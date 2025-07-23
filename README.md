# Plataforma de Desarrollo Proyecto PIAESAN
PIA Proyecto de Investigación Aplicada
Tema: DISEÑO Y EVALUACIÓN DE UN MODELO DE NEUTRAL HOST NETWORK CON CAPACIDADES MULTI-ACCESS EDGE COMPUTING (MEC) COMO HABILITADOR DE INFRAESTRUCTURA DIGITAL EN ZONAS RURALES DEL NORTE DEL PERÚ

Este repositorio contiene dos módulos principales para la consulta y procesamiento de datos públicos en Perú: cobertura de redes móviles y exportaciones agropecuarias.

## 1. Cobertura de Redes Móviles (OSIPTEL)

**Archivo:** `main_coberturaredesmoviles-source_osiptel.py`

Consulta la cobertura de tecnologías móviles (2G, 3G, 4G, 5G) por provincia y distrito usando la API pública de OSIPTEL. Procesa los resultados y los exporta en formatos CSV y JSON para su análisis.

- **Entradas:** Archivos CSV con combinaciones de ubigeo por provincia/distrito. Fuente: https://www.reniec.gob.pe/Adherentes/jsp/ListaUbigeos.jsp
- **Salidas:** 
  - `cobertura_provincial.csv` / `cobertura_provincial.json`
  - `cobertura_distrital.csv` / `cobertura_distrital.json`
- **Uso:**  
  ```sh
  python main_coberturaredesmoviles-source_osiptel.py [provincial|distrital]
  ```

## 2. Exportaciones Agropecuarias (MIDAGRI)

**Archivo:** `main_exportacionesagro-source_midagri.py`

Consulta el ranking de exportaciones agropecuarias por año (2000-2024) desde la API de MIDAGRI. Procesa los datos y los exporta a un archivo CSV, mostrando también los resultados en formato tabla.

- **Entradas:** Ninguna (consulta directa a la API).
- **Salidas:** 
  - `exportaciones.csv` con los datos de exportación por año, ranking y país.
- **Uso:**  
  ```sh
  python main_exportacionesagro-source_midagri.py
  ```

## Requisitos

- Python 3.x
- Paquetes: `requests`, `tabulate` (solo para exportaciones), `csv`

## Licencia

- Libre Uso

---

Este proyecto facilita el acceso y procesamiento de datos públicos relevantes para análisis territorial y económico
