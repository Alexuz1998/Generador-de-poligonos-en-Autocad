import streamlit as st
import pandas as pd
import base64

# Icono personalizado del título, incrustado para no depender de archivos externos.
TITLE_ICON_BASE64 = "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"
import io
from pathlib import Path
from PIL import Image

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

            # Los vértices se dibujan respetando el orden de la tabla
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


# --- CONFIGURACIÓN DE LA PÁGINA ---
TITLE_ICON = Image.open(
    io.BytesIO(base64.b64decode(TITLE_ICON_BASE64))
)

st.set_page_config(
    page_title="Generador LISP de Predios",
    page_icon=TITLE_ICON,
    layout="centered"
)

# ============================================================
# TEMA VISUAL — verde oscuro / dorado
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

#MainMenu, footer, header {
    visibility: hidden;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(
        circle at 50% 0%,
        #16261c 0%,
        #0b140d 45%,
        #050805 100%
    );
    background-attachment: fixed;
}

.block-container {
    max-width: 760px;
    padding-top: 2.2rem;
}

.atlas-main-title {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin: 0 auto 0.4rem auto;
}

.atlas-title-icon {
    width: 58px;
    height: 58px;
    object-fit: contain;
    flex-shrink: 0;
}

.atlas-main-title h1 {
    margin: 0 !important;
}

/* Título principal */
h1 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--atlas-text) !important;
    font-weight: 800 !important;
    text-align: center;
    letter-spacing: 0.2px;
}

/* Texto descriptivo */
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
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(
        135deg,
        var(--atlas-gold),
        #a97a34
    ) !important;

    color: #1a1206 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.55rem 1.1rem !important;
    transition: filter 0.2s ease, box-shadow 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
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
    padding: 7px 16px;
    margin-top: 1.2rem;
}

.atlas-footer-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    min-height: 72px;
}

.atlas-footer-box p {
    color: var(--atlas-text-dim) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px !important;
    text-align: center;
    margin: 0 !important;
}

.atlas-pikachu {
    width: 88px;
    height: 64px;
    display: block;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="atlas-main-title">
        <img
            class="atlas-title-icon"
            src="data:image/png;base64,{TITLE_ICON_BASE64}"
            alt="Pikachu"
        >
        <h1>Generador LISP para AutoCAD</h1>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    "Sube tus archivos Excel. La plataforma extraerá las coordenadas "
    "y generará automáticamente un único archivo **.lsp**."
)

# --- CARGA DE ARCHIVOS ---
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

# Pikachu incrustado directamente en el HTML.
# No depende de GIFs, imágenes o archivos externos.
pikachu_svg = r'''<svg class="atlas-pikachu" viewBox="0 0 180 130" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pikachu">
  <g stroke="#111111" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">
    <path d="M28 78 L8 62 L28 46 L20 28 L48 38 L55 62 Z" fill="#F5C400"/>
    <path d="M54 40 L43 7 L63 14 L72 42 Z" fill="#F5C400"/>
    <path d="M114 39 L133 10 L146 29 L125 53 Z" fill="#F5C400"/>
    <path d="M63 40 Q88 21 119 40 Q142 55 139 82 Q135 109 104 116 Q75 122 53 101 Q40 88 43 67 Q46 50 63 40 Z" fill="#F5C400"/>
    <path d="M43 7 L63 14 L61 26 L50 22 Z" fill="#222222" stroke="none"/>
    <path d="M133 10 L146 29 L139 38 L124 28 Z" fill="#222222" stroke="none"/>
    <ellipse cx="73" cy="67" rx="5" ry="7" fill="#111111"/>
    <ellipse cx="112" cy="67" rx="5" ry="7" fill="#111111"/>
    <circle cx="72" cy="65" r="1.8" fill="#FFFFFF" stroke="none"/>
    <circle cx="111" cy="65" r="1.8" fill="#FFFFFF" stroke="none"/>
    <circle cx="59" cy="83" r="7" fill="#E53935"/>
    <circle cx="126" cy="83" r="7" fill="#E53935"/>
    <path d="M84 86 Q92 92 101 86" fill="none"/>
  </g>
</svg>'''

st.markdown(
    f"""<div class="atlas-footer-box">
        <div class="atlas-footer-content">
            <p>© 2026. Sitio web creado por Emerson Gutierrez Vega.</p>
            {pikachu_svg}
        </div>
    </div>""",
    unsafe_allow_html=True
)
