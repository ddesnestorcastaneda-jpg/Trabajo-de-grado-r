import streamlit as st
from google import genai
import tempfile
import os

# Configuración de la página
st.set_page_config(page_title="Evaluador de Anteproyectos", page_icon="📝")

st.title("📝 Evaluador Rápido de Anteproyectos - Trabajo de Grado 1")
st.write("Herramienta de revisión automatizada para Ingeniería Industrial y Desarrollo de Software.")

# Barra lateral para la API Key
st.sidebar.header("Configuración")
api_key = st.sidebar.text_input("Ingresa tu API Key de Gemini:", type="password")

# Subida del archivo
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
                # 1. Inicializar el NUEVO cliente con tu API Key "AQ..."
                client = genai.Client(api_key=api_key)

                # 2. Guardar el PDF subido en un archivo temporal
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(archivo_subido.getvalue())
                    ruta_temporal = tmp_file.name

                # 3. Subir el archivo a los servidores de Gemini usando el nuevo cliente
                archivo_gemini = client.files.upload(file=ruta_temporal, mime_type="application/pdf")

                # 4. Prompt: Aquí puedes ajustar las instrucciones para el evaluador
                prompt = """
                Eres un profesor estricto pero constructivo que evalúa anteproyectos de grado 
                para estudiantes de Ingeniería Industrial y Desarrollo de Software. 
                Analiza este documento y entrégame:
                1. Un resumen breve.
                2. Puntos fuertes del anteproyecto.
                3. Debilidades o áreas de mejora metodológica.
                4. Veredicto preliminar (Aprobado, Requiere Cambios, Rechazado).
                """

                # 5. Generar la respuesta usando el modelo (Flash es ideal para textos largos)
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=[archivo_gemini, prompt]
                )

                # 6. Mostrar los resultados
                st.success("¡Análisis Completado!")
                st.markdown("---")
                st.markdown(response.text)

                # 7. Limpieza: Borrar el archivo temporal de tu servidor por seguridad
                os.remove(ruta_temporal)

            except Exception as e:
                # Si hay error, lo mostramos limpio
                st.error(f"❌ Ocurrió un error durante el análisis: {str(e)}")
