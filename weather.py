import requests
import json
import sys
import os
import matplotlib.pyplot as plt

def extract_labels_rainprob(item):
    _len = len(item['time'])    #how many item in the list
    x_axis = list(range(0,_len))
    x_label=[]
    y_axis=[]
    for detail in item['time']:
        y_axis.append(int(detail['elementValue'][0]['value']))
        x_label.append(detail['startTime'][5:-6])
    plt.plot(x_axis, y_axis)
    plt.ylim(0, 100)
    plt.xticks(x_axis,x_label,rotation='vertical')  #
    plt.show()

    
        



def six_hr_rain_prob(info):
    item = info['weatherElement'][7]
    print(item['description'])
    print('----------------------------------------------------------------')
    for detail in item['time']:
        print("{start}   ~   {end}\t\t {percent}%".format(start=detail['startTime'], end=detail['endTime'], percent= detail['elementValue'][0]['value']))
    print("----------------------------------------------------------------\n")
    extract_labels_rainprob(item)
    return

def feeling_temperature(info):
    item = info['weatherElement'][2]
    print(item['description'])
    print('----------------------------------------------------------------')
    for detail in item['time']:
        print("{time}\t\t {temp}°C".format(time=detail['dataTime'], temp= detail['elementValue'][0]['value']))
    print("----------------------------------------------------------------\n")
    return

def real_temperature(info):
    item = info['weatherElement'][3]
    print(item['description'])
    print('----------------------------------------------------------------')
    for detail in item['time']:
        print("{time}\t\t {temp}°C".format(time=detail['dataTime'], temp= detail['elementValue'][0]['value']))
    print("----------------------------------------------------------------\n")
    return


auth_code='??'

res = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-053?Authorization={}&limit=3&offset=0&format=JSON&sort=time".format(auth_code))

parsed_result=json.loads(res.text)
hsinchi_east_disctict = parsed_result['records']['locations'][0]['location'][1]

while 1:
    option=0
    print("1: 6hr降雨機率\t2: 體感溫度\t3: 溫度\t0: exit from the program")
    option=int(input("enter the information you want: "))
    os.system("clear")

    if option==0:
        sys.exit(0)
    elif option==1:
        six_hr_rain_prob(hsinchi_east_disctict) #7
    elif option==2:
        feeling_temperature(hsinchi_east_disctict) #2
    elif option==3:
        real_temperature(hsinchi_east_disctict) #3
    else:
        print("Please enter a number between 0~3\n\n\n")
