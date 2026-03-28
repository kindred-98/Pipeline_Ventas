import pandas as pd
import matplotlib

# Necesario para que Matplotlib funcione en GitHub Actions (sin entorno gráfico)
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def cargar_ventas(ruta_csv: str) -> pd.DataFrame:
    """
    Carga el CSV y devuelve un DataFrame.

    Lanza FileNotFoundError si el archivo no existe.
    Lanza ValueError si faltan columnas obligatorias.
    """

    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {ruta_csv} no existe.")

    columnas_obligatorias = {"producto", "cantidad", "precio_unitario", "mes"}

    if not columnas_obligatorias.issubset(df.columns):
        raise ValueError("El CSV no contiene las columnas obligatorias.")

    return df


def calcular_total_por_producto(df: pd.DataFrame) -> pd.Series:
    """
    Devuelve una Series con el total (cantidad x precio_unitario) por producto.
    """

    df = df.copy()
    df["total"] = df["cantidad"] * df["precio_unitario"]

    return df.groupby("producto")["total"].sum()


def top_productos(df: pd.DataFrame, n: int = 3) -> list:
    """
    Devuelve una lista con los n productos con mayor total de ventas.
    """

    totales = calcular_total_por_producto(df)
    ordenados = totales.sort_values(ascending=False)

    return list(ordenados.head(n).index)


def ventas_por_mes(df: pd.DataFrame) -> pd.Series:
    """
    Devuelve una Series con el total de ventas agrupado por mes.
    """

    df = df.copy()
    df["total"] = df["cantidad"] * df["precio_unitario"]

    return df.groupby("mes")["total"].sum()


def generar_grafico_barras(df: pd.DataFrame, ruta_salida: str) -> None:
    """
    Genera un gráfico de barras con ventas por producto y lo guarda en ruta_salida.
    """

    totales = calcular_total_por_producto(df)

    plt.figure(figsize=(8, 5))
    totales.plot(kind="bar", color="skyblue")
    plt.title("Ventas por producto")
    plt.xlabel("Producto")
    plt.ylabel("Total de ventas (€)")
    plt.tight_layout()

    plt.savefig(ruta_salida)
    plt.close()
