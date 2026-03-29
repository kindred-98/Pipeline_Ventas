<div align="center"> 

# 📊 Pipeline Ventas — Analizador de Ventas con Pandas y Matplotlib

[![Pipeline CI](https://github.com/kindred-98/Pipeline_Ventas/actions/workflows/pipeline.yml/badge.svg)](https://github.com/kindred-98/Pipeline_Ventas/actions/workflows/pipeline.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/kindred-98/Pipeline_Ventas/actions)
[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/tests-8%20passed-brightgreen?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![Módulo](https://img.shields.io/badge/M%C3%B3dulo-3%20%C2%B7%20Dicampus-orange)](https://github.com/kindred-98)

</div>

---

> Proyecto de análisis de datos de ventas con pipeline CI/CD automatizado.  
> Genera informes, rankings y gráficos de barras a partir de un CSV real.  
> El pipeline bloquea automáticamente si la cobertura de tests baja del 80%.

---

## 📁 Estructura del Proyecto

```
Pipeline_Ventas/
│
├── src/
│   ├── __init__.py
│   └── analizador.py          ← módulo principal (Pandas + Matplotlib)
│
├── tests/
│   ├── __init__.py
│   └── test_analizador.py     ← suite de tests (pytest + pytest-cov)
│
├── data/
│   └── ventas.csv             ← datos de prueba (9 registros, 3 meses)
│
├── docs/
│   └── Incidencia_Pipeline.md ← registro de incidencias y soluciones
│
├── requirements.txt
└── .github/
    └── workflows/
        └── pipeline.yml       ← CI/CD con cobertura mínima obligatoria
```

---

## ⚙️ Funciones del Módulo `analizador.py`

| Función | Descripción | Retorna |
|---|---|---|
| `cargar_ventas(ruta_csv)` | Carga el CSV y valida columnas obligatorias | `pd.DataFrame` |
| `calcular_total_por_producto(df)` | Calcula `cantidad × precio_unitario` por producto | `pd.Series` |
| `top_productos(df, n=3)` | Lista los N productos con mayor volumen de ventas | `list` |
| `ventas_por_mes(df)` | Agrupa el total de ventas por mes | `pd.Series` |
| `generar_grafico_barras(df, ruta_salida)` | Genera y guarda un gráfico de barras en PNG | `None` |

---

## 🚀 Instalación y Uso Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/kindred-98/Pipeline_Ventas.git
cd Pipeline_Ventas
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows (PowerShell)

pip install -r requirements.txt
```

### 3. Ejecutar los tests

```bash
# Tests básicos
pytest tests/ -v

# Tests con cobertura
pytest tests/ -v --cov=src --cov-report=term-missing

# Tests con umbral mínimo obligatorio + reporte HTML
pytest tests/ -v --cov=src --cov-report=html --cov-fail-under=80 --cache-clear
```

### 4. Ver el reporte HTML de cobertura

```bash
# Abre en el navegador tras ejecutar el comando anterior
open htmlcov/index.html          # macOS
start htmlcov/index.html         # Windows
xdg-open htmlcov/index.html      # Linux
```

---

## 🧪 Suite de Tests

| Test | Función cubierta | Tipo |
|---|---|---|
| `test_cargar_ventas_ok` | `cargar_ventas` | ✅ Éxito |
| `test_cargar_ventas_archivo_no_existe` | `cargar_ventas` | ❌ Error esperado |
| `test_cargar_ventas_columna_faltante` | `cargar_ventas` | ❌ Error esperado |
| `test_calcular_total_manzanas` | `calcular_total_por_producto` | ✅ Éxito |
| `test_top_productos_n2` | `top_productos` | ✅ Éxito |
| `test_ventas_por_mes_enero` | `ventas_por_mes` | ✅ Éxito |
| `test_generar_grafico_crea_archivo` | `generar_grafico_barras` | ✅ Éxito |
| `test_top_productos_n_mayor_total` | `top_productos` | ✅ Borde |

**Resultado:** `8/8 passed · cobertura 100% · umbral 80% superado`

---

## 🔄 Pipeline CI/CD (GitHub Actions)

El pipeline se activa automáticamente en cada `push` o `pull_request` a `main`.

```yaml
# Flujo del pipeline
Checkout → Setup Python 3.11 → Instalar dependencias
    → 🧪 Tests + cobertura mínima 80%
    → 📊 Generar reporte HTML
    → 💾 Subir artefacto htmlcov/
```

> Si la cobertura baja del **80%**, el pipeline **bloquea el merge** automáticamente.

Para descargar el reporte HTML generado por el pipeline:  
`Actions` → último run → **Artifacts** → `cobertura-html`

---

## 📦 Dependencias

```txt
pandas
matplotlib
pytest
pytest-cov
```

Instálalo todo de una vez:

```bash
pip install -r requirements.txt
```

---

## 📋 Datos de Prueba (`data/ventas.csv`)

```csv
producto,cantidad,precio_unitario,mes
Manzanas,50,1.20,enero
Naranjas,30,0.90,enero
Plátanos,80,0.60,enero
Manzanas,40,1.25,febrero
Naranjas,55,0.95,febrero
Plátanos,90,0.65,febrero
Manzanas,60,1.30,marzo
Naranjas,20,1.00,marzo
Plátanos,75,0.70,marzo
```

**Top 2 productos por ventas totales:** Manzanas (188€) · Plátanos (159.25€)

---

## 🩺 Incidencias Registradas

Durante el desarrollo del pipeline se documentaron y resolvieron 6 incidencias reales:

- Nombre de carpeta incompatible (`pipeline-ventas` → `pipeline_ventas`)
- Estructura de repositorio duplicada
- Rutas incorrectas al CSV tras reorganización
- `PYTHONPATH` no configurado en GitHub Actions
- Reporte HTML no generado por caché de pytest
- Advertencias de Node.js 20 en el runner

📄 Documentación completa: [`docs/Incidencia_Pipeline.md`](docs/Incidencia_Pipeline.md)

---

## 🎓 Contexto Académico

| Campo | Detalle |
|---|---|
| Centro | Dicampus |
| Módulo | Módulo 3 · Testing, Debugging y Documentación con IA |
| Actividad | Pipeline con Pandas y Matplotlib — Nivel Intermedio |
| Fecha | Marzo 2026 |

---
<div align="center"> 

## 👤 Autor

**A.D.E.V.** · [`kindred-98`](https://github.com/kindred-98)  
Módulo 3 · Integración de IA en Pipelines · Dicampus