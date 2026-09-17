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

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Generador LISP de Predios", page_icon="🏗️", layout="centered")

# --- ESTILOS CSS DE DISEÑO MODERNO Y PROFESIONAL ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
    }
    .main-card {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3);
    }
    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 3rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Contenedor principal con estilo de tarjeta
st.markdown('<div class="main-card">', unsafe_allow_html=True)

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
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.error("No se pudo extraer coordenadas válidas de los archivos.")

st.markdown('</div>', unsafe_allow_html=True)

# --- PIE DE PÁGINA ---
st.markdown(
    '<p class="footer-text">© 2026. Sitio web creado por Emerson Gutierrez Vega.</p>', 
    unsafe_allow_html=True
)
