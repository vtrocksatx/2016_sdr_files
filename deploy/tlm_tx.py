#!/usr/bin/env python
##################################################
# Title: E310 Serial to Ethernet Test
# Author: Zachary James Leffke
# Description: 
#   Test pyserial module on E310
# Generated: April 5, 2016
##################################################

import os
import sys
import time
import string
import serial
import socket
import threading


from optparse import OptionParser
from datetime import datetime as date
from tx_scram_sock import *

START_MSG = "$,KJ4QLP,STARTUP MESSAGE,"

class Ser2Net_Server(threading.Thread):
    def __init__ (self, options):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.addr = options.addr
        self.port = int(options.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.device = options.device
        self.baud = options.baud
        self.startup_delay = options.thread_delay
        self.rate = options.rate
        self.callsign = options.callsign
        self.ser_fault = False #flag to indicate problem with serial port
        self.err_count = 0
        self.ser_data = "$," + self.callsign + ",START MESSAGE," + self.utc_ts()
        self.port_flag = False
        
    def run(self):
        time.sleep(self.startup_delay)
        try:
            self.Open_Serial(self.device)
        except Exception as e:
            self.Handle_Exception(e)
        
        while 1:
            if self.ser_fault == False:
                try: 
                    if self.ser.inWaiting() >= 256: 
                        self.ser_data = self.ser.readline()
                except Exception as e:
                    self.Handle_Exception(e)
            if self.ser_fault == True:
                try:
                    self.Open_Serial(self.device)
                    self.ser_data = "$," + self.callsign + ",RECONNECTED TO SERIAL PORT," + str(self.device) + "," + self.utc_ts()
                except Exception as e:
                    self.Handle_Exception(e)
              
                if self.ser_fault == True: #Try other serial port
                    try:
                        self.Open_Serial("/dev/ttyACM1")
                        self.ser_data = "$," + self.callsign + ",RECONNECTED TO SERIAL PORT," + "/dev/ttyACM1," + self.utc_ts()
                    except Exception as e:
                        self.Handle_Exception(e)
            self.Write_Socket()
            time.sleep(self.rate)
        sys.exit()
    
    def Open_Serial(self, dev):
        self.ser = serial.Serial(dev, self.baud, dsrdtr=True, xonxoff=True, rtscts=True)
        #self.ser = serial.Serial()
        #self.ser.port = dev
        #self.ser.baudrate = self.baud
        #self.ser.setDTR(True)
        #self.ser.open()
        self.ser.flushInput()
        self.ser_fault = False

    def Handle_Exception(self, e):
        self.err_count += 1
        if type(e) == serial.serialutil.SerialException:
            self.ser_data = "$," + self.callsign + ",SERIAL FAULT," + str(self.err_count) + "," + self.utc_ts() + "," + str(e)
        else:
            self.ser_data = "$," + self.callsign + ",UNKNOWN FAULT," + str(self.err_count) + "," + self.utc_ts() + "," + str(e)
        self.ser_fault = True

    def Write_Socket(self):
        if len(self.ser_data) < 256:
            length = len(self.ser_data)
            pad_length = 255 - length
            for i in range(pad_length):
                self.ser_data = self.ser_data + "#"
            self.ser_data = self.ser_data + "\n"

        if len(self.ser_data) > 256:
            self.ser_data = self.ser_data[:256]
            
        #print len(self.ser_data)
        #print self.utc_ts() + self.ser_data
        self.sock.sendto(self.ser_data, (self.addr, self.port))
        

    def stop(self): 
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def utc_ts(self):
        return str(date.utcnow()) + " UTC"
    
if __name__ == '__main__':
    #ts = (date.datetime.utcnow()).strftime("%Y%m%d")

    #--------START Command Line option parser------------------------------------------------------
    usage = "usage: %prog <options>"
    parser = OptionParser(usage = usage)

    del_help = "Startup Delay [sec], [default=%default]"
    c_help = "Callsign for status packets, [default=%default]"
    parser.add_option("-w","--delay"  ,dest="delay"  ,action="store",type="float",default=".1",help=del_help)
    parser.add_option("-c","--callsign",dest="callsign",action="store",type="string",default="KM4SRC",help=c_help)

    #----Serial/socket options----
    a_help = "Destination IP Address, [default=%default]"
    p_help = "Destination Port, [default=%default]"
    d_help = "Serial Device, [default=%default]"
    b_help = "Serial Baud, [default=%default]"
    r_help = "Socket Write Speed [sec], [default=%default]"
    dev_del_h = "Serial To Ethernet Thread Delay [sec], [default=%default]"

    parser.add_option("-a","--addr"  ,dest="addr"  ,action="store",type="string",default="127.0.0.1",help=a_help)
    parser.add_option("-p","--port"  ,dest="port"  ,action="store",type="string"   ,default="4000",help=p_help)
    parser.add_option("-d","--device",dest="device",action="store",type="string",default="/dev/ttyACM0",help=d_help)
    parser.add_option("-b","--baud"  ,dest="baud"  ,action="store",type="int"   ,default="115200",help=b_help)
    parser.add_option("-r","--rate"  ,dest="rate"  ,action="store",type="float" ,default="0.044",help=r_help)
    parser.add_option("-s","--thread_delay",dest="thread_delay",action="store",type="float" ,default="4.0",help=dev_del_h)

    #GNU Radio Options
    #addr_help           = "Set addr [default=%default]"
    alpha_help          = "Set alpha [default=%default]"
    bb_gain_help        = "Set bb_gain [default=%default]"
    #port_help           = "Set port [default=%default]"
    samps_per_symb_help = "Set samps_per_symb [default=%default]"
    tx_correct_help     = "Set tx_correct [default=%default]"
    tx_freq_help        = "Set tx_freq [default=%default]"
    tx_gain_help        = "Set tx_gain [default=%default]"
    samp_rate_help      = "Set samp_rate [default=%default]"
    tx_offset_help      = "Set tx_offset [default=%default]"

    #parser.add_option("", "--addr", dest="addr", type="string", default="127.0.0.1", help=addr_help)
    parser.add_option("", "--alpha", dest="alpha", type="float", default=0.5,help=alpha_help)
    parser.add_option("", "--bb-gain", dest="bb_gain", type="float", default=0.35,help=bb_gain_help)
    #parser.add_option("", "--port", dest="port", type="string", default="4000",help=port_help)
    parser.add_option("", "--samps-per-symb", dest="samps_per_symb", type="float", default=2,help=samps_per_symb_help)
    parser.add_option("", "--tx-correct", dest="tx_correct", type="float", default=0,help=tx_correct_help)
    parser.add_option("", "--tx-freq", dest="tx_freq", type="float", default=2395e6,help=tx_freq_help)
    parser.add_option("", "--tx-gain", dest="tx_gain", type="float", default=80,help=tx_gain_help)
    parser.add_option("", "--samp-rate", dest="samp_rate", type="float", default=250e3,help=samp_rate_help)
    parser.add_option("", "--tx-offset", dest="tx_offset", type="float", default=0,help=tx_offset_help)

    (options, args) = parser.parse_args()
    #--------END Command Line option parser------------------------------------------------------

    time.sleep(options.delay)

    ser2net_thread = Ser2Net_Server(options)
    ser2net_thread.daemon = True
    #server_thread.run()
    ser2net_thread.start()

    tb = tx_scram_sock(addr=options.addr, alpha=options.alpha, bb_gain=options.bb_gain, port=options.port, samps_per_symb=options.samps_per_symb, tx_correct=options.tx_correct, tx_freq=options.tx_freq, tx_gain=options.tx_gain, samp_rate=options.samp_rate, tx_offset=options.tx_offset)
    tb.start()


    while 1:
        time.sleep(1)
    
    sys.exit()
