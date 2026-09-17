import streamlit as st
import pandas as pd
import time

def procesar_excels_a_lisp(lista_archivos_excel):
    lineas_lisp = [
        ";; ==================================================",
        ";; SCRIPT AUTOLISP GENERADO AUTOMÁTICAMENTE",
        ";; ==================================================",
        "(defun c:DIBUJAR_PREDIOS ()",
        "  (setvar \"CMDECHO\" 0)",
        "  (command \"_LAYER\" \"_M\" \"PREDIOS_AUTOMATICOS\" \"_C\" \"7\" \"\" \"\")"
    ]
    
    total_procesados = 0

    for archivo in lista_archivos_excel:
        try:
            nombre_archivo = archivo.name
            nombre_predio = nombre_archivo.rsplit('.', 1)[0]
            
            df = pd.read_excel(archivo)
            
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
            
            # Dibujo de vértices en estricto orden ascendente
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

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Generador LISP de Predios", page_icon="📐", layout="centered")

# --- ESTILOS CSS OCULTOS PARA DARLE ASPECTO PROFESIONAL ---
st.markdown("""
    <style>
    /* Ocultar menú superior y pie de página de Streamlit para que parezca una app propia */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Personalizar botón principal */
    .stButton > button {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        padding: 0.75rem;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #1e293b;
        border-color: #1e293b;
        color: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<h1 style='text-align: center; color: #1e293b;'>Generador de poligonos en LISP para Autocad</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.15rem; color: #475569; margin-bottom: 2rem;'>Sube tus archivos Excel. La plataforma extraerá las coordenadas y generará automáticamente un único archivo .lsp.</p>", unsafe_allow_html=True)

# --- PANEL DIDÁCTICO (Acordeón) ---
with st.expander("📖 Guía rápida de uso"):
    st.markdown("""
    1. **Sube tus archivos:** Arrastra uno o cientos de archivos Excel a la zona punteada.
    2. **Procesa los datos:** Haz clic en el botón de generar. El sistema limpiará las coordenadas y las ordenará automáticamente.
    3. **Llévalo a AutoCAD:** Descarga el archivo `.lsp`, escribe el comando `APPLOAD` en AutoCAD, cárgalo y ejecuta `DIBUJAR_PREDIOS`.
    """)

st.write("---")

# --- ZONA DE CARGA ---
archivos_subidos = st.file_uploader("Arrastra tus archivos Excel aquí", type=["xlsx", "xls"], accept_multiple_files=True)

if archivos_subidos:
    # Botón más ancho y profesional
    if st.button("⚙️ Procesar Coordenadas y Generar LISP", use_container_width=True):
        
        # Animación de carga moderna tipo "Terminal"
        with st.status("Analizando y procesando archivos...", expanded=True) as status:
            st.write("🔍 Extrayendo datos geométricos de los Excel...")
            time.sleep(0.5) # Pequeña pausa para que la animación se vea fluida
            st.write("📐 Trazando polígonos en orden ascendente...")
            time.sleep(0.5)
            st.write("⚙️ Compilando código LISP...")
            
            codigo_lisp, cantidad = procesar_excels_a_lisp(archivos_subidos)
            
            status.update(label="¡Procesamiento finalizado!", state="complete", expanded=False)
            
        if cantidad > 0:
            st.success(f"✅ Análisis exitoso. Se estructuraron {cantidad} predios listos para AutoCAD.")
            
            st.download_button(
                label="⬇️ Descargar archivo LISP (DIBUJAR_PREDIOS.lsp)",
                data=codigo_lisp,
                file_name="DIBUJAR_PREDIOS.lsp",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.error("No se detectaron coordenadas válidas (Mínimo 3 vértices requeridos por archivo).")

# --- PIE DE PÁGINA PERSONALIZADO ---
st.markdown("""
    <hr style="margin-top: 4rem; border: none; border-top: 1px solid #e2e8f0;">
    <p style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        © 2026. Sitio web creado por Emerson Gutierrez Vega.
    </p>
""", unsafe_allow_html=True)
