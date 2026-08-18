import subprocess
import sys

# Instalación forzada en tiempo de ejecución para evitar el ModuleNotFoundError
try:
    import google.generativeai as genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

import streamlit as st
import tempfile
import os

# Configuración de la interfaz
st.set_page_config(page_title="Evaluador de Anteproyectos", page_icon="📝", layout="wide")

st.title("📝 Evaluador Rápido de Anteproyectos - TG1")
st.write("Sube el PDF de un grupo para analizarlo automáticamente con tus criterios.")

# Barra lateral para la API Key
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.markdown("[Obtener API Key gratis en AI Studio](https://aistudio.google.com/)")

# Prompt del profesor
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
            with st.spinner("Procesando y analizando el documento..."):
                try:
                    genai.configure(api_key=api_key)
                    
                    # Guardar archivo temporal
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # Enviar a Gemini API
                    archivo_gemini = genai.upload_file(tmp_path)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content([CRITERIOS_PROFESOR, archivo_gemini])
                    
                    # Limpiar archivo temporal local
                    os.remove(tmp_path)
                    
                    # Resultados
                    st.success("Análisis completado:")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Error durante el análisis: {e}")
