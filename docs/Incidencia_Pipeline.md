# 🧩 Incidencias del Pipeline — Documentación Completa

> Proyecto: **Pipeline_Ventas** · Autor: **A.D.E.V.** (`kindred-98`)  
> Estado final del pipeline: ✅ Verde — todos los tests pasan

---

## 📝 Resumen General

Durante la construcción del pipeline CI/CD para **Pipeline_Ventas** surgieron varias incidencias relacionadas con:

- Nombre de carpeta incompatible con las convenciones de importación de Python.
- Estructura duplicada del repositorio.
- Rutas internas inconsistentes tras reorganizar carpetas.
- Fallos de importación en GitHub Actions por `PYTHONPATH` no configurado.
- Cobertura reportada como `0%` pese a que los tests pasaban.
- Reporte HTML de cobertura no generado por caché de pytest.
- Advertencias del entorno de ejecución (Node.js 20).

Tras aplicar las correcciones, el pipeline:

- ✅ Ejecuta los 8 tests correctamente.
- ✅ Genera cobertura real del 100%.
- ✅ Supera el umbral mínimo del 80%.
- ✅ Sube el artefacto HTML.
- ✅ Funciona tanto en local como en GitHub Actions.

---

## 🧨 Problemas Detectados y Soluciones Aplicadas

---

### 1. Nombre de carpeta incompatible con Python (`pipeline-ventas` → `pipeline_ventas`)

**Descripción**

El directorio raíz del paquete se llamaba `pipeline-ventas` (con guion), pero Python no permite guiones en nombres de módulos. Los tests importaban `pipeline_ventas` (con guion bajo), lo que provocaba un fallo inmediato.

**Síntomas**

- `ModuleNotFoundError: No module named 'pipeline_ventas'`
- Pipeline rojo en el primer run.

**Solución**

1. Renombrar la carpeta de `pipeline-ventas` a `pipeline_ventas`.
2. Verificar la existencia de `pipeline_ventas/__init__.py` para que Python lo reconozca como paquete.

---

### 2. Estructura duplicada del repositorio

**Descripción**

El repositorio tenía una carpeta anidada con el mismo nombre:

```
Pipeline_Ventas/
    Pipeline_Ventas/
        src/
        tests/
```

Esto impedía que Python encontrara el módulo `src` y que pytest-cov pudiera medir cobertura.

**Síntomas**

- `Module src was never imported`
- `No data was collected`
- Cobertura = 0%
- Pipeline fallando por `--cov-fail-under=80`

**Solución**

Reorganizar el repositorio moviendo todas las carpetas a la raíz:

```
src/
tests/
data/
.github/
requirements.txt
```

Eliminar la carpeta duplicada y añadir `src/__init__.py` para que Python reconozca el paquete.

---

### 3. Rutas incorrectas al CSV

**Descripción**

Los tests buscaban el archivo de datos en:

```
pipeline_ventas/data/ventas.csv
```

pero tras la reorganización del repositorio, la ruta correcta pasó a ser:

```
data/ventas.csv
```

**Síntomas**

- `FileNotFoundError: ... pipeline_ventas/data/ventas.csv no existe`
- Tests fallando antes de ejecutar lógica.
- Cobertura bajando al 55%.

**Solución**

Actualizar el fixture en `tests/test_analizador.py`:

```python
ruta = "data/ventas.csv"
```

Para máxima robustez también se usó ruta absoluta relativa al directorio de tests:

```python
os.path.join(os.path.dirname(__file__), "..", "data", "ventas.csv")
```

---

### 4. `PYTHONPATH` no configurado en GitHub Actions

**Descripción**

En local Python encontraba `src/` sin problemas, pero GitHub Actions no lo incluía en el path de importación.

**Síntomas**

- pytest ejecutaba los tests, pero coverage no detectaba imports.
- Mensajes de `module-not-imported`.

**Solución**

Añadir al workflow `.github/workflows/pipeline.yml`:

```yaml
- name: Añadir src al PYTHONPATH
  run: echo "PYTHONPATH=$PYTHONPATH:$(pwd)" >> $GITHUB_ENV
```

En la variante con estructura `pipeline_ventas/src`, el equivalente es:

```yaml
run: echo "PYTHONPATH=${GITHUB_WORKSPACE}/pipeline_ventas" >> $GITHUB_ENV
```

---

### 5. Reporte HTML de cobertura no generado

**Descripción**

El pipeline intentaba subir `htmlcov/` como artefacto, pero la carpeta no existía porque pytest usaba caché y omitía la generación del reporte.

**Solución**

Añadir `--cache-clear` al comando de pytest para forzar la ejecución completa y la generación de `htmlcov/`:

```yaml
pytest tests/ -v --cov=src --cov-report=html --cache-clear --cov-fail-under=80
```

---

### 6. Advertencias del runner (Node.js 20)

**Descripción**

GitHub Actions mostró advertencias indicando que algunas acciones usan Node.js 20, que quedará obsoleto en 2026.

**Impacto**

Solo informativo. No afecta al funcionamiento del pipeline actual.

**Recomendación**

Revisar periódicamente las versiones de las actions usadas (`actions/upload-artifact`, `actions/checkout`, etc.) y actualizar a las que soporten Node.js 22+ cuando sea necesario.

---

## 📊 Resultado Final

| Elemento          | Estado                   |
|-------------------|--------------------------|
| Tests             | 8/8 pasados              |
| Cobertura         | 100%                     |
| Reporte HTML      | Generado correctamente   |
| Artefacto         | Subido                   |
| Pipeline          | ✅ Verde                 |
| Umbral 80%        | Superado                 |

---

## 🐢 Etapa Más Lenta del Pipeline

La etapa más costosa es la ejecución de tests con cobertura:

```bash
pytest tests/ -v --cov=src --cov-report=html --cache-clear --cov-fail-under=80
```

**Motivos:**

- Cálculo de cobertura línea a línea.
- Generación del gráfico con Matplotlib en `test_generar_grafico_crea_archivo` (escritura de archivo).
- Lectura del CSV desde disco.

**Recomendación:** añadir `--durations=5` al comando para identificar automáticamente los tests más lentos en futuras ejecuciones.

---

## 📌 Recomendaciones Finales

1. **Estructura estable** — No renombrar ni mover carpetas sin actualizar rutas en tests y workflow.
2. **Paquete instalable** — Convertir el proyecto con `pip install -e .` para eliminar la necesidad de manipular `PYTHONPATH` manualmente.
3. **Detección de tests lentos** — Añadir `pytest --durations=5` al pipeline.
4. **Actualización de actions** — Revisar periódicamente las advertencias de Node.js en GitHub Actions.