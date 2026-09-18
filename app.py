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

# GIF del encabezado
# El GIF está incrustado dentro del propio archivo Python, por lo que
# Streamlit Cloud no necesita buscar un archivo externo.
GIF_BASE64 = "R0lGODlhoACgAPf/MQAAAAAABQEEAgIBAQMIBwcPFggBAQ4EARAPBhMQABUZFxsKABwYBSAmJiMYACUkEi0eAS4yLDInBDY9PTwwCD47Iz9GRklGLEpRUEs4BFNQNVVBB1hfXltfVGFKBGNqamZqYmdcMmhTCW9bFm9oSG90c3N0ZnuBf39iD4CEeoRsGYl0MYmOjIuAQ4yRhZByApednJh8TZl/DZmelZqNS6CkmqKHFaOqqqSdcqSpoaZ6J6t0C6ycU658BK+giLCTHLO5ubS5sbi9s7mjRrp2Eru9pr2AEr97EsDFvcDGxcGeBcSrP8WNF8tqEMu5ZcyZDc5/EM6oBs7U0c+RFs+TEc+2R9CUF9OfBNSNHNiwFdjcztuFFNvh3NzDT+C1B+Xr5+q7DO1NN+2sIe3SWu7AEu/17vLFBPPONvP47fP48fTGB/THBfTHFPXGB/X68/bIBPb79fb89PhGSfiMNvjKBvnQKPnYQ/n9+PtaR/xGTv6gPP7QBv/VCf/bEv///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///v///gD/ACH/C05FVFNDQVBFMi4wAwEAAAAh+QQFCAB/ACwAAAAAoACgAIYAAAAAAAUBBAICAQEDCAcHDxYIAQEOBAEQDwYTEAAVGRcbCgAcGAUgJiYjGAAlJBItHgEuMiwyJwQ2PT08MAg+OyM/RkZJRixKUVBLOARTUDVV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"

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
    width: 88px;
    height: 88px;
    object-fit: contain;
    display: block;
    filter: drop-shadow(0 0 12px rgba(138, 99, 201, 0.5));
    animation: atlas-float 2.4s ease-in-out infinite;
    transform-origin: center bottom;
    border-radius: 18px;
}

@keyframes atlas-float {
    0%, 100% { transform: translateY(0) rotate(-3deg); }
    50% { transform: translateY(-9px) rotate(3deg); }
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
            src="data:image/gif;base64,{GIF_BASE64}"
            alt="Animación de Pikachu"
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
