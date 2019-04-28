#HackMx2019
#28 abril
#Proyecto: Auto Verification for Banking
#Miembros:
#Navarro Pérez Diego Andrés: danp_0507@hotmail.com
#Luna Reyes Rodrigo: irodrigoro@gmail.com
#González Granados Adolfo: adolfognz@outlook.com


##########################################

#Lectura de -Asunto- de los correos#
#Establecer conexión con el correo

import smtplib
import time
import imaplib
import email

from email.parser import BytesParser, Parser
from email.policy import default

print ("¡Bienvenido a Banorte!")
print ("¡Utiliza nuestro nuevo sistema de seguridad implementando una clave única para que visualices la autenticidad de nuestros correos!")
x = 'no'
while x:
    #propofmg@gmail.com
    correogmail = input("Ingresa tu correo gmail asociado a tu cuenta Banorte: ")
    #sidralmundet
    contraseña = input("Ingresa tu contraseña asociada a tu cuenta Banorte: ")
    #12345678
    claveunica = input("Ingresa tu clave de identificación única: ")
    x = input("¿Estás seguro de que tus datos son correctos? yes/no ")
    if x == 'yes':
        break

#ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = correogmail
FROM_PWD    = contraseña
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL,FROM_PWD)
mail.select('inbox')

listaclave=[]
listarevisar=[]
typ, data = mail.search(None, 'UNSEEN')
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822.header)')
    msg = email.message_from_bytes(data[0][1])
    print (msg['subject'])
    if (msg['subject'].lower()).find('banorte') != -1:
        listarevisar.append(msg['subject'])

#Creamos una lista para los correos verificados y los cuestionables
i=0
for element in listarevisar:
    if (listarevisar[i]).find(claveunica) != -1:
        listaclave.append(listarevisar[i])
        listarevisar.remove(listarevisar[i])
    i+=1

print("")
print('Lista con los correo no autenticados:')
print(listarevisar)
print('Lista con los correo autenticados:')
print(listaclave)
print("")

mail.create('SpamBanorte')
#Mandamos los no reconocidos a spam
typ, data = mail.search(None, 'UNSEEN')
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822.header)')
    msg = email.message_from_bytes(data[0][1])
    if msg['subject'] in listarevisar:
        print ('Chequeo de proceso...')
        mail.copy(num, 'SpamBanorte')
#Y los eliminamos de la bandeja principal
typ, data = mail.search(None, 'UNSEEN')
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822.header)')
    msg = email.message_from_bytes(data[0][1])
    if msg['subject'] in listarevisar:
        print ('Chequeo de proceso...')
        mail.store(num, '+FLAGS', '\\Deleted')

print("")
print('Programa finalizado')
mail.close()
mail.logout()








