import requests
from assistant_functions.ListenSpeak import listen_speak 

from datetime import datetime 


api_key = '03e0a6f84da3d99aab0775a23353cba3'         # api key for openweathermap API one_call
exclude = 'minute,hourly'                            # for forecast API call exclude the minutely and hourly forecast leaving an 8 day forecast
default_city = 'pomona'                              # default city for weather calls city name
default_lat = 34.0551                                # default city pomona latitude
default_lon = -117.75                                 # default city pomona longitude

dt = datetime.now()                                  # get the current date and time from system time


def weather(request):
    # conditional statements to isolate city name from full user request string
    if 'in' in request:
        req_loc = request.split('in ', 1)[1] 
        #req_loc = req_loc.split()
    elif 'for' in request:
        splt_i = request.rfind("for")           # rfind to find last occurance of 'for' as 'for' is in 'forecast' and code is looking for the phrase 'for {city}'          
        splt_str = request[splt_i:]
        req_loc = splt_str.split('for ', 1)[1] 
    else:
            with open('WeatherCityName.txt', 'w') as f:         # write the default city name to textfile for use by front end
                f.write(f"{default_city}\n")
                f.close()

            with open('WeatherCityCoord.txt', 'w') as file:     # write the default city coordinates to textfile for use by front end
                file.write(f"{str(default_lat)}\n")
                file.write(f"{str(default_lon)}\n")
            file.close()
            # lists for weather conditions: max temps, min temps, and descriptions
            id = []
            highs = []
            lows = []
            #hum = []
            #wind = []
            #wind_deg = []
            descrip = []
            forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={default_lat}&lon={default_lon}&units=imperial&exclude={exclude}&appid={api_key}"  # call to openweathermap API forecast
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={default_lat}&lon={default_lon}&units=imperial&APPID={api_key}"                     # call to openweathermap API weather

            # for both API calls parse the data with the requests library and store it in a variable in json format
            api_forecast = requests.get(forecast_url)
            forecast_data = api_forecast.json()
            api_weather = requests.get(weather_url)
            weather_data = api_weather.json()    
            DefId = weather_data['id']
            # loop through daily weather data in forecast and populate lists with max and min temps as well as weather descriptions
            for i in forecast_data['daily']:
                #print(i)

                highs.append(round(i['temp']['max']))
                lows.append(round(i['temp']['min']))

                descrip.append(i['weather'][0]['main'] + ": " + i['weather'][0]['description'])

            # if user requested the forecast 
            if 'forecast' in request:
                x = dt.weekday()                                                                        # x gets the current day of the week as an number where 1 = monday
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']   # list of days of the week
                today = days[x]                                                                         # today gets the name of the day of the week from the list using x as the index
                today_index = days.index(today)                                                         # get index of today
                string = f'[{sel_city} - 8 day forecast]\n'                                             # print title of forecast data displaying city name

                for j in range(len(highs)):                                                             # loop through all forecast data using list of high temps arbitrarly as limit of loop
                    if j == 0:                                                                          # first day of forecast data is today
                       string += f'\n{today} (Today)\n'
                    else:                                                                               # for every day after today for 8 day forecast
                         today_index = (today_index + 1) % 7                                            # today index + 1 is tomomorrow. mod by 7 to restart week 
                         next_day = days[today_index]                                                   # next day of the week from list using the today_index
                         string += f"\n{next_day}\n"

                    # concatinate high temp, low temp, and description of conditions
                    string += 'High: ' + str(highs[j]) + "°F\n"
                    string += 'Low: ' + str(lows[j]) + "°F\n"
                    string += 'Conditions: ' + descrip[j] + "\n"

                print(string)                                                                           # print weather data
                returnVal = f"Here is this week's forecast in the default city of {default_city}"
                return returnVal

            else:                                                                                       # weather data for the default city
                des = weather_data['weather'][0]['description']                                         # description of weather conditions
                temp = round(weather_data['main']['temp'])                                              # round current temperature to nearest degree
                high = round(weather_data['main']['temp_max'])                                          # round max temp of the day to the nearest degree
                low = round(weather_data['main']['temp_min'])                                           # round the min temp of the day to the nearest degree
                print(default_city)                                                                     # print the default city name and weather data
                print(f"{temp}°F")
                print(f"H: {high}°F L: {low}°F")        
                returnVal = f"It is currently {temp} degrees Fahrenheit and {des} in the default city of {default_city}, with a high of {high} and a low of {low}"          
                return returnVal
    #if len(req_loc) > 1:
    #    req_loc = req_loc[-2]
    #else:
    #    req_loc = req_loc[-1]

    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={req_loc}&limit={5}&appid={api_key}"     # openweathermap API call to geocode city name into lat and long coords
    api_geo_req = requests.get(geo_url)                                                                 # parse data with requests library
    geo_data = api_geo_req.json()                                                                       # store in json format


    # lists for city data
    cities = []
    states = []
    country = []
    lat = []
    lon = []

    # lists for storing final city data after removing duplicates
    citiesf = []
    statesf = []
    countryf = []
    latf = []
    lonf = []

    dif_index = []

    for i in geo_data:                      # loop through geocoded data
        #print(i)
        #print()
        cities.append(i['name'])            # populate list for city names
        if 'state' in i:                    # populate list for state names if state name exists 
            states.append(i['state'])
        country.append(i['country'])        # populate country names
        lat.append(i['lat'])                # populate lat coord list
        lon.append(i['lon'])                # populate lon coord list

    if len(cities) > 1:                                             # if more than one city returned by geocoding ask user to specify
        listen_speak.say("Which of these cities did you mean?")

        # convert lat and lon coords to floating point numbers to calculate difference
        for i in range(0, len(lat)):                
            lat[i] = float(lat[i])

        for i in range(0, len(lon)):
            lon[i] = float(lon[i])
        
        # loop for removing duplicate cities returned by geocoding 
        for i in range(1,len(lat)):
            lat_dif = abs(lat[0] - lat[i])          # absolute val of difference between two city lat coords
            if(lat_dif <= 5):                       # if the difference is less than or equal to 5 degrees
                lon_dif = abs(lon[0] - lon[i])      # repeat difference for lon coords
                if(lon_dif <= 5):                   # if the lon coord dif is also <= 5 degrees 
                    dif_index.append(i)             # add the index of the duplicate city to list

        for i in range(0, len(cities)):             # loop to fill the lists of final city data if the city is not in the list that indicates it is a duplicate
            if (i not in dif_index):
                citiesf.append(cities[i])
                statesf.append(states[i])
                countryf.append(country[i])
                latf.append(lat[i])
                lonf.append(lon[i])

    
        for i in range(len(citiesf)):                                           # loop for printing locations for user to specify
            if len(states) != 0:
                loc = f"{i+1}. {citiesf[i]}, {statesf[i]}, {countryf[i]}"
            else:
                loc = f"{i+1}. {citiesf[i]}, {countryf[i]}"
            print(loc)
            print()

        answer = listen_speak.listen()                                          # user answer to specify city
        broken_answer = answer.split()                                          # break up user answer into individual words for use in conditional statements that determine choice
        
        if broken_answer[-1] in statesf:                                        # the user chose by state name
            indx = statesf.index(broken_answer[-1])         
            sel_city = citiesf[indx]
            latitude = latf[indx]
            longitude = lonf[indx]
        elif broken_answer[-1] in countryf:                                     # user chose by country name
            indx = countryf.index(broken_answer[-1])
            sel_city = citiesf[indx]
            latitude = latf[indx]
            longitude = lonf[indx]
        elif 'first' in answer:                                                 # user chose by list number
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

        with open('WeatherCityName.txt', 'w') as f:             # write final selected city to text file to be used by front end
            f.write(f"{sel_city}\n")
        f.close()

        with open('WeatherCityCoord.txt', 'w') as file:         # write final coords to text file to be used by front end
            file.write(f"{str(latitude)}\n")
            file.write(f"{str(longitude)}\n")
        file.close()

        # API calls and data collection
        forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=imperial&exclude={exclude}&appid={api_key}"
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=imperial&APPID={api_key}"

        api_forecast = requests.get(forecast_url)
        forecast_data = api_forecast.json()
        api_weather = requests.get(weather_url)
        weather_data = api_weather.json()   

        ###############
        sel_city_ID = weather_data['id']
        with open('WeatherCityID.txt', 'w') as file:         # write final coords to text file to be used by front end
            file.write(f"{str(sel_city_ID)}\n")
        file.close()
        ####################

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
        if(weather_data['cod'] == '404'):                           # conditional check of API call cod to see if city was found
            print("City Not Found")
            returnVal = "Sorry, I could not find that city"
            return returnVal

        # format and display weather data based on if the user asked for the forecast or current weather
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


    else: # if only one city returned by geocoding

        if (len(geo_data) == 0):                                                                                        # if no city returned city not found
            returnVal = f"I am sorry I could not find what you were looking for please try again (only say the city)"
            return returnVal

        # get city name and coords
        name = cities[0]                
        latitude = lat[0]
        longitude = lon[0]

        with open('WeatherCityName.txt', 'w') as f:             # write city name to text file for use by front end
            f.write(f"{name}\n")
        f.close()

        with open('WeatherCityCoord.txt', 'w') as file:         # write coords to text file for use by front end
            file.write(f"{str(latitude)}\n")
            file.write(f"{str(longitude)}\n")
        file.close()

        

        # API calls and data collection
        forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=imperial&exclude={exclude}&appid={api_key}"
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=imperial&APPID={api_key}"

        api_forecast = requests.get(forecast_url)
        forecast_data = api_forecast.json()
        api_weather = requests.get(weather_url)
        weather_data = api_weather.json()

        ###############
        sel_city_ID = weather_data['id']
        with open('WeatherCityID.txt', 'w') as file:         # write final coords to text file to be used by front end
            file.write(f"{str(sel_city_ID)}\n")
        file.close()
        #####################

        highs = []
        lows = []
        #hum = []
        #wind = []
        #wind_deg = []
        descrip = []

        # if no weather data found
        #if(forecast_data['cod'] == '404'):
        #    print("City Not Found")
        #    returnVal = "Sorry, I could not find that city"
        #    return returnVal
        if(weather_data['cod'] == '404'):
            print("City Not Found")
            returnVal = "Sorry, I could not find that city"
            return returnVal

        # collect, format, and print weather data requested by user 
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


  
    return returnVal
