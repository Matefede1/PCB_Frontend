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

## Selecionar url de Google cada uno (Diego, Mateo, Matias)
#url = ''  #MATIAS
#url = ''   #MATEO
#url = ''   #DIEGO


# Example localhost development URL
url = 'http://localhost:8000'



# App title and description
st.header('Detección de defectos en tarjetas PCB')


#Slider para elegir manualmente threshold
st.subheader('Umbral de confianza')

conf = st.slider('Seleccionar confianza del modelo: ',min_value=0.10,max_value=1.00,step=0.05,value=0.25)

st.write('El modelo solo identificará aquellos defectos para los que tenga al menos un ',conf*100,'% de seguridad en sus predicciones.')


### Create a native Streamlit file upload input
st.markdown("### Primero hay que enviar la foto de la tarjeta")
img_file_buffer = st.file_uploader('Cargar una imagen')

if img_file_buffer is not None:

  col1, col2 = st.columns(2)

  with col1:
    ### Display the image user uploaded
    st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")

  with col2:
    with st.spinner("Wait for it..."):
      ### Get bytes from the file buffer
      img_bytes = img_file_buffer.getvalue()

      ### Make request to  API (stream=True to stream response as bytes)
      res = requests.post(url + "/upload_image", files={'img': img_bytes},params={'conf':conf})

      if res.status_code == 200:
        ### Display the image returned by the API
        st.image(res.content, caption="Image returned from API ☝️")
      else:
        st.markdown("**Oops**, something went wrong 😓 Please try again.")
        print(res.status_code, res.content)
