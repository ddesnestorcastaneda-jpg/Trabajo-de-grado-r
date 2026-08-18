import streamlit as st
import google.generativeai as genai
import tempfile
import os

# 1. Configuración general de la página
st.set_page_config(
    page_title="Evaluador de Anteproyectos TG1", 
    page_icon="📝", 
    layout="wide"
)

st.title("📝 Evaluador Rápido de Anteproyectos - Trabajo de Grado 1")
st.write("Herramienta de revisión automatizada para Ingeniería Industrial y Desarrollo de Software.")

# 2. Barra lateral para ingresar la API Key
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.markdown("[👉 Obtener API Key gratis en Google AI Studio](https://aistudio.google.com/)")
    st.markdown("---")
    st.caption("Asegúrate de ingresar la clave para iniciar el análisis.")

# 3. Prompt con los criterios del profesor
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

# 4. Componente para subir el PDF del anteproyecto
uploaded_file = st.file_uploader(
    "Arrastra o selecciona el archivo PDF del anteproyecto", 
    type=["pdf"]
)

# 5. Lógica de procesamiento y evaluación
if uploaded_file is not None:
    if not api_key:
        st.warning("⚠️ Por favor ingresa tu API Key de Gemini en el panel lateral para continuar.")
    else:
        if st.button("🔍 Analizar Anteproyecto", type="primary"):
            with st.spinner("Procesando y analizando el documento con la API de Gemini..."):
                try:
                    # Configurar la API Key
                    genai.configure(api_key=api_key)
                    
                    # Guardar el PDF temporalmente en el servidor
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # Subir el PDF a la API de Gemini
                    archivo_gemini = genai.upload_file(tmp_path)
                    
                    # Generar la evaluación con el modelo Gemini 1.5 Flash
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content([CRITERIOS_PROFESOR, archivo_gemini])
                    
                    # Eliminar el archivo temporal local
                    os.remove(tmp_path)
                    
                    # Mostrar resultados en pantalla
                    st.success("✅ Análisis completado con éxito:")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"❌ Ocurrió un error durante el análisis: {e}")
