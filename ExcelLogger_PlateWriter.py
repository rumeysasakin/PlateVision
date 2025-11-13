from studio.custom_block import *
import pandas as pd
from datetime import datetime
import os

class ExcelLogger_PlateWriter(Block):
    op_code = 'ExcelLogger_PlateWriter'
    tooltip = 'Write detected plate number to Excel file with timestamp'

    def init(self):
        self.width = 300
        self.height = 150

        self.input_sockets = [
            SocketTypes.String('Detected Plate'),
        ]
        self.output_sockets = [
            SocketTypes.String('Parking Slot Info')  # 🔄 Yeni output eklendi
        ]

        self.param['label'] = Label(text='Excel Plate Logger', tooltip='Saves plate and timestamp to Excel')

    def run(self):
        plate = self.input['Detected Plate'].data

        if not plate or not isinstance(plate, str) or plate.strip() == "":
            self.logError("Boş veya geçersiz plaka bilgisi.")
            return

        file_path = os.path.join(os.getcwd(), 'plakalar.xlsx')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_data = pd.DataFrame([{'Timestamp': timestamp, 'Plate': plate.strip()}])

        try:
            if os.path.exists(file_path):
                old_data = pd.read_excel(file_path)
                df = pd.concat([old_data, new_data], ignore_index=True)
            else:
                df = new_data

            df.to_excel(file_path, index=False)

            row_index = len(df)  # Yeni eklenen plaka için satır sayısı = sıra numarası
            message = f"Aracınız ile, {row_index} numaralı yere geçiniz"
            self.output['Parking Slot Info'].data = message

            self.logInfo(f"Plaka '{plate}' ({timestamp}) Excel'e kaydedildi.")
        except Exception as e:
            self.logError(f"Excel yazma hatası: {e}")

add_block(ExcelLogger_PlateWriter.op_code, ExcelLogger_PlateWriter)
