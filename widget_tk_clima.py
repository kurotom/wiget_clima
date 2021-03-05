# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import pymongo
from geopy.geocoders import Nominatim
from mainclima_one_five import a_5_dias, hoy_dia
import json
import os


def clima_5(fuente):
    file_data_settings = "data/settings.json"
    with open(file_data_settings, "r") as fljson:
        opciones_dict = json.load(fljson)
    coord_lat_lon = opciones_dict["coord"]['lat'], opciones_dict['coord']['lon']
    unidad = opciones_dict["unit"]
    idioma = opciones_dict["lang"]
    key_api = opciones_dict["key"]
    clima5 = a_5_dias(coord_lat_lon, unidad, idioma, key_api, False)
    simbolo_grados = ""

    if idioma == "es":
        simbolo_grados = "°C"
    elif idioma == "en":
        simbolo_grados = "°F"

    iter_n = 1
    for itm in clima5:
        num_dia = datetime.strptime(itm, "%Y-%m-%d").weekday()
        nombre = fun_nombre_dia(num_dia, idioma)
        if clima5[itm]:
            temp_min = f"{clima5[itm][0][0]} {simbolo_grados}"
            temp_max = f"{clima5[itm][1][0]} {simbolo_grados}"
            cond_min = f"{clima5[itm][0][1].capitalize()}"
            cond_max = f"{clima5[itm][1][1].capitalize()}"
            fecha_label = ttk.Label(frame5, text=f"{itm}", font=fuente)
            name_label = ttk.Label(frame5, text=f"{nombre}", font=fuente)
            temp_min_max = ttk.Label(frame5, text=f"{temp_min}  -  {temp_max}", font=fuente)
            cond_label_min = ttk.Label(frame5, text=cond_min, font=fuente)
            cond_label_max = ttk.Label(frame5, text=cond_max, font=fuente)
            fecha_label["background"] = color_x
            name_label["background"] = color_x
            temp_min_max["background"] = color_x
            cond_label_min["background"] = color_x
            cond_label_max["background"] = color_x
            name_label.place(x=20, y=22 * iter_n - 15)
            fecha_label.place(x=110, y=22 * iter_n - 15)
            temp_min_max.place(x=210, y=22 * iter_n - 15)
            cond_label_max.place(x=350, y=22 * iter_n - 15)
        iter_n += 1


def actualizar():
    lista_ficheros = ["data/data_5_days.json", "data/data_1_dia.json"]
    file_data_settings = "data/settings.json"
    with open(file_data_settings, "r") as fljson:
        opciones_dict = json.load(fljson)
    coord_lat_lon = opciones_dict["coord"]['lat'], opciones_dict['coord']['lon']
    unidad = opciones_dict["unit"]
    idioma = opciones_dict["lang"]
    key_api = opciones_dict["key"]
    clima5 = a_5_dias(coord_lat_lon, unidad, idioma, key_api, False)

    title_frame = ttk.Frame(base)
    title_label = ttk.Label(title_frame, text="", font=font_titulo)

    if clima5 == 1:
        title_label['text'] = "Recargar..."
        title_frame.grid(row=3, pady=(0, 0), ipady=10, sticky="WE")
        title_label.pack(expand=True, fill="y")
        estilo_caja(title_frame)
        if os.path.exists(lista_ficheros[0]) or os.path.exists(lista_ficheros[1]):
            for xfile in lista_ficheros:
                os.remove(xfile)
    else:
        if idioma == "es":
            title_label['text'] = "Pronósticos futuros"
        elif idioma == "en":
            title_label['text'] = "Future forecast"
        file_data_settings = "data/settings.json"
        with open(file_data_settings, "r") as fljson:
            opciones_dict = json.load(fljson)
        coord_lat_lon = opciones_dict["coord"]['lat'], opciones_dict['coord']['lon']
        city = opciones_dict['city']
        unidad = opciones_dict["unit"]
        idioma = opciones_dict["lang"]
        key_api = opciones_dict['key']
        try:
            items_1 = hoy_dia(coord_lat_lon, unidad, idioma, key_api, False)
            date = items_1[0]['date']
            weather = items_1[1]
            main = items_1[2]['main']
            sys_clima = items_1[3]['sys']
            sys_sol = ""
            if idioma == "es":
                sys_sol = f"Amanecer:  {sys_clima['Amanecer']}    Ocaso:  {sys_clima['Atardecer']}"
            elif idioma == "en":
                sys_sol = f"Sunrise:  {sys_clima['Amanecer']}    Sunset:  {sys_clima['Atardecer']}"

            simbolo_grados = ""
            if idioma == "es":
                simbolo_grados = "°C"
            elif idioma == "en":
                simbolo_grados = "°F"

            n_dia = datetime.strptime(date['fecha'], "%Y-%m-%d").weekday()
            dia_nombre = fun_nombre_dia(n_dia, idioma)

            if len(city.split(",")) > 5:
                lst = f"{city.split(',')[0]}", ",".join(city.split(',')[4:]).strip()
                ciudad_text = ", ".join(lst)
            else:
                ciudad_text = city

            lbl_ciudad = ttk.Label(frame2, text=ciudad_text, font=font_contenido, justify="center")
            dia_label = ttk.Label(frame2, text=f"{dia_nombre}", font=font_contenido)
            label_date = ttk.Label(frame2, text=date['fecha'], font=font_contenido)
            label_weather = ttk.Label(frame2, text=weather['weather'][1], font=font_contenido)
            label_weather_temp = ttk.Label(frame2, text=f"{weather['weather'][2]} {simbolo_grados}",
                                           font=font_contenido)
            sol = ttk.Label(frame2, text=sys_sol, font=font_contenido)

            lbl_ciudad['background'] = color_x
            dia_label["background"] = color_x
            label_date["background"] = color_x
            label_weather["background"] = color_x
            label_weather_temp["background"] = color_x
            sol["background"] = color_x

            title_frame.grid(row=3, pady=(0, 0), ipady=10, sticky="WE")
            title_label.pack(expand=True, fill="y")
            estilo_caja(title_frame)

            lbl_ciudad.place(x=80, y=8)
            dia_label.place(x=85, y=32)
            label_date.place(x=290, y=32)
            label_weather_temp.place(x=65, y=52)
            label_weather.place(x=120, y=52)
            sol.place(x=200, y=52)

            texto = ""
            for itm in main:
                texto += f"{itm}\n"
            label_itm['text'] = texto.strip()
            label_itm["background"] = color_x
            label_itm.pack(expand=True, fill="y")

            clima_5(font_contenido)
        except:
            actualizar()


def settings_opciones():
    def get_event(*args):
        btn_aceptar['state'] = "enable"
        seleccionado = listbox_ciudades.selection_get()
        return seleccionado

    def cities():
        if entry_buscar.get() != "":
            client = pymongo.MongoClient("mongodb+srv://consulta_data:qfXLWGvZ8nZmS8Zb@db-cities.rrog3.mongodb.net"
                                         "/info_cities?retryWrites=true&w=majority")
            db = client.get_database('info_cities')
            collection = db['cities']

            geo = Nominatim(user_agent="simple_widget")

            xi = 0
            for item in collection.find({"name": {"$regex": entry_buscar.get(), "$options": "i"}}):
                ubicacion = geo.reverse(f"{item['coord']['lat']}, {item['coord']['lon']}", language="en")
                items_data = f"{item['name']}," \
                             f" {item['country']}," \
                             f" {ubicacion.address}," \
                             f" {item['coord']['lon']}," \
                             f" {item['coord']['lat']}"
                listbox_ciudades.insert(xi, items_data)
                xi += 1
            client.close()
        else:
            messagebox.showwarning(title="", message="Ingrese nombre de ciudad")

    def yes_no_menssage():
        si_no = messagebox.askyesno(message="¿Sobre-escribir opciones?", icon="question", title="Conflicto ficheros")
        return si_no

    def aceptar_guardar():
        file_opts = "data/settings.json"
        lst_evento = get_event().split(",")
        ciudad_direccion = ",".join(lst_evento[5:len(lst_evento) - 2])
        completa_direccion = f"{lst_evento[0]},{ciudad_direccion}"
        coordenadas_selecionada = lst_evento[len(lst_evento) - 2:]
        to_float = float(coordenadas_selecionada[0].strip()), float(coordenadas_selecionada[1].strip())
        if os.path.exists(file_opts):
            if lbl['text'] == "":
                f_dict = {"lang": respuesta_lang.get(),
                          "unit": unidades_respuesta.get(),
                          "city": f"{completa_direccion}",
                          "coord": {"lon": to_float[0], "lat": to_float[1]},
                          "key": f"{key_entry.get()}"}
            else:
                f_dict = {"lang": lbl['text'],
                          "unit": lbl2['text'],
                          "city": f"{completa_direccion}",
                          "coord": {"lon": to_float[0], "lat": to_float[1]},
                          "key": f"{key_entry.get()}"}
            if yes_no_menssage() is True:
                lista_ficheros = ["data/data_5_days.json", "data/data_1_dia.json", "data/settings.json"]
                if os.path.exists(lista_ficheros[0]) or os.path.exists(lista_ficheros[1]):
                    for xfile in lista_ficheros:
                        os.remove(xfile)
                    messagebox.showinfo(message="Re-iniciar Applicacion", title="")
                with open(file_opts, "w", encoding='utf8') as fl_data:
                    json.dump(f_dict, fl_data, ensure_ascii=False)
                base_cr.destroy()
            else:
                base_cr.destroy()
        else:
            if lbl['text'] == "" or lbl2['text'] == "":
                messagebox.showwarning(title="", message="Seleccione parametros en Language y/o Metric Units")
            elif key_entry.get() == "":
                messagebox.showwarning(title="", message="Ingrese Key API")
            else:
                f_dict = {"lang": lbl['text'],
                          "unit": lbl2['text'],
                          "city": f"{completa_direccion}",
                          "coord": {"lon": to_float[0], "lat": to_float[1]},
                          "key": f"{key_entry.get()}"}
                with open(file_opts, "w", encoding='utf8') as fl_data:
                    json.dump(f_dict, fl_data, ensure_ascii=False)
                base_cr.destroy()

    def ventana_salir():
        base_cr.destroy()

    base_cr = Tk()
    base_cr.title("Settings")
    frame_cr = Frame(base_cr)
    frame_cr2 = Frame(base_cr)
    frame_cr3 = Frame(base_cr)
    frame_cr4 = Frame(base_cr)
    frame_lbl = Frame(base_cr)

    respuesta_lang = StringVar()
    idioma_lbl = Label(frame_cr, text="Language")
    radio_lg_esp = Radiobutton(frame_cr, text="Spanish", variable=respuesta_lang, value="es")
    radio_lg_eng = Radiobutton(frame_cr, text="English", variable=respuesta_lang, value="en")

    unidades_respuesta = StringVar()
    change_metric_lbl = Label(frame_cr2, text="Metric Unit")
    metrico_radio = Radiobutton(frame_cr2, text="Metric", variable=unidades_respuesta, value="metric")
    imperial_radio = Radiobutton(frame_cr2, text="Imperial", variable=unidades_respuesta, value="imperial")

    entrada_label = StringVar()
    lbl_key = Label(frame_cr4, text="Key API")
    key_entry = Entry(frame_cr4, textvariable=entrada_label, show=None, width=31)

    buscar_str = StringVar()
    entry_buscar = Entry(frame_cr4, textvariable=buscar_str, show=None, width=31, justify="center")

    boton_buscar = Button(frame_cr4, command=cities, text="Search")

    listbox_ciudades = Listbox(frame_cr3, selectmode="single", width=50)

    lbl = Label(frame_lbl, textvariable=respuesta_lang)
    lbl2 = Label(frame_lbl, textvariable=unidades_respuesta)
    btn_quit = ttk.Button(frame_lbl, text="Quit", command=ventana_salir)
    btn_aceptar = ttk.Button(frame_lbl, text="Done!", command=aceptar_guardar, state="disabled")

    file_settings = "data/settings.json"
    if os.path.exists(file_settings):
        with open(file_settings, "r") as fl_read:
            local_data = json.load(fl_read)
        respuesta_lang.set(local_data['lang'])
        unidades_respuesta.set(local_data['unit'])
        key_entry.delete(0, END)
        key_entry.insert(0, local_data['key'])

    listbox_ciudades.bind('<<ListboxSelect>>', get_event)

    frame_cr.grid(column=1, row=0, padx=20, pady=(15, 10))
    idioma_lbl.grid(columnspan=3)
    radio_lg_esp.grid(column=1, row=1)
    radio_lg_eng.grid(column=2, row=1)

    frame_cr2.grid(column=2, row=0, padx=20, pady=(15, 10))
    change_metric_lbl.grid(columnspan=4)
    metrico_radio.grid(column=2, row=1)
    imperial_radio.grid(column=3, row=1)

    frame_cr4.grid(column=1, columnspan=4, rowspan=4, padx=10, pady=(10, 1))
    lbl_key.grid(column=1, row=1)
    key_entry.grid(column=2, row=1, padx=10)
    entry_buscar.grid(column=2, columnspan=4, row=2)
    boton_buscar.grid(columnspan=4, row=3, pady=(5, 1))

    frame_cr3.grid(columnspan=4, pady=5)
    listbox_ciudades.grid()

    frame_lbl.grid(columnspan=4)
    btn_aceptar.grid(column=1, row=2, padx=20, pady=5)
    btn_quit.grid(column=2, row=2, padx=20, pady=5)

    base_cr.mainloop()


def fun_nombre_dia(numero_dia, idioma):
    nombre_dia = {0: ["Lunes", "Monday"], 1: ["Martes", "Tuesday"], 2: ["Miercoles", "Wednesday"],
                  3: ["Jueves", "Thursday"], 4: ["Viernes", "Friday"], 5: ["Sabado", "Saturday"],
                  6: ["Domingo", "Sunday"]}
    dia_nombre = ""
    if numero_dia in nombre_dia.keys():
        if idioma == "es":
            dia_nombre = nombre_dia[numero_dia][0]
        elif idioma == "en":
            dia_nombre = nombre_dia[numero_dia][1]
    return dia_nombre


def estilo_caja(item):
    item["relief"] = "groove"
    item["borderwidth"] = 5


def item_centro_frame(item):
    item.pack(expand=True, fill="y")


###########################################

file_opciones = "data/settings.json"
if os.path.exists(file_opciones):
    color_x = "#EEE"
    font_titulo = ("Droid Sans", 13)
    font_contenido = ("Utopia", 12)

    base = Tk()
    base.title("Simple Weather Widget")
    base.configure(background="#818D92")

    stl = ttk.Style()
    stl.configure("color_frame.TFrame", background="#EEE")
    fr_botom_color = ttk.Style()
    fr_botom_color.configure("botom_color.TFrame", background="#525252")  # "#818D92")

    refresh_icon = PhotoImage(file="icons/refresh_icon.png").subsample(2, 2)
    quit_icon = PhotoImage(file="icons/quit_icon.png").subsample(2, 2)
    options_icon = PhotoImage(file="icons/settings.png").subsample(2, 2)

    frame_boton = ttk.Frame(base, relief="flat", style="botom_color.TFrame", height=40)
    boton1 = Button(frame_boton, bg="#525252", image=refresh_icon, borderwidth=0, highlightthickness=0,
                    command=actualizar)
    boton2 = Button(frame_boton, bg="#525252", image=options_icon, borderwidth=0, highlightthickness=0,
                    command=settings_opciones)
    boton3 = Button(frame_boton, command=quit, bg="#525252", image=quit_icon, borderwidth=0, highlightthickness=0)
    label_data_source = Label(frame_boton, text="OpenWeatherMap")
    label_data_source["background"] = "#525252"

    frame2 = ttk.Frame(base, width=500, height=90, style="color_frame.TFrame")
    frame3 = ttk.Frame(base, height=94, style="color_frame.TFrame")
    frame5 = ttk.Frame(base, height=132, style="color_frame.TFrame")

    frame2.grid(pady=(5, 0), ipady=1, sticky="WE")
    frame3.grid(row=2, column=0, pady=(0, 5), ipady=3, sticky="WE")
    estilo_caja(frame2)
    estilo_caja(frame3)

    label_itm = ttk.Label(frame3, text="", font=font_contenido, justify="center")
    actualizar()

    frame5.grid(row=5, pady=(0, 5), sticky="WE")
    frame5["relief"] = "groove"
    frame5["borderwidth"] = 5

    frame_boton.grid(row=6, column=0, ipady=5, sticky="WE")
    boton1.place(relx=0.08, rely=0.5, anchor="e")
    boton2.place(relx=0.18, rely=0.5, anchor="e")
    label_data_source.place(relx=0.5, rely=0.65, anchor="center")
    boton3.place(relx=0.92, rely=0.5, anchor="w")

    base.mainloop()
else:
    try:
        settings_opciones()
        color_x = "#EEE"
        font_titulo = ("Droid Sans", 13)
        font_contenido = ("Utopia", 12)

        base = Tk()
        base.title("Simple Weather Widget")
        base.configure(background="#818D92")

        stl = ttk.Style()
        stl.configure("color_frame.TFrame", background="#EEE")
        fr_botom_color = ttk.Style()
        fr_botom_color.configure("botom_color.TFrame", background="#525252")  # "#818D92")

        refresh_icon = PhotoImage(file="icons/refresh_icon.png").subsample(2, 2)
        quit_icon = PhotoImage(file="icons/quit_icon.png").subsample(2, 2)
        options_icon = PhotoImage(file="icons/settings.png").subsample(2, 2)

        frame_boton = ttk.Frame(base, relief="flat", style="botom_color.TFrame", height=40)
        boton1 = Button(frame_boton, bg="#525252", image=refresh_icon, borderwidth=0, highlightthickness=0,
                        command=actualizar)
        boton2 = Button(frame_boton, bg="#525252", image=options_icon, borderwidth=0, highlightthickness=0,
                        command=settings_opciones)
        boton3 = Button(frame_boton, command=quit, bg="#525252", image=quit_icon, borderwidth=0, highlightthickness=0)
        label_data_source = Label(frame_boton, text="OpenWeatherMap")
        label_data_source["background"] = "#525252"

        frame2 = ttk.Frame(base, width=500, height=90, style="color_frame.TFrame")
        frame3 = ttk.Frame(base, height=94, style="color_frame.TFrame")
        frame5 = ttk.Frame(base, height=132, style="color_frame.TFrame")

        frame2.grid(pady=(5, 0), ipady=1, sticky="WE")
        frame3.grid(row=2, column=0, pady=(0, 5), ipady=3, sticky="WE")
        estilo_caja(frame2)
        estilo_caja(frame3)

        label_itm = ttk.Label(frame3, text="", font=font_contenido, justify="center")
        actualizar()

        frame5.grid(row=5, pady=(0, 5), sticky="WE")
        frame5["relief"] = "groove"
        frame5["borderwidth"] = 5

        frame_boton.grid(row=6, column=0, ipady=5, sticky="WE")
        boton1.place(relx=0.08, rely=0.5, anchor="e")
        boton2.place(relx=0.18, rely=0.5, anchor="e")
        label_data_source.place(relx=0.5, rely=0.65, anchor="center")
        boton3.place(relx=0.92, rely=0.5, anchor="w")

        base.mainloop()
    except:
        pass
