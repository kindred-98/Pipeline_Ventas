import os
import sys
import pytest
import pandas as pd

# Asegura que el paquete local es importable desde la carpeta tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analizador import (
    cargar_ventas,
    calcular_total_por_producto,
    top_productos,
    ventas_por_mes,
    generar_grafico_barras
)


# -------------------------
# FIXTURE: DataFrame real
# -------------------------

@pytest.fixture
def df_ventas():
    ruta = "data/ventas.csv"
    return cargar_ventas(ruta)



# -------------------------
# TESTS cargar_ventas
# -------------------------

def test_cargar_ventas_ok(df_ventas):
    assert isinstance(df_ventas, pd.DataFrame)
    assert set(df_ventas.columns) == {"producto", "cantidad", "precio_unitario", "mes"}


def test_cargar_ventas_archivo_no_existe():
    with pytest.raises(FileNotFoundError):
        cargar_ventas("data/no_existe.csv")


# NUEVO TEST: columnas incompletas → cubre la validación faltante
def test_cargar_ventas_columna_faltante(tmp_path):
    ruta = tmp_path / "mal.csv"
    ruta.write_text("producto,cantidad\nManzanas,10")

    with pytest.raises(ValueError):
        cargar_ventas(str(ruta))


# -------------------------
# TESTS calcular_total_por_producto
# -------------------------

def test_calcular_total_manzanas(df_ventas):
    totales = calcular_total_por_producto(df_ventas)
    assert round(totales["Manzanas"], 2) == 188.00


# -------------------------
# TESTS top_productos
# -------------------------

def test_top_productos_n2(df_ventas):
    resultado = top_productos(df_ventas, n=2)
    assert resultado == ["Manzanas", "Plátanos"]


# NUEVO TEST: n mayor que el número de productos → cubre rama alternativa
def test_top_productos_n_mayor(df_ventas):
    resultado = top_productos(df_ventas, n=10)
    # Debe devolver todos los productos en orden
    assert resultado == ["Manzanas", "Plátanos", "Naranjas"]


# -------------------------
# TESTS ventas_por_mes
# -------------------------

def test_ventas_por_mes_enero(df_ventas):
    ventas = ventas_por_mes(df_ventas)
    assert round(ventas["enero"], 2) == 135.00


# -------------------------
# TESTS generar_grafico_barras
# -------------------------

def test_generar_grafico_crea_archivo(df_ventas, tmp_path):
    ruta_salida = tmp_path / "grafico.png"
    generar_grafico_barras(df_ventas, str(ruta_salida))

    assert ruta_salida.exists()
    assert ruta_salida.stat().st_size > 0
