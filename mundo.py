import constantes
from items import Item
from personaje import Enemigos

paredes = [6,7,8,9,10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 59]

class Mundo():
    def __init__(self):
        self.tiles_mapa = []
        self.tile_paredes = []
        self.tile_salida = None
        self.lista_item = []
        self.lista_enemigo = []

    def procesar_mapa(self, data, lista_tiles, item_imagenes, animaciones_enemigos, nivel):
        self.largo_de_nivel = len(data[0])

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                imagen = lista_tiles[tile]
                imagen_rect = imagen.get_rect()
                imagen_x = x * constantes.ESCALA_TILE
                imagen_y = y * constantes.ESCALA_TILE
                imagen_rect.center = (imagen_x, imagen_y)
                tile_data = [imagen, imagen_rect, imagen_x, imagen_y]
                
                #agregar tiles a la lista de paredes
                if tile in paredes:
                    self.tile_paredes.append(tile_data)
                elif tile == 5:
                    self.tile_salida = tile_data
                #LLAVE
                elif tile == 0:
                    llave = Item(imagen_x, imagen_y, 0, item_imagenes[0])
                    self.lista_item.append(llave)

                    if nivel == 1:
                        tile_data[0] = lista_tiles[28]
                    elif nivel == 2:
                        tile_data[0] = lista_tiles[37]
                    elif nivel == 3:
                        tile_data[0] = lista_tiles[58]
                        
                # BOTIQUIN
                elif tile == 1:
                    botiquin = Item(imagen_x, imagen_y, 1, item_imagenes[1])
                    self.lista_item.append(botiquin)

                    if nivel == 1:
                        tile_data[0] = lista_tiles[28]
                    elif nivel == 2:
                        tile_data[0] = lista_tiles[37]
                    elif nivel == 3:
                        tile_data[0] = lista_tiles[58]
                        
                #agregar enemigos
                # # MOLE
                elif tile == 4:
                    mole = Enemigos(imagen_x, imagen_y, animaciones_enemigos[2], constantes.VIDA_MOLE)
                    self.lista_enemigo.append(mole)

                    if nivel == 1:
                        tile_data[0] = lista_tiles[28]
                    elif nivel == 2:
                        tile_data[0] = lista_tiles[37]
                    elif nivel == 3:
                        tile_data[0] = lista_tiles[58]
                        
                # GHOUL
                elif tile == 3:
                    ghoul = Enemigos(imagen_x, imagen_y, animaciones_enemigos[1], constantes.VIDA_GHOUL)
                    self.lista_enemigo.append(ghoul)

                    if nivel == 1:
                        tile_data[0] = lista_tiles[28]
                    elif nivel == 2:
                        tile_data[0] = lista_tiles[37]
                    elif nivel == 3:
                        tile_data[0] = lista_tiles[58]
                        
                # DEMON
                elif tile == 2:
                    demon = Enemigos(imagen_x, imagen_y, animaciones_enemigos[0], constantes.VIDA_DEMON)
                    self.lista_enemigo.append(demon)


                    if nivel == 1:
                        tile_data[0] = lista_tiles[28]
                    elif nivel == 2:
                        tile_data[0] = lista_tiles[37]
                    elif nivel == 3:
                        tile_data[0] = lista_tiles[58]
                        

                
                


                self.tiles_mapa.append(tile_data)

    def actualizar(self, posicion_pantalla):
        for tile in self.tiles_mapa:
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])

    def dibujar(self, ventana):
        for tile in self.tiles_mapa:
            ventana.blit(tile[0], tile[1])