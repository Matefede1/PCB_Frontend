from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import torch
from PIL import Image
from io import BytesIO
import sys

# Asumiendo que tu modelo YOLOv5 está en una carpeta llamada 'yolov5_folder'
sys.path.insert(0, '/home/diegotamborelli/code/DiegoTamborelli/PCB/data_yolov7/yolov5')
from yolov5_folder import models  # Importa los módulos necesarios de YOLOv5

app = FastAPI()

# Cargar el modelo YOLOv5
model = torch.hub.load('/home/diegotamborelli/code/DiegoTamborelli/PCB/data_yolov7/yolov5', 'custom', path='/home/diegotamborelli/code/DiegoTamborelli/PCB/data_yolov7/yolov5/yolov5s.pt', source='local')

def process_image_with_yolov5(image_data):
    # Convertir los bytes de la imagen a un formato PIL Image
    image = Image.open(BytesIO(image_data))

    # Procesar la imagen con YOLOv5
    results = model(image)

    # Convertir los resultados a un formato que se pueda enviar como JSON
    # Aquí puedes personalizar cómo deseas formatear los resultados
    return results.pandas().xyxy[0].to_json(orient="records")

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()
    results = process_image_with_yolov5(image_data)
    return JSONResponse(content={"results": results})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)