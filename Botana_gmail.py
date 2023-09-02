import email
from email.header import decode_header
import imaplib
from datetime import datetime
from csv import DictWriter
from time import sleep

def correos():
    global email_address

    imap_server='imap.gmail.com'
    email_address=#[CORREO]
    password_gmail=#[PASSWORD DEL CORREO]

    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, password_gmail)

    status, mensajes = imap.select("Inbox")
    typ ,data = imap.search(None,'UnSeen')
    return_code, data = imap.search(None, 'UnSeen')
    data = data.pop()
    data = data.decode("utf-8")
    data = data.split(" ")
    print(data)

    mensajes = int(mensajes[0])

    contador = 0

    def base_temporal():

        print("Añadiendo a base temporal\n")
        headersCSV_t = ["Fecha_gmail","Nombre_gmail1","Nombre_gmail2","Nombre_gmail3","Nombre_gmail4","Monto","Estado"]
        dic_t ={"Fecha_gmail":fecha,"Nombre_gmail1":nombre1,"Nombre_gmail2":nombre2,"Nombre_gmail3":nombre3,"Nombre_gmail4":nombre4,"Monto":monto}
        archivo_t = "Recursos\Bases de datos\Botana_base_temporal.csv"
        with open (archivo_t,"a",newline="") as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV_t)
            dictwriter_object.writerow(dic_t)
            f_object.close()
        
    def sin_tildes(subject):   
        subject = subject.lower()
        tildes =  {"á":"a","é":"e","í":"i","ó":"o","ú":"u",",":"","ñ":"n"}

        for tilde in tildes.keys():
            subject = subject.replace(tilde, tildes[tilde])

        return subject

    def estandar_gmail(subject):
        
        print("Obteniendo nombres del correo")
        global monto, nombre1, nombre2, nombre3, nombre4
        asunto = sin_tildes(subject).split(" envio ")
        titular = asunto[0] + " x"
        titular = titular.split(" ") 
        nombre1 = titular[0]
        nombre2 = titular[1]
        nombre3 = titular[2]
        nombre4 = titular[3]

        print("Obteniendo monto del correo")
        monto = asunto[1]
        monto = monto.replace("$", "")
        monto = float(monto)

    def fecha_gmail(date_):

        print("Obteniendo fecha del correo")
        global fecha
        fecha = date_.replace(" -0600", "")
        fecha = datetime.strptime(fecha, "%a, %d %b %Y %H:%M:%S")
        fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")  

    def base_de_datos_gmail(subject):

        print("Obteniendo asunto del correo")
        global asunto_df
        asunto_df = sin_tildes(subject)

    def run_leer_correos():

        contador = 0
        if data == ['']:
            print("No hay mensajes por leer")
        else:
            for e in data:
                contador = contador + 1

        for i in range(mensajes, mensajes - contador, -1):

            try:
                res, mensaje = imap.fetch(str(i), '(RFC822)')
            except:
                break

            for respuesta in mensaje:
                sleep(2)
                if isinstance(respuesta, tuple):
                    #Obtener contenido
                    mensaje = email.message_from_bytes(respuesta[1])
                    #Decodificarlo
                    subject = decode_header(mensaje["Subject"])[0][0]
            
                    if isinstance(subject, bytes):
                        #Convertir a string
                        subject = subject.decode()
                    from_=mensaje.get("From")
                    date_=mensaje.get("Date")
                    print(date_)

            if (from_ == #[DIRECCION DE CORREO DE A QUIEN QUIERES LEER UNICAMENTE]) and "envió $" in subject:
                        print("\nCorreo del banco\n")
                        base_de_datos_gmail(subject)
                        estandar_gmail(subject) 
                        fecha_gmail(date_)
                        base_temporal()
            else:
                print("\nNo es correo del banco\n")

    run_leer_correos()
correos()