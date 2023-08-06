import os
import glob
import logging
import sys
import serial
import serial.tools.list_ports as list_ports
import time
import platform
import threading

import array
import usb.core
import usb.util
import usb.control

# meowbit vendor and pid
VENDER = 0xf055
PRODUCT = 0x9800
CDC_COMM_INTF = 1
EP_IN = 0x83
EP_OUT = 0x03

# http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
def serialList():
    """Lists serial ports
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    serialPortList = []
    for port in list_ports.comports():
        if port.pid and port.vid:
            serialPortList.append({'name': port.description, 'type':'serial', 'peripheralId': port.device, 'pid': port.pid, 'vid': port.vid})

    if platform.system() == "Windows":
        try:
          usbCdc = usb.core.find(idVendor=VENDER, idProduct=PRODUCT)
          if usbCdc:
            serialPortList.append({
                'name': "Mewobit CDC STM32",
                'type':'serial',
                'peripheralId': "USB_CDC_stm32",
                'pid': PRODUCT,
                'vid': VENDER
            })
        except Exception as err:
            if "No backend available" in str(err):
                pass

    return serialPortList

logger = logging.getLogger(__name__)

class serialRead(threading.Thread):
    def __init__(self,ser,cb):
        self.ser = ser
        self.cb = cb
        self.running = True
        self.rawMode = False
        self.t = time.clock()
        threading.Thread.__init__(self)
    
    def run(self):
        while self.running:
            try:
                while self.ser.pybMutex:
                    time.sleep(1)
                c = self.ser.read(64)
                if c:
                    dt = (time.clock() - self.t)*1000000
                    self.cb(c, dt)
                    self.t = time.clock()
            except Exception as err:
                logger.warn("Serial Read error %s" %err)
                self.running = False
                self.cb(None, -1)

class cdcRead(threading.Thread):
    def __init__(self,ep,cb):
        self.ep = ep
        self.cb = cb
        self.running = True
        self.t = time.clock()
        threading.Thread.__init__(self)
    
    def run(self):
        while self.running:
            try:
                while self.ep.pybMutex:
                    time.sleep(1)
                c = self.ep.read(self.ep.wMaxPacketSize, 200)
                if c:
                    dt = (time.clock() - self.t)*1000000
                    self.cb(c, dt)
                    self.t = time.clock()
            except Exception as err:
                errLog = str(err)
                if 'timeout error' in errLog:
                    pass
                else:
                    logger.warn("CDC Read error %s" %err)
                    self.running = False
                    self.cb(None, -1)

class serialCom():
    usbdev = None
    def __init__(self,rxCallback):
        self.rxcb = rxCallback
        self.ser = None
        self.dev = serialCom.usbdev
        self.rxth = None
        self.ep_out = None
        self.ep_in = None
        return

    def setPybMutex(self, v):
        if self.ser:
            self.ser.pybMutex = v
        if self.ep_in:
            self.ep_in.pybMutex = v

    def cdcCallbackHook(self, msg, dt):
        if msg == None and dt == -1:
            usb.util.release_interface (self.dev, 2)
            usb.util.release_interface (self.dev, CDC_COMM_INTF)
            usb.util.dispose_resources(self.dev)
            self.dev = serialCom.usbdev = None
        self.rxcb(msg, dt)
    
    def connect(self,port,baud=115200,timeout=0.05):
        if port == 'USB_CDC_stm32':
            # zadig mewobit stm32
            # only config once for cdc runtime
            if self.dev == None:
                serialCom.usbdev = usb.core.find(idVendor=VENDER, idProduct=PRODUCT)
                self.dev = serialCom.usbdev
                self.dev.set_configuration(1)
                usb.util.claim_interface(self.dev, CDC_COMM_INTF)

            self.cfg = self.dev.get_active_configuration()
            self.intf = self.cfg[(1, 0)]
            # stick endpoint in and out setup
            self.ep_out = self.intf[0]
            self.ep_in = self.intf[1]
            # baudrate at 115200
            self.dev.ctrl_transfer(0x21, 0x22, 0x01 | 0x02, CDC_COMM_INTF, None)
            self.dev.ctrl_transfer(0x21, 0x20, 0, CDC_COMM_INTF, array.array('B', [0x00, 0xC2, 0x01, 0x00, 0x00, 0x00, 0x08]))

            setattr(self.ep_in, 'pybMutex', False)
            self.rxth = cdcRead(self.ep_in,self.cdcCallbackHook)
            self.rxth.setDaemon(True)
            self.rxth.start()

        else:
            self.ser = serial.Serial(port, baud, timeout=timeout)
            #todo: separate serial reading to different threads
            setattr(self.ser, 'pybMutex', False)
            self.rxth = serialRead(self.ser,self.rxcb)
            self.rxth.setDaemon(True)
            self.rxth.start()
    
    def close(self):
        if self.rxth:
            self.rxth.running = False
        if self.ser:
            self.ser.flush()
            self.ser.close()
        if self.dev:
            ''
            # usb.util.release_interface (self.dev, 2)
            # usb.util.release_interface (self.dev, CDC_COMM_INTF)
            # self.dev.reset() # only reset, no replug event
            # usb.util.dispose_resources(self.dev)
        # todo: find correct api to toggle usb device on disconnect
        # self.dev = None
        self.rxth = None
        self.ser = None
        
    def write(self,msg):
        if self.ser:
            self.ser.write(msg)
        if self.ep_out:
            self.dev.write(EP_OUT, msg)

