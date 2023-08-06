import epiw

desc = epiw.hourly_weather_desc()

print(desc)

desc = epiw.daily_weather_desc()

print(desc)

values = epiw.hourly_weather('20200101', '20200101')

print(values)
