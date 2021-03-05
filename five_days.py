# -*- coding: utf-8 -*-
from calendar import monthrange
from datetime import datetime as date


class Clima5:
    def __init__(self, datos, fecha):
        self.datos = datos
        self.fecha = fecha
        self.five_data_dict = self.datos_return_temperaturas()

    def datos_return_temperaturas(self):
        """No se invoca, recibe, filtra, y genera los datos para que sea usados por 'temperaturas'"""
        dict_data_5 = {}
        fecha = ""
        year, month, day = int(self.fecha[0]), int(self.fecha[1]), int(self.fecha[2])
        dia_maximo = monthrange(year, month)[1]
        dia = day + 1
        for i in range(1, 6):
            f = f"{year}-{month}-{dia}"
            if dia > dia_maximo:
                dia = 0
                month = month + 1
            else:
                if dia < 10:
                    fecha = str(date.strptime(f, "%Y-%m-%d")).split()[0]
                else:
                    fecha = str(date.strptime(f, "%Y-%m-%d")).split()[0]
            res_temp = []
            for xdata in self.datos[3][1]:
                if fecha in xdata["dt_txt"]:
                    redondeado = round(xdata["main"]["temp"], 1)
                    datos = redondeado, xdata["weather"][0]["description"]
                    res_temp.append(datos)
            if res_temp:
                dict_data_5[fecha] = res_temp
            else:
                return 1
            dia += 1
        return dict_data_5

    def temperaturas(self):
        """Esta método se debe llamar para crear el objeto con las temperaturas de los días siguientes."""
        datos_dict_5 = self.five_data_dict
        dict_results = {}
        minimo = 0
        maximo = 0
        for key in datos_dict_5:
            temps_list = []
            if datos_dict_5[key]:
                for item in datos_dict_5[key]:
                    temps_list.append(item[0])
            if temps_list:
                minimo = min(temps_list)
                maximo = max(temps_list)
            temps_list.sort()
            resultado = []
            for itm in datos_dict_5[key]:
                if minimo in itm:
                    resultado.append(itm)
                elif maximo in itm:
                    resultado.append(itm)
            dict_results[key] = resultado
        for it in dict_results:
            if dict_results[it][0][0] > dict_results[it][1][0]:
                ordenado_min_max = [(dict_results[it][1][0], dict_results[it][1][1]), (dict_results[it][0][0],
                                                                                       dict_results[it][0][1])]
                dict_results[it] = ordenado_min_max
        return dict_results

    def __str__(self):
        return " "
