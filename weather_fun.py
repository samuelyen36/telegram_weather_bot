import requests
import json
import sys
import os
import matplotlib.pyplot as plt

def send_photo(user_id):
    auth="???"
    url = "https://api.telegram.org//sendPhoto".format(auth);
    files = {'photo': open('tmp.png', 'rb')}
    data = {'chat_id' : user_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

chat_id="???"    #token of the telegram bot

def six_hr_rain_prob(info,user_id):
    def extract_labels_rainprob(item):
        fig = plt.figure()
        _len = len(item['time'])    #how many item in the list
        x_axis = list(range(0,_len))
        x_label=[]
        y_axis=[]
        for detail in item['time']:
            y_axis.append(int(detail['elementValue'][0]['value']))
            x_label.append(detail['startTime'][5:-6])
        plt.plot(x_axis, y_axis)
        plt.ylim(0, 100)
        plt.grid(True)
        plt.xticks(x_axis,x_label,rotation='vertical')  #
        plt.savefig("tmp.png")
        return fig

    item = info['weatherElement'][7]
    res = item['description']
    res += "\n----------------------------------------------------------------"
    for detail in item['time']:
        res +="\n{start}   ~   {end}\t\t {percent}%".format(start=detail['startTime'], end=detail['endTime'], percent= detail['elementValue'][0]['value'])
    res += "\n----------------------------------------------------------------\n"
    extract_labels_rainprob(item)
    send_photo(user_id)
    os.system("rm tmp.png")
    return "here's the result\n"

def feeling_temperature(info):
    item = info['weatherElement'][2]
    res = item['description'] + '\n----------------------------------------------------------------'
    for detail in item['time']:
        #print("{time}\t\t {temp}°C".format(time=detail['dataTime'], temp= detail['elementValue'][0]['value'])
        res += "\n{time}\t\t {temp}°C".format(time=detail['dataTime'], temp= detail['elementValue'][0]['value'])
    res +="\n----------------------------------------------------------------\n"
    return

def real_temperature(info,user_id):
    def extract_labels_realtemp(item):
        fig = plt.figure()
        _len = len(item['time'])    #how many item in the list
        x_axis = list(range(0,_len))
        x_label=[]
        y_axis=[]
        for detail in item['time']:
            y_axis.append(int(detail['elementValue'][0]['value']))
            x_label.append(detail['dataTime'][5:-6])
        plt.plot(x_axis, y_axis)
        plt.ylim(min(y_axis)-3, max(y_axis)+3)
        plt.grid(True)
        plt.xticks(x_axis,x_label,rotation='vertical')  #
        plt.savefig("tmp.png")
        return fig

    item = info['weatherElement'][3]
    #print(item['description'])
    res = item['description'] + '\n----------------------------------------------------------------'
    #print('----------------------------------------------------------------')
    for detail in item['time']:
        #print("{time}\t\t {temp}°C".format(time=detail['dataTime'], temp= detail['elementValue'][0]['value']))
        res += "\n{time}\t\t {temp}°C".format(time=detail['dataTime'], temp= detail['elementValue'][0]['value'])
    res +="\n----------------------------------------------------------------\n"
    extract_labels_realtemp(item)
    send_photo(user_id)
    os.system("rm tmp.png")
    return res

def whole(fun=0,city="新竹市東區",user_id=0):   #function => 0 for temp, 1 for six_hr_rain, 2 for both
    #auth_code='???'
    if city=="新竹市東區":
        res = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-053?Authorization={}&limit=3&offset=0&format=JSON&sort=time".format(auth_code))
        parsed_result=json.loads(res.text)
        get_location_info = parsed_result['records']['locations'][0]['location'][1]
    if city=="台北市信義區":
        res = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-061?Authorization={}&limit=3&offset=0&format=JSON&sort=time＆locationName=信義區".format(auth_code))
        parsed_result=json.loads(res.text)
        get_location_info = parsed_result['records']['locations'][0]['location'][0]
    if city=="台北市南港區":
        res = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-061?Authorization={}&limit=3&offset=0&format=JSON&sort=time＆locationName=南港區".format(auth_code))
        parsed_result=json.loads(res.text)
        get_location_info = parsed_result['records']['locations'][0]['location'][0]
    if city=='新北市汐止區':
        res = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-069?Authorization={}&limit=3&offset=0&format=JSON&sort=time＆locationName=汐止區".format(auth_code))
        parsed_result=json.loads(res.text)
        get_location_info = parsed_result['records']['locations'][0]['location'][0]
    if city=='基隆市中山區':   
        res = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-049?Authorization={}&format=JSON&limit=3&offset=0&format=JSON&sort=time&locationName=%E4%B8%AD%E5%B1%B1%E5%8D%80".format(auth_code))
        parsed_result=json.loads(res.text)
        get_location_info = parsed_result['records']['locations'][0]['location'][0]

    if fun==0:
        _str = real_temperature(get_location_info,user_id)
    elif fun==1:
        _str = six_hr_rain_prob(get_location_info,user_id)
    elif fun==2:
        _str = six_hr_rain_prob(get_location_info,user_id) + real_temperature(get_location_info,user_id)
    return _str


