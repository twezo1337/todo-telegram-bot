from pprint import pprint
 
import datetime as dt
import time
from weather_token import TOKEN

def get_current_weather():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = {
        'units': 'metric',
        'lang': 'en',
        'lat': 56.035083,
        'lon': 92.869861,
        'q': 'Moscow',
        'appid': TOKEN
    }

    s = requests.get(url, params=parameters)
    data = s.json()
    pprint(data)

    city_name = data['name']

    t = data['dt']
    cdt = time.strftime('%d.%m.%Y %H:%M', time.localtime(t))

    ctemp = data['main']['temp']
    ctemp_feels = data['main']['feels_like']

    wdesc = data['weather'][0]['description']

    swind = data['wind']['speed']

    hum = data['main']['humidity']

    tsunrise = time.strftime('%H:%M', time.localtime(data['sys']['sunrise']))
    tsunset = time.strftime('%H:%M', time.localtime(data['sys']['sunset']))

    weather_msg = f'''
        Текущая погода в городе {city_name} на {cdt}:

        Температура: {ctemp} ощущается как {ctemp_feels}
        {wdesc}

        Ветер: {swind} m/s

        Влажность: {hum} %

        Время рассвета: {tsunrise}
        Время заката: {tsunset}
    '''

    return weather_msg

def get_tomorrow_weather():
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    parameters = {
        'units': 'metric',
        'lang': 'en',
        'lat': 56.035083,
        'lon': 92.869861,
        'appid': TOKEN
    }

    s = requests.get(url, parameters)
    data = s.json()

    d = dt.datetime.now() + dt.timedelta(days=1)
    tomorrow_day = d.strftime('%d.%m.%Y')
    city_name = data['city']['name']
    tsunrise = time.strftime('%H:%M', time.localtime(data['city']['sunrise']))
    tsunset = time.strftime('%H:%M', time.localtime(data['city']['sunset']))

    for m in data['list']:
        t = time.strftime('%d.%m.%Y', time.localtime(m['dt']))
        if t == tomorrow_day:
            hour = int(time.strftime('%H', time.localtime(m['dt'])))
            if hour >= 12 and hour < 15:
                temp_day = m['main']['temp']
                temp_feels_day = m['main']['feels_like']
                weather_desc_day = m['weather'][0]['description']
                wind_speed_day = m['wind']['speed']
                hum_day = m['main']['humidity']
            if hour >= 3 and hour < 6:
                temp_night = m['main']['temp']
                temp_feels_night = m['main']['feels_like']
                weather_desc_night = m['weather'][0]['description']
                wind_speed_night = m['wind']['speed']
                hum_night = m['main']['humidity']

    weather_msg = f'''
        Погода на {tomorrow_day} в городе {city_name}:

        Температура на день: {temp_day} ощущается как {temp_feels_day}
        {weather_desc_day}
        Температура на ночь: {temp_night} ощущается как {temp_feels_night}
        {weather_desc_night}

        Ветер день: {wind_speed_day} m/s
        Ветер ночь: {wind_speed_night} m/s

        Влажность день: {hum_day} %
        Влажность ночь: {hum_night} %

        Время рассвета: {tsunrise}
        Время заката: {tsunset}
    '''

    return weather_msg

def get_5days_weather(city):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    parameters = {
        'units': 'metric',
        'lang': 'en',
        'lat': 56.035083,
        'lon': 92.869861,
        'q': city,
        'appid': TOKEN
    }

    s = requests.get(url, parameters)
    data = s.json()

    city_name = data['city']['name']
    tsunrise = time.strftime('%H:%M', time.localtime(data['city']['sunrise']))
    tsunset = time.strftime('%H:%M', time.localtime(data['city']['sunset']))

    d = dt.datetime.now()
    dates = []
    for i in range(1, 5):
        d1 = d + dt.timedelta(days = i)
        day = d1.strftime('%d.%m.%Y')
        dates.append(day)
    
    weather_data = {
        #26.11.2023: {temp: 22, temp_feels: 22}
        #26.11.2023: {temp: 22, temp_feels: 22}
    }

    for day in dates:
        weather_data[day] = {}
        for m in data['list']:
            t = time.strftime('%d.%m.%Y', time.localtime(m['dt']))
            if t == day:
                h = int(time.strftime('%H', time.localtime(m['dt'])))
                if h >= 12 and h < 15:
                    weather_data[day]['temp_day'] = m['main']['temp']
                    weather_data[day]['temp_feels_day'] = m['main']['feels_like']
                    weather_data[day]['weather_desc_day'] = m['weather'][0]['description']
                    weather_data[day]['wind_speed_day'] = m['wind']['speed']
                    weather_data[day]['hum_day'] = m['main']['humidity']
                if h >= 3 and h < 6:
                    weather_data[day]['temp_night'] = m['main']['temp']
                    weather_data[day]['temp_feels_night'] = m['main']['feels_like']
                    weather_data[day]['weather_desc_night'] = m['weather'][0]['description']
                    weather_data[day]['wind_speed_night'] = m['wind']['speed']
                    weather_data[day]['hum_night'] = m['main']['humidity']

    weather_msg = f'''
        Погода на 5 дней в городе {city_name}:

    '''

    for date in weather_data:
        date_weather = weather_data[date]
        weather_msg += f'''
            Дата {date}:

            Температура на день: {date_weather['temp_day']} ощущается как {date_weather['temp_feels_day']}
            {date_weather['weather_desc_day']}
            Температура на ночь: {date_weather['temp_night']} ощущается как {date_weather['temp_feels_night']}
            {date_weather['weather_desc_night']}

            Ветер день: {date_weather['wind_speed_day']} m/s
            Ветер ночь: {date_weather['wind_speed_night']} m/s

            Влажность день: {date_weather['hum_day']} %
            Влажность ночь: {date_weather['hum_night']} %

        '''
    weather_msg += f'''
        Время рассвета: {tsunrise}
        Время заката: {tsunset}
    '''

    return weather_msg

def get_forecast_for_day(city, day):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    parameters = {
        'units': 'metric',
        'lang': 'en',
        'lat': 56.035083,
        'lon': 92.869861,
        'q': {city},
        'appid': TOKEN
    }

    s = requests.get(url, parameters)
    data = s.json()

    if day == 'Сегодня':
        d = dt.datetime.now()
    elif day == 'Завтра':
        d = dt.datetime.now() + dt.timedelta(days=1)

    d = d.strftime('%d.%m.%Y')

    weather_data = {
        
    }

    for m in data['list']:
        t = time.strftime('%d.%m.%Y', time.localtime(m['dt']))
        if t == d:
            h = time.strftime('%H.%M', time.localtime(m['dt']))
            weather_data[h] = {}
            weather_data[h]['temp'] = m['main']['temp']
            weather_data[h]['temp_feels'] = m['main']['feels_like']
            weather_data[h]['weather_desc'] = m['weather'][0]['description']
            weather_data[h]['wind_speed'] = m['wind']['speed']

    weather_msg = f'''
        Погода на {day} в городе {city}:

    '''

    for time in weather_data:
        date_weather = weather_data[time]
        weather_msg += f'''
            Время {time}:

            Температура на день: {date_weather['temp']} ощущается как {date_weather['temp_feels']}
            {date_weather['weather_desc']}

            Ветер день: {date_weather['wind_speed']} m/s

            Влажность день: {date_weather['hum_day']} %

        '''

    return weather_msg