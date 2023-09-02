from Botana_gmail import *
from Botana_base_de_datos import *
from Botana_base_so import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep

import datetime

import csv
from csv import reader

ahora = datetime.datetime.now()
hoy = ahora.strftime("%d/%m/%Y")

from datetime import datetime

hora_actual = ahora.strftime("%H:%M")
hora_actual = datetime.strptime(hora_actual, "%H:%M")
hora_cierre = "23:00"
hora_cierre = datetime.strptime(hora_cierre, "%H:%M")
hora_apertura = "07:00"
hora_apertura = datetime.strptime(hora_apertura, "%H:%M")

url =#[WEB]
path = "Recursos\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get(url)
driver.maximize_window()

def iniciar_sesion_desk():

    user_desk = #[USUARIO DE LA WEB]
    password_desk = #[PASSWORD DE LA WEB]

    print("\nIniciando sesion")
    input_user = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div/div/form/div[1]/div/div/input')
    input_user.send_keys(user_desk)

    input_password = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div/form/div[2]/div/div/input')
    input_password.send_keys(password_desk)

    button = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div/form/div[3]/button/span[1]')
    button.click()
    sleep(2)

    desk = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/ul/a[2]')
    desk.click()
    sleep(2)

def cambiando_estado():
    on_off = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div[1]/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr[1]/td[1]/button')
    on_off.click()
    sleep(0.3)
    on = driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/ul/li')
    on.click()
    sleep(0.2)
    confirmacion = driver.find_element(By.XPATH,'/html/body/div[3]/div[3]/div/div[3]/button[2]')
    confirmacion.click()
    sleep(0.2)

def evaluando_liquidez():

    global liquidez, estado

    print("\nEvaluando liquidez")
    liquidez = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div[1]/div[3]/div/div[1]/div[2]/h3').text
    liquidez = liquidez.split("\nD")
    liquidez = liquidez[1].split("RSV")
    liquidez = float(liquidez[1])
    print("Liquidez de " + str(liquidez))
    estado = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div[1]/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr[1]/td[2]/div[1]').value_of_css_property("background-color")
    
    if liquidez > 1500:
        print("\nLiquidez aceptable seguimos trabajando")
        if estado == "rgba(238, 238, 238, 1)":
            print("\nEncendiendo")
            cambiando_estado()
            
    elif liquidez < 1500:
        if estado == "rgba(186, 255, 215, 1)":
            print("\nApagando")
            cambiando_estado()
        else:
            print("\nEstamos apagados.\n\nEsperando fondos")
            pass

iniciar_sesion_desk()

def sin_tildes_desk(titular_desk):

    titular_desk = titular_desk.lower()
    tildes =  {"á":"a","é":"e","í":"i","ó":"o","ú":"u",",":""}

    for tilde in tildes.keys():
        titular_desk = titular_desk.replace(tilde, tildes[tilde])
    return titular_desk 
     
def estandar_desk_titular(titular_desk):

    print("\nObteniendo nombres del titular en solicitud")
    global nombre1_desk, nombre2_desk, nombre3_desk, nombre4_desk

    titular_desk = sin_tildes_desk(titular_desk)
    titular_desk = titular_desk + " le" + " x"
    titular_desk = titular_desk.split(" ") 
    nombre1_desk = titular_desk[0]
    nombre2_desk = titular_desk[1]
    nombre3_desk = titular_desk[2]
    nombre4_desk = titular_desk[3]   
   
def fecha_desk(hora_desk):
    print("\nConvirtiendo fecha y hora a datetime")
    hora_desk = datetime.strptime(hora_desk, "%d/%m/%Y, %H:%M")  

def base_so():
    print("\nEscribiendo en la base Special Ops")
    headersCSV = ["Fecha","Correo","Asunto","Monto"]
   
    dic = {"Fecha":fecha,"Correo":email_address,"Asunto":asunto_df,"Monto":monto}
    archivo = "Recursos\Bases de datos\Botana_base_so.csv"
    with open (archivo,"a",newline="") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        dictwriter_object.writerow(dic)
        f_object.close()
    cargar_datos_so()

    base_temp = "Recursos\Bases de datos\Botana_base_temporal.csv"
    lines = list()
    with open(archivo, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if (hoy > fecha) and (not nombre1_desk in base_temp):
                print("\nEliminando de la base temporal")
                lines.remove(row)
                with open(archivo, 'w',newline="") as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(lines)
                cargar_datos_so()

def base_de_datos():
    
    print("\nEscribiendo en la base de datos")
    headersCSV = ["Fecha","Correo","Asunto","Monto","ID Desk","Usuario Reserve","Titular Zelle en desk","ID Banco"]
   
    dic = {"Fecha":fecha,"Correo":email_address,"Asunto":asunto_df,"Monto":monto,"ID Desk":id_desk,"Usuario Reserve":usuario_p2p,"Titular Zelle en desk":titular_desk,"ID Banco":id_banco}
    archivo = "Recursos\Bases de datos\Botana_base_local.csv"
    with open (archivo,"a",newline="") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        dictwriter_object.writerow(dic)
        f_object.close()
    cargar_datos()

def borrar_de_base_temporal():

    print("\nEscribiendo en la base temporal")
    lines = list()
    with open('Recursos\Bases de datos\Botana_base_temporal.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if coincide == 1:
                print("\nEliminando de la base temporal")
                lines.remove(row)
            if hoy > fecha:
                print("\nEliminando de la base temporal")
                lines.remove(row)
                    
    with open('Recursos\Bases de datos\Botana_base_temporal.csv', 'w',newline="") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

def comparar():

    print("\nComparando nombres del titular")
    global coincide, row

    with open('Recursos\Bases de datos\Botana_base_temporal.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Verificar si el archivo está vacio
        if header != None:
            # Iterar cada linea luego de los encabezados
            for row in csv_reader:
                # La linea es una lista y cada variable un elemento de esta
                print("\nEvaluando si fecha y primer nombre del titular hacen match")
                if hoy in row[0] and nombre1_desk in row[1]:
                    print("\nEvaluando si los siguientes nombres del titular hacen match")
                    if ((row[2]==nombre2_desk or row[2]== nombre3_desk or row[2]== nombre4_desk) or (row[3]== nombre2_desk or row[3]==nombre3_desk or row[2]== nombre4_desk)) and ((row[2]==nombre3_desk or row[3]==nombre3_desk or row[4]==nombre3_desk) or (row[2]==nombre4_desk or row[3]==nombre4_desk or row[4]==nombre4_desk)):
                        print("\nNombres coinciden correctamente")
                        borrar_de_base_temporal()
                        coincide = 1
                    else:
                        print("\nSiguientes nombres del titular no hacen match")
                        coincide = 2
         
                else:
                    print("\nFecha y primer nombre del titular sin match encontrado")
                    coincide = 2 

def obtener_datos_aprobar():
                      
    global id_desk,usuario_p2p,id_banco
    print("\nObteniendo usuario p2p")
    usuario_p2p = driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[1]/div[1]/div[1]/div[3]/div/p').text
    print("Obteniendo Id del banco")        
    id_banco = driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[1]/div[1]/div[6]/div/div/div/p').text
    print("Obteniendo Id de Reserve")     
    id_desk = driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div/p').text

    aprobada = driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[2]/div[1]/div[2]/div[3]/button')
    aprobada.click()
    print("\nSolicitud aprobada")                          
    sleep(0.5)

def solicitud():

    global titular_desk, i
    
    print("\n Procesando solicitud")
    tr = driver.find_elements(By.XPATH,'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr')
    tr_inicial = 1
    contador_tr = 0

    for e in tr:
        contador_tr = contador_tr + 1
    
    for i in range(tr_inicial, contador_tr + 1, 1):
        solicitud = driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]')
        
        if int(i) % 2 != 0:

            print("\nObteniendo monto en solicitud")
            monto_desk = solicitud.find_element(By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[4]/div').text
            monto_desk = monto_desk.replace(" USD", "")
            monto_desk = monto_desk.replace(",",".")

            print("Abriendo solicitud")
            boton = solicitud.find_element(By.TAG_NAME, 'button')
            boton.click()
            sleep(5) 
            
        else:
            i+1
            
            print("\nSolicitud abierta, evaluando datos")
            print("\nObteniendo fecha y hora en solicitud")
            hora_desk = driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/div').text
            fecha_desk(hora_desk)
            print(hora_desk)
            print("\nEvaluando fecha y hora")
            from datetime import timedelta
            if hora_desk < (ahora - timedelta(minutes=25)):
              print("\nSolicitud con mas de 25 minutos, será cancelada")
              base_so()
              rechazar = Select(driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[2]/div[2]/div/div/div/div'))
              rechazar.select_by_visible_text('Cancelar, Nombre de titular no encontrado')
              cancelar = driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[2]/div[2]/div/button')
              print("\nCancelar, Nombre de titular no encontrado")
              cancelar.click()
              sleep(0.5)

            else:
                print("\nSolicitud con menos de 25 minutos\n\nEvaluando titular")
                titular_desk = driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[1]/div[1]/div[4]/div/div/div/p').text
                estandar_desk_titular(titular_desk)
                print(titular_desk)
                comparar()

                if coincide==1:
                  print("\nCoinciden los nombres del titular\n\nEvaluando montos")
                  monto_desk = float(monto_desk)
                  monto_gmail = float(row[5])

                  if monto_desk == monto_gmail:
                      print("\nMontos coinciden")
                      obtener_datos_aprobar()
                  elif monto_desk<=(monto_gmail+monto_gmail*0.15) and monto_desk>=(monto_gmail-monto_gmail*0.15):
                      print("\nMontos no coinciden, pero puedo corregirlo")
                      monto_nuevo = str(monto_gmail)
                      monto_nuevo = monto_nuevo.replace(".",",")
                      modificar_monto = driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[2]/div[1]/div[2]/div[1]/button')
                      modificar_monto.click()
                      sleep(0.5)
                      monto_input = driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td/div/div/div/div/div[2]/div[1]/div[2]/div[2]/div/div/input')
                      monto_input.send_keys(monto_nuevo)
                      obtener_datos_aprobar()
                  else:
                      print("\nDiferencia muy grande entre montos")
                      pass

                elif coincide == 2:
                  print("\nTitular sin match, prosigo")
        
    for i in range(tr_inicial, contador_tr + 1, 2):

            body = driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody')
            boton = body.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[8]/button')
            boton.click()
            sleep(0.5)            
    
def run_bot():

    correos()
    solicitud()

while hora_actual <  hora_cierre:
    
    if hora_actual < hora_apertura:
        print("\nFuera de horario")
        if estado == "rgba(186, 255, 215, 1)":
            print("\nApagando")
            cambiando_estado()

    else:
        run_bot()
        print("\nTrabajando por la patria")
        sleep(60)

while True:
    evaluando_liquidez()
    sleep(60)