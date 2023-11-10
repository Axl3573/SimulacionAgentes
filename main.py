import pygame
import sys
from Agente import *
import matplotlib.pyplot as plt

# Inicializando pygame
pygame.init()

# Definiendo pantalla principal, nombre y tamaño
width, height = 1000, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulacion")

# Colores que se usan a lo largo del programa
white = (255, 255, 255)
black = (0, 0, 0)
colorPanelAbajo = (150, 220, 150)


# Creando las cuadriculas
cuadricula = pygame.Surface((3 * width / 4, height))
cuadricula.fill(white)
pygame.draw.rect(cuadricula, black, cuadricula.get_rect(), 2)


# Creando el panel de la derecha, el cual se encarga de almacenar la informacion del agente al que se le hace click
panel_width = width / 4 + 50  
panel_surface = pygame.Surface((panel_width, height))
panel_surface.fill(white)
pygame.draw.rect(panel_surface, black, panel_surface.get_rect(), 2)


# Creando el panel de abajo, este almacena los botones
panelAuxiliar = pygame.Surface((width, height / 2))
panelAuxiliar.fill(colorPanelAbajo)


# Número de filas y columnas de la cuadrícula
# No modificar
filas, columnas = 22, 29


# Tamaño de las celdas
# No modificar o se rompe xD
cell_width = 25
cell_height = 25

# Inicializar una matriz para asi controlar por indices cada una de las celdas
# Principalmente usado para cambiar colores y obtener posiciones
cuadriculaEstado = [[white for _ in range(columnas)] for _ in range(filas)]


# Dibujar la frontera
for i in range(filas):
    cuadriculaEstado[i][14] = black


# Inicializando los agentes
listaPersonas = []

# No aumentar de mas
numeroPersonas = 120


# No modificar
diaActual = 0  

# Creando los objetos (Agentes)
for i in range(numeroPersonas):
    listaPersonas.append(Agente())


# Inicializandolos con su metodo
# No se usa un constructor ya que se necesita la lista de agentes previamente creados
for i in range(numeroPersonas):
    listaPersonas[i].inicializar(listaPersonas)


# Se agregan los agentes a la cuadricula, con su metodo getColor()
for i in range(numeroPersonas):
    cuadriculaEstado[listaPersonas[i].x][listaPersonas[i].y] = listaPersonas[i].getColor()


# Variables para graficar
historialMotivacion = [[] for i in range(numeroPersonas)]
historialDinero = [[] for i in range(numeroPersonas)]
numeroDiasSimular = 1500


crucesPorDia = [0] * numeroDiasSimular


# Funcion auxiliar para realiar la simulacion
def simular():
    global diaActual
    diaActual += 1
    # Poner de color blanco todas las celdas pintadas
    for i in range(numeroPersonas):
        cuadriculaEstado[listaPersonas[i].x][listaPersonas[i].y] = white


    # Ejecutar la funcion simular para cada agente
    for i in range(numeroPersonas):
        listaPersonas[i].simular(listaPersonas)
        if listaPersonas[i].motivacion >= 100 and (not listaPersonas[i].objetivoCumplido):
            
            listaPersonas[i].cambiarPais(listaPersonas)

        if listaPersonas[i].objetivoCumplido:
    
            crucesPorDia[diaActual] += 1

    # Repintar celdas
    for i in range(numeroPersonas):
        cuadriculaEstado[listaPersonas[i].x][listaPersonas[i].y] = listaPersonas[i].getColor()


# Funcion del boton uno, solo se ejecuta una vez
def botonUnoFuncion():
    simular()


# Funcion del boton dos, se ejecuta 5 veces
# No se pueden hacer pausas
# Continuar con lo demas, dejar esto al final
def botonDosFuncion():
    for i in range(5):
        simular()


# Funcion para forzar de cierta forma a los agentes, el dia festivo aumenta en 20 la motivacion de cada uno, en caso de anteriormente pensar en viajar por turismo
def botonTresFuncion():
    print("DIA FESTIVO")
    for i in range(numeroPersonas):
        if listaPersonas[i].tomarDesicion() == "Viajar por turismo":
            listaPersonas[i].motivacion+=20

# Aqui se cambia el agente a seguir a color verde, para no perderlo de vista
# Presionar simular un dia para ver el cambio
def botonCuatroFuncion():
    global colorAnterior
    colorAnterior = agenteSeguir.getColor()
    print("Track")
    agenteSeguir.color = (0,255,20)

# Aqui se cambia el agente a su color original
# Presionar simular un dia para ver el cambio
def botonCincoFuncion():
    print("DesTrack")
    agenteSeguir.color = colorAnterior


# Graficar la relacion Tiempo-Motivacion
def graficasUno():
    plt.figure(figsize=(14, 6))
    for i in range(numeroPersonas):
        plt.plot(historialMotivacion[i])
    plt.xlabel('Tiempo')
    plt.ylabel('Motivación')

    
    interval = 50
    xticks = range(0, numeroDiasSimular, interval)

    
    plt.xticks(xticks)

    plt.tight_layout()
    plt.show()


# Graficar la relacion Tiempo-Dinero
def graficasDos():
    plt.figure(figsize=(14, 8))
    for i in range(numeroPersonas):
        plt.plot(historialDinero[i])
    
    
    plt.xlabel('Tiempo')
    plt.ylabel('Dinero')

    interval = 50
    xticks = range(0, numeroDiasSimular, interval)

    
    plt.xticks(xticks)


    plt.tight_layout()
    plt.show()  

# Grafica para la relacion Dias-Cruces
def graficasTres():
    plt.figure(figsize=(14, 8))
    plt.plot(range(numeroDiasSimular), crucesPorDia)
    plt.xlabel('Dias')
    plt.ylabel('Número de Cruces')
    plt.title('Cruces de Agentes por Día')

    interval = 50
    xticks = range(0, numeroDiasSimular, interval)

    
    plt.xticks(xticks)
 
    plt.tight_layout()
    plt.show()


# Función para dibujar a un agente en el panel derecho
def dibujarInfoAgente(agente, panel_surface):
    global agenteSeguir
    agenteSeguir = Agente()

    if agente.motivacion >= 100:
        agente.motivacion = 100

    if agente.nacionalidad == 0:
        nacionalidad = "Pais A"
    
    if agente.nacionalidad == 1:
        nacionalidad = "Pais B"

    # Imprime info del agente
    if agente.objetivoCumplido == True:
        info_text = f"\n\n\n\n Dinero: {agente.dinero}\n\n Motivacion: {agente.motivacion}\n\n Familiares: {agente.familiares}\n\n Edad: {agente.edad}\n\n Estado Visa: {agente.estadoVisa}\n\n Nacionalidad: {nacionalidad}\n\n Pensando en: \n {agente.tomarDesicion()}\n\n Quedandose {agente.diasQuedarse} Dias"
    else:
        info_text = f"\n\n\n\n Dinero: {agente.dinero}\n\n Motivacion: {agente.motivacion}\n\n Familiares: {agente.familiares}\n\n Edad: {agente.edad}\n\n Estado Visa: {agente.estadoVisa}\n\n Nacionalidad: {nacionalidad}\n\n Pensando en: \n {agente.tomarDesicion()}"
    lineas = info_text.splitlines()
    color_box_width = 50
    color_box_height = 50
    color_box_x = 20

    agenteSeguir = agente
    
    font = pygame.font.Font(None, 26)
    panel_surface.fill(white)

    y_offset = 20 

    # Dibuja el cuadro de color antes del texto
    pygame.draw.rect(panel_surface, agente.color, (color_box_x, y_offset, color_box_width, color_box_height))

    for linea in lineas:
        text_surface = font.render(linea, True, black)
        panel_surface.blit(text_surface, (20, y_offset))
        y_offset += text_surface.get_height() + 5

# Lista de botones con sus textos y funciones correspondientes
botones = [
    {"text": "Simular 1 Dia", "function": botonUnoFuncion},
    {"text": "Simular 5 Dias", "function": botonDosFuncion},
    {"text": "Dia Festivo", "function": botonTresFuncion},
    {"text": "Seguir Agente", "function": botonCuatroFuncion},
    {"text": "Dejar De Seguir", "function": botonCincoFuncion},
]

botonesGraficas = [
    {"text": "Motivacion-Tiempo", "function": graficasUno},
    {"text": "Dinero-Tiempo", "function": graficasDos},
    {"text": "Cruces", "function": graficasTres}

]

# Coordenadas y dimensiones de los botones (dentro del panel de abajo)
botonAncho = 200
botonAlto = 40
botonX = 20
espacioBotonoes = 10  
botonY = 70

botonAnchoDos = 280
botonAltoDos = 40
botonXDos = 600
espacioBotonoesDos = 10  
botonYDos = 70



# Actualizar datos para graficarlos
def actualizarHistorial():
    for i in range(numeroPersonas):
        historialMotivacion[i].append(listaPersonas[i].motivacion)
        historialDinero[i].append(listaPersonas[i].dinero)



# Variables para controlar si el mouse esta encima de un boton
hovered_button = None
hovered_button_g = None

# Variable para controlar el bucle principal
running = True



# Etiquetas de texto para los países
font = pygame.font.Font(None, 40)
pais_a_text = font.render("        A", True, black)
pais_b_text = font.render("        B", True, black)

# Posiciones de las etiquetas de texto
paisAx = 50  
paisBx = 450
paisY = 20

while running:
    
    actualizarHistorial()

    # Dentro del bucle principal
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            # Verificar si el ratón está sobre algún botón dentro del panel
            mouse_x, mouse_y = event.pos
            hovered_button = None
            hovered_button_g = None


            for i, button in enumerate(botones):
                button_rect = pygame.Rect(botonX, botonY + (botonAlto + espacioBotonoes) * i, botonAncho, botonAlto)
                if button_rect.collidepoint(mouse_x, mouse_y+-550):
                    hovered_button = i


            for i, button in enumerate(botonesGraficas):
                otrosBotones = pygame.Rect(botonXDos, botonYDos + (botonAltoDos + espacioBotonoesDos) * i, botonAnchoDos, botonAltoDos)
                if otrosBotones.collidepoint(mouse_x, mouse_y+-550):
                    hovered_button_g = i

        # Ver si se hizo click sobre un boton
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                
                if hovered_button is not None:
                    botones[hovered_button]["function"]()

                if hovered_button_g is not None:
                    botonesGraficas[hovered_button_g]["function"]()

                # Ver si se hizo click sobre un agente
                if 0 <= mouse_x < 3 * width / 4 and 0 <= mouse_y < height:
                    col = mouse_x // cell_width
                    row = mouse_y // cell_height
                    for agente in listaPersonas:
                        if agente.x == row and agente.y == col:
                            dibujarInfoAgente(agente, panel_surface)

    # Dibujar las superficies en la pantalla principal
    screen.fill(white)
    screen.blit(cuadricula, (0, 0))
    screen.blit(panel_surface, ((3 * width / 4) - 25, 0))
    screen.blit(panelAuxiliar, (0, (height - height / 4) - 125))

    # Dibujar los botones en el panel auxiliar
    for i, button in enumerate(botones):
        button_rect = pygame.Rect(botonX, botonY + (botonAlto + espacioBotonoes) * i, botonAncho, botonAlto)
        if i == hovered_button:
            pygame.draw.rect(panelAuxiliar, (105, 161, 111), button_rect) 
        else:
            pygame.draw.rect(panelAuxiliar, (55, 148, 65), button_rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(button["text"], True, black)
        text_x = botonX + (botonAncho - text_surface.get_width()) // 2
        text_y = botonY + (botonAlto - text_surface.get_height()) // 2 + (botonAlto + espacioBotonoes) * i
        panelAuxiliar.blit(text_surface, (text_x, text_y))

    # Dibujar los botones en el panel auxiliar para el segundo conjunto de botones
    for i, button in enumerate(botonesGraficas):
        otrosBotones = pygame.Rect(botonXDos, botonYDos + (botonAltoDos + espacioBotonoesDos) * i, botonAnchoDos, botonAltoDos)
        if i == hovered_button_g:
            pygame.draw.rect(panelAuxiliar, (105, 161, 111), otrosBotones)
        else:
            pygame.draw.rect(panelAuxiliar, (55, 148, 65), otrosBotones)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(button["text"], True, black)
        text_x = botonXDos + (botonAnchoDos - text_surface.get_width()) // 2
        text_y = botonYDos + (botonAltoDos - text_surface.get_height()) // 2 + (botonAltoDos + espacioBotonoesDos) * i
        panelAuxiliar.blit(text_surface, (text_x, text_y))

    panelAuxiliar.blit(pais_a_text, (paisAx, paisY))
    panelAuxiliar.blit(pais_b_text, (paisBx, paisY))

    # Dibujar la cuadrícula en función del estado de las celdas
    for fila in range(filas):
        for columna in range(columnas):
            cell_x = columna * cell_width
            cell_y = fila * cell_height
            pygame.draw.rect(cuadricula, cuadriculaEstado[fila][columna], (cell_x, cell_y, cell_width, cell_height), 0)
            pygame.draw.rect(cuadricula, black, (cell_x, cell_y, cell_width, cell_height), 1)

    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
