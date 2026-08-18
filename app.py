import streamlit as st
from google import genai

# Configuración de la página
st.set_page_config(page_title="Evaluador de Anteproyectos", page_icon="📝")

st.title("📝 Evaluador Rápido de Anteproyectos - Trabajo de Grado 1")
st.write("Herramienta de revisión automatizada para Ingeniería Industrial y Desarrollo de Software.")

# Barra lateral para la API Key
st.sidebar.header("Configuración")
api_key = st.sidebar.text_input("Ingresa tu API Key de Gemini:", type="password")

# Subida del archivo PDF
archivo_subido = st.file_uploader("Arrastra o selecciona el archivo PDF del anteproyecto", type=["pdf"])

# Botón de análisis
if st.button("🔍 Analizar Anteproyecto"):
    if not api_key:
        st.error("❌ Por favor, ingresa tu API Key en el panel lateral.")
    elif not archivo_subido:
        st.error("❌ Por favor, sube un archivo PDF para analizar.")
    else:
        with st.spinner("Analizando el anteproyecto... esto puede tardar unos segundos."):
            try:
                # 1. Inicializar el cliente con tu API Key "AQ..."
                client = genai.Client(api_key=api_key)

                # 2. Leer los bytes del archivo subido
                pdf_bytes = archivo_subido.read()

                # 3. Preparar el Prompt de evaluación
                prompt = """
                Eres un profesor estricto pero constructivo que evalúa anteproyectos de grado 
                para estudiantes de Ingeniería Industrial y Desarrollo de Software. 
                Analiza este documento y entrégame:
                1. Un resumen breve.
                2. Puntos fuertes del anteproyecto.
                3. Debilidades o áreas de mejora metodológica.
                4. Veredicto preliminar (Aprobado, Requiere Cambios, Rechazado).
                """

                # 4. Enviar el PDF directamente en la llamada usando Part.from_bytes
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        genai.types.Part.from_bytes(
                            data=pdf_bytes,
                            mime_type='application/pdf'
                        ),
                        prompt
                    ]
                )

                # 5. Mostrar los resultados
                st.success("¡Análisis Completado!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ Ocurrió un error durante el análisis: {str(e)}")
