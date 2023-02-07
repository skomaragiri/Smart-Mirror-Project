import requests
from assistant_functions.ListenSpeak import listen_speak 
#import listen
from datetime import datetime 

#psuedo code#
# take argument
# break down input string to isolate city
# plug city into geo locater 
# ask for which city 
# get lon and lat from choice
# plug into api
# print either forecast or weather
# retern relevant string to speak

api_key = '03e0a6f84da3d99aab0775a23353cba3'
exclude = 'minute,hourly'


dt = datetime.now()


def weather(request):
    if 'in' in request:
        req_loc = request.split('in ', 1)[1] #forcast FOR, weather FOR
        req_loc = req_loc.split()
    if 'for' in request:
        splt_i = request.rfind('for')
        splt_str = request[splt_i:]
        req_loc = splt_str.split('for ', 1)[1] #forcast FOR, weather FOR
        req_loc = req_loc.split()
    if len(req_loc) > 1:
        req_loc = req_loc[-2]
    else:
        req_loc = req_loc[-1]

    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={req_loc}&limit={5}&appid={api_key}"
    api_geo_req = requests.get(geo_url)
    geo_data = api_geo_req.json()

    cities = []
    states = []
    country = []
    lat = []
    lon = []

    citiesf = []
    statesf = []
    countryf = []
    latf = []
    lonf = []

    dif_index = []

    for i in geo_data:
        #print(i)
        #print()
        cities.append(i['name'])
        if 'state' in i:
            states.append(i['state'])
        country.append(i['country'])
        lat.append(i['lat'])
        lon.append(i['lon'])

    if len(cities) > 1:
        listen_speak.say("Which of these cities did you mean?")

        for i in range(0, len(lat)):
            lat[i] = float(lat[i])

        for i in range(0, len(lon)):
            lon[i] = float(lon[i])

        for i in range(1,len(lat)):
            lat_dif = abs(lat[0] - lat[i])
            if(lat_dif <= 5):
                lon_dif = abs(lon[0] - lon[i])
                if(lon_dif <= 5):
                    dif_index.append(i)

        for i in range(0, len(cities)):
            if (i not in dif_index):
                citiesf.append(cities[i])
                statesf.append(states[i])
                countryf.append(country[i])
                latf.append(lat[i])
                lonf.append(lon[i])

    
        for i in range(len(citiesf)):
            if len(states) != 0:
                loc = f"{i+1}. {citiesf[i]}, {statesf[i]}, {countryf[i]}"
            else:
                loc = f"{i+1}. {citiesf[i]}, {countryf[i]}"
            print(loc)
            print()

        answer = listen_speak.listen()
        choices = ['first', 'number one', 'second', 'number two', 'third', 'number three', 'fourth', 'number four', 'fifth', 'number five', 'last']
        broken_answer = answer.split()
        
        if broken_answer[-1] in statesf:
            indx = statesf.index(broken_answer[-1])
            sel_city = citiesf[indx]
            latitude = latf[indx]
            longitude = lonf[indx]
        elif broken_answer[-1] in countryf:
            indx = countryf.index(broken_answer[-1])
            sel_city = citiesf[indx]
            latitude = latf[indx]
            longitude = lonf[indx]
        elif 'first' in answer:
            sel_city = citiesf[0]
            latitude = latf[0]
            longitude = lonf[0]
        elif 'number one' in answer:
            sel_city = citiesf[0]
            latitude = latf[0]
            longitude = lonf[0]
        elif 'second' in answer:
            sel_city = citiesf[1]
            latitude = latf[1]
            longitude = lonf[1]
        elif 'number two' in answer:
            sel_city = citiesf[1]
            latitude = latf[1]
            longitude = lonf[1]
        elif 'third' in answer:
            sel_city = citiesf[2]
            latitude = latf[2]
            longitude = lonf[2]
        elif 'number three' in answer:
            sel_city = citiesf[2]
            latitude = latf[2]
            longitude = lonf[2]
        elif 'fourth' in answer:
            sel_city = citiesf[3]
            latitude = latf[3]
            longitude = lonf[3]
        elif 'number four' in answer:
            sel_city = citiesf[3]
            latitude = latf[3]
            longitude = lonf[3]
        elif 'fifth' in answer:
            sel_city = citiesf[4]
            latitude = latf[4]
            longitude = lonf[4]
        elif 'number five' in answer:
            sel_city = citiesf[4]
            latitude = latf[4]
            longitude = lonf[4]
        elif 'last' in answer:
            sel_city = citiesf[-1]
            latitude = latf[-1]
            longitude = lonf[-1]
        else:
            print("Invalid selection")
            returnVal = "Sorry, I didn't understand"
            return returnVal

        forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=imperial&exclude={exclude}&appid={api_key}"
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=imperial&APPID={api_key}"

        api_forecast = requests.get(forecast_url)
        forecast_data = api_forecast.json()
        api_weather = requests.get(weather_url)
        weather_data = api_weather.json()    

        highs = []
        lows = []
        #hum = []
        #wind = []
        #wind_deg = []
        descrip = []
#        if(forecast_data['cod'] == '404'):
#            print("City Not Found")
#            returnVal = "Sorry, I could not find that city"
#            return returnVal
        if(weather_data['cod'] == '404'):
            print("City Not Found")
            returnVal = "Sorry, I could not find that city"
            return returnVal
        else:
            for i in forecast_data['daily']:
                #print(i)

                highs.append(round(i['temp']['max']))
                lows.append(round(i['temp']['min']))

                descrip.append(i['weather'][0]['main'] + ": " + i['weather'][0]['description'])

            if 'forecast' in request:
                x = dt.weekday()
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                today = days[x]
                today_index = days.index(today)
                string = f'[{sel_city} - 8 day forecast]\n'

                for j in range(len(highs)):
                    if j == 0:
                       string += f'\n{today} (Today)\n'
                    else:
                         today_index = (today_index + 1) % 7
                         next_day = days[today_index]
                         string += f"\n{next_day}\n"


                    string += 'High: ' + str(highs[j]) + "°F\n"
                    string += 'Low: ' + str(lows[j]) + "°F\n"
                    string += 'Conditions: ' + descrip[j] + "\n"

                print(string)
                returnVal = f"Here is this week's forecast in {sel_city}"

            else:
                des = weather_data['weather'][0]['description']
                temp = round(weather_data['main']['temp'])
                high = round(weather_data['main']['temp_max'])
                low = round(weather_data['main']['temp_min'])
                print(sel_city)
                print(f"{temp}°F")
                print(f"H: {high}°F L: {low}°F")

                returnVal = f"It is currently {temp} degrees Fahrenheit and {des} in {sel_city}, with a high of {high} and a low of {low}"


    else:
        name = cities[0]
        latitude = lat[0]
        longitude = lon[0]

        forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=imperial&exclude={exclude}&appid={api_key}"
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=imperial&APPID={api_key}"

        api_forecast = requests.get(forecast_url)
        forecast_data = api_forecast.json()
        api_weather = requests.get(weather_url)
        weather_data = api_weather.json()
        
        highs = []
        lows = []
        #hum = []
        #wind = []
        #wind_deg = []
        descrip = []

        if(forecast_data['cod'] == '404'):
            print("City Not Found")
            returnVal = "Sorry, I could not find that city"
            return returnVal
        elif(weather_data['cod'] == '404'):
            print("City Not Found")
            returnVal = "Sorry, I could not find that city"
            return returnVal
        else:
        
            for i in forecast_data['daily']:
                #print(i)

                highs.append(round(i['temp']['max']))
                lows.append(round(i['temp']['min']))

                descrip.append(i['weather'][0]['main'] + ": " + i['weather'][0]['description'])

            if 'forecast' in request:
            
                string = f'[{name} - 8 day forecast]\n'

                for j in range(len(highs)):
                    if j == 0:
                       string += f'\n{today} (Today)\n'
                    else:
                         today_index = (today_index + 1) % 7
                         next_day = days[today_index]
                         string += f"\n{next_day}\n"


                    string += 'High: ' + str(highs[j]) + "°F\n"
                    string += 'Low: ' + str(lows[j]) + "°F\n"
                    string += 'Conditions: ' + descrip[j] + "\n"

                print(string)
                returnVal = f"Here is this week's forecast"

            else:
                des = weather_data['weather'][0]['description']
                temp = round(weather_data['main']['temp'])
                high = round(weather_data['main']['temp_max'])
                low = round(weather_data['main']['temp_min'])
                print(name)
                print(f"{temp}°F")
                print(f"H: {high}°F L: {low}°F")

                returnVal = f"It is currently {temp} degrees Fahrenheit and {des} in {name}, with a high of {high} and a low of {low}" 


    # write code for printing either current weather or forecast
    # write code for selecting city from list 

    return returnVal
