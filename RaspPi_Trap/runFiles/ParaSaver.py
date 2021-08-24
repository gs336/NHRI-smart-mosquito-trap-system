import time
import datetime
import threading
import math
import Adafruit_ADS1x15
import numpy
import Adafruit_DHT
import os
import http.client
from pathlib import Path



adc = Adafruit_ADS1x15.ADS1115()

sensor = Adafruit_DHT.DHT22
humidity, temperature = Adafruit_DHT.read_retry(sensor, 4 )


#Gets the name of wifi or ethernet

def getEthName():
    try:
        interface = "NoneFound"
        for root,dirs,files in os.walk('/sys/class/net'):
            for d in dirs:
                if d[:4] == 'wlan' or d[:3] == 'enx' or d[:3] == 'eth':
                    interface = d
    except:
        interface = "NoneFound"
    return interface


#it will get MAC address and print
def getMAC(interface=''):
    try:
        str = open('/sys/class/net/%s/address' %interface).read()
        str = str[0:17].replace(':','')
    except:
        str = '-1'
    return str

def output_data_list(date_now,ethMAC,kind,temperature,humidity,get_co2_data):
    #for output data to a txt or csv
    str = "/mos/mosadd.php?mac=%s&s1=%s&s2=%s&s3=%.2f&s4=%.2f&s5=%.2f"%(ethMAC, date_now, kind, temperature, humidity, get_co2_data)
    if ethMAC != '-1':
        file = Path('/home/pi/runFiles/temp.txt')
        if file.is_file():
            with open('/home/pi/runFiles/temp.txt','r') as temp:
                data = temp.read()
            data = data.split('\n')
            os.remove('/home/pi/runFiles/temp.txt')
            for single_data in data:
                if single_data != '':
                    try:
                        conn = http.client.HTTPConnection("211.76.174.225",8888, timeout=60)
                        conn.request("GET", single_data)
                        #r = conn.getresponse()
                        #time.sleep(10)
                    except:# request.exceptions.RequestException as e:# requests.exceptions.RequestException as e:
                        print('Exception in single data')
                        data_output = open('/home/pi/runFiles/temp.txt','at')
                        data_output.write(single_data+'\n')
                        data_output.close()                        
        try:
            conn = http.client.HTTPConnection("211.76.174.225",8888, timeout=60)
            conn.request("GET", str)
            #r = conn.getresponse()
            #time.sleep(10)
        except: # request.exceptions.RequestException as e: #requests.exceptions.RequestException as e:
            print('Exception in data_output')
            data_output = open('/home/pi/runFiles/temp.txt','at')
            data_output.write(str+'\n')
            data_output.close()

    else:
        data_output = open('/home/pi/runFiles/temp.txt','at')
        data_output.write(str+'\n')
        data_output.close()
    return 0    
    

def CO2():
    GAIN = 1
    MG811i=0
    MG811=0
    V400=0.82*32768/4.09
    V1000=0.3*32768/4.09
    slop=(V1000-V400)/(numpy.log10(1000)-numpy.log10(400))
    i = 0
    while i<5:
        Value=0
        try:
            Value = adc.read_adc(0, gain=GAIN)
            MG811+=Value
            MG811i+=1
        except:
            print('cannot read') 
        time.sleep(0.05)
        i+=1
    if MG811i != 0:
        MG811=MG811/MG811i
    #print(MG811*4.09/32768)
    CO2percentage=2.602+(MG811-V400)/slop
    return round(math.pow(10,CO2percentage), 2)

def SaveParameter(MosquitoType):
    kind = MosquitoType
    date_now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    date_now = date_now.replace(' ','%20')
    ethMAC = getMAC(getEthName())
    get_co2_data = CO2()
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 4 )
    try:
        humidity = round(humidity, 2); temperature = round(temperature, 2)
    except:
        humidity=0.0; temperature=0.0
    output_data_list(date_now, ethMAC, kind, temperature, humidity, get_co2_data)
    return 0

SaveParameter('Culex')
