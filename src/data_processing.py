#Bibliotecas:
import pandas as pd

#Dataset:
data = pd.read_csv("../data/raw/df.csv")

#Eliminanos columnas que no usaremos:
data = data.drop(columns =["event","location"])

#Solo queremos filas que sean Victorias:
data = data[(data["status"] != "Fight was not properly finished") & (data["status"] != "draw")]
data = data.drop(columns = "status")

#Weight_class:
    #Dicionarios de valores:
division_dict = {'Middleweight': 'Peso Medio',
                'Bantamweight': 'Peso Gallo',
                'Featherweight': 'Peso Pluma',
                'Heavyweight': 'Peso Pesado',
                "Women's Bantamweight": 'Peso Gallo',
                'Lightweight': 'Peso Ligero',
                'Flyweight': 'Peso Mosca',
                "Women's Strawweight": 'Peso Paja',
                'Welterweight': 'Peso Welter',
                'Light Heavyweight': 'Peso Semipesado',
                "Women's Flyweight": 'Peso Mosca',
                'Catch Weight': 'Peso Pactado',
                "Women's Featherweight": 'Peso Pluma',
                'Super Heavyweight': 'Peso Super Pesado',
                'Open Weight': 'Peso Abierto'}

categorias_grupos = {'Peso Paja': 1, 'Peso Mosca': 1,'Peso Gallo': 1,
                     'Peso Pluma': 2,'Peso Ligero': 2,'Peso Welter': 2,
                     'Peso Medio': 3,'Peso Semipesado': 3,'Peso Pactado': 3,
                     'Peso Pesado': 4,'Peso Super Pesado': 4,'Peso Abierto': 4}

    #Mapeamos los diccionarios:
data["weight_class"] = data["weight_class"].map(division_dict)
data['weight_class'] = data['weight_class'].map(categorias_grupos)

#Method:
    #Diccionario:
method_dict = {"U-DEC": 1,
               "KO/TKO": 2,
               "SUB": 3,
               "DQ": 4,
               "S-DEC" : 5,
               "M-DEC" : 6}
    #Mapeamos:
data["method"] = data["method"].map(method_dict)

#Method_Detailed:
    #Diccionarios para rellenar missingvalues:
asignacion_method = {1: 1, 2: 1, 5: 1,
                     6: 1, 3: 2, 4: 3}

    #Mapeado:
data['method_detailed'] = data['method_detailed'].fillna(data['method'].map(asignacion_method))

    #Diccionarios de valores:
golpes = {"Punches", "Kick", "Punch", "Elbows", "Elbow", "Flying Knee", 
          "Knees", "Knee", "Kicks", "Spinning Back Kick", 
          "Spinning Back Fist", "Spinning Back Elbow", 
          "Headbutts", "Slam"}

suelo = {"Rear Naked Choke","D'Arce Choke","Guillotine Choke","Arm Triangle","Armbar","Triangle Choke","Anaconda Choke",
        "Neck Crank","Kimura","Kneebar","Inverted Triangle","Von Flue Choke","Scarf Hold","Straight Armbar","Heel Hook",
        "Ankle Lock","Forearm Choke","Ezekiel Choke","Peruvian Necktie","Schultz Front Headlock","Bulldog Choke",
        "Suloev Stretch","Omoplata","Calf Slicer","North-South Choke","Pace/Pillory Choke","Toe Hold",
        "Shoulder Choke","Twister","Triangle Armbar"}

descalificacion = {"Other", "Other - Lock", "Other - Choke", "Injury", "Gi Choke", "Keylock","Headbutt"}

data["method_detailed"] = data["method_detailed"].replace(golpes, 1).replace(suelo, 2).replace(descalificacion, 3).astype(int)

#Time:
data['time'] = data['time'].str.split(':').str[0].astype(int)
data = data[data['time'] <= 5] #Eliminar peleas en las que no haya rounds de máximo 5 minutos

#Round:
data['time'] = (data['round'] - 1) * 5 + data['time']
data = data.drop(columns = "round")

#Date:
data.loc[:,'date'] = pd.to_datetime(data['date'], format='%m/%d/%Y')

#Eliminar MissingValues generales:
data = data.dropna()

#Guarduamos en processed:
data.to_csv("../data/processed/data_processed.csv")


#Creamos dataset métricas de algunos peleadores
    #Contar las apariciones de cada peleador en ambas columnas:
peleas_r = data['r_fighter'].value_counts()
peleas_b = data['b_fighter'].value_counts()

peleas_totales = peleas_r.add(peleas_b, fill_value=0)

#Peleadores con más de 25 peleas:
luchadores_mas_25_peleas = peleas_totales[peleas_totales > 25]

data_filtrado_ganadores = data[data['r_fighter'].isin(luchadores_mas_25_peleas.index)]
data_filtrado_perdedores = data[data['b_fighter'].isin(luchadores_mas_25_peleas.index)]

medianas_ganadores = data_filtrado_ganadores.groupby('r_fighter')[['r_kd', 'r_str', 'r_td', 'r_sub']].median()
medianas_perdedores = data_filtrado_perdedores.groupby('b_fighter')[['b_kd', 'b_str', 'b_td', 'b_sub']].median()

medianas_ganadores.columns = ['kd', 'str', 'td', 'sub']
medianas_perdedores.columns = ['kd', 'str', 'td', 'sub']

#Estadisticas serán la media de las medianas de todos sus combates:
metrics_media = (medianas_ganadores + medianas_perdedores) / 2

weight_class_ganadores = data_filtrado_ganadores.groupby('r_fighter')['weight_class'].apply(lambda x: x.mode()[0]).reset_index()
weight_class_perdedores = data_filtrado_perdedores.groupby('b_fighter')['weight_class'].apply(lambda x: x.mode()[0]).reset_index()

weight_class_ganadores.rename(columns={'r_fighter': 'fighter', 'weight_class': 'weight_class'}, inplace=True)
weight_class_perdedores.rename(columns={'b_fighter': 'fighter', 'weight_class': 'weight_class'}, inplace=True)

weight_classes_combined = pd.concat([weight_class_ganadores, weight_class_perdedores], axis=0)

weight_class_final = weight_classes_combined.groupby('fighter')['weight_class'].apply(lambda x: x.mode()[0])

metrics_media = metrics_media.reset_index()
metrics_media.rename(columns={'r_fighter': 'fighter'}, inplace=True)

metrics_media = metrics_media.merge(weight_class_final, on='fighter', how='left')

#Elimino la categoría de pelea 1 ya que solo habia un peleador entre los 29 escogidos
metrics_media = metrics_media[metrics_media["weight_class"] != 1]

metrics_media.to_csv("../data/processed/metrics_media_1.csv")

