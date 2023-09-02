import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ['https://www.googleapis.com/auth/spreadsheets' ,'https://www.googleapis.com/auth/drive']

credencials = ServiceAccountCredentials.from_json_keyfile_name('Recursos\Botana.json', scope )
client = gspread.authorize(credencials)

# sheet = client.create("Botana Special Ops Carlos Mogollon")
# sheet.share("[TU CORREO]@gmail.com", perm_type="user", role="writer")

def cargar_datos_so():

    print("\nCargando base de datos a Google Sheet")

    sheet = client.open("Botana Special Ops Carlos Mogollon").sheet1
    df = pd.read_csv("Recursos\Bases de datos\Botana_base_so.csv")
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("\nBase cargada")
cargar_datos_so()