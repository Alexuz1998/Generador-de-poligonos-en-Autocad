import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# GIF de Pikachu para el pie de página, incrustado directamente en el código.
FOOTER_PIKACHU_GIF_BASE64 = "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"

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
st.set_page_config(
    page_title="Generador LISP de Predios",
    page_icon="🏗️",
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

.atlas-footer-gif {
    width: 117px;
    height: auto;
    display: block;
    flex-shrink: 0;
    image-rendering: pixelated;
}

.atlas-title {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 7px;
    width: 100%;
}

.atlas-title-pikachu {
    width: 66px;
    height: 60px;
    display: block;
    flex-shrink: 0;
    align-self: center;
}

.atlas-title-text {
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="atlas-title">
        <div class="atlas-title-pikachu"><svg class="atlas-title-pikachu" viewBox="0 0 180 130" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pikachu">
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
</svg></div>
        <h1 class="atlas-title-text">Generador LISP para AutoCAD</h1>
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

st.markdown(
    f"""
    <div class="atlas-footer-box">
        <div class="atlas-footer-content">
            <p>© 2026. Sitio web creado por Emerson Gutierrez Vega.</p>
            <img
                class="atlas-footer-gif"
                src="data:image/gif;base64,{FOOTER_PIKACHU_GIF_BASE64}"
                alt="Pikachu animado"
            >
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
