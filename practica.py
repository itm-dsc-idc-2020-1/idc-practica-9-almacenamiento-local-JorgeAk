#Equipo 3 practica 9
import time
import os
import ntplib
import hashlib
import random
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

caracteres = "abcdefghijklmnopqrstuvwxyz0123456789"
temperatura = int(input("¿Dame la temperatura actual? "))
latitud = "19.721812"
longitud = "-101.185806"
dispositivo = "temperatura_1"
#obtner la zona horaria UTC
def zonaHoraria():
    import datetime
    import time
    now = datetime.datetime.now()
    from pytz import reference
    localtime = reference.LocalTimezone()
    localtime.tzname(now)
    zona = -time.timezone / 3600
    return zona
#Generar la firma
def generaCadena():
    cadena = ""
    for x in range(1,10):
        cadena += random.choice(caracteres)
    return cadena
    

for prueba in range(1,10):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='datos',
                                             user='root',
                                             password='')
        firm = generaCadena()

        firmas = (hashlib.md5(firm.encode())).hexdigest()
        #Para obtener la fecha del servidor y la hora
        try:
            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org')
            ts = response.tx_time
            _date = time.strftime('%Y-%m-%d', time.localtime(ts))
            print(_date)
            _time = time.strftime('%X', time.localtime(ts))
            print(_time)
            # Si deseamos actualizar la fecha en Linux...
            os.system('date' + time.strftime('%m%d%H%M%Y.%S', time.localtime(response.tx_time)))

        except:
            print('ERROR EN EL SERVIDO DE TIEMPO')
        #termina programa para obtener la fecha y hora}
        #Codigo para insertar en la BD
        miZona = zonaHoraria()
        inserta_Clima = (
            "INSERT INTO clima(nombre, firma, latitud,longitud,fecha,hora,utc,variable,valor) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        datos_Clima = (dispositivo, firmas, latitud, longitud, _date, _time, miZona, "temperatura", temperatura)

        cursor = connection.cursor()
        cursor.execute(inserta_Clima, datos_Clima)
        emp_no = cursor.lastrowid
        connection.commit()
        print(cursor.rowcount, "Registro insertado con éxito")
        temperatura = temperatura+1
        time.sleep(2)
        cursor.close()
    except mysql.connector.Error as error:
        print("No se pudo insertar el registro  {}".format(error))
    finally:
        if (connection.is_connected()):
            connection.close()
            print("MySQL Conexion cerrada")
