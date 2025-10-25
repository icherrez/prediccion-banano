# ============================================================
# Pruebas ligeras para la interfaz Tkinter y utilidades de app.py
# Ejecuta con: pytest -q
# ============================================================

import os
import sys
import types
import numpy as np
import pandas as pd
import pytest

# Evitar backends interactivos de Matplotlib en CI/headless
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Importar la app
# Estructura esperada: repo_root/app/app.py
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "app"))

# Import directo de símbolos necesarios de app.py
import app as appmod  # app/app.py


# -----------------------------
# Skips/markers útiles
# -----------------------------
def _has_display():
    # En Linux headless, DISPLAY suele no estar
    if sys.platform.startswith("linux"):
        return bool(os.environ.get("DISPLAY"))
    # En Windows/macOS normalmente OK
    return True

# Marcador opcional si quieres saltar tests Tk con problemas de display
tk_skip = pytest.mark.skipif(not _has_display(), reason="No DISPLAY disponible (entorno headless)")


# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def mini_df():
    """DataFrame mínimo válido para la app."""
    data = {
        "Año":   [2025, 2025, 2025, 2025, 2025, 2025, 2025],
        "Semana":[10,   11,   12,   13,   14,   15,   16],
        "Precio":[1.00, 1.02, 1.05, 1.01, 1.08, 1.10, 1.12],
    }
    return pd.DataFrame(data)


# -----------------------------
# Tests de VentanaProgreso
# -----------------------------
@tk_skip
def test_ventana_progreso_init_add_close():
    vp = appmod.VentanaProgreso()
    # Debe crear atributos básicos
    assert hasattr(vp, "ventana")
    assert hasattr(vp, "texto")
    # Agregar un texto y asegurar que no rompe
    vp.agregar_texto("Prueba de mensaje en ventana.")
    # Cerrar
    vp.cerrar()


# -----------------------------
# Test de cargar_excel_desde_dialogo con mocks
# -----------------------------
@tk_skip
def test_cargar_excel_desde_dialogo_mocks(monkeypatch, mini_df):
    vp = appmod.VentanaProgreso()

    # Mockear askopenfilename para devolver una ruta ficticia
    dummy_path = os.path.join(REPO_ROOT, "app", "assets", "precio_ecuador.xlsx")
    monkeypatch.setattr(appmod.filedialog, "askopenfilename", lambda **kwargs: dummy_path)

    # Mockear pd.read_excel para devolver nuestro mini_df
    monkeypatch.setattr(appmod.pd, "read_excel", lambda path: mini_df.copy())

    df, ruta = appmod.cargar_excel_desde_dialogo()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(mini_df)
    assert ruta == dummy_path

    vp.cerrar()


# -----------------------------
# Test: embebido de gráfico en frame_grafico
# -----------------------------
@tk_skip
def test_embed_matplotlib_in_frame():
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    vp = appmod.VentanaProgreso()

    # Crear figura simple
    fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
    ax.plot([0, 1, 2], [1.0, 1.1, 1.2])
    ax.set_title("Test Plot")

    # Insertar en frame_grafico (como en el código de 'bloque 13')
    canvas = FigureCanvasTkAgg(fig, master=vp.frame_grafico)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(row=0, column=0, sticky="nsew")

    # El widget debe pertenecer al frame_grafico
    assert widget.master == vp.frame_grafico

    vp.cerrar()

