import streamlit as st
import pandas as pd

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
            
            df_valido = pd.DataFrame({'E': estes_limpios, 'N': nortes_limpios}).dropna()
            
            if len(df_valido) < 3:
                continue
            
            estes = df_valido['E'].tolist()
            nortes = df_valido['N'].tolist()
            
            lineas_lisp.append("  (command \"_PLINE\"")
            
            # Los vértices se dibujan respetando el orden ascendente de la tabla
            for e, n in zip(estes, nortes):
                lineas_lisp.append(f'    (list {e:.4f} {n:.4f})')
            lineas_lisp.append('    "_C")')
            
            centro_x = sum(estes) / len(estes)
            centro_y = sum(nortes) / len(nortes)
            
            lineas_lisp.append(
                f'  (command "_TEXT" "_J" "MC" (list {centro_x:.4f} {centro_y:.4f}) 2.5 0 "{nombre_predio}")'
            )
            
            total_procesados += 1
            
        except Exception:
            continue

    lineas_lisp.append("  (setvar \"CMDECHO\" 1)")
    lineas_lisp.append('  (princ "\\n¡Proceso completado! Polígonos generados con éxito.")')
    lineas_lisp.append("  (princ)")
    lineas_lisp.append(")")
    
    return "\n".join(lineas_lisp), total_procesados

# --- DISEÑO Y ESTRUCTURA VISUAL DE LA WEB ---
st.set_page_config(page_title="Generador LISP de Predios", page_icon="🏗️", layout="centered")

# ============================================================
# TEMA VISUAL — inspirado en la paleta verde oscuro / dorado
# y el emblema animado de referencia (Motor de Apoyo Predial ATLAS)
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

/* Emblema animado — fantasma travieso original en tono morado (diseño propio, sin usar ningún personaje con derechos de autor) */
.atlas-emblem-wrap {
    display: flex;
    justify-content: center;
    margin-bottom: 0.6rem;
}
.atlas-ghost {
    width: 78px;
    height: 78px;
    filter: drop-shadow(0 0 12px rgba(138,99,201,0.5));
    animation: atlas-float 2.4s ease-in-out infinite;
    transform-origin: center bottom;
}
.atlas-ghost svg {
    width: 100%;
    height: 100%;
    display: block;
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

/* Alertas (éxito / error) */
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

/* Caja del pie de página */
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

<div class="atlas-emblem-wrap">
  <div class="atlas-ghost">
    <svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="ghostGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#9b6fd6"/>
          <stop offset="100%" stop-color="#5c3f92"/>
        </linearGradient>
      </defs>
      <path d="M50 6 C24 6 10 26 10 52 L10 96 L21 84 L32 97 L43 84 L50 97 L57 84 L68 97 L79 84 L90 96 L90 52 C90 26 76 6 50 6 Z" fill="url(#ghostGrad)"/>
      <ellipse cx="34" cy="48" rx="8" ry="10" fill="#f5f3ff"/>
      <ellipse cx="66" cy="48" rx="8" ry="10" fill="#f5f3ff"/>
      <circle cx="35" cy="52" r="3.6" fill="#1a1206"/>
      <circle cx="65" cy="52" r="3.6" fill="#1a1206"/>
      <path d="M30 66 Q50 82 70 66" stroke="#1a1206" stroke-width="3.2" fill="none" stroke-linecap="round"/>
    </svg>
  </div>
</div>
""", unsafe_allow_html=True)

st.title("🏗️ Generador LISP para AutoCAD")
st.markdown("Sube tus archivos Excel. La plataforma extraerá las coordenadas y generará automáticamente un único archivo **.lsp**.")

# Casilla para arrastrar archivos
archivos_subidos = st.file_uploader("Arrastra tus archivos Excel aquí", type=["xlsx", "xls"], accept_multiple_files=True)

if archivos_subidos:
    if st.button("🚀 Generar Archivo LISP"):
        with st.spinner("Procesando vértices en orden ascendente..."):
            codigo_lisp, cantidad = procesar_excels_a_lisp(archivos_subidos)
            
            if cantidad > 0:
                st.success(f"✅ ¡Perfecto! Se procesaron {cantidad} predios sin errores.")
                
                # Botón de descarga
                st.download_button(
                    label="⬇️ Descargar archivo DIBUJAR_PREDIOS.lsp",
                    data=codigo_lisp,
                    file_name="DIBUJAR_PREDIOS.lsp",
                    mime="text/plain"
                )
            else:
                st.error("No se pudo extraer coordenadas válidas de los archivos.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    "<div class='atlas-footer-box'><p style='text-align: center; color: gray; font-size: 14px;'>"
    "© 2026. Sitio web creado por Emerson Gutierrez Vega."
    "</p></div>", 
    unsafe_allow_html=True
)
