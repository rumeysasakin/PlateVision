from studio.custom_block import *
import cv2
import numpy as np
import os

class YOLO_PlateDetector(Block):
    op_code = 'YOLO_PlateDetector'
    tooltip = 'Detect license plate region using YOLOv8'

    def init(self):
        self.width = 350
        self.height = 300
        self.input_sockets = [SocketTypes.ImageAny('Input Image')]
        self.output_sockets = [
            SocketTypes.ImageAny('Cropped Plate Image')
        ]

        self.param['label'] = Label(text='YOLOv8 Plate Detector', tooltip='Detect license plates using pre-trained YOLO model')

        # 💡 Model yolunu burada belirt
        try:
            from ultralytics import YOLO
            model_path = r"C:\models\Automatic-License-Plate-Recognition-using-YOLOv8-main\license_plate_detector.pt"  # Burayı kendi yoluna göre değiştir
            self.model = YOLO(model_path)
        except Exception as e:
            self.model = None
            self.logError(f"Model yükleme hatası: {e}")

    def run(self):
        if self.model is None:
            self.logError("Model yüklenemedi.")
            return

        img = self.input['Input Image'].data
        if img is None or not isinstance(img, np.ndarray):
            self.logError("Geçersiz görüntü girişi.")
            return

        try:
            results = self.model.predict(source=img, imgsz=640, conf=0.25, device='cpu', verbose=False)
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        except Exception as e:
            self.logError(f"YOLO tahmin hatası: {e}")
            return

        if len(boxes) == 0:
            self.log("Plaka bulunamadı.")
            self.output['Cropped Plate Image'].data = None
            self.output['Plate Box'].data = []
            return

        # İlk tespit edilen kutuyu al
        x1, y1, x2, y2 = boxes[0]
        crop = img[y1:y2, x1:x2]
        self.output['Cropped Plate Image'].data = crop

add_block(YOLO_PlateDetector.op_code, YOLO_PlateDetector)
