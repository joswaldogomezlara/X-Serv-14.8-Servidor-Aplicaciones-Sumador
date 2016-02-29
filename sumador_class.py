#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket


class Conexion:
    """Esta clase va a ocuparse del envio y recepcion de paquetes HTTP"""

    def conectar(self):

        host = socket.gethostname()
        port = 1235
        self.primer_num = True

        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.mySocket.bind((host, port))

        self.mySocket.listen(5)

        print 'Eres el host:', host
        print 'Estas en el puerto:', str(port)

    def recibir(self):

        print 'Esperando conexiones...'

        (recvSocket, address) = self.mySocket.accept()
        self.recvSocket = recvSocket

        print 'Peticion recibida:'

        self.recibido = recvSocket.recv(2048)

        print self.recibido

    def enviar(self):

        if self.primer_num:

            self.sumando1 = self.recibido.split(' ')[1][1:]

            if self.sumando1 == 'favicon.ico':
                print 'Peticion de icono, no hay sumandos'
            elif self.sumando1 == '':
                print 'Peticion vacia'
            else:

                print 'Recibido el número: ', self.sumando1

                print 'Respondiendo...'
                self.recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                                "<html><body>" +
                                "<p>Recibido el numero: " + str(self.sumando1) + "</p>"
                                "<p>Esperando el segundo numero a sumar...</p>" + 
                                "</body></html>" + "\r\n")
                self.recvSocket.close()

                self.primer_num = False

        else:

            sumando2 = self.recibido.split(' ')[1][1:]

            if sumando2 == 'favicon.ico':
                print 'Peticion de icono, no hay sumandos'
            elif sumando2 == '':
                print 'Peticion vacia'
            else:

                print 'Recibido el número: ', sumando2

                resultado = int(self.sumando1) + int(sumando2)

                print 'Respondiendo...'
                self.recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                                "<html><body>" +
                                "<p>" + 
                                str(self.sumando1) + 
                                "+" + 
                                str(sumando2) + 
                                "=" + 
                                str(resultado) +
                                "</p>" + 
                                "</body></html>" + "\r\n")
                self.recvSocket.close()

                self.primer_num = True

    def cerrar(self):

        self.mySocket.close()
        print "\nCerrando la conexion"

"""Hasta aqui la clase Conexion"""
"""Empezamos el main"""


Sumador = Conexion()
Sumador.conectar()

try:
    while True:

        Sumador.recibir()
        Sumador.enviar()

except KeyboardInterrupt:

    Sumador.cerrar()
















