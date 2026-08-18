import streamlit as st
import google.generativeai as genai
import tempfile
import os

# Configuración de la página
st.set_page_config(page_title="Evaluador de Anteproyectos", page_icon="📝", layout="wide")

st.title("📝 Evaluador Rápido de Anteproyectos - TG1")
st.write("Sube el PDF de un grupo para analizarlo automáticamente con los criterios de evaluación.")

# Ingreso seguro de la API Key en la barra lateral
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.markdown("[Obtener API Key de Google](https://aistudio.google.com/)")

# Prompt con las reglas del profesor
CRITERIOS_PROFESOR = """
Actúa como un profesor riguroso de Trabajo de Grado 1 para las carreras de Ingeniería Industrial y Desarrollo de Software.
Revisa el anteproyecto en PDF adjunto y genera un reporte breve y directo estructurado de la siguiente manera:

1. ESTADO GENERAL: (Aprobado / Requiere Ajustes / Rechazado)
2. CUMPLIMIENTO DE CHECKLIST:
   - Título y Formato: (Pasa / No pasa + observación corta)
   - Planteamiento del Problema: (Pasa / No pasa + observación corta)
   - Objetivos (General y Específicos): Verificar si el Objetivo 1 es de diagnóstico. (Pasa / No pasa + observación)
   - Justificación y Alcance: (Pasa / No pasa + observación)
   - Metodología e Instrumentos: (Pasa / No pasa + observación)
3. CORRECCIONES CRÍTICAS PARA ESTA SEMANA: (Máximo 3 puntos clave que deben corregir de inmediato antes de aplicar instrumentos)

Sé directo, constructivo y enfócate en la coherencia técnica de ingeniería y software.
"""

# Carga de archivo
uploaded_file = st.file_uploader("Arrastra o selecciona el archivo PDF del anteproyecto", type=["pdf"])

if uploaded_file is not None:
    if not api_key:
        st.warning("Por favor ingresa tu API Key de Gemini en el panel lateral para continuar.")
    else:
        if st.button("🔍 Analizar Anteproyecto"):
            with st.spinner("Procesando y analizando el documento con la API..."):
                try:
                    # Configurar la API
                    genai.configure(api_key=api_key)
                    
                    # Guardar temporalmente el PDF subido
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # Subir el archivo a la File API de Gemini
                    archivo_gemini = genai.upload_file(tmp_path)
                    
                    # Generar la evaluación
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content([CRITERIOS_PROFESOR, archivo_gemini])
                    
                    # Eliminar el archivo temporal local
                    os.remove(tmp_path)
                    
                    # Mostrar resultados
                    st.success("Análisis completado:")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Ocurrió un error al analizar el documento: {e}")
