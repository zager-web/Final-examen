"""
------------------------------
-                            -
- by: Valentina Diaz Arrieta -
-                            -
------------------------------
            ---
            ---
*/*/*/*/*/*/---*/*/*/*/*/*/*/*
______________________________

"""
# IMPORTACION DE TIEMPO CODIGO, LIBRERIA RANDOM Y CADENA CARACTER
import time
import random
import string
#*_*_*_*_*_*_*_*_*_*_ LIBRERIA DE UTILIZAD - EL ARCHIVO LLAMADO COMPLEMENTO.PY AL LADO DE ESTE
from complemento import * 
#*_*_*_*_*_*_*_*_*_*_ ASIGNACION DE DATOS MATRIZ
def crear_matrix(nxn):
    """Devuelve matrix de nxn filas/columnas."""
    matrix =[]
    for i in range(nxn):
        matrix.append([])
        for e in range(nxn):
            matrix[i].append("")
    return matrix
def completar_matrix(mtx, n, randomChar=True):
    """Completa y devuelve una matriz con letras aleatorias o con asteriscos.
    Parametros:
    mtx        -- matriz a completar
    n          -- entero de filas/columnas a completar
    randomChar -- booleano que indica si son letras aleatorias o asteriscos
    """
    for i in range(n):
        for e in range(n):
            if randomChar :
                if mtx[i][e] == "" : mtx[i][e] = random.choice(string.ascii_lowercase)
            else:
                if mtx[i][e] == "" : mtx[i][e] = "*"
    return mtx
def valores_posicion(matrix, nxn, isrow, pos):
    """Devuelve una lista con informacion acerca de una fila/columna especifica de la matriz.
    Parametros:
    isrow -- booleano que indica si es fila o columna
    pos   -- entero que indica fila/columna
    """
    valores = []
    espacios = 0
    for i in range(nxn):
        if isrow:
            if matrix[pos][i] != "":
                valores.append(espacios)
                valores.append(matrix[pos][i])
            else:
                espacios+=1
        else:
            if matrix[i][pos] != "":
                valores.append(espacios)
                valores.append(matrix[i][pos])
                espacios = 0
            else:
                espacios+=1
    # Si la fila/columna esta vacia, indicar que existen nxn espacios vacios
    if espacios == nxn :
        valores.append(espacios)
        valores.append("0")
    return valores
def procesar_palabras(matrix, nxn, palabras):
    """Acomoda las palabras en la matriz tablero, y la devuelve junto a una lista de posiciones y entero de las palabras salteadas.

    Para acomodar las palabras se les asigna un sentido, una direccion y una posicion aleatoria dentro de la matriz.
    Se pide informacion de tal fila/columna a la funcion "valores_posicion" hasta que la palabra en cuestion pueda ser correctamente acomodada dentro de la matriz.
    Si la palabra no puede ser acomodada en la fila/columna random, con la direccion random, se prueba en la siguiente fila/columna con la misma direccion; una vez
    recorridas todas las filas/columnas, cambia la direccion y prueba nuevamente una por una. Si tampoco sirve, se saltea la palabra
    Las primeras dos palabras cumplen con ciertas condiciones:
    1) La primer palabra debe tener direccion vertical y estar posicionada de arriba hacia abajo
    2) La segunda palabra debe tener direccion horizontal y estar posicionada de derecha a izquierda
    Parametros:
    matrix   -- matriz en la que procesar las palabras
    nxn      -- entero que indica la longitud de la matrix
    palabras -- lista de palabras para procesar
    """
    salteadas = 0
    posiciones = []
    # direccion       -- bool  indica la direccion de la palabra
    # posicion        
    # sentido_inverso -- bool indica el sentido de la palabra
    for i in range(len(palabras)):
        posicion_inicial = random.randint(0,nxn-1)
        sentido_inverso = bool(random.randint(0,1))
        if i == 0:
            direccion_inicial = False # Primer palabra siempre Vertical
        elif i == 1:
            direccion_inicial = True  # Segunda palabra  Horizontal
            sentido_inverso = True    # Segunda palabra Invertida
        else:
            direccion_inicial = bool(random.randint(0,1))
        posicion = posicion_inicial
        direccion = direccion_inicial
        if sentido_inverso:
            palabras[i] = palabras[i][::-1]
        colocada = False
        while(not colocada):
            # Siempre Par
            valores_en_posicion = valores_posicion(matrix, nxn, direccion, posicion)
            for e in range(len(valores_en_posicion)/2):
                #  margen random a la palabra
                if int(valores_en_posicion[e*2]) >= len(palabras[i]) :
                    margen = int(valores_en_posicion[e*2]) - len(palabras[i])
                    if margen > 0:
                        inicio = random.randint(0,margen)
                    matrix = colocar_palabra(matrix, palabras[i], direccion, posicion, margen)
                    if direccion :
                        fila_inicio = posicion
                        columna_inicio = margen
                        fila_final = posicion
                        columna_final = margen + len(palabras[i])-1
                    else:
                        columna_inicio = posicion
                        fila_inicio = margen
                        columna_final = posicion
                        fila_final = margen + len(palabras[i])-1
                    if sentido_inverso :
                        aux = fila_final
                        fila_final = fila_inicio
                        fila_inicio = aux
                        aux = columna_final
                        columna_final = columna_inicio
                        columna_inicio = aux  
                    # Alternativa  "legible" a las posiciones
                    # posiciones
                    posiciones.append(str(columna_inicio)+str(fila_inicio)+str(columna_final)+str(fila_final))
                    colocada = True
                    print "colocada"
                    break
            if not colocada:
                print "no colocada"
                # Si en esa posicion no entra, probar en la siguiente
                if posicion < nxn-1: posicion += 1
                else: posicion = 0
                # prueba todas las posiciones, cambiar direccion y probar de nuevo
                if posicion == posicion_inicial :
                    direccion = not direccion
                    # Si cambiar la direccion y probar en todas las posiciones tampoco sirve, entonces saltear palabra
                    if direccion == direccion_inicial:
                        salteadas+=1
                        # Si, "Break" porque el while esta dentro del For.
                        break
    if salteadas != 0 : return matrix,posiciones,salteadas
    else: return matrix,posiciones,0
def colocar_palabra(matrix, palabra, esfila, pos, inicio) :
    """Coloca la palabra dentro de la matriz en la fila/columna especificada.
    Params:
        - palabra: cadena a ubicar
        - esfila: determina si es fila o columna
        - pos: posicion de la fila/columna
        - inicio: margen que tiene desde el inicio de la fila/columna
    """
    for x in range(inicio, inicio+len(palabra) ) :
        if esfila:
            matrix[pos][x] = palabra[x-inicio]
        else:
            matrix[x][pos] = palabra[x-inicio]
    return matrix
def mostrar_tablero(mtx, n):
    """Imprime la matriz en forma de tablero, con letras para indicar las columnas y numeros para indicar las filas."""
    # Cabecera de Columnas
    fila = "/ |"
    for i in range(n):
        fila = fila + " " + chr(65+i)
    print fila
    print "-"*(2*n+3)
    # Cabecera de Filas
    for i in range(n):
        fila = str(i+1)
        if i < 9 : fila += " |"
        else:
            fila+="|"
        for e in range(n):
            fila = fila+" "+mtx[i][e]
        print fila
        fila = ""
    # Nueva linea
    print ""
#============== Ingreso de datos
def pedir_entero(msg, min, max):
    """Devuelve entero aceptado entre los definidos por parametros.
    Parametros:
    msg -- mensaje para mostrar
    min -- entero minimo para aceptar
    max -- entero maximo para aceptar
    """
    while True:
        n = str(raw_input(msg))
        if not n.isdigit() :
            show_msg("Oops! Parece que eso no era un numero entero")
            continue
        n = int(n)
        if n <= max and n >= min :
            return n
        else:
            show_msg("Numero fuera de rango")
            continue
def pedir_palabra(msg, min, max):
    """Devuelve cadena aceptada con longitud entre la definida por parametros.
    Parametros:
    msg -- mensaje para mostrar
    min -- longitud entera minima para aceptar
    max -- longitud entera maxima para aceptar
    """
    while True:
        txt = str(raw_input(msg))
        if not txt.isalpha() :
            show_msg("Oops! Parece que eso no era una palabra valida")
            continue
        if len(txt) > max:
            show_msg("Palabra muy larga (Max %d caracteres)"%max)
            continue
        elif len(txt) < min :
            show_msg("Palabra muy corta (Min %d caracteres)"%min)
            continue
        else:
            return txt.lower()
def pedir_coordenadas():
    """Devuelve una cadena con las coordenadas y direccion de la palabra si son validas, o falso y un mensaje de error."""
    entrada = raw_input(obtener_mensaje("rawinput_coordenadas"))
    # Las coordenadas deben tener un minimo de 5 caractes y un maximo de 7, dada la manera en la que estan escritas (A10,A20)
    # PD: No son numeros inventados.
    if len(entrada) < 5 or len(entrada) > 7 or not "," in entrada:
        return False, obtener_mensaje("entrada_incorrecta")
    entradas = entrada.split(",")
    if len(entradas) != 2 :
        return False, obtener_mensaje("entrada_incorrecta")
    if not str(entradas[0][1:]).isdigit() or not entradas[1][1:].isdigit() :
        return False, obtener_mensaje("entrada_incorrecta")
    return entradas, ""
def procesar_coordenadas(entradas, nxn, posiciones, matrix):
    """Devuelve la matriz modificada si las coordenadas dadas refieren a una palabra, mostrandola en mayuscula y la remueve de posiciones."""
    columna_inicio = entradas[0][0]
    fila_inicio    = int(entradas[0][1:])-1

    columna_final = entradas[1][0]
    fila_final    = int(entradas[1][1:])-1
    if fila_final >= nxn or fila_inicio >= nxn :
        return False, obtener_mensaje("rango_fila"), posiciones, matrix
    # 65 es el valor decimal de la letra A en la tabla ASCII, la cual coincide con el origen de coordenadas de nuestro tablero.
    if ord(columna_inicio.upper())-65 >= nxn or ord(columna_final.upper())-65 >= nxn :
        return False, obtener_mensaje("rango_columna"), posiciones, matrix
    else:
        columna_inicio = ord(columna_inicio.upper())-65
        columna_final  = ord(columna_final.upper())-65
    if columna_inicio != columna_final and fila_inicio != fila_final :
        return False, obtener_mensaje("fila_o_columa_igual"), posiciones, matrix
    if columna_inicio == columna_final :
        vertical = True
    else:
        vertical = False
    # Se arma una cadena con las coordenadas de la misma forma como fue agregada anteriormente a la lista "posiciones"
    cadena_de_posicion = str(columna_inicio)+str(fila_inicio)+str(columna_final)+str(fila_final)
    #============== Comprobar si existe la palabra. Removerla en caso afirmativo
    if not cadena_de_posicion in posiciones :
        return False, obtener_mensaje("error_coordenadas"), posiciones, matrix
    posiciones.remove(cadena_de_posicion)
    #============== Mostrar la palabra en mayuscula
    if vertical :
        for fila in range(min(fila_inicio, fila_final),max(fila_inicio, fila_final)+1) : 
            matrix[fila][columna_final] = str(matrix[fila][columna_final]).upper()
    else:
        for columna in range(min(columna_inicio, columna_final),max(columna_inicio, columna_final)+1) :
            matrix[fila_inicio][columna] = str(matrix[fila_inicio][columna]).upper()
    return True, "", posiciones, matrix
def procesar_juego(matrix,nxn,n_palabras,salteadas,posiciones):
    """Devuelve el estado del juego cuando este termina.

    La parte de procesado se encarga de verificar que se hayan encontrado todas las palabras o que el se haya rendido.

    Parametros:
    matrix     -- matrix tablero para procesar
    nxn        -- dimension de la matriz tablero
    n_palabras -- cantidad de palabras en la matriz
    salteadas  -- cantidad de palabras salteadas para mostrar en un mensaje
    posiciones -- posiciones de las palabras
    """
    palabras_restantes = n_palabras
    msg_to_show = ""

    while palabras_restantes > 0:
        clear_window()
        show_title("Encuentre las palabras")
        # Si por parametro se indica que existen palabras salteadas, mostramos un mensaje
        if salteadas != None:
            show_msg("Palabras restantes: %d Salteadas: %d \n"%(palabras_restantes, salteadas))
        else:
            show_msg("Palabras restantes: %d \n"%palabras_restantes)
        mostrar_tablero(matrix, nxn)
        # Mostramos el mensaje y le agregamos una linea nueva
        if msg_to_show != "":
            show_msg(msg_to_show+"\n")
            msg_to_show = ""
        coordenadas, msg_to_show = pedir_coordenadas()
        if not coordenadas : continue
        encontrada, msg_to_show, posiciones, matrix = procesar_coordenadas(coordenadas, nxn, posiciones, matrix)
        if not encontrada : continue
        else:
            palabras_restantes -= 1
            msg_to_show = "Muy Bien! Encontraste una palabra!"
    mostrar_fin_juego(n_palabras)
    return True
def mostrar_fin_juego(n_palabras):
    """Imprime un mensaje de fin de juego."""
    clear_window()
    show_title("FELICIDADES! GANASTE!")
    show_msg("Muy bien, encontraste las %d palabras!" % n_palabras)
    raw_input("Enter para menu principal ")
#============== Opciones del menu
def juego_nuevo():
    """Pide al jugador la cantidad de filas/columnas, cantidad de palabras y las palabras."""
    show_title("Crear sopa de NxN letras")
    nxn         = pedir_entero("Ingrese un numero entero de la cantidad de\nfilas y columnas que desea (Entre 10 y 20):\n",10,20)
    n_palabras  = pedir_entero("Ingrese un numero entero de la cantidad de\npalabas que deasea agregar (Entre 0 y %d):\n"%(nxn/2),0,(nxn/2))
    palabras = []
    palabra_min_caracteres = 3
    palabra_repetida = False
    while len(palabras)<n_palabras:
        if palabra_repetida :
            show_msg("Ingreso una palabra repetida")
            palabra_repetida = False
        # Pedir una palabra que cumpla con los requisitos
        palabra = pedir_palabra("[%d|%d]Ingrese una palabra entre %d y %d caracteres: "%(len(palabras)+1,n_palabras,palabra_min_caracteres,(nxn/2)),palabra_min_caracteres,(nxn/2))
        if palabra in palabras:
            palabra_repetida = True
        else :
            palabras.append(palabra)
    matrix = crear_matrix(nxn)
    matrix,posiciones,salteadas = procesar_palabras(matrix, nxn, palabras)
    matrix = completar_matrix(matrix, nxn)
    return procesar_juego(matrix,nxn,n_palabras,salteadas,posiciones)
def mostrar_acerca_de():
    """Imprime un mensaje de parte del desarrollador."""
    show_title("Informacion del Juego")
    show_msg("""              ------------------------------\n""")
    show_msg("              -                            -\n")
    show_msg("              - by: Valentina Diaz Arrieta -\n")
    show_msg("              -                            -\n")
    show_msg("              ------------------------------\n")
    raw_input("Enter para ir al menu principal ")
    return True
#============== Init
def menu_inicial():
    """Imprime el menu inial con sus opciones."""
    clear_window()
    items = ["Juego Nuevo", "Acerca de", "Salir"]
    while True:
        show_title("____ Menu Inicial ____")
        item = show_menu(items)
        clear_window()
        if item == 0 :
            juego_nuevo()
            clear_window()
        elif item==1 :
            mostrar_acerca_de()
            clear_window()
        elif item==2 :
            return
        else:
            print "Opcion invalida"
def main():
    """Imprime splash screen y llama al menu inicial."""
    show_title("BENVENID@")
    # Splash 10x10 matriz BOOTLOOP
    splash =[
         [ "","","","","","","","","","" ],
         [ "","","","U","N","A","L","","","" ],
         [ "","","","","","","","","","" ],
         [ "","","","","","","","","","" ],
         [ "","","","S","O","P","A","","","" ],
         [ "","","","","","","","","","" ],
         [ "","","","","D","E","","","","" ],
         [ "","","","","","","","","","" ],
         [ "","","L","E","T","R","A","S","","" ],
         [ "","","","","","","","","","" ]
         ]
    completar_matrix(splash, 10, False) 
    mostrar_tablero(splash, 10)  
    time.sleep(5)                # Tiempo de espera 5 segundos
    clear_window()
    menu_inicial()
main()

