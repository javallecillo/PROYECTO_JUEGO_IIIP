import os
import pygame
import csv
import sys
import constantes
from personaje import Personaje
from arma import Arma
from textos import Texto_de_danio
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
    for i in range(5):
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

def pantalla_inicio():
    ventana.fill(constantes.COLOR_INICIO)  # Color

    text_rect = texto_inicio.get_rect(center=(constantes.ANCHO_VENTANA/2, constantes.ALTO_VENTANA/4))
    ventana.blit(texto_inicio, text_rect)

    pygame.draw.rect(ventana, constantes.COLOR_BTN_INICIO, btn_jugar)
    pygame.draw.rect(ventana, constantes.COLOR_BTN_INICIO, btn_salir)

    ventana.blit(texto_btn_jugar, (btn_jugar.x + 90, btn_jugar.y + 20))
    ventana.blit(texto_btn_salir, (btn_salir.x + 90, btn_salir.y + 20))

    pygame.display.update()


# Función para cargar datos de un archivo CSV
def cargar_datos_csv(ruta_archivo):
    data = []
    with open(ruta_archivo, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for fila in reader:
            data.append([int(columna) for columna in fila])
    return data

# resetear el nivel
def resetear_nivel():
    grupo_texto_danio.empty()
    grupo_balas.empty()
    grupo_items.empty()
    lista_enemigos.clear()
    

    # crear lista de tile vacias
    data_mapa = []
    for filas in range (constantes.FILAS):
        filas = [2] * constantes.COLUMNAS
        data_mapa.append(filas)

    return data_mapa

# Inicializamos la libreria
pygame.init()
pygame.mixer.init()

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
fuente_niveles = pygame.font.Font("assets//fonts//Super_Mario_Bros_NES.ttf", constantes.ESCALA_TEXTO_GO)
fuente_game_over = pygame.font.Font("assets//fonts//Super_Mario_Bros_NES.ttf", constantes.ESCALA_TEXTO_GO)
fuente_reinicio = pygame.font.Font("assets//fonts//Super_Mario_Bros_NES.ttf", constantes.ESCALA_TEXTO_BTN)
fuente_llave = pygame.font.Font("assets//fonts//Super_Mario_Bros_NES.ttf", constantes.ESCALA_TEXTO_LLAVE)

texto_btn_reinicio = fuente_reinicio.render("REINICIAR", True, constantes.COLOR_BG)
texto_game_over = fuente_game_over.render("GAME OVER", True, constantes.COLOR_TEXTO)
texto_inicio = fuente_game_over.render("ESCAPE ROOM", True, constantes.COLOR_TEXTO)
texto_btn_jugar = fuente_reinicio.render("JUGAR", True, constantes.COLOR_TEXTO)
texto_btn_salir = fuente_reinicio.render("SALIR", True, constantes.COLOR_TEXTO)

#BOTON REINICIO
btn_reinicio = pygame.Rect(constantes.ANCHO_VENTANA/2 - 150, constantes.ALTO_VENTANA/2.5 + 150, 300, 60)
btn_jugar = pygame.Rect(constantes.ANCHO_VENTANA/2 - 150, constantes.ALTO_VENTANA/2 - 50, 300, 60)
btn_salir = pygame.Rect(constantes.ANCHO_VENTANA/2 - 150, constantes.ALTO_VENTANA/2 + 100, 300, 60)


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
    tile_imagen = pygame.image.load(f"assets//images//tiles//tileset_{x}.png").convert_alpha()
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
data_fondo = cargar_datos_csv("niveles//nivel_1.csv")

# Crear data_mapa combinando piso y paredes
data_mapa = []

filas = [7] * constantes.COLUMNAS
for filas in range(constantes.FILAS):
    filas = [7] * constantes.COLUMNAS
    data_mapa.append(filas)

# Cargar datos de los elementos del mapa
with open("niveles//nivel_1.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            data_mapa[x][y] = int(columna)


# Crear un objeto de la clase mundo
mapa = Mundo()
mapa.procesar_mapa(data_mapa, lista_tiles, item_imagenes, animaciones_enemigos, nivel)

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
pygame.mouse.set_visible(True)

mostrar_inicio = True

inicio_musica = pygame.mixer.music.load("assets//sounds//nivel_1.mp3")
pygame.mixer.music.play(-1)

sonido_disparo = pygame.mixer.Sound("assets//sounds//bala.mp3")

# ciclo para mantener ventana
run = True
while run:
  
    if mostrar_inicio:

        pantalla_inicio()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                    # Ocultar el puntero predeterminado
                    pygame.mouse.set_visible(False)
                if btn_salir.collidepoint(event.pos):
                    run = False
    else:

        # velocidad de 60 fps
        reloj.tick(constantes.FPS)
        
        ventana.fill(constantes.COLOR_BG)

        if jugador.vivo == True:
            

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
            posicion_pantalla, nivel_completo = jugador.movimiento(delta_x, delta_y, mapa.tile_paredes, mapa.tile_salida)
            #print(posicion_pantalla)

            # actualizar el mapa
            mapa.actualizar(posicion_pantalla)

            # actualizar al jugador
            jugador.actualizar()

            for enemigo in lista_enemigos:
                enemigo.actualizar(jugador, posicion_pantalla, mapa.tile_paredes)

            # actualizar al arma
            bala = pistola.actualizar(jugador)
            if bala:
                grupo_balas.add(bala)
                sonido_disparo.play()
            
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
                #enemigo.actualizar(jugador, posicion_pantalla, mapa.tile_paredes)
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
        dibujar_texto(f"Nivel {nivel}", fuente_llave, constantes.COLOR_TEXTO, (constantes.ANCHO_VENTANA/2) , 10)
        
        # dibujar texto de daño
        grupo_texto_danio.draw(ventana)


        # verificar si el nivel esta completado
        if nivel_completo == True and jugador.llave == 1 and jugador.vivo == True:

            if nivel < constantes.MAX_NIVELES:
                # Crear una superficie semi-transparente
                overlay = pygame.Surface((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
                overlay.set_alpha(175)  # Ajustar la transparencia (0-255)
                overlay.fill((0, 0, 0))  # Color negro

                nivel += 1
                data_mapa = resetear_nivel()
                jugador.llave = 0

                # Cargar datos de los elementos del mapa
                with open(f"niveles//nivel_{nivel}.csv", newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    for x, fila in enumerate(reader):
                        for y, columna in enumerate(fila):
                            data_mapa[x][y] = int(columna)

                # Crear un objeto de la clase mundo
                mapa = Mundo()
                mapa.procesar_mapa(data_mapa, lista_tiles, item_imagenes, animaciones_enemigos, nivel)

                jugador.actualizar_coordenadas(constantes.COORDENADAS_INICIALES[str(nivel)])

                # añadir items desde los datos del mapa
                for item in mapa.lista_item:
                    grupo_items.add(item)

                # añadir enemigos desde los datos del mapa
                for enemigos in mapa.lista_enemigo:
                    lista_enemigos.append(enemigos)

                # Dibujar el nuevo nivel
                ventana.fill(constantes.COLOR_BG)
                mapa.dibujar(ventana)
                jugador.dibujar(ventana)

                ventana.fill((0, 0, 0))

                # Superponer el texto del siguiente nivel
                texto_niveles = fuente_niveles.render(f"NIVEL {nivel}", True, constantes.COLOR_TEXTO)
                text_rect_2 = texto_niveles.get_rect(center=(constantes.ANCHO_VENTANA/2, constantes.ALTO_VENTANA/2.5))
                ventana.blit(texto_niveles, text_rect_2)


                # Actualizar la pantalla para mostrar el mensaje
                pygame.display.update()

                pygame.time.wait(4000)


        if jugador.vivo == False:
            ventana.fill((0, 0, 0))  # Color negro
            text_rect = texto_game_over.get_rect(center=(constantes.ANCHO_VENTANA/2, constantes.ALTO_VENTANA/2.5))
            
            # Ventana GAME OVER
            ventana.blit(texto_game_over, text_rect)

            pygame.draw.rect(ventana, constantes.COLOR_TEXTO, btn_reinicio)
            ventana.blit(texto_btn_reinicio, (btn_reinicio.x + 60, btn_reinicio.y + 20))


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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_reinicio.collidepoint(event.pos) and jugador.vivo == False:
                    jugador.vivo = True
                    jugador.energia = constantes.VIDA_PERSONAJE
                    jugador.llave = 0
                    nivel = 1
                    data_mapa = resetear_nivel()

                    # Cargar datos de los elementos del mapa
                    with open(f"niveles//nivel_{nivel}.csv", newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=';')
                        for x, fila in enumerate(reader):
                            for y, columna in enumerate(fila):
                                data_mapa[x][y] = int(columna)

                    mapa = Mundo()
                    mapa.procesar_mapa(data_mapa, lista_tiles, item_imagenes, animaciones_enemigos, nivel)

                    jugador.actualizar_coordenadas(constantes.COORDENADAS_INICIALES[str(nivel)])

                    # añadir items desde los datos del mapa
                    for item in mapa.lista_item:
                        grupo_items.add(item)

                    # añadir enemigos desde los datos del mapa
                    for enemigos in mapa.lista_enemigo:
                        lista_enemigos.append(enemigos)

                    # Dibujar el nuevo nivel
                    ventana.fill(constantes.COLOR_BG)
                    mapa.dibujar(ventana)
                    jugador.dibujar(ventana)

                    ventana.fill((0, 0, 0))

                    # Superponer el texto del siguiente nivel
                    texto_niveles = fuente_niveles.render(f"NIVEL {nivel}", True, constantes.COLOR_TEXTO)
                    text_rect_2 = texto_niveles.get_rect(center=(constantes.ANCHO_VENTANA/2, constantes.ALTO_VENTANA/2.5))
                    ventana.blit(texto_niveles, text_rect_2)


                    # Actualizar la pantalla para mostrar el mensaje
                    pygame.display.update()

                    pygame.time.wait(3000)

        # Obtener la posición del cursor
        pos_cursor = pygame.mouse.get_pos()

        # Dibujar la imagen del puntero en la posición del cursor
        ventana.blit(puntero_img, pos_cursor)

        pygame.display.update()

        

pygame.quit()