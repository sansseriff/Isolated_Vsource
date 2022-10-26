"""
vsource_controll.py
author: Andrew Mueller
Date: May 17, 2022
Adapted from code by Lautaro and Ioana

This file defines functions for using an isolated voltage source with triax outputs build by Lautaro.
The interface is over ethernet UDP

This is only for use by the FastAPI webserver. 
"""
import socket


class isolatedVSource():
    def __init__(self, ipAddress, timeout, upd_remote_port, udp_local_port, testChannel, **kwargs):
        self.ipAddress = str(ipAddress)
        self.timeout = timeout
        self.upd_remote_port = upd_remote_port
        self.udp_local_port = udp_local_port
        self.testChannel = testChannel
        self.sock = -1
        

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        sock.bind(('', self.udp_local_port))
        #sock.listen(1)
        #sock.setblocking(0)
        self.sock = sock

    def setVoltage(self, chan, volt):
        assert chan >= 1 and chan <= 4, "channel number not within 1-4"
        assert volt >= -5 and volt <= 5, "voltage less than -5 or greater than 5"
        var='V_set='+str(chan)+'_'+str(volt)
        if self.sock == -1:
            print("Socket not connected")
        else:
            self.sock.sendto(var.encode(), (self.ipAddress, self.upd_remote_port))