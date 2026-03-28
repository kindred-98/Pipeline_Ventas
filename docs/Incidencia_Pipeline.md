# Incidencia Pipeline

## Resumen
- El pipeline fue corregido y ahora pasa correctamente.
- En el primer "run" local completo tras la corrección, todos los tests pasaron.
- Cobertura reportada: 100% para `pipeline_ventas/src/analizador.py`.

## Causa del primer fallo
- El primer run falló porque el paquete estaba en `pipeline-ventas` (guion) y los tests importaban `pipeline_ventas`.
- También se intentó usar `--cov=src` en lugar de `--cov=pipeline_ventas/src`.
- Error observado: `ModuleNotFoundError: No module named 'pipeline_ventas'`.

## Cómo se solucionó
1. Ajuste del paquete
   - Cambiar el nombre de la carpeta de `pipeline-ventas` a `pipeline_ventas`. 
   - Verificar que exista `pipeline_ventas/__init__.py` para ser paquete Python.
2. Ajuste en tests
   - En `tests/test_analizador.py`, agregar:
     - `sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))`.
   - Usar ruta absoluta de CSV desde carpeta de tests:
     - `os.path.join(os.path.dirname(__file__), "..", "pipeline_ventas", "data", "ventas.csv")`.
3. Ajuste CI / workflow
   - En `.github/workflows/pipeline.yml`, establecer `PYTHONPATH` en `pipeline_ventas`:
     - `echo "PYTHONPATH=${GITHUB_WORKSPACE}/pipeline_ventas" >> $GITHUB_ENV`
   - Ejecutar pytest con cobertura correcta:
     - `pytest tests/ -v --cov=pipeline_ventas/src --cov-fail-under=80`

## Detalle de ejecución
- Comando de test ejecutado:
  - `pytest tests/ -v --cov=pipeline_ventas/src --cov-fail-under=80`
- Resultado:
  - 8 tests ejecutados
  - 8 pasados
  - 0 fallos
  - 100% cobertura
- El report de cobertura se generó correctamente y el paso de validación (`--cov-fail-under=80`) fue exitoso.

## Etapa más lenta
- Como primer análisis, el paso que más tiempo consume generalmente es el de ejecución de tests + cobertura (`pytest ... --cov=...`), porque se recolecta y calcula información de cobertura.
- En la prueba de `test_generar_grafico_crea_archivo`, se genera un gráfico con Matplotlib y se escribe un archivo, lo que puede tener un ligero peso adicional en comparación con otros tests rápidos.

## Acciones realizadas
1. Se renombró el directorio `pipeline-ventas` a `pipeline_ventas` para cumplir con convenciones de importación Python.
2. Se ajustó `tests/test_analizador.py` para agregar `sys.path` y referenciar el CSV con ruta absoluta relativa al directorio de tests.
3. Se actualizó `.github/workflows/pipeline.yml` para establecer `PYTHONPATH` y usar `--cov=pipeline_ventas/src`.

## Recomendación
- Mantener `pipeline_ventas` como paquete instalable (`pip install -e .`) para evitar configuraciones manuales de `PYTHONPATH`.
- Añadir en el workflow una ejecución con `pytest --durations=5` para identificar de forma automática tests/etapas lentas futuras.
