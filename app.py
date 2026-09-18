import streamlit as st
import pandas as pd
import base64
from pathlib import Path

def procesar_excels_a_lisp(lista_archivos_excel):
    lineas_lisp = [
        ";; ==================================================",
        ";; SCRIPT AUTOLISP GENERADO AUTOMÁTICAMENTE",
        ";; ==================================================",
        "(defun c:DIBUJAR_PREDIOS ()",
        "  (setvar \"CMDECHO\" 0)",
        "  (command \"_LAYER\" \"_M\" \"PREDIOS_AUTOMATICOS\" \"_C\" \"3\" \"\" \"\")"
    ]

    total_procesados = 0

    for archivo in lista_archivos_excel:
        try:
            nombre_archivo = archivo.name
            nombre_predio = nombre_archivo.rsplit('.', 1)[0]

            df = pd.read_excel(archivo)

            # Extrae columnas D (Este) y E (Norte)
            col_este = df.iloc[:, 3]
            col_norte = df.iloc[:, 4]

            estes_limpios = pd.to_numeric(col_este, errors='coerce')
            nortes_limpios = pd.to_numeric(col_norte, errors='coerce')

            df_valido = pd.DataFrame({
                'E': estes_limpios,
                'N': nortes_limpios
            }).dropna()

            if len(df_valido) < 3:
                continue

            estes = df_valido['E'].tolist()
            nortes = df_valido['N'].tolist()

            lineas_lisp.append('  (command "_PLINE"')

            # Los vértices se dibujan respetando el orden ascendente de la tabla
            for e, n in zip(estes, nortes):
                lineas_lisp.append(f'    (list {e:.4f} {n:.4f})')

            lineas_lisp.append('    "_C")')

            centro_x = sum(estes) / len(estes)
            centro_y = sum(nortes) / len(nortes)

            lineas_lisp.append(
                f'  (command "_TEXT" "_J" "MC" '
                f'(list {centro_x:.4f} {centro_y:.4f}) 2.5 0 "{nombre_predio}")'
            )

            total_procesados += 1

        except Exception:
            continue

    lineas_lisp.append("  (setvar \"CMDECHO\" 1)")
    lineas_lisp.append(
        '  (princ "\\n¡Proceso completado! Polígonos generados con éxito.")'
    )
    lineas_lisp.append("  (princ)")
    lineas_lisp.append(")")

    return "\n".join(lineas_lisp), total_procesados


def cargar_gif_base64(ruta_gif):
    """Carga el GIF y lo convierte a Base64 para mostrarlo directamente en HTML."""
    ruta = Path(ruta_gif)

    if not ruta.exists():
        return None

    return base64.b64encode(ruta.read_bytes()).decode("utf-8")


# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Generador LISP de Predios",
    page_icon="🏗️",
    layout="centered"
)

# Animación del encabezado
# APNG HD con fondo completamente transparente y contorno negro limpio.
# Está incrustado en el propio archivo para que funcione directamente en Streamlit Cloud.
GIF_BASE64 = "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"


# ============================================================
# TEMA VISUAL — inspirado en la paleta verde oscuro / dorado
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');

:root {
    --atlas-gold: #d3a15a;
    --atlas-gold-soft: #c9974a;
    --atlas-text: #f2f1ea;
    --atlas-text-dim: #a3ada4;
    --atlas-card-bg: rgba(255,255,255,0.035);
    --atlas-card-border: rgba(211,161,90,0.28);
}

#MainMenu, footer, header {visibility: hidden;}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 50% 0%, #16261c 0%, #0b140d 45%, #050805 100%);
    background-attachment: fixed;
}

.block-container {
    max-width: 760px;
    padding-top: 2.2rem;
}

/* Emblema GIF */
.atlas-emblem-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0.6rem;
}

.atlas-gif {
    width: 176px;
    height: 176px;
    object-fit: contain;
    display: block;
}

/* Título principal */
h1 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--atlas-text) !important;
    font-weight: 800 !important;
    text-align: center;
    letter-spacing: 0.2px;
}

/* Texto descriptivo bajo el título */
div[data-testid="stMarkdownContainer"] p {
    color: var(--atlas-text-dim);
    text-align: center;
    font-size: 15.5px;
}

div[data-testid="stMarkdownContainer"] strong {
    color: var(--atlas-gold);
}

/* Zona de carga de archivos */
[data-testid="stFileUploaderDropzone"] {
    background: var(--atlas-card-bg) !important;
    border: 1.5px dashed var(--atlas-card-border) !important;
    border-radius: 16px !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] * {
    color: var(--atlas-text-dim) !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: transparent !important;
    border: 1px solid var(--atlas-gold) !important;
    color: var(--atlas-gold) !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploaderFile"] {
    background: var(--atlas-card-bg) !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploaderFile"] * {
    color: var(--atlas-text) !important;
}

/* Botones principales */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, var(--atlas-gold), #a97a34) !important;
    color: #1a1206 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.55rem 1.1rem !important;
    transition: filter 0.2s ease, box-shadow 0.2s ease;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    filter: brightness(1.08);
    box-shadow: 0 0 16px rgba(211,161,90,0.35);
}

/* Spinner */
[data-testid="stSpinner"] * {
    color: var(--atlas-text-dim) !important;
}

/* Alertas */
.stAlert {
    background: var(--atlas-card-bg) !important;
    border: 1px solid var(--atlas-card-border) !important;
    border-radius: 12px !important;
}

.stAlert * {
    color: var(--atlas-text) !important;
}

/* Divisor */
hr {
    border-color: rgba(211,161,90,0.2) !important;
}

/* Pie de página */
.atlas-footer-box {
    border: 1px solid var(--atlas-card-border);
    background: rgba(211,161,90,0.05);
    border-radius: 14px;
    padding: 12px 18px;
    margin-top: 1.2rem;
}

.atlas-footer-box p {
    color: var(--atlas-text-dim) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px !important;
    text-align: center;
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# --- EMBLEMA ANIMADO ---
st.markdown(
    f"""
    <div class="atlas-emblem-wrap">
        <img
            class="atlas-gif"
            src="data:image/png;base64,{GIF_BASE64}"
            alt="Pikachu animado"
        >
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🏗️ Generador LISP para AutoCAD")
st.markdown(
    "Sube tus archivos Excel. La plataforma extraerá las coordenadas "
    "y generará automáticamente un único archivo **.lsp**."
)

# Casilla para arrastrar archivos
archivos_subidos = st.file_uploader(
    "Arrastra tus archivos Excel aquí",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

if archivos_subidos:
    if st.button("🚀 Generar Archivo LISP"):
        with st.spinner("Procesando vértices en orden ascendente..."):
            codigo_lisp, cantidad = procesar_excels_a_lisp(archivos_subidos)

            if cantidad > 0:
                st.success(
                    f"✅ ¡Perfecto! Se procesaron {cantidad} predios sin errores."
                )

                st.download_button(
                    label="⬇️ Descargar archivo DIBUJAR_PREDIOS.lsp",
                    data=codigo_lisp,
                    file_name="DIBUJAR_PREDIOS.lsp",
                    mime="text/plain"
                )
            else:
                st.error(
                    "No se pudo extraer coordenadas válidas de los archivos."
                )

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    "<div class='atlas-footer-box'>"
    "<p>© 2026. Sitio web creado por Emerson Gutierrez Vega.</p>"
    "</div>",
    unsafe_allow_html=True
)
