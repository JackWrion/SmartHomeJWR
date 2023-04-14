import sys
from Adafruit_IO import MQTTClient, Client, Feed
import random
import time
import serial.tools.list_ports


AIO_FEED_ID = "bbc-led"
AIO_USERNAME = "jackwrion12345"
AIO_KEY = "aio_PKBs417u0k1FTGBNzxZ1laAXB0nl"


######### Config Adafruit ######################

#Function about Adafruit
def connected ( client ) :
    print ("Ket noi thanh cong ...")
    client.subscribe( AIO_FEED_ID )

def subscribe ( client , userdata , mid , granted_qos ) :
    print(" Subcribe thanh cong ...")

def disconnected ( client ) :
    print(" Ngat ket noi ...")
    sys.exit(1)

def message ( client , feed_id , payload ):
    print (" Nhan du lieu : " + payload )
    ser.write(  ( str(payload) + "#").encode() )


#################################################################






#readSerial from Microbit --> processData --> publish to Adafruit
#Get message from Adafruit --> ser.write to Microbit

###################################################################################
######################    Send from Microbit to Gateway   #########################


def getPort () :
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range (0 , N) :
        port = ports [ i ]
        strPort = str( port )
        if "USB Serial Device" in strPort :
            splitPort = strPort.split (" ")
            commPort = ( splitPort [0])
    return commPort



# Connect to Microbit
ser = serial.Serial(port = getPort() , baudrate =115200)


#Function about Reading process
def processData ( data ) :
    data = data.replace ("!", "")
    data = data.replace ("#", "")
    splitData = data.split(":")
    print ( splitData )
    if splitData[1] == "TEMP":
        client.publish("bbc-temp", splitData[2])

# Read from Microbit
mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


###################################################################################











client = MQTTClient ( AIO_USERNAME , AIO_KEY )
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background ()





while True:
    readSerial()
    time.sleep (5)
    