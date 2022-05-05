# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:44:49 2022
@author: SOLILOP
"""

from socket import *

socket_del_cliente = socket(AF_INET, SOCK_DGRAM)
client_address = ('192.168.56.1', 50001)
canal_socket_adress = ('192.168.56.1', 40010)

print('connecting to {} port {}'.format(*client_address))

socket_del_cliente.bind(client_address)
socket_del_cliente.settimeout(10.0)

def CheckSum(msg):
    suma = 0
    for i in msg:
        n_ascii = ord(i)
        suma += n_ascii
    ck1 = suma//256
    ck2 = suma%256
    
    ck1_ch = chr(ck1)
    ck2_ch = chr(ck2)
    
    return f'{msg}{ck1_ch}{ck2_ch}'

def DAT(msg):
    
    tp = 'DAT'
    sec = '0'
    
    return f'{tp}{sec}{msg}'



"""
envio mensaje con el checksum

DESDE EL SERVIDOR compruevo el checksum que son 2 caracteres al final
"""
try:

    for i in range(4):
        
        msg = DAT('hola'*100) #construir mensaje
        mensaje_tx = CheckSum(msg) #anyado el checksum
        
        #enviar mensaje atraves del canal
        #es decir, mandamos el mensaje por el puerto 40001
        socket_del_cliente.sendto(mensaje_tx.encode(), canal_socket_adress)
        print('\nEl mensaje ha sido enviado. Esperando respuesta...')
        
        #recibimos la respuesta del servidor que llega por el canal
        mensaje_rx, recv_address= socket_del_cliente.recvfrom(2048)
        
        #decimos que si hay mensaje de respuesta
        if mensaje_rx:

            #separ checksum del mensaje recibido
            msg_rx = mensaje_rx.decode()[:-2]
            ck_rx = mensaje_rx.decode()[-2:]     
   
            #calcular checksum de msg_rx
            ck_rx_prima = CheckSum(msg_rx)      
      
            #si no coincidel los checksums, imprime NAK por pantalla
            if ck_rx != ck_rx_prima[-2:]: 
                print('NAK')
                
            else:
                print(msg_rx)
                
finally:
    print('closing socket')    
    socket_del_cliente.close()