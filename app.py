from flask import Flask, request, render_template, send_file
import pandas as pd
import os
import pickle
import zipfile

app = Flask(__name__)

zip_path = '/workspaces/proyecto_final_icfes_definitivo/random_forest_classifier_default_42.zip'

# Nombre del archivo del modelo dentro del ZIP
model_filename = 'random_forest_classifier_default_42.sav'

# Abrir el archivo ZIP
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    # Leer el archivo del modelo desde el ZIP sin extraerlo
    with zip_ref.open(model_filename) as model_file:
        # Cargar el modelo usando pickle
        model = pickle.load(model_file)


#definir las categorias
categories = (
    'EDAD', 
    'ESTU_COD_DEPTO_PRESENTACION', 
    'ESTU_DEDICACIONINTERNET', 
    'ESTU_DEDICACIONLECTURADIARIA', 
    'ESTU_DEPTO_RESIDE', 
    'ESTU_HORASSEMANATRABAJA', 
    'ESTU_TIPOREMUNERACION', 
    'FAMI_COMECARNEPESCADOHUEVO', 
    'FAMI_COMECEREALFRUTOSLEGUMBRE', 
    'FAMI_COMELECHEDERIVADOS', 
    'FAMI_CUARTOSHOGAR', 
    'FAMI_EDUCACIONMADRE', 
    'FAMI_EDUCACIONPADRE', 
    'FAMI_ESTRATOVIVIENDA', 
    'FAMI_NUMLIBROS', 
    'FAMI_PERSONASHOGAR', 
    'FAMI_SITUACIONECONOMICA', 
    'FAMI_TRABAJOLABORMADRE', 
    'FAMI_TRABAJOLABORPADRE', 
    'ESTU_GENERO', 
    'FAMI_TIENEINTERNET', 
    'FAMI_TIENECOMPUTADOR', 
    'FAMI_TIENEHORNOMICROOGAS', 
    'FAMI_TIENEMOTOCICLETA'
    'PUNT_GLOBAL'
)

# Definir las respuestas
answers = {
    'EDAD': [], 
    'ESTU_COD_DEPTO_PRESENTACION': ['AMAZONAS', 'ANTIOQUIA', 'ARAUCA', 'ATLANTICO', 'BOGOTÁ', 'BOLIVAR', 'BOYACA', 'CALDAS', 'CAQUETA', 'CASANARE', 'CAUCA', 'CESAR', 'CHOCO', 'CORDOBA', 'CUNDINAMARCA', 'GUAINIA', 'GUAVIARE', 'HUILA', 'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO', 'NORTE SANTANDER', 'PUTUMAYO', 'QUINDIO', 'RISARALDA', 'SANTANDER', 'SUCRE', 'TOLIMA', 'VALLE', 'VAUPES', 'VICHADA', 'SAN ANDRES'], 
    'ESTU_DEDICACIONINTERNET':['30 minutos o menos', 'Entre 1 y 3 horas', 'Entre 30 y 60 minutos', 'Más de 3 horas', 'No Navega Internet'],
    'ESTU_DEDICACIONLECTURADIARIA': ['30 minutos o menos', 'Entre 1 y 2 horas', 'Entre 30 y 60 minutos', 'Más de 2 horas', 'No leo por entretenimiento'],
    'ESTU_DEPTO_RESIDE': ['AMAZONAS', 'ANTIOQUIA', 'ARAUCA', 'ATLANTICO', 'BOGOTÁ', 'BOLIVAR', 'BOYACA', 'CALDAS', 'CAQUETA', 'CASANARE', 'CAUCA', 'CESAR', 'CHOCO', 'CORDOBA', 'CUNDINAMARCA', 'GUAINIA', 'GUAVIARE', 'HUILA', 'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO', 'NORTE SANTANDER', 'PUTUMAYO', 'QUINDIO', 'RISARALDA', 'SANTANDER', 'SUCRE', 'TOLIMA', 'VALLE', 'VAUPES', 'VICHADA', 'SAN ANDRES', 'EXTRANJERO'],
    'ESTU_HORASSEMANATRABAJA': ['0 horas', 'Entre 11 y 20 horas', 'Entre 21 y 30 horas', 'Menos de 10 horas', 'Más de 30 horas'],
    'ESTU_TIPOREMUNERACION': ['No', 'Si, en efectivo', 'Si, en efectivo y especie', 'Si, en especie'],
    'FAMI_COMECARNEPESCADOHUEVO': ['1 o 2 veces por semana', '3 a 5 veces por semana', 'Nunca o rara vez comemos eso', 'Todos o casi todos los días'],
    'FAMI_COMECEREALFRUTOSLEGUMBRE': ['1 o 2 veces por semana', '3 a 5 veces por semana', 'Nunca o rara vez comemos eso', 'Todos o casi todos los días'],
    'FAMI_COMELECHEDERIVADOS': ['1 o 2 veces por semana', '3 a 5 veces por semana', 'Nunca o rara vez comemos eso', 'Todos o casi todos los días'],
    'FAMI_CUARTOSHOGAR': ['Cinco', 'Cuatro', 'Dos', 'Seis o mas', 'Tres', 'Uno'],
    'FAMI_EDUCACIONMADRE': ['Educación profesional completa', 'Educación profesional incompleta', 'Ninguno', 'No Aplica', 'No sabe', 'Postgrado', 'Primaria completa', 'Primaria incompleta', 'Secundaria (Bachillerato) completa', 'Secundaria (Bachillerato) incompleta', 'Técnica o tecnológica completa', 'Técnica o tecnológica incompleta'],
    'FAMI_EDUCACIONPADRE': ['Educación profesional completa', 'Educación profesional incompleta', 'Ninguno', 'No Aplica', 'No sabe', 'Postgrado', 'Primaria completa', 'Primaria incompleta', 'Secundaria (Bachillerato) completa', 'Secundaria (Bachillerato) incompleta', 'Técnica o tecnológica completa', 'Técnica o tecnológica incompleta'],
    'FAMI_ESTRATOVIVIENDA': ['Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4', 'Estrato 5', 'Estrato 6', 'Sin Estrato'],
    'FAMI_NUMLIBROS': ['0 A 10 LIBROS', '11 A 25 LIBROS', '26 A 100 LIBROS', 'MÁS DE 100 LIBROS'],
    'FAMI_PERSONASHOGAR': ['1 a 2', '3 a 4', '5 a 6', '7 a 8', '9 o más'],
    'FAMI_SITUACIONECONOMICA': ['Igual', 'Mejor', 'Peor'],
    'FAMI_TRABAJOLABORMADRE': ['Es agricultor, pesquero o jornalero', 'Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial', 'Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc', 'Es operario de máquinas o conduce vehículos (taxita, chofer)', 'Es vendedor o trabaja en atención al público', 'No aplica', 'No sabe', 'Pensionado', 'Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)', 'Trabaja como personal de limpieza, mantenimiento, seguridad o construcción', 'Trabaja como profesional (por ejemplo médico, abogado, ingeniero)', 'Trabaja en el hogar, no trabaja o estudia', 'Trabaja por cuenta propia (por ejemplo plomero, electricista)'],
    'FAMI_TRABAJOLABORPADRE': ['Es agricultor, pesquero o jornalero', 'Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial', 'Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc', 'Es operario de máquinas o conduce vehículos (taxita, chofer)', 'Es vendedor o trabaja en atención al público', 'No aplica', 'No sabe', 'Pensionado', 'Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)', 'Trabaja como personal de limpieza, mantenimiento, seguridad o construcción', 'Trabaja como profesional (por ejemplo médico, abogado, ingeniero)', 'Trabaja en el hogar, no trabaja o estudia', 'Trabaja por cuenta propia (por ejemplo plomero, electricista)'],
    'ESTU_GENERO': ['F', 'M'],
    'FAMI_TIENEINTERNET': ['No', 'Si'],
    'FAMI_TIENECOMPUTADOR': ['No', 'Si'],
    'FAMI_TIENEHORNOMICROOGAS': ['No', 'Si'],
    'FAMI_TIENEMOTOCICLETA': ['No', 'Si']
}

# Diccionario de mapeo de nombres de columnas a preguntas descriptivas
questions = {
    'EDAD': '¿Que edad tiene?', 
    'ESTU_COD_DEPTO_PRESENTACION': '¿En que departamento presentó la prueba?', 
    'ESTU_DEDICACIONINTERNET': '¿Cuanto tiempo pasa en internet?',
    'ESTU_DEDICACIONLECTURADIARIA': '¿Cuanto tiempo le dedica a la lectura diariamente?',
    'ESTU_DEPTO_RESIDE': '¿En que departamento reside?',
    'ESTU_HORASSEMANATRABAJA': '¿Trabaja?, ¿Por cuantas horas?',
    'ESTU_TIPOREMUNERACION': 'Si trabaja, ¿Como le pagan?',
    'FAMI_COMECARNEPESCADOHUEVO': '¿Cuantas veces a la semana come carne, pescado y/o huevo?',
    'FAMI_COMECEREALFRUTOSLEGUMBRE': '¿Cuantas veces a la semana come cereal, frutos y/o legumbres?',
    'FAMI_COMELECHEDERIVADOS': '¿Cuantas veces a la semana come leche o derivados de leche?',
    'FAMI_CUARTOSHOGAR': '¿Cuantos cuartos hay en su hogar?',
    'FAMI_EDUCACIONMADRE': '¿Que nivel educativo tiene su madre?',
    'FAMI_EDUCACIONPADRE': '¿Que nivel educativo tiene su padre?',
    'FAMI_ESTRATOVIVIENDA': '¿Cual es su estrato?',
    'FAMI_NUMLIBROS': '¿Cuantos libros tiene?',
    'FAMI_PERSONASHOGAR': '¿Cuantas personas viven con usted?',
    'FAMI_SITUACIONECONOMICA': 'En comparación con el año anterior, ¿como esta la economia familiar hoy?',
    'FAMI_TRABAJOLABORMADRE': '¿Mamá tiene empleo?, ¿Cual?',
    'FAMI_TRABAJOLABORPADRE': '¿Papá tiene empleo?, ¿Cual?',
    'ESTU_GENERO': '¿Con que género biologico nacio?',
    'FAMI_TIENEINTERNET': '¿Tiene internet?',
    'FAMI_TIENECOMPUTADOR': '¿Tiene computador?',
    'FAMI_TIENEHORNOMICROOGAS': '¿Tiene horno, microondas y/o estufa a gas?',
    'FAMI_TIENEMOTOCICLETA': '¿Tiene moto?'
}

answer_mapping = {
    'EDAD': {}, 
    'ESTU_COD_DEPTO_PRESENTACION': {
        'AMAZONAS': 91, 'ANTIOQUIA': 5, 'ARAUCA': 81, 'ATLANTICO': 8, 
        'BOGOTÁ': 11, 'BOLIVAR': 13, 'BOYACA': 15, 'CALDAS': 17, 
        'CAQUETA': 18, 'CASANARE': 85, 'CAUCA': 19, 'CESAR': 20, 
        'CHOCO': 27, 'CORDOBA': 23, 'CUNDINAMARCA': 25, 'GUAINIA': 94, 
        'GUAVIARE': 95, 'HUILA': 41, 'LA GUAJIRA': 44, 'MAGDALENA': 47, 
        'META': 50, 'NARIÑO': 52, 'NORTE SANTANDER': 54, 'PUTUMAYO': 86, 
        'QUINDIO': 63, 'RISARALDA': 66, 'SANTANDER': 68, 'SUCRE': 70, 
        'TOLIMA': 73, 'VALLE': 76, 'VAUPES': 97, 'VICHADA': 99, 'SAN ANDRES': 88
        },
    'ESTU_DEDICACIONINTERNET':{
        '30 minutos o menos': 0, 'Entre 1 y 3 horas': 1, 'Entre 30 y 60 minutos': 2, 
        'Más de 3 horas': 3, 'No Navega Internet': 4
        },
    'ESTU_DEDICACIONLECTURADIARIA': {
        '30 minutos o menos': 0, 'Entre 1 y 2 horas': 1, 'Entre 30 y 60 minutos': 2, 
        'Más de 2 horas': 3, 'No leo por entretenimiento': 4
        },
    'ESTU_DEPTO_RESIDE': {
        'AMAZONAS': 0, 'ANTIOQUIA': 1, 'ARAUCA': 2, 'ATLANTICO': 3, 
        'BOGOTÁ': 4, 'BOLIVAR': 5, 'BOYACA': 6, 'CALDAS': 7, 'CAQUETA': 8, 
        'CASANARE': 9, 'CAUCA': 10, 'CESAR': 11, 'CHOCO': 12, 
        'CORDOBA': 13, 'CUNDINAMARCA': 14, 'GUAINIA': 15, 'GUAVIARE': 16, 
        'HUILA': 17, 'LA GUAJIRA': 18, 'MAGDALENA': 19, 'META': 20, 
        'NARIÑO': 21, 'NORTE SANTANDER': 22, 'PUTUMAYO': 23, 'QUINDIO': 24, 
        'RISARALDA': 25, 'SANTANDER': 26, 'SUCRE': 27, 'TOLIMA': 28, 
        'VALLE': 29, 'VAUPES': 30, 'VICHADA': 31, 'SAN ANDRES': 32, 'EXTRANJERO': 33
        },
    'ESTU_HORASSEMANATRABAJA': {
        '0 horas': 0, 'Entre 11 y 20 horas': 1, 'Entre 21 y 30 horas': 2, 
        'Menos de 10 horas': 3, 'Más de 30 horas': 4
        },
    'ESTU_TIPOREMUNERACION': {
        'No': 0, 'Si, en efectivo': 1, 'Si, en efectivo y especie': 2, 'Si, en especie': 3
        },
    'FAMI_COMECARNEPESCADOHUEVO': {
        '1 o 2 veces por semana': 0, '3 a 5 veces por semana': 1, 'Nunca o rara vez comemos eso': 2, 'Todos o casi todos los días': 3
        },
    'FAMI_COMECEREALFRUTOSLEGUMBRE': {
        '1 o 2 veces por semana': 0, '3 a 5 veces por semana': 1, 'Nunca o rara vez comemos eso': 2, 'Todos o casi todos los días': 3
        },
    'FAMI_COMELECHEDERIVADOS': {
        '1 o 2 veces por semana': 0, '3 a 5 veces por semana': 1, 'Nunca o rara vez comemos eso': 2, 'Todos o casi todos los días': 3
        },
    'FAMI_CUARTOSHOGAR': {
        'Cinco': 0, 'Cuatro': 1, 'Dos': 2, 'Seis o mas': 2, 
        'Tres': 3, 'Uno': 4
        },
    'FAMI_EDUCACIONMADRE': {
        'Educación profesional completa': 0, 'Educación profesional incompleta': 1, 'Ninguno': 2, 'No Aplica': 3, 
        'No sabe': 4, 'Postgrado': 5, 'Primaria completa': 6, 'Primaria incompleta': 7, 'Secundaria (Bachillerato) completa': 8, 
        'Secundaria (Bachillerato) incompleta': 9, 'Técnica o tecnológica completa': 10, 'Técnica o tecnológica incompleta': 11
        },
    'FAMI_EDUCACIONPADRE': {
        'Educación profesional completa': 0, 'Educación profesional incompleta': 1, 'Ninguno': 2, 'No Aplica': 3, 
        'No sabe': 4, 'Postgrado': 5, 'Primaria completa': 6, 'Primaria incompleta': 7, 'Secundaria (Bachillerato) completa': 8, 
        'Secundaria (Bachillerato) incompleta': 9, 'Técnica o tecnológica completa': 10, 'Técnica o tecnológica incompleta': 11
        },
    'FAMI_ESTRATOVIVIENDA': {
        'Estrato 1': 0, 'Estrato 2': 1, 'Estrato 3': 2, 'Estrato 4': 3, 
        'Estrato 5': 4, 'Estrato 6': 5, 'Sin Estrato': 6
        },
    'FAMI_NUMLIBROS': {
        '0 A 10 LIBROS': 0, '11 A 25 LIBROS': 1, '26 A 100 LIBROS': 2, 'MÁS DE 100 LIBROS': 3
        },
    'FAMI_PERSONASHOGAR': {
        '1 a 2': 0, '3 a 4': 1, '5 a 6': 2, '7 a 8': 3, '9 o más': 4
        },
    'FAMI_SITUACIONECONOMICA': {
        'Igual': 0, 'Mejor': 1, 'Peor': 2
        },
    'FAMI_TRABAJOLABORMADRE': {
        'Es agricultor, pesquero o jornalero': 0, 
        'Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial': 1, 
        'Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc': 2, 
        'Es operario de máquinas o conduce vehículos (taxita, chofer)': 3, 
        'Es vendedor o trabaja en atención al público': 4, 'No aplica': 5, 
        'No sabe': 6, 
        'Pensionado': 7, 
        'Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)': 8, 
        'Trabaja como personal de limpieza, mantenimiento, seguridad o construcción': 9, 
        'Trabaja como profesional (por ejemplo médico, abogado, ingeniero)': 10, 
        'Trabaja en el hogar, no trabaja o estudia': 11, 'Trabaja por cuenta propia (por ejemplo plomero, electricista)': 12
        },
    'FAMI_TRABAJOLABORPADRE': {
        'Es agricultor, pesquero o jornalero': 0, 
        'Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial': 1, 
        'Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc': 2, 
        'Es operario de máquinas o conduce vehículos (taxita, chofer)': 3, 'Es vendedor o trabaja en atención al público': 4, 
        'No aplica': 5, 'No sabe': 6, 'Pensionado': 7, 'Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)': 8, 
        'Trabaja como personal de limpieza, mantenimiento, seguridad o construcción': 9, 'Trabaja como profesional (por ejemplo médico, abogado, ingeniero)': 10, 
        'Trabaja en el hogar, no trabaja o estudia': 11, 'Trabaja por cuenta propia (por ejemplo plomero, electricista)': 12
        },
    'ESTU_GENERO': {
        'F': 0, 'M': 1
        },
    'FAMI_TIENEINTERNET': {
        'No': 0, 'Si': 1
        },
    'FAMI_TIENECOMPUTADOR': {
        'No': 0, 'Si': 1
        },
    'FAMI_TIENEHORNOMICROOGAS': {
        'No': 0, 'Si': 1
        },
    'FAMI_TIENEMOTOCICLETA': {
        'No': 0, 'Si': 1
        }
}

#Quiero ser capaz de visualizar ambos dataframes, el numerico es el que el modelo usa para la predicción y el otro me permite ver los valores string, es decir, las opciones elegidas por los usuarios, para la visualizacion de datos.
original_data_df = pd.DataFrame(columns=categories)
numeric_data_df = pd.DataFrame(columns=categories)

@app.route('/', methods=["GET", "POST"])
def home():
    prediction = None
    input_data = {}
    numeric_input_data = {}  # Para almacenar valores numéricos

    if request.method == "POST":
        for feature, question in questions.items():
            if feature == 'EDAD':
                input_data[feature] = int(request.form[feature])
            else:
                input_data[feature] = request.form[feature]

                # Convertir la respuesta a un valor numérico
                if feature in answer_mapping:
                    numeric_input_data[feature] = answer_mapping[feature][input_data[feature]]
                else:
                    numeric_input_data[feature] = input_data[feature]

        # Convertir los datos del formulario a un DataFrame de Pandas
        input_df = pd.DataFrame([numeric_input_data])
        
        # Realizar predicción con el modelo
        prediction = model.predict(input_df)[0]

        # Añadir la predicción al input_data y numeric_input_data
        input_data['PUNT_GLOBAL'] = prediction
        numeric_input_data['PUNT_GLOBAL'] = prediction

        # Agregar los datos originales al DataFrame
        original_data_df.loc[len(original_data_df)] = input_data
        
        # Agregar los datos numéricos al DataFrame
        numeric_data_df.loc[len(numeric_data_df)] = numeric_input_data

    return render_template("index.html", questions=questions, answers=answers, prediction=prediction)

# Rutas para descargar los archivos CSV
@app.route('/original_data_csv')
def download_original_data_csv():
    # Guardar el DataFrame como un archivo CSV con los nombres de columnas de categories
    original_data_df.to_csv('original_data.csv', index=False)
    # Retornar el archivo CSV como una respuesta para descargar
    return send_file('original_data.csv', as_attachment=True)

@app.route('/numeric_data_csv')
def download_numeric_data_csv():
    # Guardar el DataFrame como un archivo CSV con los nombres de columnas de categories
    numeric_data_df.to_csv('numeric_data.csv', index=False)
    # Retornar el archivo CSV como una respuesta para descargar
    return send_file('numeric_data.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)