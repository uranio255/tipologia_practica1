import json
from urllib.request import urlopen

# Esta función toma la información de entrada y la transforma en una tabla
# -> nombreX: Cadena. Nombre de la variable del eje X de la tabla.
# -> valoresX: Lista. Contiene todos los valores de que deben aparecer en el eje X de la tabla. La primera fila.
# -> nombreY: Cadena. Nombre de la variable del eje Y de la tabla.
# -> valoresY: Lista. Contiene todos los valores de que deben aparecer en el eje Y de la tabla. La primera columna.
# -> valores: Lista. El resto de valores que forman parte del propio
# contenido de la tabla.
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

# Esta función toma como entrada una tabla de valores y la escribe en un fichero en disco utilizando el formato CSV (líneas separadas por un retorno de carro y valores separados por comas dentro de una misma línea).
# -> tablaDatos: Lista de listas. La tabla de entrada.
# -> nombreFichero: Cadena. Nombre del fichero que debe escribirse en disco sin extensión ya que se asume ".csv"
def escribeFicheroCSV(tablaDatos, nombreFichero):
    
    # Crear el fichero de salida.
    ficheroSalida = open(nombreFichero + ".csv", "w")

    # Escribir cada línea de la tabla en el fichero CSV.
    for linea in tablaDatos:
        for i in range(0, len(tablaDatos[0]) - 1):
            ficheroSalida.write(str(linea[i]) + ",")
        
        ficheroSalida.write(str(linea[len(tablaDatos[0]) - 1]))
        ficheroSalida.write("\n")
    
    # Finalmente cerrar el fichero.
    ficheroSalida.close()

    
# Comienzo del programa principal

# La variable URL indica de dónde se toman los datos JSON.
url = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/tsdcc210?precision=1&airpol=GHG&unit=MIO_T&airemsect=CRF1A3"

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
escribeFicheroCSV(tabla, "GreenHouseGases")
