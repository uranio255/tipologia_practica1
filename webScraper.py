import os
import json
from urllib.request import urlopen

# Esta función toma la información de entrada y la transforma en una tabla
# -> nombreX: Cadena. Nombre de la variable del eje X de la tabla.
# -> valoresX: Lista. Contiene todos los valores de que deben aparecer en el eje X de la tabla. La primera fila.
# -> nombreY: Cadena. Nombre de la variable del eje Y de la tabla.
# -> valoresY: Lista. Contiene todos los valores de que deben aparecer en el eje Y de la tabla. La primera columna.
# -> valores: Lista. El resto de valores que forman parte del propio contenido de la tabla.
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
    
    directorio = "./ficherosCSV"
    
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

# Esta función toma como entrada un código correspondiente a una fuente contaminante y extrae de la web de Eurostat los datos de producción de gases de efecto invernadero referidos a esa fuente para cada uno de los países de la Unión entre 1990 y 2015. Tras haberlos recogido los graba en un fichero CSV cuyo nombre resulta de prefijar la cadena "GreenHouseGases_" y el código de la fuente contaminante.
# -> codigo: Cadena. Código correspondiente a la fuente contaminante.
def procesaDatosFuenteContaminante(codigo):
    
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

for codigoFC in codigosFuenteContaminante:
    procesaDatosFuenteContaminante(codigoFC)
