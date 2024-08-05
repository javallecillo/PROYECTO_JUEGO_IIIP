import os
import pygame
import csv
import constantes
from personaje import Personaje
from personaje import Enemigos
from arma import Arma
from textos import Texto_de_danio
from items import Item
from mundo import Mundo

#Funciones
# escalar imagen
def escalar_imagen(imagen, escala):
    w = imagen.get_width()
    h = imagen.get_height()
    nueva_imagen = pygame.transform.scale(imagen, (w*escala, h*escala))
    return nueva_imagen

# funcion contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#funcion listar nombres de elementos
def nombres_carpetas(directorio):
    return os.listdir(directorio)

def dibujar_texto(texto, fuente, color, x, y):
    imagen_texto = fuente.render(texto, True, color)
    ventana.blit(imagen_texto, (x, y))


def vida_jugador():
    for i in range(3):
        energia_actual = jugador.energia - (i * 100)
        if energia_actual >= 76:
            ventana.blit(corazon_100, (10 + i * 40, 10))
        elif energia_actual >= 51:
            ventana.blit(corazon_75, (10 + i * 40, 10))
        elif energia_actual >= 26:
            ventana.blit(corazon_50, (10 + i * 40, 10))
        elif energia_actual >= 1:
            ventana.blit(corazon_25, (10 + i * 40, 10))
        else:
            ventana.blit(corazon_0, (10 + i * 40, 10))

def dibujar_malla():
    for x in range(28):
        pygame.draw.line(ventana, constantes.COLOR_TEXTO, (x*constantes.ESCALA_TILE, 0), (x*constantes.ESCALA_TILE, constantes.ALTO_VENTANA))
        pygame.draw.line(ventana, constantes.COLOR_TEXTO, (0, x*constantes.ESCALA_TILE), (constantes.ANCHO_VENTANA, x*constantes.ESCALA_TILE))

# Función para cargar datos de un archivo CSV
def cargar_datos_csv(ruta_archivo):
    data = []
    with open(ruta_archivo, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for fila in reader:
            data.append([int(columna) for columna in fila])
    return data

# Inicializamos la libreria
pygame.init()

# ventana del juego
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

# Nombre de la ventana
pygame.display.set_caption("Juego Progra. Avanzada")

# posicion de la pantalla
posicion_pantalla = [0, 0]

# nivel
nivel = 1

# Inicializar fuente
fuente = pygame.font.Font("assets//fonts//Super_Mario_Bros_NES.ttf", constantes.ESCALA_TEXTO_DANIO)
fuente_llave = pygame.font.Font("assets//fonts//Super_Mario_Bros_NES.ttf", constantes.ESCALA_TEXTO_LLAVE)

#importar imagenes

# Vida del personaje
corazon_0 = pygame.image.load("assets//images//items//vida//vida_0.png").convert_alpha()
corazon_25 = pygame.image.load("assets//images//items//vida//vida_25.png").convert_alpha()
corazon_50 = pygame.image.load("assets//images//items//vida//vida_50.png").convert_alpha()
corazon_75 = pygame.image.load("assets//images//items//vida//vida_75.png").convert_alpha()
corazon_100 = pygame.image.load("assets//images//items//vida//vida_100.png").convert_alpha()

# Escalar imagenes de corazones
corazon_0 = escalar_imagen(corazon_0, constantes.ESCALA_CORAZON)
corazon_25 = escalar_imagen(corazon_25, constantes.ESCALA_CORAZON)
corazon_50 = escalar_imagen(corazon_50, constantes.ESCALA_CORAZON)
corazon_75 = escalar_imagen(corazon_75, constantes.ESCALA_CORAZON)
corazon_100 = escalar_imagen(corazon_100, constantes.ESCALA_CORAZON)

# Personaje
animaciones = []
for i in range (7):
    img = pygame.image.load(f"assets//images//character//jugador//caminar//caminar_{i}.png").convert_alpha()
    img = escalar_imagen(img, constantes.ESCALA_PERSONAJE)
    animaciones.append(img)

# Enemigos
directorio_enemigos = "assets//images//character//enemigos"
tipo_enemigos = nombres_carpetas(directorio_enemigos)
animaciones_enemigos = []
for enemigo in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets//images//character//enemigos//{enemigo}//caminar"
    num_animaciones = contar_elementos(ruta_temp)

    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"assets//images//character//enemigos//{enemigo}//caminar//caminar_{i}.png").convert_alpha()
        img_enemigo = escalar_imagen(img_enemigo, constantes.ESCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    
    animaciones_enemigos.append(lista_temp)
    lista_enemigos = []

# Imagenes de tiles del mapa
lista_tiles = []
for x in range(constantes.NUM_TILES_N1):
    tile_imagen = pygame.image.load(f"assets//images//tiles//nivel_1//tileset_{x+1}.png").convert_alpha()
    tile_imagen = pygame.transform.scale(tile_imagen, (constantes.ESCALA_TILE, constantes.ESCALA_TILE))
    lista_tiles.append(tile_imagen)

# Arma
imagen_pistola = pygame.image.load(f"assets//images//armas//arma.png").convert_alpha()
imagen_pistola = escalar_imagen(imagen_pistola, constantes.ESCALA_ARMA)

# Balas
imagen_balas = pygame.image.load(f"assets//images//armas//bala.png").convert_alpha()
imagen_balas = escalar_imagen(imagen_balas, constantes.ESCALA_ARMA)

# Items
imagen_botiquin = pygame.image.load("assets//images//items//salud//botiquin.png").convert_alpha()
imagen_botiquin = escalar_imagen(imagen_botiquin, constantes.ESCALA_BOTIQUIN)

imagenes_llave = []
ruta_img_llave = "assets//images//items//llave"
num_img_llave = contar_elementos(ruta_img_llave)

for i in range(num_img_llave):
    img_llave = pygame.image.load(f"{ruta_img_llave}//llave_{i}.png").convert_alpha()
    img_llave = escalar_imagen(img_llave, constantes.ESCALA_LLAVE)
    imagenes_llave.append(img_llave)

item_imagenes = [imagenes_llave, [imagen_botiquin]]

# Crear un objeto de la clase personaje
jugador = Personaje(150,150, animaciones, constantes.VIDA_PERSONAJE)

# Crear un enemigo de la clase personaje
# demon = Enemigos(1300,300, animaciones_enemigos[0], constantes.VIDA_DEMON)
# ghoul = Enemigos(1300,400, animaciones_enemigos[1], constantes.VIDA_GHOUL)
# mole = Enemigos(1300,500, animaciones_enemigos[2], constantes.VIDA_MOLE)
# Para agregar mas enemigos solo se debe agregar mas objetos de la clase enemigos


# Crear un arma de la clase arma
pistola = Arma(imagen_pistola, imagen_balas)

# Crear grupo de sprites
grupo_balas = pygame.sprite.Group()
grupo_texto_danio = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()



# Crear items
# item_llave = Item(2600, 1700, 0, imagenes_llave)
# item_botiquin = Item(150, 50, 1, [imagen_botiquin])

# grupo_items.add(item_llave)
# grupo_items.add(item_botiquin)


#definir variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

# controlar el movimiento del jugador
reloj = pygame.time.Clock()


# Cargar datos del mapa
data_fondo = cargar_datos_csv("niveles//nivel_1//nivel_1.csv")

# Crear data_mapa combinando piso y paredes
data_mapa = []

filas = [7] * constantes.COLUMNAS
for filas in range(constantes.FILAS):
    filas = [7] * constantes.COLUMNAS
    data_mapa.append(filas)

# Cargar datos de los elementos del mapa
with open("niveles//nivel_1//nivel_1.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            data_mapa[x][y] = int(columna)


# Crear un objeto de la clase mundo
mapa = Mundo()
mapa.procesar_mapa(data_mapa, lista_tiles, item_imagenes, animaciones_enemigos)

# añadir items desde los datos del mapa
for item in mapa.lista_item:
    grupo_items.add(item)

# añadir enemigos desde los datos del mapa
for enemigos in mapa.lista_enemigo:
    lista_enemigos.append(enemigos)

# Cargar imagen del puntero
puntero_img = pygame.image.load("assets//images//armas//mira.png").convert_alpha()
puntero_img = pygame.transform.scale(puntero_img, constantes.ESCALA_PUNTERO)

# Ocultar el puntero predeterminado
pygame.mouse.set_visible(False)

# ciclo para mantener ventana
run = True
while run:

    # velocidad de 60 fps
    reloj.tick(constantes.FPS)
    
    ventana.fill(constantes.COLOR_BG)

    # dibujar malla
    # dibujar_malla()

    # calcular movimiento del jugador
    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = constantes.VELOCIDAD_PERSONAJE

    if mover_izquierda == True:
        delta_x = -constantes.VELOCIDAD_PERSONAJE

    if mover_arriba == True:
        delta_y = -constantes.VELOCIDAD_PERSONAJE

    if mover_abajo == True:
        delta_y = constantes.VELOCIDAD_PERSONAJE

    # mover al jugar
    posicion_pantalla = jugador.movimiento(delta_x, delta_y, mapa.tile_paredes)
    #print(posicion_pantalla)

    # actualizar el mapa
    mapa.actualizar(posicion_pantalla)

    # actualizar al jugador
    jugador.actualizar()

    # actualizar al arma
    bala = pistola.actualizar(jugador)
    if bala:
        grupo_balas.add(bala)
    
    # actualizar balas
    for bala in grupo_balas:
        danio, posicion_danio = bala.actualizar(lista_enemigos, mapa.tile_paredes)

        if danio:
            texto_danio = Texto_de_danio(posicion_danio.centerx, posicion_danio.centery, f"-{danio}", fuente, constantes.COLOR_TEXTO_DANIO)
            grupo_texto_danio.add(texto_danio)


    # actualizar texto de daño
    grupo_texto_danio.update(posicion_pantalla)

    # actualizar items
    grupo_items.update(posicion_pantalla, jugador)

    # dibujar mapa
    mapa.dibujar(ventana)

    # dibujar items
    grupo_items.draw(ventana)
        
    # dibujar al jugador
    jugador.dibujar(ventana)

    # dibujar al enemigo
    for enemigo in lista_enemigos:
        if enemigo.energia > 0:
            enemigo.actualizar(jugador, posicion_pantalla, mapa.tile_paredes)
            enemigo.dibujar(ventana)
        else:
            lista_enemigos.remove(enemigo)

    # dibujar al arma
    pistola.dibujar(ventana)

    # dibujar balas
    for bala in grupo_balas:
        bala.dibujar(ventana)

    # dibujar vida del jugador
    vida_jugador()
    dibujar_texto(f"Llave {jugador.llave}/1", fuente_llave, constantes.COLOR_TEXTO, 1200, 10)
    dibujar_texto(f"Nivel {nivel}", fuente_llave, constantes.COLOR_TEXTO, 680, 10)
    
    # dibujar texto de daño
    grupo_texto_danio.draw(ventana)



    # for para ver los eventos del jquery
    for event in pygame.event.get():

        #evento para cerra la ventana
        if event.type == pygame.QUIT:
            run = False

        # evento para mover el personaje
        if event.type == pygame.KEYDOWN:
            if event.key ==  pygame.K_a or event.key == pygame.K_LEFT:
                mover_izquierda = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                mover_derecha = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                mover_arriba = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                mover_abajo = True

        # evento para dejar de mover el personaje
        if event.type == pygame.KEYUP:
            if event.key ==  pygame.K_a or event.key == pygame.K_LEFT:
                mover_izquierda = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                mover_derecha = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                mover_arriba = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                mover_abajo = False

    # Obtener la posición del cursor
    pos_cursor = pygame.mouse.get_pos()

    # Dibujar la imagen del puntero en la posición del cursor
    ventana.blit(puntero_img, pos_cursor)

    pygame.display.update()

pygame.quit()