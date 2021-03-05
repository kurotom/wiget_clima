# -*- coding: utf-8 -*-
from five_days import Clima5
from one_day import ClimaOne
from datetime import date
import json
import requests
import os


def objeto_clima_one(data, unidad_medida, idioma, debug=False):
    if debug is True:
        print("DEBUG_1.0-obj_clima_one --- Cargando datos.")
    with open(data, "r") as file:
        datos = json.load(file)
    if debug is True:
        print("DEBUG_1.1-obj_clima_one --- Creando objeto 'Clima_one'.")
    obj_one = ClimaOne(datos, unidad_medida, idioma)
    if debug is True:
        print("DEBUG_1.2-obj_clima_one --- Éxito, retornando datos.\n")
    return obj_one.fecha(), obj_one.weather_clima(), obj_one.main_clima(), obj_one.sys_clima()


def objeto_clima_five(data, debug=False):
    list_data = []
    date_today = str(date.today()).split("-")
    if debug is True:
        print("| Obteniendo datos locales. |")
        print("| Leyendo informacion. |")
    with open(data, "r") as file:
        data = json.load(file)
        for item in data:
            list_data.append([item, data[item]])
    if debug is True:
        print("| Creando Objeto, filtrando y procesando data... |")
    objeto_clima_5 = Clima5(list_data, date_today)
    temperaturas_5 = objeto_clima_5.temperaturas()
    if debug is True:
        print("| Finalizado, entregando resultados. |")
    return temperaturas_5


def hoy_dia(coords_lon_lat, unit_of_measurement, language, key_api, debug=False):
    fichero_data_1 = "data/data_1_dia.json"
    if debug is True:
        print("DEBUG_1.0 --- *** Iniciando ***")
    if not os.path.exists(fichero_data_1):
        if debug is True:
            print("DEBUG_1.1 --- Recopilando data desde API openweather.")

        url_1dia = f"https://api.openweathermap.org/data/2.5/weather?lat={coords_lon_lat[0]}&lon={coords_lon_lat[1]}&appid={key_api}&units={unit_of_measurement}&lang={language}"
        respuesta = requests.get(url_1dia)
        informacion = json.loads(respuesta.text)
        if debug is True:
            print(f"DEBUG_1.2 --- escribiendo data en: '{fichero_data_1}'")
        with open(fichero_data_1, 'w') as outfile:
            json.dump(informacion, outfile)
        return objeto_clima_one(fichero_data_1, unit_of_measurement, debug)
    else:
        fichero_data_1 = "data/data_1_dia.json"
        if debug is True:
            print(f"DEBUG_2.0 --- Usando fichero local: {fichero_data_1}.")
        if debug is True:
            print("DEBUG_2.1 --- Cargando datos.")
        return objeto_clima_one(fichero_data_1, unit_of_measurement, language, debug)


def a_5_dias(coords_lon_lat, unit_of_measurement, language, key_api, debug=False):
    fichero_data_5 = "data/data_5_days.json"
    if not os.path.exists(fichero_data_5):
        if debug is True:
            print("| Obteniendo datos desde Openweather... |")

        url_5dias = f"https://api.openweathermap.org/data/2.5/forecast?lat={coords_lon_lat[0]}&lon={coords_lon_lat[1]}&appid={key_api}&units={unit_of_measurement}&lang={language}"
        respuesta = requests.get(url_5dias)
        informacion = json.loads(respuesta.text)
        with open(fichero_data_5, "w") as outfile:
            json.dump(informacion, outfile)
        if debug is True:
            print("| Datos guardados, iniciando filtrado y procesado de datos. |")
        return objeto_clima_five(fichero_data_5, debug)
    else:
        if debug is True:
            print("| Datos Locales, iniciando filtrado y procesado de datos. |")
        datos5 = "data/data_5_days.json"
        try:
            return objeto_clima_five(datos5, unit_of_measurement)
        except:
            return 1


if __name__ == "__main__":
    hoy_dia()
    a_5_dias()

