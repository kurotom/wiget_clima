# -*- coding: utf-8 -*-
import datetime as dt


class ClimaOne:
    def __init__(self, datos, unidad_medida, idioma):
        self.datos = datos
        self.medida = unidad_medida
        self.idioma = idioma

    def fecha(self):
        fecha, hora = str(dt.datetime.fromtimestamp(self.datos["dt"])).split()
        return {"date": {"fecha": fecha, "hora": fecha}}

    def weather_clima(self):
        tipo_clima = {"Thunderstorm": "Tormenta", "Drizzle": "Llovizna", "Rain": "Lluvia", "Snow": "Nieve", "Atmosphere": "Atmósfera", "Clear": "Despejado", "Clouds": "Nubes", "Mist": "Niebla"}
        temp = self.datos['main']['temp']
        datos_clima = self.datos['weather'][0]
        cond_clima = datos_clima['main']
        desc_clima = datos_clima['description'].title()
        c_clima = ""
        if cond_clima in tipo_clima.keys():
            c_clima = tipo_clima[cond_clima].title()
        return {"weather": [c_clima, desc_clima, f"{round(temp, 1)}"]}

    def main_clima(self):
        idioma = self.idioma
        pressure = ""
        vel_viento = ""
        if self.medida == "metric":
            pressure = f"{round(self.datos['main']['pressure'] * 0.0145037738, 1)} psi"   # hPa a PSI
            vel_viento = f"{round(((self.datos['wind']['speed'] / 1) * (3600/1000)), 1)} km/h"  # transforma a Km/H
        elif self.medida == "imperial":
            pressure = f"{self.datos['main']['pressure']} hPa"  # hPa
            vel_viento = f"{round((self.datos['wind']['speed'] * 2.237), 1)} mph"  # transforma a milla/H
        humidity = self.datos['main']['humidity']
        deg_viento = self.datos['wind']['deg']
        nubes = self.datos['clouds']['all']
        rosa_viento = ""
        if deg_viento >= 0 and deg_viento <= 22.5 or deg_viento >= 337.5 and deg_viento <= float(360):
            rosa_viento = "N"
        elif deg_viento >= 22.5 and deg_viento <= 67.5:
            rosa_viento = "NE"
        elif deg_viento >= 67.5 and deg_viento <= 112.5:
            rosa_viento = "E"
        elif deg_viento >= 112.5 and deg_viento <= 157.5:
            rosa_viento = "SE"
        elif deg_viento >= 157.5 and deg_viento <= 202.5:
            rosa_viento = "S"
        elif deg_viento >= 202.5 and deg_viento <= 247.5:
            rosa_viento = "SW"
        elif deg_viento >= 247.5 and deg_viento <= 292.5:
            rosa_viento = "W"
        elif deg_viento >= 292.5 and deg_viento <= 337.5:
            rosa_viento = "NW"
        resultado = {}
        if idioma == "es":
            resultado = {"main": [f"Presión  {pressure}", f"Humedad  {humidity} %", f"Nubosidad  {nubes} %", f"Viento  {vel_viento} {rosa_viento}"]}
        elif idioma == "en":
            resultado = {"main": [f"Pressure {pressure}", f"Humidity {humidity}%", f"Cloudiness {nubes}%", f"Wind {vel_viento} {rosa_viento}"]}
        return resultado

    def sys_clima(self):
        sunrise_fecha, sunrise_hora = str(dt.datetime.fromtimestamp(self.datos['sys']['sunrise'])).split()
        sunset_fecha, sunset_hora = str(dt.datetime.fromtimestamp(self.datos['sys']['sunset'])).split()
        return {"sys": {"Amanecer": f"{sunrise_hora[:5]}", "Atardecer": f"{sunset_hora[:5]}"}}

    def __str__(self):
        return str(self.datos)
