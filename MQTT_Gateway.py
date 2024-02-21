import random
import time
import sys
import serial.tools.list_ports
from datetime import date
from Adafruit_IO import MQTTClient

today = date.today()
strTextToday = today.strftime("%B %d %Y")
print(strTextToday)

AIO_FEED_ID_1 = "led"
AIO_FEED_ID_2 = "humid-sensor"
AIO_FEED_ID_3 = "light-sensor"
AIO_FEED_ID_4 = "thermometer"
AIO_FEED_ID_5 = "relay"
AIO_USERNAME = "YncognitoMei"
AIO_KEY = "aio_Bifl808YcND5NZnZKC3ZSLTPEC6N"

def connected(client):
  print("Ket noi thanh cong.......")
  client.subscribe(AIO_FEED_ID_1)
  client.subscribe(AIO_FEED_ID_2)
  client.subscribe(AIO_FEED_ID_3)
  client.subscribe(AIO_FEED_ID_4)
  client.subscribe(AIO_FEED_ID_5)

def subscribe(client, userdata, mid, granted_qos):
  print("Subcribe thanh cong.......")

def disconnected(client):
  print("Ngat ket noi......")
  sys.exit(1)

def message(client, feed_id, payload):
  print("Nhan du lieu: " + payload)
  if isMicrobitConnected:
    ser.write((str(payload) + "#").encode())

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
  ports = serial.tools.list_ports.comports()
  N = len(ports)
  commPort = "COM5"
  for i in range(0, N):
    port = ports[i]
    strPort = str(port)
    if "USB Serial Device" in strPort:
      splitPort = strPort.split(" ")
      commPort = (splitPort[0])
  return commPort

isMicrobitConnected = False
if getPort() != "None":
  ser = serial.Serial(port = getPort(), baudrate = 115200)
  isMicrobitConnected = True


def processData(data):
  data = data.replace("!", "")
  data = data.replace("#", "")
  splitData = data.split(":")
  print(splitData)
  if splitData[1] == "temperature":
    client.publish("thermometer", splitData[2])
  if splitData[1] == "humid":
    client.publish("humid-sensor", splitData[2])
  if splitData[1] == "light":
    client.publish("light-sensor", splitData[2])

mess = ""
def readSerial():
  bytesToRead = ser.inWaiting()
  if (bytesToRead > 0):
    global mess
    while ("#" in mess) and ("!" in mess):
      start = mess.find("!")
      end = mess.find("#")
      processData(mess[start:end + 1])
      if(end == len(mess)):
        mess = ""
      else:
        mess = mess[end + 1:]

while True:
  if isMicrobitConnected:
      readSerial()
  time.sleep(1)

  led = 0
  relay = 0

  humid = random.randint(0, 100)
  print("Cap nhat do am:", humid)
  client.publish("humid-sensor", humid)
  time.sleep(1)


  if humid <= 50:
    relay = 1
    print("May bom da bat")
    client.publish("relay", relay)
  elif humid > 50:
    relay = 0
    print("May bom da tat")
    client.publish("relay", relay)
  time.sleep(5)

  light = random.randint(2000, 10000)
  print("Cap nhat do sang:", light)
  client.publish("light-sensor", light)
  time.sleep(1)

  if light <= 3000:
    led = 1
    print("Den da bat")
    client.publish("led", led)
  elif light > 3000:
    led = 0
    print("Den da tat")
    client.publish("led", led)
  time.sleep(5)

  temp = random.randint(0, 40)
  print("Cap nhat nhiet do:", temp)
  client.publish("thermometer", temp)
  time.sleep(1)

pass
