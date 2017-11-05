import os
import json
import numpy
from urllib.request import urlopen
from urllib.parse import quote

# Esta función toma la información de entrada y la transforma en una tabla
# -> nombreX: Cadena. Nombre de la variable del eje X de la tabla.
# -> valoresX: Lista. Contiene todos los valores de que deben aparecer en el eje X de la tabla. La primera fila.
# -> nombreY: Cadena. Nombre de la variable del eje Y de la tabla.
# -> valoresY: Lista. Contiene todos los valores de que deben aparecer en el eje Y de la tabla. La primera columna.
# -> valores: Lista. El resto de valores que forman parte del propio contenido de la tabla.
# <- La tabla construída.
def construyeTabla(nombreX, valoresX, nombreY, valoresY, valores):

    # Crear la tabla.
    tabla = []

    # Contenido de la esquina superior izquierda de la tabla. Se muestran los nombre de los dos ejes.
    lineaCabecera = [nombreY + "/" +nombreX]

    # Poner los valores X en la primera fila de la tabla.
    for x in valoresX:
        lineaCabecera.append(valoresX[x])

    # Añadir la primera línea a la tabla.
    tabla.append(lineaCabecera)

    # Añadir el resto de valores a la tabla sabiendo que el primer valor de cada línea es uno del eje Y.
    i = 0
    for y in valoresY:
        linea = []
        linea.append(valoresY[y])

        for j in range(0, len(valoresX)):
            linea.append(valores[str(i*len(valoresX) + j)])

        tabla.append(linea)
        i += 1

    return tabla

# Esta función toma como entrada una tabla de valores y la escribe en un fichero en disco utilizando el formato CSV (líneas separadas por un retorno de carro y valores separados por comas dentro de una misma línea). El fichero CSV creado se guardará en un directorio llamado "ficherosCSV" creado justo por debajo de donde está este script.
# -> tablaDatos: Lista de listas. La tabla de entrada.
# -> nombreFichero: Cadena. Nombre del fichero que debe escribirse en disco sin extensión ya que se asume ".csv"
def escribeFicheroCSV(tablaDatos, nombreFichero):

    # Directorio donde se creará el fichero CSV.
    directorio = "./ficherosCSV"

    # Asegurar que el directorio existe, si no, crearlo.
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    # Crear el fichero de salida.
    ficheroSalida = open(directorio + "/" + nombreFichero + ".csv", "w")

    # Escribir cada línea de la tabla en el fichero CSV.
    for linea in tablaDatos:
        for i in range(0, len(tablaDatos[0]) - 1):
            ficheroSalida.write(str(linea[i]) + ",")

        ficheroSalida.write(str(linea[len(tablaDatos[0]) - 1]))
        ficheroSalida.write("\n")

    # Finalmente cerrar el fichero.
    ficheroSalida.close()

# Esta función toma como entrada una tabla y le añade varias columnas correspondientes diferentes medidas de estadística descriptiva referidas a los distintos valores de la dimensión representada en vertical.
# Las medidas estadísticas que se hallan son las siguientes: valor máximo y mínimo, media, mediana, desviación estándar y varianza.
# -> tabla: Lista de listas. La tabla de entrada.
def agregarColumnasEstadisticas(tabla):

    # Agregación del máximo
    tabla[0].append("Valor máximo")
    for i in range(1, len(tabla)):
        tabla[i].append(numpy.max(tabla[i][1:]))

    # Agregación del máximo
    tabla[0].append("Valor mínimo")
    for i in range(1, len(tabla)):
        tabla[i].append(numpy.min(tabla[i][1:]))

    # Agregación de la media
    tabla[0].append("Media")
    for i in range(1, len(tabla)):
        tabla[i].append(numpy.mean(tabla[i][1:]))

    # Agregación de la mediana
    tabla[0].append("Mediana")
    for i in range(1, len(tabla)):
        tabla[i].append(numpy.median(tabla[i][1:]))

    # Agregación de la mediana
    tabla[0].append("Desviación estándar")
    for i in range(1, len(tabla)):
        tabla[i].append(numpy.std(tabla[i][1:]))

    # Agregación de la mediana
    tabla[0].append("Varianza")
    for i in range(1, len(tabla)):
        tabla[i].append(numpy.var(tabla[i][1:]))

# Esta función geocodifica una localización o dirección textual utilizando la API de Google.
# -> localizacion: Cadena. Referencia textual a geocodificar.
# -> geoDiccionario: Diccionario de localizaciones.
def geoCodifica(localizacion, geoDiccionario):

    # Valor particular no geocodificable.
    if localizacion == 'European Union (28 countries)':
        return 0,0

    # Valor particular que debe corregirse antes de geocodificarlo.
    if localizacion == 'Germany (until 1990 former territory of the FRG)':
        localizacion = 'Germany'

    # Si la localizacion ha sido geocodificada ya durante el transcurso de la ejecución de este script recuperar longitud y latitud del geo diccionario. Si no, llamar a la API de Google para obtener las coordenadas.
    if localizacion in geoDiccionario:
        return geoDiccionario[localizacion]["longitud"], geoDiccionario[localizacion]["latitud"]
    else:

        # La key a utilizar para llamar a la API de geocodificación de Google.
        googleAPIKey = "AIzaSyDWMptQo1kPSv3zunxq0fUwEWnFc-NkbFQ"

        # URL de la api de geocodificación de Google
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + quote(localizacion) + "&key=" + googleAPIKey

        # Cargar la respuesta JSON de Google.
        jsonData = json.load(urlopen(url))

        # Obtener la longitud y latitud.
        longitud = jsonData["results"][0]["geometry"]["location"]["lng"]
        latitud = jsonData["results"][0]["geometry"]["location"]["lat"]

        # Actualizar el geo diccionario.
        geoDiccionario[localizacion] = {"longitud": longitud, "latitud": latitud}

        return longitud, latitud

# Esta función ejecuta una geocodificación de todos los valores presentados en el eje vertical de la tabla. Normalmente deberían ser nombres de países.
# -> tabla: Lista de listas. La tabla en cuestión.
# -> geoDiccionario: Diccionario de localizaciones.
def geoCodificaValoresY(tabla, geoDiccionario):

    # Añade dos columnas nuevas para la longitud y la latitud.
    tabla[0].append("Longitud")
    tabla[0].append("Latitud")

    # Rellena ambas columnas.
    for i in range(1, len(tabla)):
        longitud, latitud = geoCodifica(tabla[i][0], geoDiccionario)
        tabla[i].append(longitud)
        tabla[i].append(latitud)

# Esta función toma como entrada un código correspondiente a una fuente contaminante y extrae de la web de Eurostat los datos de producción de gases de efecto invernadero referidos a esa fuente para cada uno de los países de la Unión entre 1990 y 2015. Tras haberlos recogido los graba en un fichero CSV cuyo nombre resulta de prefijar la cadena "GreenHouseGases_" y el código de la fuente contaminante.
# -> codigo: Cadena. Código correspondiente a la fuente contaminante.
def procesaDatosFuenteContaminante(codigo, geoDiccionario):

    # URL para obtener los datos de la fuente contaminante en formato JSON de Eurostat
    url = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/tsdcc210?airemsect=" + codigo

    # Cargar los datos JSON y los pone en una variable de tipo diccionario.
    jsonData = json.load(urlopen(url))

    # Obtiene del JSON la lista de valores correspondientes a los años.
    dimensionTiempo = jsonData["dimension"]["time"]["category"]["label"]

    # Obtiene del JSON la lista de valores correspondientes a los países.
    dimensionPais = jsonData["dimension"]["geo"]["category"]["label"]

    # Obtiene del JSON la lista del resto de los valores que forman el contenido del dataset.
    valores = jsonData["value"]

    # Construye la tabla
    tabla = construyeTabla("Año", dimensionTiempo, "Pais", dimensionPais, valores)

    # Agregar columnas estadísticas
    agregarColumnasEstadisticas(tabla)

    # Geocodifica los valores dispuestos en la vertical (típicamente países)
    geoCodificaValoresY(tabla, geoDiccionario)

    # Escribe la tabla construida anteriormente en un fichero CSV en disco.
    escribeFicheroCSV(tabla, "GreenHouseGases_" + codigo)

# Comienzo del programa principal

# La variable codigosFuenteContaminante almacena todas las fuentes contaminantes posibles y existentes en el portal Eurostat para el dataset de gases de efecto invernadero producidos en Europa. Estos códigos son importantes para extraer los datos en formato JSON de este portal web.

# Fuentes contaminantes (código - descripción):
# CRF1-6X4_MEMONIA - All sectors (excluding LULUCF and memo items, including international aviation)
# CRF1A1 - Fuel combustion in energy industries
# CRF1A2 - Fuel combustion in manufacturing industries and construction
# CRF1A3 - Fuel combustion in transport
# CRF2 - Industrial processes and product use
# CRF3 - Agriculture
# CRF5 - Waste management
# TOTX4_MEMONIA - All sectors and indirect CO2 (excluding LULUCF and memo items, including international aviation)

codigosFuenteContaminante = []
codigosFuenteContaminante.append("CRF1-6X4_MEMONIA")
codigosFuenteContaminante.append("CRF1A1")
codigosFuenteContaminante.append("CRF1A2")
codigosFuenteContaminante.append("CRF1A3")
codigosFuenteContaminante.append("CRF2")
codigosFuenteContaminante.append("CRF3")
codigosFuenteContaminante.append("CRF5")
codigosFuenteContaminante.append("TOTX4_MEMONIA")

# Inicializa el geo diccionario a utilizar.
# La idea es utilizarlo con el fin de evitar llamar más de una vez a la API de Google para geocodificar una localización ya geocodificada anteriormente durante el transcurso de la ejecución de este script.
geoDiccionario = {}

for codigoFC in codigosFuenteContaminante:
    procesaDatosFuenteContaminante(codigoFC, geoDiccionario)
