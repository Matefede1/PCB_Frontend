import streamlit as st
from PIL import Image
import requests
# from python-dotenv import load_dotenv
import os


# Set page tab display
st.set_page_config(
   page_title="PCB Defect Detection",
   page_icon= '🖼️',
   layout="wide",
   initial_sidebar_state="expanded",
)

# Example local Docker container URL
# url = 'http://api:8000'
# Example localhost development URL
#url = 'http://127.0.0.1:8000'
# load_dotenv()
#url = os.getenv('API_URL')

## Selecionar url de google cada uno (Diego, Mateo, Matias)
#url = 'https://docker-test-pcb-cfiqqvqtva-uc.a.run.app' #MATIAS: Imagen sin conf thres customizable
url = 'https://docker-test-pcb-cfiqqvqtva-uw.a.run.app'  #MATIAS con conf thres
#url = ''   #MATEO
#url = ''   #DIEGO

# Define the local CSS file location or the URL to the image
header_image = "https://lirp.cdn-website.com/a0bf26f7/dms3rep/multi/opt/shutterstock_1588316845-1920w.jpg"



header_html = """
<style>
    .header {
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("https://lirp.cdn-website.com/a0bf26f7/dms3rep/multi/opt/shutterstock_1588316845-1920w.jpg");

        background-size: cover;
        background-position: center;
        height: 400px;
        position: relative;
        color: white;
        text-align: center;
    }

    .header::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0.6;
        background: rgba(0, 0, 0, 0.8); /* Black background with opacity */
        z-index: -1;
    }

    .header h1, .header p {
        position: relative;
        z-index: 1;
    }

    /* Streamlit container adjustments */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
    }
</style>

<div class="header">
    <div style="padding: 190px 0;">
        <h1>Detección de defectos en tarjetas PCB</h1>
    </div>
    <div class="overlay"></div>
</div>
"""
# Inject CSS with Markdown
st.markdown(header_html, unsafe_allow_html=True)


# st.header('Detección de defectos en tarjetas PCB')





with st.container():



    st.subheader('Umbral de confianza')

    col1, col2, col3= st.columns(3)

    with col1:
        conf = st.slider('Seleccionar confianza del modelo: ',min_value=0.10,max_value=1.00,step=0.05,value=0.25)
        st.write('El modelo solo identificará aquellos defectos para los que tenga al menos un ',conf*100,'% de seguridad en sus predicciones.')

    with col2:
        st.write(' ')
    with col3:
        st.write(' ')


    ### Create a native Streamlit file upload input
    st.markdown("### Cargar la foto de la tarjeta")
    img_file_buffer = st.file_uploader('Cargar una imagen')

    if img_file_buffer is not None:




        ### Display the image user uploaded
        st.image(Image.open(img_file_buffer), caption="Esta es la imagen cargada ☝️")


        with st.spinner("Cargando..."):
            ### Get bytes from the file buffer
            img_bytes = img_file_buffer.getvalue()

            ### Make request to  API (stream=True to stream response as bytes)
            res = requests.post(url + "/upload_image", files={'img': img_bytes},params={'conf':conf})

            if res.status_code == 200:
                ### Display the image returned by the API
                st.image(res.content, caption="Estos son los defectos en la PCB ☝️")
                col4, col5, col6= st.columns(3)
                with col4:
                    st.write(' ')
                with col5:
                    st.success('Exito!')
                with col6:
                    st.write(' ')
            else:
                st.markdown("**Oops**, something went wrong 😓 Please try again.")
                print(res.status_code, res.content)

col7, col8, col9 = st.columns(3)

with col7:
    st.write(' ')

with col8:
    image = Image.open('images/wagon.png')
    st.image(image,caption= 'Powered by', use_column_width=False)

with col9:
    st.write(' ')
