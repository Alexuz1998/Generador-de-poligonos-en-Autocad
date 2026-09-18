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

.atlas-title {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 7px;
    width: 100%;
}

.atlas-title-pikachu {
    width: 33px;
    height: 30px;
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
    """
    <div class="atlas-footer-box">
        <div class="atlas-footer-content">
            <p>© 2026. Sitio web creado por Emerson Gutierrez Vega.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
