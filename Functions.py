import requests,csv,pandas
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pathlib import Path
global date_list
date_list = []
global weather_data
weather_data = {}
global All_Data_Dict
All_Data_Dict = []
log_file = "weather_for_7_Dayes.csv"
def get_data_for_days(data_url="https://eg.freemeteo.com/weather/cairo/daily-forecast/day1/?gid=360630&language=english&country=egypt"):
        dayes = 7
        dayes_url_dict = {}
        url_split = data_url.partition("day1")
        url = ""
        for day in range(0,dayes+1):
            temp = f"Day{day}"
            if day == 0:
                temp = "today"
                response1 = requests.get(url_split[0]+temp+url_split[2])
                url = url_split[0]+temp+url_split[2]
                dayes_url_dict[temp]= [url,response1]
                Get_all_data(url)    
            elif day == 1:
                temp = "tomorrow"
                response1 = requests.get(url_split[0]+temp+url_split[2])
                url = url_split[0]+temp+url_split[2]
                dayes_url_dict[temp]= [url,response1]
                Get_all_data(url)              
            else:
                response1 = requests.get(url_split[0]+temp+url_split[2])
                url = url_split[0]+temp+url_split[2]
                dayes_url_dict[temp]= [url,response1]
                Get_all_data(url)
def Get_max_temp(url):
        response1 = requests.get(url)
        soup = bs(response1.text, 'html.parser')
        temperature_list = []
        temperature_list.append(int(soup.findAll('span', attrs={'class': 'temp'})[0].get_text().split("°C")[0]))
        temperature_list.append(int(soup.findAll('span', attrs={'class': 'temp'})[1].get_text().split("°C")[0]))
        temperature_list.append(int(soup.findAll('span', attrs={'class': 'temp'})[2].get_text().split("°C")[0]))
        temperature_list.append(int(soup.findAll('span', attrs={'class': 'temp'})[3].get_text().split("°C")[0]))
        return max(temperature_list)
def Get_min_temp(url):
        response1 = requests.get(url)
        soup = bs(response1.text, 'html.parser')
        temperature_list = []
        temperature_list.append(int(soup.findAll('span', attrs={'class': 'temp'})[0].get_text().split("°C")[0]))
        temperature_list.append(int(soup.findAll('span', attrs={'class': 'temp'})[1].get_text().split("°C")[0]))
        temperature_list.append(int(soup.findAll('span', attrs={'class': 'temp'})[2].get_text().split("°C")[0]))
        temperature_list.append(int(soup.findAll('span', attrs={'class': 'temp'})[3].get_text().split("°C")[0]))
        return min(temperature_list)    
def Get_Temperature(url):
        return f"max = {Get_max_temp(url)}°C | min = {Get_min_temp(url)}°C"
def Get_all_data(url):
        response1 = ""
        soup = ""
        city = ""
        date_weather = ""
        temperature = ""
        wind_speed = ""
        humidity = ""
        air_pressure = ""
        url = url
        response1 = requests.get(url)
        soup = bs(response1.text, 'html.parser')
        city = soup.findAll('h1')[0].get_text().split("-")[0].split(" ")[0]
        date_weather = soup.findAll('h2')[0].get_text()[-13:]
        temperature = Get_Temperature(url)
        wind_speed = soup.findAll('span', attrs={'class': 'wind'})[3].get_text()
        humidity = soup.findAll('span', attrs={'class': 'info'})[3].find("strong").get_text()
        date_list.append(date_weather)
        if len(date_list) == 8:
                air_pressure = soup.findAll('span', attrs={'class': 'info'})[3].findAll("strong")[3].get_text()
        elif len(date_list) < 8:
                air_pressure = soup.findAll('span', attrs={'class': 'info'})[3].findAll("strong")[4].get_text()
        ################### Add Data To Dict #####################
        weather_data["city"] = city
        weather_data["Temperature"] = temperature
        weather_data["humidity"] = humidity
        weather_data["Air_Pressure"] = air_pressure
        weather_data["wind_speed"] = wind_speed
        weather_data["Date"] = date_weather
        All_Data_Dict.append(weather_data)
        #date_list.append(date_weather)
        save_data()
        print(weather_data)
def save_data():
            if Path(log_file).is_file(): 
                log_save()
            else:
                with open(log_file,"w+",newline="")as create_file:
                   writer = csv.DictWriter(create_file,fieldnames=["city","Temperature","humidity","Air_Pressure","wind_speed","Date"])
                   writer.writeheader()
                   writer.writerow(weather_data)
        ##################################################################
def log_save():
        with open(log_file,"r+",newline="")as read_row:
                row = read_row.readline()
                if "city" in row:
                        temp = True
                else:
                        temp = False
                if temp ==True:
                    with  open(log_file,"a",newline="") as f:
                        writer = csv.DictWriter(f,fieldnames=["city","Temperature","humidity","Air_Pressure","wind_speed","Date"])
                        writer.writerow(weather_data)
                else:
                    with  open(log_file,"w+",newline="") as f:
                        writer = csv.DictWriter(f,fieldnames=["city","Temperature","humidity","Air_Pressure","wind_speed","Date"])
                        writer.writeheader()
        ##################################################################              
def Show_Table():
        table = pandas.read_csv(log_file,encoding= 'unicode_escape')
        print(table)
        ##################################################################
def Main():
        print("                                     Scrap_weather_temperature_Script                                        ")
        print("ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ")
        get_data_for_days()
        print(f"                                          Show File Content                                                 ")
        print("ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ")        Show_Table()


        ########################### END ###############################