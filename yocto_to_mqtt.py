import sys, os
import time
import paho.mqtt.client as mqtt
import flynn
import json
from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *
sys.path.append("/home/ubuntu/yoctolib_python/Sources")

flag = False
host = "192.168.2.254"
data = {}
errmsg=YRefParam()

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname+' <serial_number>')
    print(scriptname+' <logical_name>')
    print(scriptname+' any  ')
    sys.exit()

if len(sys.argv)<2 :  usage()

target=sys.argv[1]


# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)

if target=='any':
    # retreive any humidity sensor
    sensor = YHumidity.FirstHumidity()
    if sensor is None :
        die('No module connected')
    m = sensor.get_module()
    target = m.get_serialNumber()

else:
    m = YModule.FindModule(target)

if not m.isOnline() : die('device not connected')

while flag == False :
    try :
        client = mqtt.Client()
        client.connect("173.38.154.151", 80, 60)
        flag=True
        client.loop_start()
    except :
        print "Waiting for connectivity"
	time.sleep(3)

humSensor = YHumidity.FindHumidity(target+'.humidity')
pressSensor = YPressure.FindPressure(target+'.pressure')
tempSensor = YTemperature.FindTemperature(target+'.temperature')

while True :
	data['devid'] = '1122334455'
    	data['proto'] = 'tcp'
    	data['type'] = 'iox'
    	data['hum'] = humSensor.get_currentValue()
	data['press'] = pressSensor.get_currentValue()
	data['temp'] = tempSensor.get_currentValue()
    	msg = json.dumps(data)
    	client.publish("adt/tcp/iox/1122334455", msg, qos=0, retain=False)
	time.sleep(3)
    # or with cbor - that should first go to our GW
    #enc = flynn.dumps(msg)
    #encArr = bytearray(enc)
    #client.publish("ioxsensor", encArr, qos=0, retain=False)