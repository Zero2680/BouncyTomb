from pygame import*
from pygame.math import Vector2
from random import*
from threading import*
from button import Button
from sys import*
from SaveLoadManager import SaveLoadSystem
init()
screen = display.set_mode((1280, 720), FULLSCREEN) 
display.set_caption('BOMBY TOMB')
encendido = True
finish = False
background = transform.scale(image.load("bouncy_images/menu.png"), (1280, 720))
flecha_right = transform.scale(image.load("bouncy_images/flecha2.png"), (100, 100))
flecha_left = transform.scale(image.load("bouncy_images/flecha1.png"), (100, 100))
win = transform.scale(image.load("bouncy_images/win.png"), (500, 500))
main_font = font.SysFont('cambria', 50)
saveloadmanager = SaveLoadSystem(".save", "save_data")
surface = Surface((1280, 720), SRCALPHA)

def play(): #PLAY SCREEN
	display.set_caption('Play')
	class Objeto(sprite.Sprite):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			sprite.Sprite.__init__(self)
			self.x = x
			self.y = y
			self.ancho = ancho
			self.largo = largo
			self.direccionx = direccionx
			self.direcciony = direcciony
			self.color = color
			self.vidas = vidas
			self.puntuacion = puntuacion

		def DibujarObjeto(self):
			draw.rect(screen, self.color, (self.x,self.y,self.ancho,self.largo))

	class Personaje(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx , direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)
			
		def Movimiento(self):
			x = self.x
			y = self.y
			if self.vidas == 3:
				self.ancho = 120
				max_x = 1145
			elif self.vidas == 2:
				self.ancho = 90
				max_x = 1175
			elif self.vidas == 1:
				self.ancho = 60
				max_x = 1205
			elif self.vidas == 0:
				max_x = 0
			keys = key.get_pressed()
			if keys[K_RIGHT]==1:
				x1 = x
				x = x + 3
				self.x = x
				if x > max_x:
					self.x = x1
			if keys[K_LEFT]==1:
				x1 = x
				x = x - 3
				self.x = x
				if x < 15:
					self.x = x1
			if final_boss == True:
				if keys[K_UP]==1:
					y1 = y
					y = y - 3
					self.y = y
					if y < 0:
						self.y = y1
				if keys[K_DOWN]==1:
					y1 = y
					y = y + 3
					self.y = y
					if y > 720:
						self.y = y1
			self.DibujarObjeto()
		
		def check_colisiones(sprite1, sprite2):
			xsprite1 = sprite1.x
			ysprite1 = sprite1.y
			anchosprite1 = sprite1.ancho
			largosprite1 = sprite1.largo
			xsprite2 = sprite2.x
			ysprite2 = sprite2.y
			anchosprite2 = sprite2.ancho
			largosprite2 = sprite2.largo
			if (ysprite1 + largosprite1) > ysprite2 and ysprite1 < (ysprite2 + largosprite2) and (xsprite1 + anchosprite1) > xsprite2 and xsprite1 < (xsprite2 + anchosprite2):
				return True

	class Bola(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)
		
		def Movimiento(self):
			#TOCA EL BORDE
			if self.x <= 15:
				ball_sound.play()
				self.direccionx = 1
			elif self.x >= 1265:
				ball_sound.play()
				self.direccionx = -1
			elif self.y <= 0:
				ball_sound.play()
				self.direcciony = 1
			#MOVIMIENTO
			if self.direccionx == 1:
				self.x = self.x + 2
				if self.direcciony == -1:
					self.y = self.y - 2
				else:
					self.y = self.y + 2
			elif self.direccionx == -1:
				self.x = self.x - 2
				if self.direcciony == -1:
					self.y = self.y - 2
				else:
					self.y = self.y + 2
			self.DibujarObjeto()

		def Golpear_personaje(self, plataforma):
			if self.vidas != 1:
				self.vidas += 1
			if self.vidas == 30:
				self.vidas = 1
			if Personaje.check_colisiones(self, plataforma) == True and self.vidas == 1:
				ball_sound.play()
				self.direcciony = -self.direcciony
				self.vidas += 1

	class Bloque(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)
			self.bomba = Bomba(self.x+20, self.y+50, 10, 10, 1, 1, (8, 2, 13), 0, 0)
			self.rayo = Rayo(self.x+20, self.y+50-50000, 50, 700, 1, 1, (255,255,0), 0, 0)
			self.boomerang = Boomerang(self.x+20, self.y+50, 10, 10, 1, 1, (8, 2, 13), 0, 0)
			self.pinchos = Pinchos(0, 680, 150, 100, 1, 1, (255,0,0), 1, 0)
			self.caparazon = Caparazon(self.x-50, self.y, 50, 50, 1, 1, (255,0,0), 0, 0)
			self.jumper = Jumper(0, 680, 150, 100, 1, 1, (255,0,0), 1, 0)

		def Rebotar(self, bola, plataforma):
			global numero_bloques, contador_rebotes, dibujo
			if dibujo == 0:
				self.DibujarObjeto()
			if Personaje.check_colisiones(self, bola) == True and contador_rebotes == 0:
				if bola.y == self.y + self.largo or bola.y - bola.largo == self.y or bola.y == self.y + self.largo - 1 or bola.y - bola.largo - 1 == self.y or bola.y == self.y + self.largo - 2 or bola.y - bola.largo - 2 == self.y:
					bola.direcciony = -bola.direcciony
				if bola.x == self.x + self.ancho or bola.x + bola.ancho == self.x or bola.x == self.x + self.ancho - 1 or bola.x + bola.ancho - 1 == self.x or bola.x == self.x + self.ancho - 2 or bola.x + bola.ancho - 2 == self.x:
					bola.direccionx = -bola.direccionx
				self.vidas -= 1
				plataforma.puntuacion += self.puntuacion
				if self.y <= 150:
					numero_bloques -= 1
				ball_sound.play()
				self.y = self.y + 50000
				self.bomba.y = self.bomba.y + 50000
				self.boomerang.y = self.bomba.y + 50000
				contador_rebotes += 1
			if contador_rebotes != 0:
				contador_rebotes += 1
				if contador_rebotes == 100:
					contador_rebotes = 0
			if Personaje.check_colisiones(self, plataforma) == True:
				plataforma.vidas -= 1
		
		def LanzarBomba(self, plataforma):
			self.bomba.Movimiento(self, plataforma)
		
		def LanzarRayo(self, plataforma):
			self.rayo.Movimiento(plataforma)
		
		def LanzarBoomerang(self, plataforma, invertir):
			y = self.y
			self.boomerang.Movimiento(plataforma, invertir, y)
		
		def LanzarPinchos(self, plataforma, bola):
			self.pinchos.Pinchar(plataforma, bola)
		
		def LanzarCaparazon(self, plataforma):
			self.caparazon.Movimiento(self, plataforma)
		
		def LanzarJumper(self, plataforma, bola):
			self.jumper.Jump(plataforma, bola)

	class Bomba(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)
		
		def Movimiento(self,bloque,plataforma):
			if self.y > 0 and self.y < 720:
				self.y = self.y + (self.direcciony*2)
				if Personaje.check_colisiones(self, plataforma) == True:
					hueso_sound.play()
					plataforma.vidas -= 1
					self.y = bloque.y + 50
			else:
				self.y = bloque.y + 50
			self.DibujarObjeto()
		
	class Rayo(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)
		
		def Movimiento(self,plataforma):
			self.vidas += 1
			if self.vidas >= 800 and self.vidas <= 1000:
				self.color = (255,255,0)
				if Personaje.check_colisiones(self, plataforma) == True:
					plataforma.vidas -= 1
					self.vidas = 0
				self.DibujarObjeto()
			if self.vidas >= 1200:
				self.vidas = 0

	class Boomerang(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)
		
		def Movimiento(self, plataforma, invertir, y):
			global hit
			self.y = self.y + (self.direcciony*2)
			if Personaje.check_colisiones(self, plataforma) == True and self.puntuacion == 0:
				fuego_sound.play()
				plataforma.vidas -= 1 
				self.puntuacion = 1
			if invertir == False:
				if self.y <= y:
					self.direcciony = -self.direcciony
				elif self.y >= 700:
					self.vidas += 1
					self.direcciony = 0
					if self.vidas >= 300 and self.y == 700:
						self.direcciony = -1
						self.vidas = 0
						self.puntuacion = 0
					elif self.vidas >= 300 and self.y == 30:
						self.direcciony = 1
						self.vidas = 0
						self.puntuacion = 0
			else:
				if self.y >= y:
					self.direcciony = -self.direcciony
				elif self.y <= 30:
					self.vidas += 1
					self.direcciony = 0
					if self.vidas >= 300 and self.y == 700:
						self.direcciony = -1
						self.vidas = 0
						self.puntuacion = 0
					elif self.vidas >= 300 and self.y == 30:
						self.direcciony = 1
						self.vidas = 0
						self.puntuacion = 0
			self.DibujarObjeto()

	class Pinchos(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)
		
		def Pinchar(self, plataforma, bola):
			global numero_pinchos
			self.puntuacion += 1
			if self.puntuacion >= 600 and self.puntuacion <= 1000:
				self.color = (8, 2, 13)
				self.DibujarObjeto()
			if self.puntuacion >= 1200 and self.vidas == 1:
				self.color = (8, 2, 13)
				if Personaje.check_colisiones(self, bola) == True and contador_rebotes == 0:
					if bola.y == self.y + self.largo - 1 or bola.y - bola.largo - 1 == self.y:
						bola.direcciony = -bola.direcciony
					if bola.x == self.x + self.ancho - 1 or bola.x + bola.ancho - 1 == self.x:
						bola.direccionx = -bola.direccionx
				if Personaje.check_colisiones(self, plataforma) == True:
					plataforma.vidas -= 1
					self.vidas = 0
				self.DibujarObjeto()
			if self.puntuacion >= 1400:
				numero_pinchos = 1
				self.vidas = 1
				self.puntuacion = 0

	class Caparazon(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)

		def Movimiento(self,bloque,plataforma):
			if self.x > -50 and self.x < 1300:
				self.x = self.x - self.direccionx
				if Personaje.check_colisiones(self, plataforma) == True:
					plataforma.vidas -= 1
					self.x = bloque.x - 50
			else:
				self.x = bloque.x - 50
			self.DibujarObjeto()

	class Jumper(Objeto):
		def __init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion):
			Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, color, vidas, puntuacion)
		
		def Jump(self, plataforma, bola):
			global numero_pinchos
			self.puntuacion += 1
			if self.puntuacion >= 600 and self.puntuacion <= 1000:
				self.color = (8, 2, 13)
				self.DibujarObjeto()
			if self.puntuacion >= 1200 and self.vidas == 1:
				self.ancho = 50
				self.largo = 720
				self.y = 0
				self.color = (8, 2, 13)
				if Personaje.check_colisiones(self, bola) == True and contador_rebotes == 0:
					if bola.y == self.y + self.largo - 1 or bola.y - bola.largo - 1 == self.y:
						bola.direcciony = -bola.direcciony
					if bola.x == self.x + self.ancho - 1 or bola.x + bola.ancho - 1 == self.x:
						bola.direccionx = -bola.direccionx
				if Personaje.check_colisiones(self, plataforma) == True:
					plataforma.vidas -= 1
					self.vidas = 0
				self.DibujarObjeto()
			if self.puntuacion >= 1600:
				self.ancho = 150
				self.largo = 100
				self.y = 680
				numero_pinchos = 1
				self.vidas = 1
				self.puntuacion = 0

	def PantallaChica(plataforma, bola):
		bloque1_4 = Bloque(0,100,300,800, 1, 1, (8, 2, 13), 100000, 0)
		bloque2_4 = Bloque(900,100,300,800, 1, 1, (8, 2, 13), 100000, 0)
		bloque1_4.Rebotar(bola, plataforma)
		bloque2_4.Rebotar(bola, plataforma)

	def Gusanos(plataforma, bola, aleatorio1, aleatorio2):
		global numero_gusanos, gusano1_y, gusano2_y
		if bola.puntuacion >= 100:
			gusano1_y = -550
			gusano2_y = -550
		if bola.puntuacion >= 200:
			gusano1_y = -500
			gusano2_y = -500
		if bola.puntuacion >= 300:
			gusano1_y = -450
			gusano2_y = -450
		if bola.puntuacion >= 400:
			gusano1_y = -400
			gusano2_y = -400
		if bola.puntuacion >= 500:
			gusano1_y = -350
			gusano2_y = -350
		if bola.puntuacion >= 600:
			gusano1_y = -300
			gusano2_y = -300
		if bola.puntuacion >= 700:
			gusano1_y = -250
			gusano2_y = -250
		if bola.puntuacion >= 800:
			gusano1_y = -200
			gusano2_y = -200
		if bola.puntuacion >= 900:
			gusano1_y = -150
			gusano2_y = -150
		if bola.puntuacion >= 1000:
			gusano1_y = -100
			gusano2_y = -100
		if bola.puntuacion >= 1100:
			gusano1_y = -50
			gusano2_y = -50
		if bola.puntuacion >= 1200:
			gusano1_y = 0
			gusano2_y = 0
		if bola.puntuacion >= 1300:
			gusano1_y = 50
			gusano2_y = 50
		if bola.puntuacion >= 1400:
			gusano1_y = 100
			gusano2_y = 100
		if bola.puntuacion >= 1500:
			gusano1_y = 150
			gusano2_y = 150
		if bola.puntuacion >= 1600:
			gusano1_y = 150
			gusano2_y = 150
		if bola.puntuacion >= 1695:
			gusano1_y = -550
			gusano2_y = -550
		if numero_gusanos == 2:
			if aleatorio1 == 1 or aleatorio2 == 1:
				bloque1_1 = Bloque(25,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_1 = Bloque(25,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_1 = Bloque(25,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_1 = Bloque(25,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_1 = Bloque(25,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_1 = Bloque(25,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_1 = Bloque(25,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_1 = Bloque(25,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_1 = Bloque(25,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_1 = Bloque(25,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_1 = Bloque(25,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_1 = Bloque(25,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_1 = Bloque(25,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_1 = Bloque(25,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_1 = Bloque(25,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_1.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_1.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_1.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_1.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_1.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_1.Rebotar(bola, plataforma)
					bloque1_1.y += 50000
				if bola.puntuacion >= 800:
					bloque7_1.Rebotar(bola, plataforma)
					bloque2_1.y += 50000
				if bola.puntuacion >= 900:
					bloque8_1.Rebotar(bola, plataforma)
					bloque3_1.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_1.Rebotar(bola, plataforma)
					bloque4_1.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_1.Rebotar(bola, plataforma)
					bloque5_1.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_1.Rebotar(bola, plataforma)
					bloque6_1.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_1.Rebotar(bola, plataforma)
					bloque7_1.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_1.Rebotar(bola, plataforma)
					bloque8_1.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_1.Rebotar(bola, plataforma)
					bloque9_1.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_1.Rebotar(bola, plataforma)
					bloque10_1.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_1.y += 50000
					bloque12_1.y += 50000
					bloque13_1.y += 50000
					bloque14_1.y += 50000
					bloque15_1.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 2 or aleatorio2 == 2:
				bloque1_2 = Bloque(75,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_2 = Bloque(75,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_2 = Bloque(75,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_2 = Bloque(75,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_2 = Bloque(75,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_2 = Bloque(75,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_2 = Bloque(75,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_2 = Bloque(75,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_2 = Bloque(75,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_2 = Bloque(75,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_2 = Bloque(75,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_2 = Bloque(75,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_2 = Bloque(75,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_2 = Bloque(75,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_2 = Bloque(75,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_2.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_2.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_2.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_2.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_2.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_2.Rebotar(bola, plataforma)
					bloque1_2.y += 50000
				if bola.puntuacion >= 800:
					bloque7_2.Rebotar(bola, plataforma)
					bloque2_2.y += 50000
				if bola.puntuacion >= 900:
					bloque8_2.Rebotar(bola, plataforma)
					bloque3_2.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_2.Rebotar(bola, plataforma)
					bloque4_2.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_2.Rebotar(bola, plataforma)
					bloque5_2.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_2.Rebotar(bola, plataforma)
					bloque6_2.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_2.Rebotar(bola, plataforma)
					bloque7_2.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_2.Rebotar(bola, plataforma)
					bloque8_2.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_2.Rebotar(bola, plataforma)
					bloque9_2.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_2.Rebotar(bola, plataforma)
					bloque10_2.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_2.y += 50000
					bloque12_2.y += 50000
					bloque13_2.y += 50000
					bloque14_2.y += 50000
					bloque15_2.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 3 or aleatorio2 == 3:
				bloque1_3 = Bloque(125,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_3 = Bloque(125,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_3 = Bloque(125,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_3 = Bloque(125,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_3 = Bloque(125,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_3 = Bloque(125,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_3 = Bloque(125,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_3 = Bloque(125,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_3 = Bloque(125,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_3 = Bloque(125,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_3 = Bloque(125,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_3 = Bloque(125,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_3 = Bloque(125,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_3 = Bloque(125,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_3 = Bloque(125,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_3.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_3.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_3.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_3.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_3.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_3.Rebotar(bola, plataforma)
					bloque1_3.y += 50000
				if bola.puntuacion >= 800:
					bloque7_3.Rebotar(bola, plataforma)
					bloque2_3.y += 50000
				if bola.puntuacion >= 900:
					bloque8_3.Rebotar(bola, plataforma)
					bloque3_3.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_3.Rebotar(bola, plataforma)
					bloque4_3.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_3.Rebotar(bola, plataforma)
					bloque5_3.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_3.Rebotar(bola, plataforma)
					bloque6_3.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_3.Rebotar(bola, plataforma)
					bloque7_3.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_3.Rebotar(bola, plataforma)
					bloque8_3.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_3.Rebotar(bola, plataforma)
					bloque9_3.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_3.Rebotar(bola, plataforma)
					bloque10_3.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_3.y += 50000
					bloque12_3.y += 50000
					bloque13_3.y += 50000
					bloque14_3.y += 50000
					bloque15_3.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 4 or aleatorio2 == 4:
				bloque1_4 = Bloque(175,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_4 = Bloque(175,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_4 = Bloque(175,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_4 = Bloque(175,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_4 = Bloque(175,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_4 = Bloque(175,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_4 = Bloque(175,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_4 = Bloque(175,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_4 = Bloque(175,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_4 = Bloque(175,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_4 = Bloque(175,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_4 = Bloque(175,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_4 = Bloque(175,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_4 = Bloque(175,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_4 = Bloque(175,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_4.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_4.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_4.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_4.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_4.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_4.Rebotar(bola, plataforma)
					bloque1_4.y += 50000
				if bola.puntuacion >= 800:
					bloque7_4.Rebotar(bola, plataforma)
					bloque2_4.y += 50000
				if bola.puntuacion >= 900:
					bloque8_4.Rebotar(bola, plataforma)
					bloque3_4.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_4.Rebotar(bola, plataforma)
					bloque4_4.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_4.Rebotar(bola, plataforma)
					bloque5_4.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_4.Rebotar(bola, plataforma)
					bloque6_4.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_4.Rebotar(bola, plataforma)
					bloque7_4.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_4.Rebotar(bola, plataforma)
					bloque8_4.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_4.Rebotar(bola, plataforma)
					bloque9_4.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_4.Rebotar(bola, plataforma)
					bloque10_4.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_4.y += 50000
					bloque12_4.y += 50000
					bloque13_4.y += 50000
					bloque14_4.y += 50000
					bloque15_4.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 5 or aleatorio2 == 5:
				bloque1_5 = Bloque(225,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_5 = Bloque(225,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_5 = Bloque(225,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_5 = Bloque(225,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_5 = Bloque(225,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_5 = Bloque(225,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_5 = Bloque(225,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_5 = Bloque(225,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_5 = Bloque(225,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_5 = Bloque(225,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_5 = Bloque(225,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_5 = Bloque(225,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_5 = Bloque(225,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_5 = Bloque(225,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_5 = Bloque(225,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_5.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_5.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_5.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_5.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_5.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_5.Rebotar(bola, plataforma)
					bloque1_5.y += 50000
				if bola.puntuacion >= 800:
					bloque7_5.Rebotar(bola, plataforma)
					bloque2_5.y += 50000
				if bola.puntuacion >= 900:
					bloque8_5.Rebotar(bola, plataforma)
					bloque3_5.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_5.Rebotar(bola, plataforma)
					bloque4_5.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_5.Rebotar(bola, plataforma)
					bloque5_5.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_5.Rebotar(bola, plataforma)
					bloque6_5.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_5.Rebotar(bola, plataforma)
					bloque7_5.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_5.Rebotar(bola, plataforma)
					bloque8_5.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_5.Rebotar(bola, plataforma)
					bloque9_5.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_5.Rebotar(bola, plataforma)
					bloque10_5.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_5.y += 50000
					bloque12_5.y += 50000
					bloque13_5.y += 50000
					bloque14_5.y += 50000
					bloque15_5.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 6 or aleatorio2 == 6:
				bloque1_6 = Bloque(275,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_6 = Bloque(275,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_6 = Bloque(275,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_6 = Bloque(275,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_6 = Bloque(275,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_6 = Bloque(275,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_6 = Bloque(275,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_6 = Bloque(275,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_6 = Bloque(275,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_6 = Bloque(275,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_6 = Bloque(275,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_6 = Bloque(275,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_6 = Bloque(275,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_6 = Bloque(275,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_6 = Bloque(275,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_6.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_6.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_6.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_6.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_6.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_6.Rebotar(bola, plataforma)
					bloque1_6.y += 50000
				if bola.puntuacion >= 800:
					bloque7_6.Rebotar(bola, plataforma)
					bloque2_6.y += 50000
				if bola.puntuacion >= 900:
					bloque8_6.Rebotar(bola, plataforma)
					bloque3_6.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_6.Rebotar(bola, plataforma)
					bloque4_6.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_6.Rebotar(bola, plataforma)
					bloque5_6.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_6.Rebotar(bola, plataforma)
					bloque6_6.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_6.Rebotar(bola, plataforma)
					bloque7_6.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_6.Rebotar(bola, plataforma)
					bloque8_6.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_6.Rebotar(bola, plataforma)
					bloque9_6.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_6.Rebotar(bola, plataforma)
					bloque10_6.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_6.y += 50000
					bloque12_6.y += 50000
					bloque13_6.y += 50000
					bloque14_6.y += 50000
					bloque15_6.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 7 or aleatorio2 == 7:
				bloque1_7 = Bloque(325,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_7 = Bloque(325,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_7 = Bloque(325,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_7 = Bloque(325,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_7 = Bloque(325,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_7 = Bloque(325,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_7 = Bloque(325,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_7 = Bloque(325,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_7 = Bloque(325,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_7 = Bloque(325,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_7 = Bloque(325,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_7 = Bloque(325,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_7 = Bloque(325,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_7 = Bloque(325,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_7 = Bloque(325,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_7.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_7.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_7.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_7.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_7.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_7.Rebotar(bola, plataforma)
					bloque1_7.y += 50000
				if bola.puntuacion >= 800:
					bloque7_7.Rebotar(bola, plataforma)
					bloque2_7.y += 50000
				if bola.puntuacion >= 900:
					bloque8_7.Rebotar(bola, plataforma)
					bloque3_7.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_7.Rebotar(bola, plataforma)
					bloque4_7.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_7.Rebotar(bola, plataforma)
					bloque5_7.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_7.Rebotar(bola, plataforma)
					bloque6_7.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_7.Rebotar(bola, plataforma)
					bloque7_7.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_7.Rebotar(bola, plataforma)
					bloque8_7.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_7.Rebotar(bola, plataforma)
					bloque9_7.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_7.Rebotar(bola, plataforma)
					bloque10_7.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_7.y += 50000
					bloque12_7.y += 50000
					bloque13_7.y += 50000
					bloque14_7.y += 50000
					bloque15_7.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 8 or aleatorio2 == 8:
				bloque1_8 = Bloque(375,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_8 = Bloque(375,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_8 = Bloque(375,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_8 = Bloque(375,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_8 = Bloque(375,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_8 = Bloque(375,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_8 = Bloque(375,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_8 = Bloque(375,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_8 = Bloque(375,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_8 = Bloque(375,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_8 = Bloque(375,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_8 = Bloque(375,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_8 = Bloque(375,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_8 = Bloque(375,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_8 = Bloque(375,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_8.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_8.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_8.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_8.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_8.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_8.Rebotar(bola, plataforma)
					bloque1_8.y += 50000
				if bola.puntuacion >= 800:
					bloque7_8.Rebotar(bola, plataforma)
					bloque2_8.y += 50000
				if bola.puntuacion >= 900:
					bloque8_8.Rebotar(bola, plataforma)
					bloque3_8.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_8.Rebotar(bola, plataforma)
					bloque4_8.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_8.Rebotar(bola, plataforma)
					bloque5_8.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_8.Rebotar(bola, plataforma)
					bloque6_8.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_8.Rebotar(bola, plataforma)
					bloque7_8.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_8.Rebotar(bola, plataforma)
					bloque8_8.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_8.Rebotar(bola, plataforma)
					bloque9_8.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_8.Rebotar(bola, plataforma)
					bloque10_8.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_8.y += 50000
					bloque12_8.y += 50000
					bloque13_8.y += 50000
					bloque14_8.y += 50000
					bloque15_8.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 9 or aleatorio2 == 9:
				bloque1_9 = Bloque(425,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_9 = Bloque(425,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_9 = Bloque(425,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_9 = Bloque(425,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_9 = Bloque(425,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_9 = Bloque(425,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_9 = Bloque(425,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_9 = Bloque(425,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_9 = Bloque(425,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_9 = Bloque(425,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_9 = Bloque(425,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_9 = Bloque(425,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_9 = Bloque(425,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_9 = Bloque(425,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_9 = Bloque(425,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_9.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_9.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_9.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_9.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_9.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_9.Rebotar(bola, plataforma)
					bloque1_9.y += 50000
				if bola.puntuacion >= 800:
					bloque7_9.Rebotar(bola, plataforma)
					bloque2_9.y += 50000
				if bola.puntuacion >= 900:
					bloque8_9.Rebotar(bola, plataforma)
					bloque3_9.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_9.Rebotar(bola, plataforma)
					bloque4_9.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_9.Rebotar(bola, plataforma)
					bloque5_9.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_9.Rebotar(bola, plataforma)
					bloque6_9.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_9.Rebotar(bola, plataforma)
					bloque7_9.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_9.Rebotar(bola, plataforma)
					bloque8_9.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_9.Rebotar(bola, plataforma)
					bloque9_9.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_9.Rebotar(bola, plataforma)
					bloque10_9.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_9.y += 50000
					bloque12_9.y += 50000
					bloque13_9.y += 50000
					bloque14_9.y += 50000
					bloque15_9.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 10 or aleatorio2 == 10:
				bloque1_10 = Bloque(475,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_10 = Bloque(475,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_10 = Bloque(475,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_10 = Bloque(475,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_10 = Bloque(475,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_10 = Bloque(475,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_10 = Bloque(475,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_10 = Bloque(475,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_10 = Bloque(475,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_10 = Bloque(475,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_10 = Bloque(475,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_10 = Bloque(475,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_10 = Bloque(475,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_10 = Bloque(475,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_10 = Bloque(475,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_10.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_10.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_10.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_10.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_10.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_10.Rebotar(bola, plataforma)
					bloque1_10.y += 50000
				if bola.puntuacion >= 800:
					bloque7_10.Rebotar(bola, plataforma)
					bloque2_10.y += 50000
				if bola.puntuacion >= 900:
					bloque8_10.Rebotar(bola, plataforma)
					bloque3_10.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_10.Rebotar(bola, plataforma)
					bloque4_10.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_10.Rebotar(bola, plataforma)
					bloque5_10.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_10.Rebotar(bola, plataforma)
					bloque6_10.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_10.Rebotar(bola, plataforma)
					bloque7_10.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_10.Rebotar(bola, plataforma)
					bloque8_10.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_10.Rebotar(bola, plataforma)
					bloque9_10.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_10.Rebotar(bola, plataforma)
					bloque10_10.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_10.y += 50000
					bloque12_10.y += 50000
					bloque13_10.y += 50000
					bloque14_10.y += 50000
					bloque15_10.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 11 or aleatorio2 == 11:
				bloque1_11 = Bloque(525,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_11 = Bloque(525,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_11 = Bloque(525,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_11 = Bloque(525,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_11 = Bloque(525,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_11 = Bloque(525,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_11 = Bloque(525,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_11 = Bloque(525,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_11 = Bloque(525,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_11 = Bloque(525,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_11 = Bloque(525,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_11 = Bloque(525,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_11 = Bloque(525,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_11 = Bloque(525,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_11 = Bloque(525,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_11.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_11.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_11.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_11.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_11.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_11.Rebotar(bola, plataforma)
					bloque1_11.y += 50000
				if bola.puntuacion >= 800:
					bloque7_11.Rebotar(bola, plataforma)
					bloque2_11.y += 50000
				if bola.puntuacion >= 900:
					bloque8_11.Rebotar(bola, plataforma)
					bloque3_11.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_11.Rebotar(bola, plataforma)
					bloque4_11.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_11.Rebotar(bola, plataforma)
					bloque5_11.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_11.Rebotar(bola, plataforma)
					bloque6_11.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_11.Rebotar(bola, plataforma)
					bloque7_11.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_11.Rebotar(bola, plataforma)
					bloque8_11.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_11.Rebotar(bola, plataforma)
					bloque9_11.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_11.Rebotar(bola, plataforma)
					bloque10_11.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_11.y += 50000
					bloque12_11.y += 50000
					bloque13_11.y += 50000
					bloque14_11.y += 50000
					bloque15_11.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 12 or aleatorio2 == 12:
				bloque1_12 = Bloque(575,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_12 = Bloque(575,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_12 = Bloque(575,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_12 = Bloque(575,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_12 = Bloque(575,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_12 = Bloque(575,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_12 = Bloque(575,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_12 = Bloque(575,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_12 = Bloque(575,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_12 = Bloque(575,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_12 = Bloque(575,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_12 = Bloque(575,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_12 = Bloque(575,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_12 = Bloque(575,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_12 = Bloque(575,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_12.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_12.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_12.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_12.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_12.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_12.Rebotar(bola, plataforma)
					bloque1_12.y += 50000
				if bola.puntuacion >= 800:
					bloque7_12.Rebotar(bola, plataforma)
					bloque2_12.y += 50000
				if bola.puntuacion >= 900:
					bloque8_12.Rebotar(bola, plataforma)
					bloque3_12.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_12.Rebotar(bola, plataforma)
					bloque4_12.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_12.Rebotar(bola, plataforma)
					bloque5_12.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_12.Rebotar(bola, plataforma)
					bloque6_12.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_12.Rebotar(bola, plataforma)
					bloque7_12.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_12.Rebotar(bola, plataforma)
					bloque8_12.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_12.Rebotar(bola, plataforma)
					bloque9_12.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_12.Rebotar(bola, plataforma)
					bloque10_12.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_12.y += 50000
					bloque12_12.y += 50000
					bloque13_12.y += 50000
					bloque14_12.y += 50000
					bloque15_12.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 13 or aleatorio2 == 13:
				bloque1_13 = Bloque(625,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_13 = Bloque(625,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_13 = Bloque(625,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_13 = Bloque(625,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_13 = Bloque(625,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_13 = Bloque(625,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_13 = Bloque(625,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_13 = Bloque(625,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_13 = Bloque(625,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_13 = Bloque(625,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_13 = Bloque(625,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_13 = Bloque(625,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_13 = Bloque(625,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_13 = Bloque(625,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_13 = Bloque(625,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_13.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_13.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_13.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_13.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_13.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_13.Rebotar(bola, plataforma)
					bloque1_13.y += 50000
				if bola.puntuacion >= 800:
					bloque7_13.Rebotar(bola, plataforma)
					bloque2_13.y += 50000
				if bola.puntuacion >= 900:
					bloque8_13.Rebotar(bola, plataforma)
					bloque3_13.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_13.Rebotar(bola, plataforma)
					bloque4_13.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_13.Rebotar(bola, plataforma)
					bloque5_13.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_13.Rebotar(bola, plataforma)
					bloque6_13.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_13.Rebotar(bola, plataforma)
					bloque7_13.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_13.Rebotar(bola, plataforma)
					bloque8_13.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_13.Rebotar(bola, plataforma)
					bloque9_13.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_13.Rebotar(bola, plataforma)
					bloque10_13.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_13.y += 50000
					bloque12_13.y += 50000
					bloque13_13.y += 50000
					bloque14_13.y += 50000
					bloque15_13.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 14 or aleatorio2 == 14:
				bloque1_14 = Bloque(675,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_14 = Bloque(675,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_14 = Bloque(675,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_14 = Bloque(675,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_14 = Bloque(675,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_14 = Bloque(675,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_14 = Bloque(675,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_14 = Bloque(675,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_14 = Bloque(675,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_14 = Bloque(675,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_14 = Bloque(675,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_14 = Bloque(675,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_14 = Bloque(675,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_14 = Bloque(675,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_14 = Bloque(675,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_14.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_14.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_14.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_14.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_14.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_14.Rebotar(bola, plataforma)
					bloque1_14.y += 50000
				if bola.puntuacion >= 800:
					bloque7_14.Rebotar(bola, plataforma)
					bloque2_14.y += 50000
				if bola.puntuacion >= 900:
					bloque8_14.Rebotar(bola, plataforma)
					bloque3_14.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_14.Rebotar(bola, plataforma)
					bloque4_14.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_14.Rebotar(bola, plataforma)
					bloque5_14.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_14.Rebotar(bola, plataforma)
					bloque6_14.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_14.Rebotar(bola, plataforma)
					bloque7_14.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_14.Rebotar(bola, plataforma)
					bloque8_14.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_14.Rebotar(bola, plataforma)
					bloque9_14.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_14.Rebotar(bola, plataforma)
					bloque10_14.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_14.y += 50000
					bloque12_14.y += 50000
					bloque13_14.y += 50000
					bloque14_14.y += 50000
					bloque15_14.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 15 or aleatorio2 == 15:
				bloque1_15 = Bloque(725,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_15 = Bloque(725,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_15 = Bloque(725,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_15 = Bloque(725,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_15 = Bloque(725,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_15 = Bloque(725,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_15 = Bloque(725,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_15 = Bloque(725,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_15 = Bloque(725,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_15 = Bloque(725,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_15 = Bloque(725,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_15 = Bloque(725,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_15 = Bloque(725,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_15 = Bloque(725,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_15 = Bloque(725,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_15.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_15.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_15.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_15.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_15.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_15.Rebotar(bola, plataforma)
					bloque1_15.y += 50000
				if bola.puntuacion >= 800:
					bloque7_15.Rebotar(bola, plataforma)
					bloque2_15.y += 50000
				if bola.puntuacion >= 900:
					bloque8_15.Rebotar(bola, plataforma)
					bloque3_15.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_15.Rebotar(bola, plataforma)
					bloque4_15.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_15.Rebotar(bola, plataforma)
					bloque5_15.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_15.Rebotar(bola, plataforma)
					bloque6_15.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_15.Rebotar(bola, plataforma)
					bloque7_15.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_15.Rebotar(bola, plataforma)
					bloque8_15.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_15.Rebotar(bola, plataforma)
					bloque9_15.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_15.Rebotar(bola, plataforma)
					bloque10_15.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_15.y += 50000
					bloque12_15.y += 50000
					bloque13_15.y += 50000
					bloque14_15.y += 50000
					bloque15_15.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 16 or aleatorio2 == 16:
				bloque1_16 = Bloque(775,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_16 = Bloque(775,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_16 = Bloque(775,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_16 = Bloque(775,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_16 = Bloque(775,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_16 = Bloque(775,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_16 = Bloque(775,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_16 = Bloque(775,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_16 = Bloque(775,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_16 = Bloque(775,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_16 = Bloque(775,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_16 = Bloque(775,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_16 = Bloque(775,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_16 = Bloque(775,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_16 = Bloque(775,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_16.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_16.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_16.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_16.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_16.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_16.Rebotar(bola, plataforma)
					bloque1_16.y += 50000
				if bola.puntuacion >= 800:
					bloque7_16.Rebotar(bola, plataforma)
					bloque2_16.y += 50000
				if bola.puntuacion >= 900:
					bloque8_16.Rebotar(bola, plataforma)
					bloque3_16.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_16.Rebotar(bola, plataforma)
					bloque4_16.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_16.Rebotar(bola, plataforma)
					bloque5_16.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_16.Rebotar(bola, plataforma)
					bloque6_16.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_16.Rebotar(bola, plataforma)
					bloque7_16.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_16.Rebotar(bola, plataforma)
					bloque8_16.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_16.Rebotar(bola, plataforma)
					bloque9_16.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_16.Rebotar(bola, plataforma)
					bloque10_16.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_16.y += 50000
					bloque12_16.y += 50000
					bloque13_16.y += 50000
					bloque14_16.y += 50000
					bloque15_16.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 17 or aleatorio2 == 17:
				bloque1_17 = Bloque(825,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_17 = Bloque(825,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_17 = Bloque(825,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_17 = Bloque(825,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_17 = Bloque(825,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_17 = Bloque(825,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_17 = Bloque(825,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_17 = Bloque(825,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_17 = Bloque(825,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_17 = Bloque(825,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_17 = Bloque(825,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_17 = Bloque(825,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_17 = Bloque(825,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_17 = Bloque(825,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_17 = Bloque(825,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_17.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_17.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_17.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_17.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_17.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_17.Rebotar(bola, plataforma)
					bloque1_17.y += 50000
				if bola.puntuacion >= 800:
					bloque7_17.Rebotar(bola, plataforma)
					bloque2_17.y += 50000
				if bola.puntuacion >= 900:
					bloque8_17.Rebotar(bola, plataforma)
					bloque3_17.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_17.Rebotar(bola, plataforma)
					bloque4_17.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_17.Rebotar(bola, plataforma)
					bloque5_17.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_17.Rebotar(bola, plataforma)
					bloque6_17.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_17.Rebotar(bola, plataforma)
					bloque7_17.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_17.Rebotar(bola, plataforma)
					bloque8_17.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_17.Rebotar(bola, plataforma)
					bloque9_17.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_17.Rebotar(bola, plataforma)
					bloque10_17.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_17.y += 50000
					bloque12_17.y += 50000
					bloque13_17.y += 50000
					bloque14_17.y += 50000
					bloque15_17.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 18 or aleatorio2 == 18:
				bloque1_18 = Bloque(875,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_18 = Bloque(875,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_18 = Bloque(875,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_18 = Bloque(875,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_18 = Bloque(875,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_18 = Bloque(875,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_18 = Bloque(875,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_18 = Bloque(875,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_18 = Bloque(875,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_18 = Bloque(875,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_18 = Bloque(875,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_18 = Bloque(875,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_18 = Bloque(875,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_18 = Bloque(875,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_18 = Bloque(875,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_18.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_18.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_18.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_18.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_18.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_18.Rebotar(bola, plataforma)
					bloque1_18.y += 50000
				if bola.puntuacion >= 800:
					bloque7_18.Rebotar(bola, plataforma)
					bloque2_18.y += 50000
				if bola.puntuacion >= 900:
					bloque8_18.Rebotar(bola, plataforma)
					bloque3_18.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_18.Rebotar(bola, plataforma)
					bloque4_18.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_18.Rebotar(bola, plataforma)
					bloque5_18.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_18.Rebotar(bola, plataforma)
					bloque6_18.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_18.Rebotar(bola, plataforma)
					bloque7_18.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_18.Rebotar(bola, plataforma)
					bloque8_18.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_18.Rebotar(bola, plataforma)
					bloque9_18.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_18.Rebotar(bola, plataforma)
					bloque10_18.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_18.y += 50000
					bloque12_18.y += 50000
					bloque13_18.y += 50000
					bloque14_18.y += 50000
					bloque15_18.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 19 or aleatorio2 == 19:
				bloque1_19 = Bloque(925,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_19 = Bloque(925,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_19 = Bloque(925,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_19 = Bloque(925,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_19 = Bloque(925,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_19 = Bloque(925,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_19 = Bloque(925,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_19 = Bloque(925,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_19 = Bloque(925,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_19 = Bloque(925,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_19 = Bloque(925,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_19 = Bloque(925,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_19 = Bloque(925,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_19 = Bloque(925,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_19 = Bloque(925,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_19.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_19.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_19.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_19.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_19.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_19.Rebotar(bola, plataforma)
					bloque1_19.y += 50000
				if bola.puntuacion >= 800:
					bloque7_19.Rebotar(bola, plataforma)
					bloque2_19.y += 50000
				if bola.puntuacion >= 900:
					bloque8_19.Rebotar(bola, plataforma)
					bloque3_19.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_19.Rebotar(bola, plataforma)
					bloque4_19.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_19.Rebotar(bola, plataforma)
					bloque5_19.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_19.Rebotar(bola, plataforma)
					bloque6_19.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_19.Rebotar(bola, plataforma)
					bloque7_19.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_19.Rebotar(bola, plataforma)
					bloque8_19.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_19.Rebotar(bola, plataforma)
					bloque9_19.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_19.Rebotar(bola, plataforma)
					bloque10_19.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_19.y += 50000
					bloque12_19.y += 50000
					bloque13_19.y += 50000
					bloque14_19.y += 50000
					bloque15_19.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 20 or aleatorio2 == 20:
				bloque1_20 = Bloque(975,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_20 = Bloque(975,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_20 = Bloque(975,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_20 = Bloque(975,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_20 = Bloque(975,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_20 = Bloque(975,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_20 = Bloque(975,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_20 = Bloque(975,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_20 = Bloque(975,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_20 = Bloque(975,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_20 = Bloque(975,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_20 = Bloque(975,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_20 = Bloque(975,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_20 = Bloque(975,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_20 = Bloque(975,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_20.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_20.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_20.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_20.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_20.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_20.Rebotar(bola, plataforma)
					bloque1_20.y += 50000
				if bola.puntuacion >= 800:
					bloque7_20.Rebotar(bola, plataforma)
					bloque2_20.y += 50000
				if bola.puntuacion >= 900:
					bloque8_20.Rebotar(bola, plataforma)
					bloque3_20.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_20.Rebotar(bola, plataforma)
					bloque4_20.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_20.Rebotar(bola, plataforma)
					bloque5_20.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_20.Rebotar(bola, plataforma)
					bloque6_20.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_20.Rebotar(bola, plataforma)
					bloque7_20.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_20.Rebotar(bola, plataforma)
					bloque8_20.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_20.Rebotar(bola, plataforma)
					bloque9_20.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_20.Rebotar(bola, plataforma)
					bloque10_20.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_20.y += 50000
					bloque12_20.y += 50000
					bloque13_20.y += 50000
					bloque14_20.y += 50000
					bloque15_20.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 21 or aleatorio2 == 21:
				bloque1_21 = Bloque(1025,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_21 = Bloque(1025,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_21 = Bloque(1025,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_21 = Bloque(1025,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_21 = Bloque(1025,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_21 = Bloque(1025,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_21 = Bloque(1025,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_21 = Bloque(1025,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_21 = Bloque(1025,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_21 = Bloque(1025,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_21 = Bloque(1025,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_21 = Bloque(1025,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_21 = Bloque(1025,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_21 = Bloque(1025,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_21 = Bloque(1025,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_21.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_21.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_21.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_21.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_21.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_21.Rebotar(bola, plataforma)
					bloque1_21.y += 50000
				if bola.puntuacion >= 800:
					bloque7_21.Rebotar(bola, plataforma)
					bloque2_21.y += 50000
				if bola.puntuacion >= 900:
					bloque8_21.Rebotar(bola, plataforma)
					bloque3_21.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_21.Rebotar(bola, plataforma)
					bloque4_21.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_21.Rebotar(bola, plataforma)
					bloque5_21.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_21.Rebotar(bola, plataforma)
					bloque6_21.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_21.Rebotar(bola, plataforma)
					bloque7_21.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_21.Rebotar(bola, plataforma)
					bloque8_21.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_21.Rebotar(bola, plataforma)
					bloque9_21.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_21.Rebotar(bola, plataforma)
					bloque10_21.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_21.y += 50000
					bloque12_21.y += 50000
					bloque13_21.y += 50000
					bloque14_21.y += 50000
					bloque15_21.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 22 or aleatorio2 == 22:
				bloque1_22 = Bloque(1075,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_22 = Bloque(1075,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_22 = Bloque(1075,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_22 = Bloque(1075,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_22 = Bloque(1075,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_22 = Bloque(1075,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_22 = Bloque(1075,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_22 = Bloque(1075,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_22 = Bloque(1075,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_22 = Bloque(1075,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_22 = Bloque(1075,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_22 = Bloque(1075,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_22 = Bloque(1075,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_22 = Bloque(1075,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_22 = Bloque(1075,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_22.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_22.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_22.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_22.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_22.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_22.Rebotar(bola, plataforma)
					bloque1_22.y += 50000
				if bola.puntuacion >= 800:
					bloque7_22.Rebotar(bola, plataforma)
					bloque2_22.y += 50000
				if bola.puntuacion >= 900:
					bloque8_22.Rebotar(bola, plataforma)
					bloque3_22.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_22.Rebotar(bola, plataforma)
					bloque4_22.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_22.Rebotar(bola, plataforma)
					bloque5_22.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_22.Rebotar(bola, plataforma)
					bloque6_22.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_22.Rebotar(bola, plataforma)
					bloque7_22.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_22.Rebotar(bola, plataforma)
					bloque8_22.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_22.Rebotar(bola, plataforma)
					bloque9_22.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_22.Rebotar(bola, plataforma)
					bloque10_22.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_22.y += 50000
					bloque12_22.y += 50000
					bloque13_22.y += 50000
					bloque14_22.y += 50000
					bloque15_22.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 23 or aleatorio2 == 23:
				bloque1_23 = Bloque(1125,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_23 = Bloque(1125,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_23 = Bloque(1125,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_23 = Bloque(1125,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_23 = Bloque(1125,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_23 = Bloque(1125,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_23 = Bloque(1125,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_23 = Bloque(1125,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_23 = Bloque(1125,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_23 = Bloque(1125,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_23 = Bloque(1125,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_23 = Bloque(1125,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_23 = Bloque(1125,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_23 = Bloque(1125,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_23 = Bloque(1125,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_23.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_23.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_23.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_23.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_23.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_23.Rebotar(bola, plataforma)
					bloque1_23.y += 50000
				if bola.puntuacion >= 800:
					bloque7_23.Rebotar(bola, plataforma)
					bloque2_23.y += 50000
				if bola.puntuacion >= 900:
					bloque8_23.Rebotar(bola, plataforma)
					bloque3_23.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_23.Rebotar(bola, plataforma)
					bloque4_23.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_23.Rebotar(bola, plataforma)
					bloque5_23.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_23.Rebotar(bola, plataforma)
					bloque6_23.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_23.Rebotar(bola, plataforma)
					bloque7_23.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_23.Rebotar(bola, plataforma)
					bloque8_23.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_23.Rebotar(bola, plataforma)
					bloque9_23.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_23.Rebotar(bola, plataforma)
					bloque10_23.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_23.y += 50000
					bloque12_23.y += 50000
					bloque13_23.y += 50000
					bloque14_23.y += 50000
					bloque15_23.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 24 or aleatorio2 == 24:
				bloque1_24 = Bloque(1175,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_24 = Bloque(1175,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_24 = Bloque(1175,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_24 = Bloque(1175,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_24 = Bloque(1175,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_24 = Bloque(1175,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_24 = Bloque(1175,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_24 = Bloque(1175,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_24 = Bloque(1175,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_24 = Bloque(1175,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_24 = Bloque(1175,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_24 = Bloque(1175,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_24 = Bloque(1175,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_24 = Bloque(1175,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_24 = Bloque(1175,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_24.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_24.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_24.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_24.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_24.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_24.Rebotar(bola, plataforma)
					bloque1_24.y += 50000
				if bola.puntuacion >= 800:
					bloque7_24.Rebotar(bola, plataforma)
					bloque2_24.y += 50000
				if bola.puntuacion >= 900:
					bloque8_24.Rebotar(bola, plataforma)
					bloque3_24.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_24.Rebotar(bola, plataforma)
					bloque4_24.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_24.Rebotar(bola, plataforma)
					bloque5_24.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_24.Rebotar(bola, plataforma)
					bloque6_24.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_24.Rebotar(bola, plataforma)
					bloque7_24.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_24.Rebotar(bola, plataforma)
					bloque8_24.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_24.Rebotar(bola, plataforma)
					bloque9_24.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_24.Rebotar(bola, plataforma)
					bloque10_24.y += 50000
				if bola.puntuacion >= 1700:
					bola.puntuacion = 0
					bloque11_24.y += 50000
					bloque12_24.y += 50000
					bloque13_24.y += 50000
					bloque14_24.y += 50000
					bloque15_24.y += 50000
					numero_gusanos -= 1
			if aleatorio1 == 25 or aleatorio2 == 25:
				bloque1_25 = Bloque(1225,0,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque2_25 = Bloque(1225,50,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque3_25 = Bloque(1225,100,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque4_25 = Bloque(1225,150,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque5_25 = Bloque(1225,200,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque6_25 = Bloque(1225,250,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque7_25 = Bloque(1225,300,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque8_25 = Bloque(1225,350,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque9_25 = Bloque(1225,400,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque10_25 = Bloque(1225,450,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque11_25 = Bloque(1225,500,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque12_25 = Bloque(1225,550,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque13_25 = Bloque(1225,600,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque14_25 = Bloque(1225,650,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bloque15_25 = Bloque(1225,700,30,50, 1, 1, (8, 2, 13), 100000, 0)
				bola.puntuacion += 1
				if bola.puntuacion >= 200:
					bloque1_25.Rebotar(bola, plataforma)
				if bola.puntuacion >= 300:
					bloque2_25.Rebotar(bola, plataforma)
				if bola.puntuacion >= 400:
					bloque3_25.Rebotar(bola, plataforma)
				if bola.puntuacion >= 500:
					bloque4_25.Rebotar(bola, plataforma)
				if bola.puntuacion >= 600:
					bloque5_25.Rebotar(bola, plataforma)
				if bola.puntuacion >= 700:
					bloque6_25.Rebotar(bola, plataforma)
					bloque1_25.y += 50000
				if bola.puntuacion >= 800:
					bloque7_25.Rebotar(bola, plataforma)
					bloque2_25.y += 50000
				if bola.puntuacion >= 900:
					bloque8_25.Rebotar(bola, plataforma)
					bloque3_25.y += 50000
				if bola.puntuacion >= 1000:
					bloque9_25.Rebotar(bola, plataforma)
					bloque4_25.y += 50000
				if bola.puntuacion >= 1100:
					bloque10_25.Rebotar(bola, plataforma)
					bloque5_25.y += 50000
				if bola.puntuacion >= 1200:
					bloque11_25.Rebotar(bola, plataforma)
					bloque6_25.y += 50000
				if bola.puntuacion >= 1300:
					bloque12_25.Rebotar(bola, plataforma)
					bloque7_25.y += 50000
				if bola.puntuacion >= 1400:
					bloque13_25.Rebotar(bola, plataforma)
					bloque8_25.y += 50000
				if bola.puntuacion >= 1500:
					bloque14_25.Rebotar(bola, plataforma)
					bloque9_25.y += 50000
				if bola.puntuacion >= 1600:
					bloque15_25.Rebotar(bola, plataforma)
					bloque10_25.y += 50000
				if bola.puntua4cion >= 1700:
					bola.puntuacion = 0
					bloque11_25.y += 50000
					bloque12_25.y += 50000
					bloque13_25.y += 50000
					bloque14_25.y += 50000
					bloque15_25.y += 50000
					numero_gusanos -= 1

	def InvertirPantalla(plataforma, bola, bola2, bola3, bloque1_1, bloque2_1, bloque3_1, bloque4_1, bloque5_1, bloque6_1, bloque7_1, bloque8_1, bloque9_1, bloque10_1, bloque11_1, bloque12_1, bloque13_1, bloque14_1, bloque15_1, bloque16_1, bloque17_1, bloque18_1, bloque19_1, bloque20_1, bloque21_1, bloque22_1, bloque23_1, bloque24_1, bloque1_2, bloque2_2, bloque3_2, bloque4_2, bloque5_2, bloque6_2, bloque7_2, bloque8_2, bloque9_2, bloque10_2, bloque11_2, bloque12_2, bloque13_2, bloque14_2, bloque15_2, bloque16_2, bloque17_2, bloque18_2, bloque19_2, bloque20_2, bloque21_2, bloque22_2, bloque23_2, bloque24_2, bloque1_3, bloque2_3, bloque3_3, bloque4_3, bloque5_3, bloque6_3, bloque7_3, bloque8_3, bloque9_3, bloque10_3, bloque11_3, bloque12_3, bloque13_3, bloque14_3, bloque15_3, bloque16_3, bloque17_3, bloque18_3, bloque19_3, bloque20_3, bloque21_3, bloque22_3, bloque23_3, bloque24_3):
		#Invertir plataforma
		plataforma.y = 20
		#Invertir bola
		bola.y = 700 - bola.y
		bola.direcciony = -bola.direcciony
		if numero_bolas == 2:
			bola2.y = 700 - bola2.y
			bola2.direcciony = -bola2.direcciony
		if numero_bolas == 3:
			bola3.y = 700 - bola3.y
			bola3.direcciony = -bola3.direcciony
		#Invertir bloques
		bloque1_1.y = 700 - bloque1_1.y
		bloque2_1.y = 700 - bloque2_1.y
		bloque3_1.y = 700 - bloque3_1.y
		bloque4_1.y = 700 - bloque4_1.y
		bloque5_1.y = 700 - bloque5_1.y
		bloque6_1.y = 700 - bloque6_1.y
		bloque7_1.y = 700 - bloque7_1.y
		bloque8_1.y = 700 - bloque8_1.y
		bloque9_1.y = 700 - bloque9_1.y
		bloque10_1.y = 700 - bloque10_1.y
		bloque11_1.y = 700 - bloque11_1.y
		bloque12_1.y = 700 - bloque12_1.y
		bloque13_1.y = 700 - bloque13_1.y
		bloque14_1.y = 700 - bloque14_1.y
		bloque15_1.y = 700 - bloque15_1.y
		bloque16_1.y = 700 - bloque16_1.y
		bloque17_1.y = 700 - bloque17_1.y
		bloque18_1.y = 700 - bloque18_1.y
		bloque19_1.y = 700 - bloque19_1.y
		bloque20_1.y = 700 - bloque20_1.y
		bloque21_1.y = 700 - bloque21_1.y
		bloque22_1.y = 700 - bloque22_1.y
		bloque23_1.y = 700 - bloque23_1.y
		bloque24_1.y = 700 - bloque24_1.y
		bloque25_1.y = 700 - bloque25_1.y
		bloque1_2.y = 700 - bloque1_2.y
		bloque2_2.y = 700 - bloque2_2.y
		bloque3_2.y = 700 - bloque3_2.y
		bloque4_2.y = 700 - bloque4_2.y
		bloque5_2.y = 700 - bloque5_2.y
		bloque6_2.y = 700 - bloque6_2.y
		bloque7_2.y = 700 - bloque7_2.y
		bloque8_2.y = 700 - bloque8_2.y
		bloque9_2.y = 700 - bloque9_2.y
		bloque10_2.y = 700 - bloque10_2.y
		bloque11_2.y = 700 - bloque11_2.y
		bloque12_2.y = 700 - bloque12_2.y
		bloque13_2.y = 700 - bloque13_2.y
		bloque14_2.y = 700 - bloque14_2.y
		bloque15_2.y = 700 - bloque15_2.y
		bloque16_2.y = 700 - bloque16_2.y
		bloque17_2.y = 700 - bloque17_2.y
		bloque18_2.y = 700 - bloque18_2.y
		bloque19_2.y = 700 - bloque19_2.y
		bloque20_2.y = 700 - bloque20_2.y
		bloque21_2.y = 700 - bloque21_2.y
		bloque22_2.y = 700 - bloque22_2.y
		bloque23_2.y = 700 - bloque23_2.y
		bloque24_2.y = 700 - bloque24_2.y
		bloque25_2.y = 700 - bloque25_2.y
		bloque1_3.y = 700 - bloque1_3.y
		bloque2_3.y = 700 - bloque2_3.y
		bloque3_3.y = 700 - bloque3_3.y
		bloque4_3.y = 700 - bloque4_3.y
		bloque5_3.y = 700 - bloque5_3.y
		bloque6_3.y = 700 - bloque6_3.y
		bloque7_3.y = 700 - bloque7_3.y
		bloque8_3.y = 700 - bloque8_3.y
		bloque9_3.y = 700 - bloque9_3.y
		bloque10_3.y = 700 - bloque10_3.y
		bloque11_3.y = 700 - bloque11_3.y
		bloque12_3.y = 700 - bloque12_3.y
		bloque13_3.y = 700 - bloque13_3.y
		bloque14_3.y = 700 - bloque14_3.y
		bloque15_3.y = 700 - bloque15_3.y
		bloque16_3.y = 700 - bloque16_3.y
		bloque17_3.y = 700 - bloque17_3.y
		bloque18_3.y = 700 - bloque18_3.y
		bloque19_3.y = 700 - bloque19_3.y
		bloque20_3.y = 700 - bloque20_3.y
		bloque21_3.y = 700 - bloque21_3.y
		bloque22_3.y = 700 - bloque22_3.y
		bloque23_3.y = 700 - bloque23_3.y
		bloque24_3.y = 700 - bloque24_3.y
		bloque25_3.y = 700 - bloque25_3.y
		#Invertir bombas
		bloque1_3.bomba.direcciony = -1
		bloque24_3.bomba.direcciony = -1
		bloque5_2.bomba.direcciony = -1
		bloque20_2.bomba.direcciony = -1
		bloque10_1.bomba.direcciony = -1
		bloque15_1.bomba.direcciony = -1
		bloque1_3.bomba.vidas = 0
		bloque24_3.bomba.vidas = 0
		bloque5_2.bomba.vidas = 0
		bloque20_2.bomba.vidas = 0
		bloque10_1.bomba.vidas = 0
		bloque15_1.bomba.vidas = 0
		bloque1_3.bomba.y = bloque1_3.y + 50
		bloque24_3.bomba.y = bloque24_3.y + 50
		bloque5_2.bomba.y = bloque5_2.y + 25
		bloque20_2.bomba.y = bloque20_2.y + 25
		bloque10_1.bomba.y = bloque10_1.y
		bloque15_1.bomba.y = bloque15_1.y
		#Invertir rayos
		bloque13_3.rayo.y -= 100
		bloque5_3.rayo.y -= 100
		bloque21_3.rayo.y -= 100
		#Invertir boomerangs
		bloque10_1.boomerang.y = 750 - bloque10_1.boomerang.y
		bloque5_1.boomerang.y = 750 - bloque5_1.boomerang.y
		bloque10_1.boomerang.direcciony = -1
		bloque5_1.boomerang.direcciony = -1
		#Para los pinchos solamente hay que cambiar la y

	def draw_pause(marco_pausa):
		global pause, change_level, mp, tiempo
		draw.rect(surface, (8,2,13,150), [0,0,1280,720])
		#draw.rect(surface, (180,131,230), [500,150,300,300])
		mouse_pos = mouse.get_pos()
		mouse_pos = mouse.get_pos()
		screen.blit(surface, (0,0))
		screen.blit(marco_pausa, (400,75))

		PLAY_BUTTON = Button(image=transform.scale(image.load("bouncy_images/rect.png"), (200, 100)), pos=(640,200), text_input='RESUME', font=main_font, base_color=(255, 255, 255), hovering_color=(194, 184, 204))
		OPTIONS_BUTTON = Button(image=transform.scale(image.load("bouncy_images/rect.png"), (200, 100)), pos=(640,325), text_input='RESTART', font=main_font, base_color=(255, 255, 255), hovering_color=(194, 184, 204))
		EXIT_BUTTON = Button(image=transform.scale(image.load("bouncy_images/rect.png"), (200, 100)), pos=(640,450), text_input='EXIT', font=main_font, base_color=(255, 255, 255), hovering_color=(194, 184, 204))

		for button in [PLAY_BUTTON, OPTIONS_BUTTON, EXIT_BUTTON]:
			button.changeColor(mouse_pos)
			button.update(screen)

		for evento in event.get():
			if evento.type == QUIT:
				quit()
				exit()
			if evento.type == KEYDOWN:
				if evento.key == K_1 and musica_menu.get_volume() > 0.0:
					musica_menu.set_volume(musica_menu.get_volume() - 0.1)
				if evento.key == K_2 and musica_menu.get_volume() > 0.0:
					musica_menu.set_volume(musica_menu.get_volume() + 0.1)
				if evento.key == K_0:
					musica_menu.set_volume(0.0)
				if evento.key == K_9:
					musica_menu.set_volume(1.0)
			if evento.type == MOUSEBUTTONDOWN:
					if PLAY_BUTTON.checkForInput(mouse_pos):
						pause = False
					if OPTIONS_BUTTON.checkForInput(mouse_pos):
						change_level = True
						tiempo = 0
						pause = False
					if EXIT_BUTTON.checkForInput(mouse_pos):
						main_menu()

	def barra_vida(screen, x, y, vida):
		largo = 200
		ancho = 25
		if vida < 25:
			color = (166, 86, 91)
		else:
			color = (163, 154, 171)
		calculo_barra = int((vida/100)*largo)
		borde = Rect(x, y, largo, ancho)
		rectangulo = Rect(x, y, calculo_barra, ancho)
		draw.rect(screen, color, borde, 3)
		draw.rect(screen, color, rectangulo)

	plataforma = Personaje(600, 700, 120, 20, 1, 1, (0,0,0), 3, 0)
	bola = Bola(plataforma.x, plataforma.y, 15, 15, 1, 1, (0,0,0), 1, 0)
	add_bola = True
	bola1 = Bola(plataforma.x, plataforma.y, 10, 10, 1, 1, (255,255,255), 1, 0)
	bola2 = Bola(plataforma.x, plataforma.y, 10, 10, 1, 1, (255,255,255), 1, 0)
	bola3 = Bola(plataforma.x, plataforma.y, 10, 10, 1, 1, (255,255,255), 1, 0)
	numero_bolas = 1
	#PRIMERA FILA
	bloque1_1 = Bloque(15,0,50,50, 1, 1, (0,0,0), 1, 100)
	bloque2_1 = Bloque(65,0,50,50, 1, 1, (0,0,0), 1, 108)
	bloque3_1 = Bloque(115,0,50,50, 1, 1, (0,0,0), 1, 116)
	bloque4_1 = Bloque(165,0,50,50, 1, 1, (0,0,0), 1, 132)
	bloque5_1 = Bloque(215,0,50,50, 1, 1, (0,0,0), 1, 140)
	bloque6_1 = Bloque(265,0,50,50, 1, 1, (0,0,0), 1, 148)
	bloque7_1 = Bloque(315,0,50,50, 1, 1, (0,0,0), 1, 156)
	bloque8_1 = Bloque(365,0,50,50, 1, 1, (0,0,0), 1, 164)
	bloque9_1 = Bloque(415,0,50,50, 1, 1, (0,0,0), 1, 172)
	bloque10_1 = Bloque(465,0,50,50, 1, 1, (0,0,0), 1, 180)
	bloque11_1 = Bloque(515,0,50,50, 1, 1, (0,0,0), 1, 188)
	bloque12_1 = Bloque(565,0,50,50, 1, 1, (0,0,0), 1, 200)
	bloque13_1 = Bloque(615,0,50,50, 1, 1, (0,0,0), 1, 200)
	bloque14_1 = Bloque(665,0,50,50, 1, 1, (0,0,0), 1, 188)
	bloque15_1 = Bloque(715,0,50,50, 1, 1, (0,0,0), 1, 180)
	bloque16_1 = Bloque(765,0,50,50, 1, 1, (0,0,0), 1, 172)
	bloque17_1 = Bloque(815,0,50,50, 1, 1, (0,0,0), 1, 164)
	bloque18_1 = Bloque(865,0,50,50, 1, 1, (0,0,0), 1, 156)
	bloque19_1 = Bloque(915,0,50,50, 1, 1, (0,0,0), 1, 148)
	bloque20_1 = Bloque(965,0,50,50, 1, 1, (0,0,0), 1, 140)
	bloque21_1 = Bloque(1015,0,50,50, 1, 1, (0,0,0), 1, 132)
	bloque22_1 = Bloque(1065,0,50,50, 1, 1, (0,0,0), 1, 124)
	bloque23_1 = Bloque(1115,0,50,50, 1, 1, (0,0,0), 1, 116)
	bloque24_1 = Bloque(1165,0,50,50, 1, 1, (0,0,0), 1, 108)
	bloque25_1 = Bloque(1215,0,50,50, 1, 1, (0,0,0), 1, 100)
	#SEGUNDA FILA
	bloque1_2 = Bloque(15,50000,50,50, 1, 1, (0,0,0), 1, 100)
	bloque2_2 = Bloque(65,50000,50,50, 1, 1, (0,0,0), 1, 108)
	bloque3_2 = Bloque(115,50000,50,50, 1, 1, (0,0,0), 1, 116)
	bloque4_2 = Bloque(165,50000,50,50, 1, 1, (0,0,0), 1, 132)
	bloque5_2 = Bloque(215,50000,50,50, 1, 1, (0,0,0), 1, 140)
	bloque6_2 = Bloque(265,50000,50,50, 1, 1, (0,0,0), 1, 148)
	bloque7_2 = Bloque(315,50000,50,50, 1, 1, (0,0,0), 1, 156)
	bloque8_2 = Bloque(365,50000,50,50, 1, 1, (0,0,0), 1, 164)
	bloque9_2 = Bloque(415,50000,50,50, 1, 1, (0,0,0), 1, 172)
	bloque10_2 = Bloque(465,50000,50,50, 1, 1, (0,0,0), 1, 180)
	bloque11_2 = Bloque(515,50000,50,50, 1, 1, (0,0,0), 1, 188)
	bloque12_2 = Bloque(565,50000,50,50, 1, 1, (0,0,0), 1, 200)
	bloque13_2 = Bloque(615,50000,50,50, 1, 1, (0,0,0), 1, 200)
	bloque14_2 = Bloque(665,50000,50,50, 1, 1, (0,0,0), 1, 188)
	bloque15_2 = Bloque(715,50000,50,50, 1, 1, (0,0,0), 1, 180)
	bloque16_2 = Bloque(765,50000,50,50, 1, 1, (0,0,0), 1, 172)
	bloque17_2 = Bloque(815,50000,50,50, 1, 1, (0,0,0), 1, 164)
	bloque18_2 = Bloque(865,50000,50,50, 1, 1, (0,0,0), 1, 156)
	bloque19_2 = Bloque(915,50000,50,50, 1, 1, (0,0,0), 1, 148)
	bloque20_2 = Bloque(965,50000,50,50, 1, 1, (0,0,0), 1, 140)
	bloque21_2 = Bloque(1015,50000,50,50, 1, 1, (0,0,0), 1, 132)
	bloque22_2 = Bloque(1065,50000,50,50, 1, 1, (0,0,0), 1, 124)
	bloque23_2 = Bloque(1115,50000,50,50, 1, 1, (0,0,0), 1, 116)
	bloque24_2 = Bloque(1165,50000,50,50, 1, 1, (0,0,0), 1, 108)
	bloque25_2 = Bloque(1215,50000,50,50, 1, 1, (0,0,0), 1, 100)
	#TERCERA FILA
	bloque1_3 = Bloque(15,50000,50,50, 1, 1, (0,0,0), 1, 100)
	bloque2_3 = Bloque(65,50000,50,50, 1, 1, (0,0,0), 1, 108)
	bloque3_3 = Bloque(115,50000,50,50, 1, 1, (0,0,0), 1, 116)
	bloque4_3 = Bloque(165,50000,50,50, 1, 1, (0,0,0), 1, 124)
	bloque5_3 = Bloque(215,50000,50,50, 1, 1, (0,0,0), 1, 132)
	bloque6_3 = Bloque(265,50000,50,50, 1, 1, (0,0,0), 1, 148)
	bloque7_3 = Bloque(315,50000,50,50, 1, 1, (0,0,0), 1, 156)
	bloque8_3 = Bloque(365,50000,50,50, 1, 1, (0,0,0), 1, 164)
	bloque9_3 = Bloque(415,50000,50,50, 1, 1, (0,0,0), 1, 172)
	bloque10_3 = Bloque(465,50000,50,50, 1, 1, (0,0,0), 1, 180)
	bloque11_3 = Bloque(515,50000,50,50, 1, 1, (0,0,0), 1, 188)
	bloque12_3 = Bloque(565,50000,50,50, 1, 1, (0,0,0), 1, 200)
	bloque13_3 = Bloque(615,50000,50,50, 1, 1, (0,0,0), 1, 200)
	bloque14_3 = Bloque(665,50000,50,50, 1, 1, (0,0,0), 1, 188)
	bloque15_3 = Bloque(715,50000,50,50, 1, 1, (0,0,0), 1, 180)
	bloque16_3 = Bloque(765,50000,50,50, 1, 1, (0,0,0), 1, 172)
	bloque17_3 = Bloque(815,50000,50,50, 1, 1, (0,0,0), 1, 164)
	bloque18_3 = Bloque(865,50000,50,50, 1, 1, (0,0,0), 1, 156)
	bloque19_3 = Bloque(915,50000,50,50, 1, 1, (0,0,0), 1, 148)
	bloque20_3 = Bloque(965,50000,50,50, 1, 1, (0,0,0), 1, 140)
	bloque21_3 = Bloque(1015,50000,50,50, 1, 1, (0,0,0), 1, 132)
	bloque22_3 = Bloque(1065,50000,50,50, 1, 1, (0,0,0), 1, 124)
	bloque23_3 = Bloque(1115,50000,50,50, 1, 1, (0,0,0), 1, 116)
	bloque24_3 = Bloque(1165,50000,50,50, 1, 1, (0,0,0), 1, 108)
	bloque25_3 = Bloque(1215,50000,50,50, 1, 1, (0,0,0), 1, 100)
	z = 0
	t = 0
	pinchos1 = Bloque(0,0,50,50, 1, 1, (0,0,0), 1, 100)
	pinchos2 = Bloque(50,0,50,50, 1, 1, (0,0,0), 1, 109)
	jumper1 = Bloque(1215,50000,50,50, 1, 1, (0,0,0), 1, 100)
	borde1 = Bloque(0,0,15,1000, 1, 1, (180, 131, 230), 1, 0)
	borde2 = Bloque(1265,0,15,1000, 1, 1, (180, 131, 230), 1, 0)
	a = True
	b = True
	invertir = False
	level = 1
	imagenes = False
	huesos = 0
	animacion = 0
	ball = 0
	level = saveloadmanager.load_game_data(['level'], [1])
	ball_sound = mixer.Sound('bouncy_images/sound/ball_sound.ogg')
	hueso_sound = mixer.Sound('bouncy_images/sound/hueso_sound.ogg')
	fuego_sound = mixer.Sound('bouncy_images/sound/fuego_sound.ogg')
	gusano_chico_sound = mixer.Sound('bouncy_images/sound/gusano_chico_sound.ogg')
	musica1 = mixer.Sound('bouncy_images/musica/musica1.ogg')
	musica2 = mixer.Sound('bouncy_images/musica/musica2.ogg')
	musica3 = mixer.Sound('bouncy_images/musica/musica3.ogg')
	musica4 = mixer.Sound('bouncy_images/musica/musica4.ogg')
	musica5 = mixer.Sound('bouncy_images/musica/musica5.ogg')
	musica_boss1 = mixer.Sound('bouncy_images/musica/musica_boss1.ogg')
	musica_boss2 = mixer.Sound('bouncy_images/musica/musica_boss2.ogg')
	musica1.set_volume(0.5)
	musica2.set_volume(0.5)
	musica3.set_volume(0.5)
	musica4.set_volume(0.5)
	musica5.set_volume(0.5)
	musica_boss1.set_volume(0.5)
	musica_boss2.set_volume(0.5)
	while True:
		global numero_bloques, numero_gusanos, contador_rebotes, numero_pinchos, hit, w, gusano1_y, gusano2_y, final_boss, pause, change_level, mp, musica_menu, dibujo, tiempo
		if finish == False:
			if z == 0:
				numero_bloques = 25
				numero_gusanos = 1
				numero_pinchos = 1
				contador_rebotes = 0
				w = 1
				hit = False
				final_boss = False
				pause = False
				change_level = False
				mp = 0
				z = 1
				dibujo = 0
				tiempo = 0
			screen.fill((8, 2, 13))
			if not pause:
				plataforma.Movimiento()
				if add_bola == True:
					bola.Movimiento()
					bola.Golpear_personaje(plataforma)
					if bola.y >= 720:
						numero_bolas -= 1
						add_bola = False
			#PRIMERA FILA
			borde1.DibujarObjeto()
			borde2.DibujarObjeto()
			bloque1_1.Rebotar(bola, plataforma)
			bloque2_1.Rebotar(bola, plataforma)
			bloque3_1.Rebotar(bola, plataforma)
			bloque4_1.Rebotar(bola, plataforma)
			bloque5_1.Rebotar(bola, plataforma)
			bloque6_1.Rebotar(bola, plataforma)
			bloque7_1.Rebotar(bola, plataforma)
			bloque8_1.Rebotar(bola, plataforma)
			bloque9_1.Rebotar(bola, plataforma)
			bloque10_1.Rebotar(bola, plataforma)
			bloque11_1.Rebotar(bola, plataforma)
			bloque12_1.Rebotar(bola, plataforma)
			bloque13_1.Rebotar(bola, plataforma)
			bloque14_1.Rebotar(bola, plataforma)
			bloque15_1.Rebotar(bola, plataforma)
			bloque16_1.Rebotar(bola, plataforma)
			bloque17_1.Rebotar(bola, plataforma)
			bloque18_1.Rebotar(bola, plataforma)
			bloque19_1.Rebotar(bola, plataforma)
			bloque20_1.Rebotar(bola, plataforma)
			bloque21_1.Rebotar(bola, plataforma)
			bloque22_1.Rebotar(bola, plataforma)
			bloque23_1.Rebotar(bola, plataforma)
			bloque24_1.Rebotar(bola, plataforma)
			bloque25_1.Rebotar(bola, plataforma)
			#SEGUDA FILA
			bloque1_2.Rebotar(bola, plataforma)
			bloque2_2.Rebotar(bola, plataforma)
			bloque3_2.Rebotar(bola, plataforma)
			bloque4_2.Rebotar(bola, plataforma)
			bloque5_2.Rebotar(bola, plataforma)
			bloque6_2.Rebotar(bola, plataforma)
			bloque7_2.Rebotar(bola, plataforma)
			bloque8_2.Rebotar(bola, plataforma)
			bloque9_2.Rebotar(bola, plataforma)
			bloque10_2.Rebotar(bola, plataforma)
			bloque11_2.Rebotar(bola, plataforma)
			bloque12_2.Rebotar(bola, plataforma)
			bloque13_2.Rebotar(bola, plataforma)
			bloque14_2.Rebotar(bola, plataforma)
			bloque15_2.Rebotar(bola, plataforma)
			bloque16_2.Rebotar(bola, plataforma)
			bloque17_2.Rebotar(bola, plataforma)
			bloque18_2.Rebotar(bola, plataforma)
			bloque19_2.Rebotar(bola, plataforma)
			bloque20_2.Rebotar(bola, plataforma)
			bloque21_2.Rebotar(bola, plataforma)
			bloque22_2.Rebotar(bola, plataforma)
			bloque23_2.Rebotar(bola, plataforma)
			bloque24_2.Rebotar(bola, plataforma)
			bloque25_2.Rebotar(bola, plataforma)
			#TERCERA FILA
			bloque1_3.Rebotar(bola, plataforma)
			bloque2_3.Rebotar(bola, plataforma)
			bloque3_3.Rebotar(bola, plataforma)
			bloque4_3.Rebotar(bola, plataforma)
			bloque5_3.Rebotar(bola, plataforma)
			bloque6_3.Rebotar(bola, plataforma)
			bloque7_3.Rebotar(bola, plataforma)
			bloque8_3.Rebotar(bola, plataforma)
			bloque9_3.Rebotar(bola, plataforma)
			bloque10_3.Rebotar(bola, plataforma)
			bloque11_3.Rebotar(bola, plataforma)
			bloque12_3.Rebotar(bola, plataforma)
			bloque13_3.Rebotar(bola, plataforma)
			bloque14_3.Rebotar(bola, plataforma)
			bloque15_3.Rebotar(bola, plataforma)
			bloque16_3.Rebotar(bola, plataforma)
			bloque17_3.Rebotar(bola, plataforma)
			bloque18_3.Rebotar(bola, plataforma)
			bloque19_3.Rebotar(bola, plataforma)
			bloque20_3.Rebotar(bola, plataforma)
			bloque21_3.Rebotar(bola, plataforma)
			bloque22_3.Rebotar(bola, plataforma)
			bloque23_3.Rebotar(bola, plataforma)
			bloque24_3.Rebotar(bola, plataforma)
			bloque25_3.Rebotar(bola, plataforma)

			if change_level == True and level != 30:
				plataforma.x = 600
				bola.x = plataforma.x + 60
				bola.y = plataforma.y - 20
				bola.direcciony = 1
				#bola.direccionx = 1
				bola1.y = bola1.y + 50000
				bloque1_1.vidas = 1
				bloque1_1.y = 0
				bloque1_1.color = (8, 2, 13)
				bloque2_1.vidas = 1
				bloque2_1.y = 0
				bloque2_1.color = (8, 2, 13)
				bloque3_1.vidas = 1
				bloque3_1.y = 0
				bloque3_1.color = (8, 2, 13)
				bloque4_1.vidas = 1
				bloque4_1.y = 0
				bloque4_1.color = (8, 2, 13)
				bloque5_1.vidas = 1
				bloque5_1.y = 0
				bloque5_1.color = (8, 2, 13)
				bloque6_1.vidas = 1
				bloque6_1.y = 0
				bloque6_1.color = (8, 2, 13)
				bloque7_1.vidas = 1
				bloque7_1.y = 0
				bloque7_1.color = (8, 2, 13)
				bloque8_1.vidas = 1
				bloque8_1.y = 0
				bloque8_1.color = (8, 2, 13)
				bloque9_1.vidas = 1
				bloque9_1.y = 0
				bloque9_1.color = (8, 2, 13)
				bloque10_1.vidas = 1
				bloque10_1.y = 0
				bloque10_1.color = (8, 2, 13)
				bloque11_1.vidas = 1
				bloque11_1.y = 0
				bloque11_1.color = (8, 2, 13)
				bloque12_1.vidas = 1
				bloque12_1.y = 0
				bloque12_1.color = (8, 2, 13)
				bloque13_1.vidas = 1
				bloque13_1.y = 0
				bloque13_1.color = (8, 2, 13)
				bloque14_1.vidas = 1
				bloque14_1.y = 0
				bloque14_1.color = (8, 2, 13)
				bloque15_1.vidas = 1
				bloque15_1.y = 0
				bloque15_1.color = (8, 2, 13)
				bloque16_1.vidas = 1
				bloque16_1.y = 0
				bloque16_1.color = (8, 2, 13)
				bloque17_1.vidas = 1
				bloque17_1.y = 0
				bloque17_1.color = (8, 2, 13)
				bloque18_1.vidas = 1
				bloque18_1.y = 0
				bloque18_1.color = (8, 2, 13)
				bloque19_1.vidas = 1
				bloque19_1.y = 0
				bloque19_1.color = (8, 2, 13)
				bloque20_1.vidas = 1
				bloque20_1.y = 0
				bloque20_1.color = (8, 2, 13)
				bloque21_1.vidas = 1
				bloque21_1.y = 0
				bloque21_1.color = (8, 2, 13)
				bloque22_1.vidas = 1
				bloque22_1.y = 0
				bloque22_1.color = (8, 2, 13)
				bloque23_1.vidas = 1
				bloque23_1.y = 0
				bloque23_1.color = (8, 2, 13)
				bloque24_1.vidas = 1
				bloque24_1.y = 0
				bloque24_1.color = (8, 2, 13)
				bloque25_1.vidas = 1
				bloque25_1.y = 0
				bloque25_1.color = (8, 2, 13)
				numero_bloques = 25
				if level != 1:
					bloque1_2.vidas = 1
					bloque1_2.y = 50
					bloque1_2.color = (8, 2, 13)
					bloque2_2.vidas = 1
					bloque2_2.y = 50
					bloque2_2.color = (8, 2, 13)
					bloque3_2.vidas = 1
					bloque3_2.y = 50
					bloque3_2.color = (8, 2, 13)
					bloque4_2.vidas = 1
					bloque4_2.y = 50
					bloque4_2.color = (8, 2, 13)
					bloque5_2.vidas = 1
					bloque5_2.y = 50
					bloque5_2.color = (8, 2, 13)
					bloque6_2.vidas = 1
					bloque6_2.y = 50
					bloque6_2.color = (8, 2, 13)
					bloque7_2.vidas = 1
					bloque7_2.y = 50
					bloque7_2.color = (8, 2, 13)
					bloque8_2.vidas = 1
					bloque8_2.y = 50
					bloque8_2.color = (8, 2, 13)
					bloque9_2.vidas = 1
					bloque9_2.y = 50
					bloque9_2.color = (8, 2, 13)
					bloque10_2.vidas = 1
					bloque10_2.y = 50
					bloque10_2.color = (8, 2, 13)
					bloque11_2.vidas = 1
					bloque11_2.y = 50
					bloque11_2.color = (8, 2, 13)
					bloque12_2.vidas = 1
					bloque12_2.y = 50
					bloque12_2.color = (8, 2, 13)
					bloque13_2.vidas = 1
					bloque13_2.y = 50
					bloque13_2.color = (8, 2, 13)
					bloque14_2.vidas = 1
					bloque14_2.y = 50
					bloque14_2.color = (8, 2, 13)
					bloque15_2.vidas = 1
					bloque15_2.y = 50
					bloque15_2.color = (8, 2, 13)
					bloque16_2.vidas = 1
					bloque16_2.y = 50
					bloque16_2.color = (8, 2, 13)
					bloque17_2.vidas = 1
					bloque17_2.y = 50
					bloque17_2.color = (8, 2, 13)
					bloque18_2.vidas = 1
					bloque18_2.y = 50
					bloque18_2.color = (8, 2, 13)
					bloque19_2.vidas = 1
					bloque19_2.y = 50
					bloque19_2.color = (8, 2, 13)
					bloque20_2.vidas = 1
					bloque20_2.y = 50
					bloque20_2.color = (8, 2, 13)
					bloque21_2.vidas = 1
					bloque21_2.y = 50
					bloque21_2.color = (8, 2, 13)
					bloque22_2.vidas = 1
					bloque22_2.y = 50
					bloque22_2.color = (8, 2, 13)
					bloque23_2.vidas = 1
					bloque23_2.y = 50
					bloque23_2.color = (8, 2, 13)
					bloque24_2.vidas = 1
					bloque24_2.y = 50
					bloque24_2.color = (8, 2, 13)
					bloque25_2.vidas = 1
					bloque25_2.y = 50
					bloque25_2.color = (8, 2, 13)
					bloque1_3.vidas = 1
					bloque1_3.y = 100
					bloque1_3.color = (8, 2, 13)
					bloque2_3.vidas = 1
					bloque2_3.y = 100
					bloque2_3.color = (8, 2, 13)
					bloque3_3.vidas = 1
					bloque3_3.y = 100
					bloque3_3.color = (8, 2, 13)
					bloque4_3.vidas = 1
					bloque4_3.y = 100
					bloque4_3.color = (8, 2, 13)
					bloque5_3.vidas = 1
					bloque5_3.y = 100
					bloque5_3.color = (8, 2, 13)
					bloque6_3.vidas = 1
					bloque6_3.y = 100
					bloque6_3.color = (8, 2, 13)
					bloque7_3.vidas = 1
					bloque7_3.y = 100
					bloque7_3.color = (8, 2, 13)
					bloque8_3.vidas = 1
					bloque8_3.y = 100
					bloque8_3.color = (8, 2, 13)
					bloque9_3.vidas = 1
					bloque9_3.y = 100
					bloque9_3.color = (8, 2, 13)
					bloque10_3.vidas = 1
					bloque10_3.y = 100
					bloque10_3.color = (8, 2, 13)
					bloque11_3.vidas = 1
					bloque11_3.y = 100
					bloque11_3.color = (8, 2, 13)
					bloque12_3.vidas = 1
					bloque12_3.y = 100
					bloque12_3.color = (8, 2, 13)
					bloque13_3.vidas = 1
					bloque13_3.y = 100
					bloque13_3.color = (8, 2, 13)
					bloque14_3.vidas = 1
					bloque14_3.y = 100
					bloque14_3.color = (8, 2, 13)
					bloque15_3.vidas = 1
					bloque15_3.y = 100
					bloque15_3.color = (8, 2, 13)
					bloque16_3.vidas = 1
					bloque16_3.y = 100
					bloque16_3.color = (8, 2, 13)
					bloque17_3.vidas = 1
					bloque17_3.y = 100
					bloque17_3.color = (8, 2, 13)
					bloque18_3.vidas = 1
					bloque18_3.y = 100
					bloque18_3.color = (8, 2, 13)
					bloque19_3.vidas = 1
					bloque19_3.y = 100
					bloque19_3.color = (8, 2, 13)
					bloque20_3.vidas = 1
					bloque20_3.y = 100
					bloque20_3.color = (8, 2, 13)
					bloque21_3.vidas = 1
					bloque21_3.y = 100
					bloque21_3.color = (8, 2, 13)
					bloque22_3.vidas = 1
					bloque22_3.y = 100
					bloque22_3.color = (8, 2, 13)
					bloque23_3.vidas = 1
					bloque23_3.y = 100
					bloque23_3.color = (8, 2, 13)
					bloque24_3.vidas = 1
					bloque24_3.y = 100
					bloque24_3.color = (8, 2, 13)
					bloque25_3.vidas = 1
					bloque25_3.y = 100
					bloque25_3.color = (8, 2, 13)
					numero_bloques = 75
				numero_bolas = 1
				add_bola = True
				plataforma.vidas = 3
				huesos = 0
				animacion = 0
				if level == 2:
					musica2.stop()
					musica2.set_volume(musica1.get_volume())
					musica1.stop()
					musica2.play(-1)
					bloque9_1.bomba.y = 50
					bloque17_1.bomba.y = 50
					bloque1_2.bomba.y = 100
					bloque25_2.bomba.y = 100
				if level == 3:
					musica3.stop()
					musica3.set_volume(musica2.get_volume())
					musica2.stop()
					musica3.play(-1)
					bloque11_1.bomba.y = 50
					bloque15_1.bomba.y = 50
					bloque6_2.boomerang.y = 100
					bloque6_2.boomerang.direcciony = 1
					bloque6_2.boomerang.vidas = 0
					bloque20_2.boomerang.y = 100
					bloque20_2.boomerang.direcciony = 1
					bloque20_2.boomerang.vidas = 0
					bloque1_3.bomba.y = 50
					bloque25_3.bomba.y = 50
				if level == 4:
					musica5.stop()
					musica5.set_volume(musica3.get_volume())
					musica3.stop()
					musica5.play(-1)
					plataforma.puntuacion = 0
					numero_bolas = 2
					plataforma.vidas = 3
					bloque5_1.bomba.y = 50
					bloque5_3.bomba.y = 50
					bloque21_1.bomba.y = 50
					bloque21_3.bomba.y = 50
					bloque1_2.boomerang.y = 100
					bloque1_2.boomerang.direcciony = 1
					bloque1_2.boomerang.vidas = 0
					bloque10_2.boomerang.y = 100
					bloque10_2.boomerang.direcciony = 1
					bloque10_2.boomerang.vidas = 0
					bloque16_2.boomerang.y = 100
					bloque16_2.boomerang.direcciony = 1
					bloque16_2.boomerang.vidas = 0
					bloque25_2.boomerang.y = 100
					bloque25_2.boomerang.direcciony = 1
					bloque25_2.boomerang.vidas = 0
				if level == 5:
					musica_boss2.stop()
					musica_boss2.set_volume(musica5.get_volume())
					musica5.stop()
					musica_boss2.play(-1)
					plataforma.puntuacion = 0
					invertir = False
					a = True
					b = True
					familia_topo_y = 0
					barra_y = 175
					w = 1
					t = 0
				if level == 6:
					musica1.stop()
					musica1.set_volume(musica_boss2.get_volume())
					musica_boss2.stop()
					musica1.play(-1)
					bloque8_1.bomba.color = (8, 2, 13)
					bloque17_1.bomba.color = (8, 2, 13)
					bloque1_2.bomba.color = (8, 2, 13)
					bloque24_2.bomba.color = (8, 2, 13)
					bloque12_2.bomba.color = (8, 2, 13)
					bloque13_2.bomba.color = (8, 2, 13)
					bloque8_3.bomba.color = (8, 2, 13)
					bloque17_3.bomba.color = (8, 2, 13)
					plataforma.y = 700
					bola.y = plataforma.y
				if level == 7:
					musica2.stop()
					musica2.set_volume(musica1.get_volume())
					musica1.stop()
					musica2.play(-1)
					bloque1_2.bomba.y = 50
					bloque1_3.vidas = 3
					bloque25_2.bomba.y = 50
					bloque25_3.vidas = 3
					bloque5_1.bomba.y = 100
					bloque5_2.vidas = 3
					bloque21_1.bomba.y = 100
					bloque21_2.vidas = 3
					bloque9_3.bomba.y = 100
					bloque17_3.bomba.y = 100
					bloque13_1.bomba.y = 100
					pinchos1.pinchos.puntuacion = 0
					pinchos2.pinchos.puntuacion = 0
				if level == 8:
					musica3.stop()
					musica3.set_volume(musica2.get_volume())
					musica2.stop()
					musica3.play(-1)
					bloque1_1.bomba.y = 50
					bloque25_1.bomba.y = 50
					bloque7_2.bomba.y = 50
					bloque19_2.bomba.y = 50
					bloque12_3.vidas = 3
					bloque13_3.vidas = 3
					bloque14_3.vidas = 3
				if level == 9:
					musica4.stop()
					musica4.set_volume(musica3.get_volume())
					musica3.stop()
					musica4.play(-1)
					bola.direccionx = 1
					bola1.direccionx = 1
					z = 1
				if level == 10:
					musica_boss1.stop()
					musica_boss1.set_volume(musica4.get_volume())
					musica4.stop()
					musica_boss1.play(-1)
					plataforma.puntuacion = 0
					z = 1
					bloque1_3.largo = 25
					bloque2_3.largo = 25
					bloque3_3.largo = 25
					bloque4_3.largo = 25
					bloque5_3.largo = 25
					bloque6_3.largo = 25
					bloque7_3.largo = 25
					bloque8_3.largo = 25
					bloque9_3.largo = 25
					bloque10_3.largo = 25
					bloque11_3.largo = 25
					bloque12_3.largo = 25
					bloque13_3.largo = 25
					bloque14_3.largo = 25
					bloque15_3.largo = 25
					bloque16_3.largo = 25
					bloque17_3.largo = 25
					bloque18_3.largo = 25
					bloque19_3.largo = 25
					bloque20_3.largo = 25
					bloque21_3.largo = 25
					bloque22_3.largo = 25
					bloque23_3.largo = 25
					bloque24_3.largo = 25
					bloque25_3.largo = 25
					bloque8_1.bomba.y = 50
					bloque17_1.bomba.y = 50
					bloque1_2.bomba.y = 100
					bloque24_2.bomba.y = 100
					bloque12_2.bomba.y = 100
					bloque13_2.bomba.y = 100
					bloque8_3.bomba.y = 150
					bloque17_3.bomba.y = 150
					bloque8_1.bomba.color = (180, 131, 230)
					bloque17_1.bomba.color = (180, 131, 230)
					bloque1_2.bomba.color = (180, 131, 230)
					bloque25_2.bomba.color = (180, 131, 230)
					bloque12_2.bomba.color = (180, 131, 230)
					bloque13_2.bomba.color = (180, 131, 230)
					bloque8_3.bomba.color = (180, 131, 230)
					bloque17_3.bomba.color = (180, 131, 230)
				plataforma.puntuacion = 0
				change_level = False
			if level == 1 and z == 1 and bola.y != 701:
				musica1.set_volume(musica_menu.get_volume())
				musica1.play(-1)
				z = 2
			if imagenes == False:
				esqueleto1 = transform.scale(image.load("bouncy_images/esqueleto/esqueleto1.png"), (50, 50))
				esqueleto2 = transform.scale(image.load("bouncy_images/esqueleto/esqueleto2.png"), (50, 50))
				hueso1 = transform.scale(image.load("bouncy_images/hueso/hueso1.png"), (20, 20))
				hueso2 = transform.scale(image.load("bouncy_images/hueso/hueso2.png"), (20, 20))
				hueso3 = transform.scale(image.load("bouncy_images/hueso/hueso3.png"), (20, 20))
				hueso4 = transform.scale(image.load("bouncy_images/hueso/hueso4.png"), (20, 20))
				fantasma1 = transform.scale(image.load("bouncy_images/fantasma/fantasma1.png"), (60, 60))
				fantasma2 = transform.scale(image.load("bouncy_images/fantasma/fantasma2.png"), (60, 60))
				llama1 = transform.scale(image.load("bouncy_images/llama/llama1.png"), (20, 20))
				llama2 = transform.scale(image.load("bouncy_images/llama/llama2.png"), (20, 20))
				boss1 = transform.scale(image.load("bouncy_images/gusano_boss/gusano_boss1.png"), (1300, 150))
				boss2 = transform.scale(image.load("bouncy_images/gusano_boss/gusano_boss2.png"), (1300, 150))
				boss3 = transform.scale(image.load("bouncy_images/gusano_boss/gusano_boss3.png"), (1300, 150))
				boss4 = transform.scale(image.load("bouncy_images/gusano_boss/gusano_boss4.png"), (1300, 150))
				boss7 = transform.scale(image.load("bouncy_images/gusano_boss/gusano_boss7.png"), (1300, 150))
				boss8 = transform.scale(image.load("bouncy_images/gusano_boss/gusano_boss8.png"), (1300, 150))
				gusano1 = transform.scale(image.load("bouncy_images/gusano_chico/gusano_chico1.png"), (50, 700))
				gusano2 = transform.scale(image.load("bouncy_images/gusano_chico/gusano_chico2.png"), (50, 700))
				gusano1_x = 0
				gusano1_y = 0
				gusano2_x = 0
				gusano2_y = 0
				spider1 = transform.scale(image.load("bouncy_images/spider/spider1.png"), (150, 100))
				spider2 = transform.scale(image.load("bouncy_images/spider/spider2.png"), (150, 100))
				spider1_x = 0
				spider2_x = 0
				spider1_y = 680
				spider2_y = 680
				familia_topo1 = transform.scale(image.load("bouncy_images/familia_topo/familia_topo1.png"), (1250, 150))
				familia_topo2 = transform.scale(image.load("bouncy_images/familia_topo/familia_topo2.png"), (1250, 150))
				familia_topo3 = transform.scale(image.load("bouncy_images/familia_topo/familia_topo3.png"), (1250, 150))
				familia_topo4 = transform.scale(image.load("bouncy_images/familia_topo/familia_topo4.png"), (1250, 150))
				familia_topo1r = transform.scale(image.load("bouncy_images/familia_topo/familia_topo1r.png"), (1250, 150))
				familia_topo2r = transform.scale(image.load("bouncy_images/familia_topo/familia_topo2r.png"), (1250, 150))
				familia_topo3r = transform.scale(image.load("bouncy_images/familia_topo/familia_topo3r.png"), (1250, 150))
				familia_topo4r = transform.scale(image.load("bouncy_images/familia_topo/familia_topo4r.png"), (1250, 150))
				luz1_1 = transform.scale(image.load("bouncy_images/familia_topo/luz1_1.png"), (1250, 150))
				luz1_2 = transform.scale(image.load("bouncy_images/familia_topo/luz1_2.png"), (1250, 150))
				luz1_3 = transform.scale(image.load("bouncy_images/familia_topo/luz1_3.png"), (1250, 150))
				luz1_4 = transform.scale(image.load("bouncy_images/familia_topo/luz1_4.png"), (1250, 150))
				luz2_1 = transform.scale(image.load("bouncy_images/familia_topo/luz2_1.png"), (1250, 150))
				luz2_2 = transform.scale(image.load("bouncy_images/familia_topo/luz2_2.png"), (1250, 150))
				luz2_3 = transform.scale(image.load("bouncy_images/familia_topo/luz2_3.png"), (1250, 150))
				luz2_4 = transform.scale(image.load("bouncy_images/familia_topo/luz2_4.png"), (1250, 150))
				luz3_1 = transform.scale(image.load("bouncy_images/familia_topo/luz3_1.png"), (1250, 150))
				luz3_2 = transform.scale(image.load("bouncy_images/familia_topo/luz3_2.png"), (1250, 150))
				luz3_3 = transform.scale(image.load("bouncy_images/familia_topo/luz3_3.png"), (1250, 150))
				luz3_4 = transform.scale(image.load("bouncy_images/familia_topo/luz3_4.png"), (1250, 150))
				luz1_1r = transform.scale(image.load("bouncy_images/familia_topo/luz1_1r.png"), (1250, 150))
				luz1_2r = transform.scale(image.load("bouncy_images/familia_topo/luz1_2r.png"), (1250, 150))
				luz1_3r = transform.scale(image.load("bouncy_images/familia_topo/luz1_3r.png"), (1250, 150))
				luz1_4r = transform.scale(image.load("bouncy_images/familia_topo/luz1_4r.png"), (1250, 150))
				luz2_1r = transform.scale(image.load("bouncy_images/familia_topo/luz2_1r.png"), (1250, 150))
				luz2_2r = transform.scale(image.load("bouncy_images/familia_topo/luz2_2r.png"), (1250, 150))
				luz2_3r = transform.scale(image.load("bouncy_images/familia_topo/luz2_3r.png"), (1250, 150))
				luz2_4r = transform.scale(image.load("bouncy_images/familia_topo/luz2_4r.png"), (1250, 150))
				luz3_1r = transform.scale(image.load("bouncy_images/familia_topo/luz3_1r.png"), (1250, 150))
				luz3_2r = transform.scale(image.load("bouncy_images/familia_topo/luz3_2r.png"), (1250, 150))
				luz3_3r = transform.scale(image.load("bouncy_images/familia_topo/luz3_3r.png"), (1250, 150))
				luz3_4r = transform.scale(image.load("bouncy_images/familia_topo/luz3_4r.png"), (1250, 150))
				luz12_1 = transform.scale(image.load("bouncy_images/familia_topo/luz12_1.png"), (1250, 150))
				luz12_2 = transform.scale(image.load("bouncy_images/familia_topo/luz12_2.png"), (1250, 150))
				luz12_3 = transform.scale(image.load("bouncy_images/familia_topo/luz12_3.png"), (1250, 150))
				luz12_4 = transform.scale(image.load("bouncy_images/familia_topo/luz12_4.png"), (1250, 150))
				luz13_1 = transform.scale(image.load("bouncy_images/familia_topo/luz13_1.png"), (1250, 150))
				luz13_2 = transform.scale(image.load("bouncy_images/familia_topo/luz13_2.png"), (1250, 150))
				luz13_3 = transform.scale(image.load("bouncy_images/familia_topo/luz13_3.png"), (1250, 150))
				luz13_4 = transform.scale(image.load("bouncy_images/familia_topo/luz13_4.png"), (1250, 150))
				luz23_1 = transform.scale(image.load("bouncy_images/familia_topo/luz23_1.png"), (1250, 150))
				luz23_2 = transform.scale(image.load("bouncy_images/familia_topo/luz23_2.png"), (1250, 150))
				luz23_3 = transform.scale(image.load("bouncy_images/familia_topo/luz23_3.png"), (1250, 150))
				luz23_4 = transform.scale(image.load("bouncy_images/familia_topo/luz23_4.png"), (1250, 150))
				luz12_1r = transform.scale(image.load("bouncy_images/familia_topo/luz12_1r.png"), (1250, 150))
				luz12_2r = transform.scale(image.load("bouncy_images/familia_topo/luz12_2r.png"), (1250, 150))
				luz12_3r = transform.scale(image.load("bouncy_images/familia_topo/luz12_3r.png"), (1250, 150))
				luz12_4r = transform.scale(image.load("bouncy_images/familia_topo/luz12_4r.png"), (1250, 150))
				luz13_1r = transform.scale(image.load("bouncy_images/familia_topo/luz13_1r.png"), (1250, 150))
				luz13_2r = transform.scale(image.load("bouncy_images/familia_topo/luz13_2r.png"), (1250, 150))
				luz13_3r = transform.scale(image.load("bouncy_images/familia_topo/luz13_3r.png"), (1250, 150))
				luz13_4r = transform.scale(image.load("bouncy_images/familia_topo/luz13_4r.png"), (1250, 150))
				luz23_1r = transform.scale(image.load("bouncy_images/familia_topo/luz23_1r.png"), (1250, 150))
				luz23_2r = transform.scale(image.load("bouncy_images/familia_topo/luz23_2r.png"), (1250, 150))
				luz23_3r = transform.scale(image.load("bouncy_images/familia_topo/luz23_3r.png"), (1250, 150))
				luz23_4r = transform.scale(image.load("bouncy_images/familia_topo/luz23_4r.png"), (1250, 150))
				minitopo1 = transform.scale(image.load("bouncy_images/minitopo/minitopo1.png"), (150, 50))
				minitopo2 = transform.scale(image.load("bouncy_images/minitopo/minitopo2.png"), (150, 50))
				minitopo1_reverse = transform.scale(image.load("bouncy_images/minitopo/minitopo1_reverse.png"), (150, 50))
				minitopo2_reverse = transform.scale(image.load("bouncy_images/minitopo/minitopo2_reverse.png"), (150, 50))
				familia_topo_x = 15
				familia_topo_y = 0
				minitopo1_x = 0
				minitopo1_y = 680
				minitopo2_x = 0
				minitopo2_y = 680
				bloque1 = transform.scale(image.load("bouncy_images/bloque/bloque1.png"), (50, 50))
				bloque2 = transform.scale(image.load("bouncy_images/bloque/bloque2.png"), (50, 50))
				ataud1 = transform.scale(image.load("bouncy_images/personaje/ataud1.png"), (120, 20))
				ataud2 = transform.scale(image.load("bouncy_images/personaje/ataud2.png"), (120, 20))
				ataud3 = transform.scale(image.load("bouncy_images/personaje/ataud3.png"), (120, 20))
				ball1 = transform.scale(image.load("bouncy_images/bola/bola1.png"), (20, 20))
				ball2 = transform.scale(image.load("bouncy_images/bola/bola2.png"), (20, 20))
				ball3 = transform.scale(image.load("bouncy_images/bola/bola3.png"), (20, 20))
				ball4 = transform.scale(image.load("bouncy_images/bola/bola4.png"), (20, 20))
				marco_pausa = transform.scale(image.load("bouncy_images/marco_pausa.png"), (500, 500))
				imagenes = True
			if level != 5 and level != 10:
				screen.blit(bloque1, (bloque1_1.x, bloque1_1.y))
				screen.blit(bloque1, (bloque2_1.x, bloque2_1.y))
				screen.blit(bloque1, (bloque3_1.x, bloque3_1.y))
				screen.blit(bloque1, (bloque4_1.x, bloque4_1.y))
				screen.blit(bloque1, (bloque5_1.x, bloque5_1.y))
				screen.blit(bloque1, (bloque6_1.x, bloque6_1.y))
				screen.blit(bloque1, (bloque7_1.x, bloque7_1.y))
				screen.blit(bloque1, (bloque8_1.x, bloque8_1.y))
				screen.blit(bloque1, (bloque9_1.x, bloque9_1.y))
				screen.blit(bloque1, (bloque10_1.x, bloque10_1.y))
				screen.blit(bloque1, (bloque11_1.x, bloque11_1.y))
				screen.blit(bloque1, (bloque12_1.x, bloque12_1.y))
				screen.blit(bloque1, (bloque13_1.x, bloque13_1.y))
				screen.blit(bloque1, (bloque14_1.x, bloque14_1.y))
				screen.blit(bloque1, (bloque15_1.x, bloque15_1.y))
				screen.blit(bloque1, (bloque16_1.x, bloque16_1.y))
				screen.blit(bloque1, (bloque17_1.x, bloque17_1.y))
				screen.blit(bloque1, (bloque18_1.x, bloque18_1.y))
				screen.blit(bloque1, (bloque19_1.x, bloque19_1.y))
				screen.blit(bloque1, (bloque20_1.x, bloque20_1.y))
				screen.blit(bloque1, (bloque21_1.x, bloque21_1.y))
				screen.blit(bloque1, (bloque22_1.x, bloque22_1.y))
				screen.blit(bloque1, (bloque23_1.x, bloque23_1.y))
				screen.blit(bloque1, (bloque24_1.x, bloque24_1.y))
				screen.blit(bloque1, (bloque25_1.x, bloque25_1.y))
				screen.blit(bloque2, (bloque1_2.x, bloque1_2.y))
				screen.blit(bloque2, (bloque2_2.x, bloque2_2.y))
				screen.blit(bloque2, (bloque3_2.x, bloque3_2.y))
				screen.blit(bloque2, (bloque4_2.x, bloque4_2.y))
				screen.blit(bloque2, (bloque5_2.x, bloque5_2.y))
				screen.blit(bloque2, (bloque6_2.x, bloque6_2.y))
				screen.blit(bloque2, (bloque7_2.x, bloque7_2.y))
				screen.blit(bloque2, (bloque8_2.x, bloque8_2.y))
				screen.blit(bloque2, (bloque9_2.x, bloque9_2.y))
				screen.blit(bloque2, (bloque10_2.x, bloque10_2.y))
				screen.blit(bloque2, (bloque11_2.x, bloque11_2.y))
				screen.blit(bloque2, (bloque12_2.x, bloque12_2.y))
				screen.blit(bloque2, (bloque13_2.x, bloque13_2.y))
				screen.blit(bloque2, (bloque14_2.x, bloque14_2.y))
				screen.blit(bloque2, (bloque15_2.x, bloque15_2.y))
				screen.blit(bloque2, (bloque16_2.x, bloque16_2.y))
				screen.blit(bloque2, (bloque17_2.x, bloque17_2.y))
				screen.blit(bloque2, (bloque18_2.x, bloque18_2.y))
				screen.blit(bloque2, (bloque19_2.x, bloque19_2.y))
				screen.blit(bloque2, (bloque20_2.x, bloque20_2.y))
				screen.blit(bloque2, (bloque21_2.x, bloque21_2.y))
				screen.blit(bloque2, (bloque22_2.x, bloque22_2.y))
				screen.blit(bloque2, (bloque23_2.x, bloque23_2.y))
				screen.blit(bloque2, (bloque24_2.x, bloque24_2.y))
				screen.blit(bloque2, (bloque25_2.x, bloque25_2.y))
				screen.blit(bloque2, (bloque1_3.x, bloque1_3.y))
				screen.blit(bloque2, (bloque2_3.x, bloque2_3.y))
				screen.blit(bloque2, (bloque3_3.x, bloque3_3.y))
				screen.blit(bloque2, (bloque4_3.x, bloque4_3.y))
				screen.blit(bloque2, (bloque5_3.x, bloque5_3.y))
				screen.blit(bloque2, (bloque6_3.x, bloque6_3.y))
				screen.blit(bloque2, (bloque7_3.x, bloque7_3.y))
				screen.blit(bloque2, (bloque8_3.x, bloque8_3.y))
				screen.blit(bloque2, (bloque9_3.x, bloque9_3.y))
				screen.blit(bloque2, (bloque10_3.x, bloque10_3.y))
				screen.blit(bloque2, (bloque11_3.x, bloque11_3.y))
				screen.blit(bloque2, (bloque12_3.x, bloque12_3.y))
				screen.blit(bloque2, (bloque13_3.x, bloque13_3.y))
				screen.blit(bloque2, (bloque14_3.x, bloque14_3.y))
				screen.blit(bloque2, (bloque15_3.x, bloque15_3.y))
				screen.blit(bloque2, (bloque16_3.x, bloque16_3.y))
				screen.blit(bloque2, (bloque17_3.x, bloque17_3.y))
				screen.blit(bloque2, (bloque18_3.x, bloque18_3.y))
				screen.blit(bloque2, (bloque19_3.x, bloque19_3.y))
				screen.blit(bloque2, (bloque20_3.x, bloque20_3.y))
				screen.blit(bloque2, (bloque21_3.x, bloque21_3.y))
				screen.blit(bloque2, (bloque22_3.x, bloque22_3.y))
				screen.blit(bloque2, (bloque23_3.x, bloque23_3.y))
				screen.blit(bloque2, (bloque24_3.x, bloque24_3.y))
				screen.blit(bloque2, (bloque25_3.x, bloque25_3.y))
			if plataforma.vidas == 3:
				screen.blit(ataud1, (plataforma.x, plataforma.y))
			if plataforma.vidas == 2:
				screen.blit(ataud2, (plataforma.x, plataforma.y))
			if plataforma.vidas == 1:
				screen.blit(ataud3, (plataforma.x, plataforma.y))
			ball += 1
			if ball >= 0 and ball < 25:
				screen.blit(ball1, (bola.x, bola.y))
			if ball >= 25 and ball < 50:
				screen.blit(ball2, (bola.x, bola.y))
			if ball >= 50 and ball < 75:
				screen.blit(ball3, (bola.x, bola.y))
			if ball >= 75:
				screen.blit(ball4, (bola.x, bola.y))
				if ball >= 100:
					ball = 0
			#NIVELES
			#NIVEL 1 ROMPER BLOQUES
			if level == 1:
				if numero_bloques <= 0:
					level = 2
					numero_bloques = 75
					change_level = True
			#NIVEL 2 BOMBAS
			if level == 2:
				plataforma.puntuacion = 0
				huesos += 1
				animacion += 1
				esqueleto1_x = bloque9_1.x
				esqueleto1_y = bloque9_1.y
				esqueleto2_x = bloque17_1.x
				esqueleto2_y = bloque17_1.y
				esqueleto3_x = bloque1_2.x
				esqueleto3_y = bloque1_2.y
				esqueleto4_x = bloque25_2.x
				esqueleto4_y = bloque25_2.y
				if not pause:
					bloque9_1.LanzarBomba(plataforma)
					bloque17_1.LanzarBomba(plataforma)
					bloque1_2.LanzarBomba(plataforma)
					bloque25_2.LanzarBomba(plataforma)
				hueso1_x = bloque9_1.bomba.x - 5
				hueso1_y = bloque9_1.bomba.y - 5
				hueso2_x = bloque17_1.bomba.x - 5
				hueso2_y = bloque17_1.bomba.y - 5
				hueso3_x = bloque1_2.bomba.x - 5
				hueso3_y = bloque1_2.bomba.y - 5
				hueso4_x = bloque25_2.bomba.x - 5
				hueso4_y = bloque25_2.bomba.y - 5
				if numero_bloques <= 0:
					level = 3
					numero_bloques = 75
					change_level = True
				if huesos >= 0 and huesos < 50:
					screen.blit(hueso1, (hueso1_x, hueso1_y))
					screen.blit(hueso1, (hueso2_x, hueso2_y))
					screen.blit(hueso1, (hueso3_x, hueso3_y))
					screen.blit(hueso1, (hueso4_x, hueso4_y))
				if huesos >= 50 and huesos < 100:
					screen.blit(hueso2, (hueso1_x, hueso1_y))
					screen.blit(hueso2, (hueso2_x, hueso2_y))
					screen.blit(hueso2, (hueso3_x, hueso3_y))
					screen.blit(hueso2, (hueso4_x, hueso4_y))
				if huesos >= 100 and huesos < 150:
					screen.blit(hueso3, (hueso1_x, hueso1_y))
					screen.blit(hueso3, (hueso2_x, hueso2_y))
					screen.blit(hueso3, (hueso3_x, hueso3_y))
					screen.blit(hueso3, (hueso4_x, hueso4_y))
				if huesos >= 150:
					screen.blit(hueso4, (hueso1_x, hueso1_y))
					screen.blit(hueso4, (hueso2_x, hueso2_y))
					screen.blit(hueso4, (hueso3_x, hueso3_y))
					screen.blit(hueso4, (hueso4_x, hueso4_y))
					if huesos >= 200:
						huesos = 0
				if animacion >= 0 and animacion < 200:
					screen.blit(esqueleto1, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto1, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto1, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto1, (esqueleto4_x, esqueleto4_y))
				if animacion >= 200 and animacion < 400:
					screen.blit(esqueleto2, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto2, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto2, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto2, (esqueleto4_x, esqueleto4_y))
					if animacion == 399:
						animacion = 0
			#NIVEL 3 BOOMERANGS
			if level == 3:
				plataforma.puntuacion = 0
				huesos += 1
				animacion += 1
				esqueleto1_x = bloque11_1.x
				esqueleto1_y = bloque11_1.y
				esqueleto2_x = bloque15_1.x
				esqueleto2_y = bloque15_1.y
				esqueleto3_x = bloque1_3.x
				esqueleto3_y = bloque1_3.y
				esqueleto4_x = bloque25_3.x
				esqueleto4_y = bloque25_3.y
				fantasma1_x = bloque6_2.x - 5
				fantasma1_y = bloque6_2.y - 5
				fantasma2_x = bloque20_2.x - 5
				fantasma2_y = bloque20_2.y - 5
				if not pause:
					bloque11_1.LanzarBomba(plataforma)
					bloque15_1.LanzarBomba(plataforma)
					bloque1_3.LanzarBomba(plataforma)
					bloque25_3.LanzarBomba(plataforma)
					bloque6_2.LanzarBoomerang(plataforma, invertir)
					bloque20_2.LanzarBoomerang(plataforma, invertir)
				hueso1_x = bloque11_1.bomba.x - 5
				hueso1_y = bloque11_1.bomba.y - 5
				hueso2_x = bloque15_1.bomba.x - 5
				hueso2_y = bloque15_1.bomba.y - 5
				hueso3_x = bloque1_3.bomba.x - 5
				hueso3_y = bloque1_3.bomba.y - 5
				hueso4_x = bloque25_3.bomba.x - 5
				hueso4_y = bloque25_3.bomba.y - 5
				llama1_x = bloque6_2.boomerang.x - 5
				llama1_y = bloque6_2.boomerang.y - 5
				llama2_x = bloque20_2.boomerang.x - 5
				llama2_y = bloque20_2.boomerang.y - 5
				if numero_bloques <= 0:
					level = 4
					numero_bloques = 75
					z = 1
					change_level = True
				if huesos >= 0 and huesos < 50:
					screen.blit(hueso1, (hueso1_x, hueso1_y))
					screen.blit(hueso1, (hueso2_x, hueso2_y))
					screen.blit(hueso1, (hueso3_x, hueso3_y))
					screen.blit(hueso1, (hueso4_x, hueso4_y))
					screen.blit(llama1, (llama1_x, llama1_y))
					screen.blit(llama1, (llama2_x, llama2_y))
				if huesos >= 50 and huesos < 100:
					screen.blit(hueso2, (hueso1_x, hueso1_y))
					screen.blit(hueso2, (hueso2_x, hueso2_y))
					screen.blit(hueso2, (hueso3_x, hueso3_y))
					screen.blit(hueso2, (hueso4_x, hueso4_y))
					screen.blit(llama1, (llama1_x, llama1_y))
					screen.blit(llama1, (llama2_x, llama2_y))
				if huesos >= 100 and huesos < 150:
					screen.blit(hueso3, (hueso1_x, hueso1_y))
					screen.blit(hueso3, (hueso2_x, hueso2_y))
					screen.blit(hueso3, (hueso3_x, hueso3_y))
					screen.blit(hueso3, (hueso4_x, hueso4_y))
					screen.blit(llama2, (llama1_x, llama1_y))
					screen.blit(llama2, (llama2_x, llama2_y))
				if huesos >= 150:
					screen.blit(hueso4, (hueso1_x, hueso1_y))
					screen.blit(hueso4, (hueso2_x, hueso2_y))
					screen.blit(hueso4, (hueso3_x, hueso3_y))
					screen.blit(hueso4, (hueso4_x, hueso4_y))
					screen.blit(llama2, (llama1_x, llama1_y))
					screen.blit(llama2, (llama2_x, llama2_y))
					if huesos >= 200:
						huesos = 0
				if animacion >= 0 and animacion < 200:
					screen.blit(esqueleto1, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto1, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto1, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto1, (esqueleto4_x, esqueleto4_y))
					screen.blit(fantasma1, (fantasma1_x, fantasma1_y))
					screen.blit(fantasma1, (fantasma2_x, fantasma2_y))
				if animacion >= 200 and animacion < 400:
					screen.blit(esqueleto2, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto2, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto2, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto2, (esqueleto4_x, esqueleto4_y))
					screen.blit(fantasma2, (fantasma1_x, fantasma1_y))
					screen.blit(fantasma2, (fantasma2_x, fantasma2_y))
					if animacion == 399:
						animacion = 0
			#LEVEL 4 PUNTUACION EN X TIEMPO
			if level == 4:
				tiempo += 1
				huesos += 1
				animacion += 1
				bloque1_3.y = 100
				bloque2_3.y = 100
				bloque3_3.y = 100
				bloque4_3.y = 100
				bloque5_3.y = 100
				bloque6_3.y = 100
				bloque7_3.y = 100
				bloque8_3.y = 100
				bloque9_3.y = 100
				bloque10_3.y = 100
				bloque11_3.y = 100
				bloque12_3.y = 100
				bloque13_3.y = 100
				bloque14_3.y = 100
				bloque15_3.y = 100
				bloque16_3.y = 100
				bloque17_3.y = 100
				bloque18_3.y = 100
				bloque19_3.y = 100
				bloque20_3.y = 100
				bloque21_3.y = 100
				bloque22_3.y = 100
				bloque23_3.y = 100
				bloque24_3.y = 100
				bloque25_3.y = 100
				numero_bloques = 75
				bloque5_3.bomba.y = bloque5_1.bomba.y + 100
				bloque21_3.bomba.y = bloque21_1.bomba.y + 100
				esqueleto1_x = bloque5_1.x
				esqueleto1_y = bloque5_1.y
				esqueleto2_x = bloque5_3.x
				esqueleto2_y = bloque5_3.y
				esqueleto3_x = bloque21_1.x
				esqueleto3_y = bloque21_1.y
				esqueleto4_x = bloque21_3.x
				esqueleto4_y = bloque21_3.y
				fantasma1_x = bloque1_2.x - 5
				fantasma1_y = bloque1_2.y - 5
				fantasma2_x = bloque10_2.x - 5
				fantasma2_y = bloque10_2.y - 5
				fantasma3_x = bloque16_2.x - 5
				fantasma3_y = bloque16_2.y - 5
				fantasma4_x = bloque25_2.x - 5
				fantasma4_y = bloque25_2.y - 5
				if not pause:
					bloque5_1.LanzarBomba(plataforma)
					bloque5_3.LanzarBomba(plataforma)
					bloque21_1.LanzarBomba(plataforma)
					bloque21_3.LanzarBomba(plataforma)
					bloque1_2.LanzarBoomerang(plataforma, invertir)
					bloque10_2.LanzarBoomerang(plataforma, invertir)
					bloque16_2.LanzarBoomerang(plataforma, invertir)
					bloque25_2.LanzarBoomerang(plataforma, invertir)
				hueso1_x = bloque5_1.bomba.x - 5
				hueso1_y = bloque5_1.bomba.y - 5
				hueso2_x = bloque5_3.bomba.x - 5
				hueso2_y = bloque5_3.bomba.y - 5
				hueso3_x = bloque21_1.bomba.x - 5
				hueso3_y = bloque21_1.bomba.y - 5
				hueso4_x = bloque21_3.bomba.x - 5
				hueso4_y = bloque21_3.bomba.y - 5
				llama1_x = bloque1_2.boomerang.x - 5
				llama1_y = bloque1_2.boomerang.y - 5
				llama2_x = bloque10_2.boomerang.x - 5
				llama2_y = bloque10_2.boomerang.y - 5
				llama3_x = bloque16_2.boomerang.x - 5
				llama3_y = bloque16_2.boomerang.y - 5
				llama4_x = bloque25_2.boomerang.x - 5
				llama4_y = bloque25_2.boomerang.y - 5
				if plataforma.vidas == 2 or plataforma.vidas == 1:
					plataforma.puntuacion -= 50
					plataforma.vidas = 3
				if numero_bolas == 1:
					plataforma.puntuacion -= 100
					bola.x = plataforma.x + 60
					bola.y = plataforma.y - 20
					bola.direcciony = 1
					add_bola = True
					numero_bolas = 2
				if plataforma.puntuacion >= 4000: #5000 en 2 min se puede fácil
					level = 5
					numero_bloques = 75
					plataforma.puntuacion = 0
					change_level = True
				if tiempo >= 18000 and plataforma.puntuacion < 4000: #18000 = 1 min
					tiempo = 0
					change_level = True
				if huesos >= 0 and huesos < 50:
					screen.blit(hueso1, (hueso1_x, hueso1_y))
					screen.blit(hueso1, (hueso2_x, hueso2_y))
					screen.blit(hueso1, (hueso3_x, hueso3_y))
					screen.blit(hueso1, (hueso4_x, hueso4_y))
					screen.blit(llama1, (llama1_x, llama1_y))
					screen.blit(llama1, (llama2_x, llama2_y))
					screen.blit(llama1, (llama3_x, llama1_y))
					screen.blit(llama1, (llama4_x, llama2_y))
				if huesos >= 50 and huesos < 100:
					screen.blit(hueso2, (hueso1_x, hueso1_y))
					screen.blit(hueso2, (hueso2_x, hueso2_y))
					screen.blit(hueso2, (hueso3_x, hueso3_y))
					screen.blit(hueso2, (hueso4_x, hueso4_y))
					screen.blit(llama1, (llama1_x, llama1_y))
					screen.blit(llama1, (llama2_x, llama2_y))
					screen.blit(llama1, (llama3_x, llama1_y))
					screen.blit(llama1, (llama4_x, llama2_y))
				if huesos >= 100 and huesos < 150:
					screen.blit(hueso3, (hueso1_x, hueso1_y))
					screen.blit(hueso3, (hueso2_x, hueso2_y))
					screen.blit(hueso3, (hueso3_x, hueso3_y))
					screen.blit(hueso3, (hueso4_x, hueso4_y))
					screen.blit(llama2, (llama1_x, llama1_y))
					screen.blit(llama2, (llama2_x, llama2_y))
					screen.blit(llama2, (llama3_x, llama1_y))
					screen.blit(llama2, (llama4_x, llama2_y))
				if huesos >= 150:
					screen.blit(hueso4, (hueso1_x, hueso1_y))
					screen.blit(hueso4, (hueso2_x, hueso2_y))
					screen.blit(hueso4, (hueso3_x, hueso3_y))
					screen.blit(hueso4, (hueso4_x, hueso4_y))
					screen.blit(llama2, (llama1_x, llama1_y))
					screen.blit(llama2, (llama2_x, llama2_y))
					screen.blit(llama2, (llama3_x, llama1_y))
					screen.blit(llama2, (llama4_x, llama2_y))
					if huesos >= 200:
						huesos = 0
				if animacion >= 0 and animacion < 200:
					screen.blit(esqueleto1, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto1, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto1, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto1, (esqueleto4_x, esqueleto4_y))
					screen.blit(fantasma1, (fantasma1_x, fantasma1_y))
					screen.blit(fantasma1, (fantasma2_x, fantasma2_y))
					screen.blit(fantasma1, (fantasma3_x, fantasma1_y))
					screen.blit(fantasma1, (fantasma4_x, fantasma2_y))
				if animacion >= 200 and animacion < 400:
					screen.blit(esqueleto2, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto2, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto2, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto2, (esqueleto4_x, esqueleto4_y))
					screen.blit(fantasma2, (fantasma1_x, fantasma1_y))
					screen.blit(fantasma2, (fantasma2_x, fantasma2_y))
					screen.blit(fantasma2, (fantasma3_x, fantasma1_y))
					screen.blit(fantasma2, (fantasma4_x, fantasma2_y))
					if animacion == 399:
						animacion = 0

				PUNTUACION_TEXT = main_font.render(str(plataforma.puntuacion) + " / 4000", True, (255,255,255))
				PUNTUACION_RECT = PUNTUACION_TEXT.get_rect(center=(160,25))

				if (18000 - tiempo)/60 > 300:
					if (18000 - tiempo)/60 > 600:
						minutos = "2"
						segundos = str(((18000-tiempo)/60-600)//5)
					else:
						minutos = "1"
						segundos = str(((18000-tiempo)/60-300)//5)
				else:
					minutos = "0"
					segundos = str(((18000-tiempo)/60)//5)
				if segundos[1] == ".":
					segundos = "0" + segundos[0]
				TIEMPO_TEXT = main_font.render(minutos + ":" + segundos[0] + segundos[1], True, (255,255,255))
				TIEMPO_RECT = TIEMPO_TEXT.get_rect(center=(1190,25))

				screen.blit(PUNTUACION_TEXT, PUNTUACION_RECT)
				screen.blit(TIEMPO_TEXT, TIEMPO_RECT)
			#LEVEL 5 BOSS DEL TOPO (invertir pantalla)
			if level == 5:
				animacion += 1
				if z != 100:
					barra_y = 175
					bloque5_3.rayo.x -= 37.5
					bloque13_3.rayo.x -= 20
					plataforma.puntuacion = 0
					z = 100
				if invertir == True:
					bloque1_3.y = 600
					bloque2_3.y = 600
					bloque3_3.y = 600
					bloque4_3.y = 600
					bloque5_3.y = 600
					bloque6_3.y = 600
					bloque7_3.y = 600
					bloque8_3.y = 600
					bloque9_3.y = 600
					bloque10_3.y = 600
					bloque11_3.y = 600
					bloque12_3.y = 600
					bloque13_3.y = 600
					bloque14_3.y = 600
					bloque15_3.y = 600
					bloque16_3.y = 600
					bloque17_3.y = 600
					bloque18_3.y = 600
					bloque19_3.y = 600
					bloque20_3.y = 600
					bloque21_3.y = 600
					bloque22_3.y = 600
					bloque23_3.y = 600
					bloque24_3.y = 600
					bloque25_3.y = 600
					topo_boss_y = 575
					minitopo1_y = -10
					pinchos1.pinchos.y = -50
					bloque1_3.rayo.y = 0
					bloque4_3.rayo.y = 0
					bloque21_3.rayo.y = 0
					bloque24_3.rayo.y = 0
					bloque14_3.rayo.y = 0
					bloque17_3.rayo.y = 0
					bloque8_3.rayo.y = 0
					bloque11_3.rayo.y = 0
					if plataforma.vidas <= 0:
						print('wow')
						plataforma.puntuacion = 0
						invertir = False
						a = True
						numero_bolas -= 1
						bloque1_3.y = 100
						bloque2_3.y = 100
						bloque3_3.y = 100
						bloque4_3.y = 100
						bloque5_3.y = 100
						bloque6_3.y = 100
						bloque7_3.y = 100
						bloque8_3.y = 100
						bloque9_3.y = 100
						bloque10_3.y = 100
						bloque11_3.y = 100
						bloque12_3.y = 100
						bloque13_3.y = 100
						bloque14_3.y = 100
						bloque15_3.y = 100
						bloque16_3.y = 100
						bloque17_3.y = 100
						bloque18_3.y = 100
						bloque19_3.y = 100
						bloque20_3.y = 100
						bloque21_3.y = 100
						bloque22_3.y = 100
						bloque23_3.y = 100
						bloque24_3.y = 100
						bloque25_3.y = 100
						bola.y = plataforma.y
						bola.x = plataforma.x
				else:
					bloque1_3.y = 100
					bloque2_3.y = 100
					bloque3_3.y = 100
					bloque4_3.y = 100
					bloque5_3.y = 100
					bloque6_3.y = 100
					bloque7_3.y = 100
					bloque8_3.y = 100
					bloque9_3.y = 100
					bloque10_3.y = 100
					bloque11_3.y = 100
					bloque12_3.y = 100
					bloque13_3.y = 100
					bloque14_3.y = 100
					bloque15_3.y = 100
					bloque16_3.y = 100
					bloque17_3.y = 100
					bloque18_3.y = 100
					bloque19_3.y = 100
					bloque20_3.y = 100
					bloque21_3.y = 100
					bloque22_3.y = 100
					bloque23_3.y = 100
					bloque24_3.y = 100
					bloque25_3.y = 100
				if not pause:
					if w == 1 or t == 1:
						bloque5_3.LanzarRayo(plataforma)
						if bloque5_3.rayo.vidas >= 1199:
							if w == 1:
								w = 2
							elif t == 1:
								t = 2
					if w == 2 or t == 2:
						bloque21_3.LanzarRayo(plataforma)
						if bloque21_3.rayo.vidas >= 1199:
							if w == 2:
								w = 3
							elif t == 2:
								t = 3
					if w == 3 or t == 3:
						bloque13_3.LanzarRayo(plataforma)
						if bloque13_3.rayo.vidas >= 1199:
							if w == 3:
								w = 1
							elif t == 3:
								t = 1
				if numero_pinchos == 1:
					aleatorio1 = randrange(0,22)
					pinchos1.pinchos.x = (aleatorio1 * 50) + 15
					minitopo1_x = (aleatorio1 * 50) + 15
					if t > 0:
						aleatorio2 = randrange(0,22)
						if aleatorio1 != aleatorio2 and (aleatorio1 - aleatorio2 >= 6 or aleatorio2 - aleatorio1 >= 6):
							pinchos2.pinchos.x = (aleatorio1 * 50) + 15
							minitopo2_x = (aleatorio1 * 50) + 15
					numero_pinchos = 2
				if t != 0:
					if w == 1:
						bloque13_3.rayo.vidas = bloque5_3.rayo.vidas
					elif w == 2:
						bloque5_3.rayo.vidas = bloque21_3.rayo.vidas
					elif w == 3:
						bloque21_3.rayo.vidas = bloque13_3.rayo.vidas	
				if not pause:		
					pinchos1.LanzarPinchos(plataforma, bola)
				if plataforma.puntuacion > 5000 and a == True: #5001?? tiene que ser mayor que el nivel 9 o se buguea
					InvertirPantalla(plataforma, bola, bola2, bola3, bloque1_1, bloque2_1, bloque3_1, bloque4_1, bloque5_1, bloque6_1, bloque7_1, bloque8_1, bloque9_1, bloque10_1, bloque11_1, bloque12_1, bloque13_1, bloque14_1, bloque15_1, bloque16_1, bloque17_1, bloque18_1, bloque19_1, bloque20_1, bloque21_1, bloque22_1, bloque23_1, bloque24_1, bloque1_2, bloque2_2, bloque3_2, bloque4_2, bloque5_2, bloque6_2, bloque7_2, bloque8_2, bloque9_2, bloque10_2, bloque11_2, bloque12_2, bloque13_2, bloque14_2, bloque15_2, bloque16_2, bloque17_2, bloque18_2, bloque19_2, bloque20_2, bloque21_2, bloque22_2, bloque23_2, bloque24_2, bloque1_3, bloque2_3, bloque3_3, bloque4_3, bloque5_3, bloque6_3, bloque7_3, bloque8_3, bloque9_3, bloque10_3, bloque11_3, bloque12_3, bloque13_3, bloque14_3, bloque15_3, bloque16_3, bloque17_3, bloque18_3, bloque19_3, bloque20_3, bloque21_3, bloque22_3, bloque23_3, bloque24_3)
					familia_topo_y = 575
					bola.y = plataforma.y
					bola.direcciony = 1
					barra_y = 525
					invertir = True
					a = False
				if plataforma.puntuacion >= 6000 and b == True: #se pone serio el boss
					w = 1
					t = 3
					b = False
				if invertir == False:
					if animacion >= 0 and animacion < 100:
						if t != 1 and t != 2 and t != 3:
							if w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz1_1, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo1, (familia_topo_x, familia_topo_y))
							elif w == 2:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz3_1, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo1, (familia_topo_x, familia_topo_y))
							elif w == 3:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz2_1, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo1, (familia_topo_x, familia_topo_y))
							else:
								screen.blit(familia_topo1, (familia_topo_x, familia_topo_y))
						else:
							if t == 1 and w == 2:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz12_1, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							if t == 2 and w == 3:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz23_1, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							if t == 3 and w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz13_1, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
					if animacion >= 100 and animacion < 200:
						if t != 1 and t != 2 and t != 3:
							if w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz1_2, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo2, (familia_topo_x, familia_topo_y))
							elif w == 2:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz3_2, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo2, (familia_topo_x, familia_topo_y))
							elif w == 3:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz2_2, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo2, (familia_topo_x, familia_topo_y))
							else:
								screen.blit(familia_topo2, (familia_topo_x, familia_topo_y))
						else:
							if t == 1 and w == 2:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz12_2, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							if t == 2 and w == 3:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz23_2, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							if t == 3 and w == 1:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz13_2, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
					if animacion >= 200 and animacion < 300:
						if t != 1 and t != 2 and t != 3:
							if w == 1:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz1_3, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							elif w == 2:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz3_3, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							elif w == 3:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz2_3, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							else:
								screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
						else:
							if t == 1 and w == 2:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz12_3, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							if t == 2 and w == 3:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz23_3, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							if t == 3 and w == 1:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz13_3, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
					if animacion >= 300 and animacion < 400:
						if t != 1 and t != 2 and t != 3:
							if w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz1_4, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo4, (familia_topo_x, familia_topo_y))
							elif w == 2:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz3_4, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo4, (familia_topo_x, familia_topo_y))
							elif w == 3:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz2_4, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo4, (familia_topo_x, familia_topo_y))
							else:
								screen.blit(familia_topo4, (familia_topo_x, familia_topo_y))
						else:
							if t == 1 and w == 2:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz12_4, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							if t == 2 and w == 3:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz23_4, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
							if t == 3 and w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz13_4, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3, (familia_topo_x, familia_topo_y))
						if animacion == 399:
							animacion = 0
					if pinchos1.pinchos.puntuacion >= 600 and pinchos1.pinchos.puntuacion <= 1000:
						screen.blit(minitopo2, (minitopo1_x, minitopo1_y))
					elif pinchos1.pinchos.puntuacion >= 1200 and pinchos1.pinchos.vidas == 1:
						screen.blit(minitopo1, (minitopo1_x, minitopo1_y))
				if invertir == True:
					if bola.y <= 0:
						bola.y = plataforma.y + 25
						bola.x = plataforma.x + 50
						plataforma.vidas -= 1
						bola.direcciony = 1
					if bola.y >= 500:
						bola.direcciony = -1
						plataforma.puntuacion += 200
					if pinchos1.pinchos.puntuacion >= 600 and pinchos1.pinchos.puntuacion <= 1000:
						screen.blit(minitopo2_reverse, (minitopo1_x, minitopo1_y))
					elif pinchos1.pinchos.puntuacion >= 1200 and pinchos1.pinchos.vidas == 1:
						screen.blit(minitopo1_reverse, (minitopo1_x, minitopo1_y))
					if animacion >= 0 and animacion < 100:
						if t != 1 and t != 2 and t != 3:
							if w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz3_1r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo1r, (familia_topo_x, familia_topo_y))
							elif w == 2:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz1_1r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo1r, (familia_topo_x, familia_topo_y))
							elif w == 3:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz2_1r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo1r, (familia_topo_x, familia_topo_y))
							else:
								screen.blit(familia_topo1r, (familia_topo_x, familia_topo_y))
						else:
							if t == 1 and w == 2:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz12_1r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							if t == 2 and w == 3:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz13_1r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							if t == 3 and w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz23_1r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
					if animacion >= 100 and animacion < 200:
						if t != 1 and t != 2 and t != 3:
							if w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz3_2r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo2r, (familia_topo_x, familia_topo_y))
							elif w == 2:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz1_2r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo2r, (familia_topo_x, familia_topo_y))
							elif w == 3:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz2_2r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo2r, (familia_topo_x, familia_topo_y))
							else:
								screen.blit(familia_topo2r, (familia_topo_x, familia_topo_y))
						else:
							if t == 1 and w == 2:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz12_2r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							if t == 2 and w == 3:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz13_2r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							if t == 3 and w == 1:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz23_2r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
					if animacion >= 200 and animacion < 300:
						if t != 1 and t != 2 and t != 3:
							if w == 1:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz3_3r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							elif w == 2:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz1_3r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							elif w == 3:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz2_3r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							else:
								screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
						else:
							if t == 1 and w == 2:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz12_3r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							if t == 2 and w == 3:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz13_3r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							if t == 3 and w == 1:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz23_3r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
					if animacion >= 300 and animacion < 400:
						if t != 1 and t != 2 and t != 3:
							if w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz3_4r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo4r, (familia_topo_x, familia_topo_y))
							elif w == 2:
								if (bloque21_3.rayo.vidas >= 400 and bloque21_3.rayo.vidas <= 450) or (bloque21_3.rayo.vidas >= 500 and bloque21_3.rayo.vidas <= 550) or (bloque21_3.rayo.vidas >= 600 and bloque21_3.rayo.vidas <= 650) or (bloque21_3.rayo.vidas >= 800 and bloque21_3.rayo.vidas <= 1000):
									screen.blit(luz1_4r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo4r, (familia_topo_x, familia_topo_y))
							elif w == 3:
								if (bloque13_3.rayo.vidas >= 400 and bloque13_3.rayo.vidas <= 450) or (bloque13_3.rayo.vidas >= 500 and bloque13_3.rayo.vidas <= 550) or (bloque13_3.rayo.vidas >= 600 and bloque13_3.rayo.vidas <= 650) or (bloque13_3.rayo.vidas >= 800 and bloque13_3.rayo.vidas <= 1000):
									screen.blit(luz2_4r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo4r, (familia_topo_x, familia_topo_y))
							else:
								screen.blit(familia_topo4r, (familia_topo_x, familia_topo_y))
						else:
							if t == 1 and w == 2:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz12_4r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							if t == 2 and w == 3:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz13_4r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
							if t == 3 and w == 1:
								if (bloque5_3.rayo.vidas >= 400 and bloque5_3.rayo.vidas <= 450) or (bloque5_3.rayo.vidas >= 500 and bloque5_3.rayo.vidas <= 550) or (bloque5_3.rayo.vidas >= 600 and bloque5_3.rayo.vidas <= 650) or (bloque5_3.rayo.vidas >= 800 and bloque5_3.rayo.vidas <= 1000):
									screen.blit(luz23_4r, (familia_topo_x, familia_topo_y))
								else:
									screen.blit(familia_topo3r, (familia_topo_x, familia_topo_y))
						if animacion == 399:
							animacion = 0
				barra_vida(screen, 540, barra_y, (100 - (plataforma.puntuacion/75)))
				if plataforma.puntuacion >= 7500: #7500
					level = 6
					numero_bloques = 75
					change_level = True
			#NIVEL 6 BOMBAS DIFÍCIL
			if level == 6:
				plataforma.puntuacion = 0
				huesos += 1
				animacion += 1
				esqueleto1_x = bloque5_1.x
				esqueleto1_y = bloque5_1.y
				esqueleto2_x = bloque21_1.x
				esqueleto2_y = bloque21_1.y
				esqueleto3_x = bloque1_2.x
				esqueleto3_y = bloque1_2.y
				esqueleto4_x = bloque25_2.x
				esqueleto4_y = bloque25_2.y
				esqueleto5_x = bloque9_3.x
				esqueleto5_y = bloque9_3.y
				esqueleto6_x = bloque17_3.x
				esqueleto6_y = bloque17_3.y
				esqueleto7_x = bloque13_1.x
				esqueleto7_y = bloque13_1.y
				if not pause:
					bloque5_1.LanzarBomba(plataforma)
					bloque21_1.LanzarBomba(plataforma)
					bloque1_2.LanzarBomba(plataforma)
					bloque25_2.LanzarBomba(plataforma)
					bloque9_3.LanzarBomba(plataforma)
					bloque17_3.LanzarBomba(plataforma)
					bloque13_1.LanzarBomba(plataforma)
				hueso1_x = bloque5_1.bomba.x - 5
				hueso1_y = bloque5_1.bomba.y - 5
				hueso2_x = bloque21_1.bomba.x - 5
				hueso2_y = bloque21_1.bomba.y - 5
				hueso3_x = bloque1_2.bomba.x - 5
				hueso3_y = bloque1_2.bomba.y - 5
				hueso4_x = bloque25_2.bomba.x - 5
				hueso4_y = bloque25_2.bomba.y - 5
				hueso5_x = bloque9_3.bomba.x - 5
				hueso5_y = bloque9_3.bomba.y - 5
				hueso6_x = bloque17_3.bomba.x - 5
				hueso6_y = bloque17_3.bomba.y - 5
				hueso7_x = bloque13_1.bomba.x - 5
				hueso7_y = bloque13_1.bomba.y - 5
				if numero_bloques <= 0:
					level = 7
					numero_bloques = 75
					change_level = True
				if huesos >= 0 and huesos < 50:
					screen.blit(hueso1, (hueso1_x, hueso1_y))
					screen.blit(hueso1, (hueso2_x, hueso2_y))
					screen.blit(hueso1, (hueso3_x, hueso3_y))
					screen.blit(hueso1, (hueso4_x, hueso4_y))
					screen.blit(hueso1, (hueso5_x, hueso5_y))
					screen.blit(hueso1, (hueso6_x, hueso6_y))
					screen.blit(hueso1, (hueso7_x, hueso7_y))
				if huesos >= 50 and huesos < 100:
					screen.blit(hueso2, (hueso1_x, hueso1_y))
					screen.blit(hueso2, (hueso2_x, hueso2_y))
					screen.blit(hueso2, (hueso3_x, hueso3_y))
					screen.blit(hueso2, (hueso4_x, hueso4_y))
					screen.blit(hueso2, (hueso5_x, hueso5_y))
					screen.blit(hueso2, (hueso6_x, hueso6_y))
					screen.blit(hueso2, (hueso7_x, hueso7_y))
				if huesos >= 100 and huesos < 150:
					screen.blit(hueso3, (hueso1_x, hueso1_y))
					screen.blit(hueso3, (hueso2_x, hueso2_y))
					screen.blit(hueso3, (hueso3_x, hueso3_y))
					screen.blit(hueso3, (hueso4_x, hueso4_y))
					screen.blit(hueso3, (hueso5_x, hueso5_y))
					screen.blit(hueso3, (hueso6_x, hueso6_y))
					screen.blit(hueso3, (hueso7_x, hueso7_y))
				if huesos >= 150:
					screen.blit(hueso4, (hueso1_x, hueso1_y))
					screen.blit(hueso4, (hueso2_x, hueso2_y))
					screen.blit(hueso4, (hueso3_x, hueso3_y))
					screen.blit(hueso4, (hueso4_x, hueso4_y))
					screen.blit(hueso4, (hueso5_x, hueso5_y))
					screen.blit(hueso4, (hueso6_x, hueso6_y))
					screen.blit(hueso4, (hueso7_x, hueso7_y))
					if huesos >= 200:
						huesos = 0
				if animacion >= 0 and animacion < 200:
					screen.blit(esqueleto1, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto1, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto1, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto1, (esqueleto4_x, esqueleto4_y))
					screen.blit(esqueleto1, (esqueleto5_x, esqueleto5_y))
					screen.blit(esqueleto1, (esqueleto6_x, esqueleto6_y))
					screen.blit(esqueleto1, (esqueleto7_x, esqueleto7_y))
				if animacion >= 200 and animacion < 400:
					screen.blit(esqueleto2, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto2, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto2, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto2, (esqueleto4_x, esqueleto4_y))
					screen.blit(esqueleto2, (esqueleto5_x, esqueleto5_y))
					screen.blit(esqueleto2, (esqueleto6_x, esqueleto6_y))
					screen.blit(esqueleto2, (esqueleto7_x, esqueleto7_y))
					if animacion == 399:
						animacion = 0
			#LEVEL 7 PINCHOS
			if level == 7:
				plataforma.puntuacion = 0
				if numero_pinchos == 1:
					aleatorio1 = randrange(0,22)
					aleatorio2 = randrange(0,22)
					if aleatorio1 != aleatorio2 and (aleatorio1 - aleatorio2 >= 6 or aleatorio2 - aleatorio1 >= 6):
						pinchos1.pinchos.x = (aleatorio1 * 50) + 15
						pinchos2.pinchos.x = (aleatorio2 * 50) + 15
						spider1_x = (aleatorio1 * 50) + 15
						spider2_x = (aleatorio2 * 50) + 15
						numero_pinchos = 2
				if not pause:
					pinchos1.LanzarPinchos(plataforma, bola)
					pinchos2.LanzarPinchos(plataforma, bola)
				if numero_bloques <= 0:
					level = 8
					numero_bloques = 75
					change_level = True
				if pinchos1.pinchos.puntuacion >= 600 and pinchos1.pinchos.puntuacion <= 1000:
					screen.blit(spider1, (spider1_x, spider1_y))
				elif pinchos1.pinchos.puntuacion >= 1200 and pinchos1.pinchos.vidas == 1:
					screen.blit(spider2, (spider1_x, spider1_y))
				if pinchos2.pinchos.puntuacion >= 600 and pinchos2.pinchos.puntuacion <= 1000:
					screen.blit(spider1, (spider2_x, spider2_y))
				elif pinchos2.pinchos.puntuacion >= 1200 and pinchos2.pinchos.vidas == 1:
					screen.blit(spider2, (spider2_x, spider2_y))
			#LEVEL 8 BOMBAS Y PINCHOS
			if level == 8:
				plataforma.puntuacion = 0
				huesos += 1
				animacion += 1
				esqueleto1_x = bloque1_1.x
				esqueleto1_y = bloque1_1.y
				esqueleto2_x = bloque25_1.x
				esqueleto2_y = bloque25_1.y
				esqueleto3_x = bloque7_2.x
				esqueleto3_y = bloque7_2.y
				esqueleto4_x = bloque19_2.x
				esqueleto4_y = bloque19_2.y
				if not pause:
					bloque1_1.LanzarBomba(plataforma)
					bloque25_1.LanzarBomba(plataforma)
					bloque7_2.LanzarBomba(plataforma)
					bloque19_2.LanzarBomba(plataforma)
				hueso1_x = bloque1_1.bomba.x - 5
				hueso1_y = bloque1_1.bomba.y - 5
				hueso2_x = bloque25_1.bomba.x - 5
				hueso2_y = bloque25_1.bomba.y - 5
				hueso3_x = bloque7_2.bomba.x - 5
				hueso3_y = bloque7_2.bomba.y - 5
				hueso4_x = bloque19_2.bomba.x - 5
				hueso4_y = bloque19_2.bomba.y - 5
				if numero_pinchos == 1:
					aleatorio1 = randrange(0,22)
					aleatorio2 = randrange(0,22)
					if aleatorio1 != aleatorio2 and (aleatorio1 - aleatorio2 >= 6 or aleatorio2 - aleatorio1 >= 6):
						pinchos1.pinchos.x = (aleatorio1 * 50) + 15
						pinchos2.pinchos.x = (aleatorio2 * 50) + 15
						spider1_x = (aleatorio1 * 50) + 15
						spider2_x = (aleatorio2 * 50) + 15
						numero_pinchos = 2
				if not pause:
					pinchos1.LanzarPinchos(plataforma, bola)
					#pinchos2.LanzarPinchos(plataforma, bola)
				if numero_bloques <= 0:
						level = 9
						numero_bloques = 75
						change_level = True
				if pinchos1.pinchos.puntuacion >= 600 and pinchos1.pinchos.puntuacion <= 1000:
					screen.blit(spider1, (spider1_x, spider1_y))
				elif pinchos1.pinchos.puntuacion >= 1200 and pinchos1.pinchos.vidas == 1:
					screen.blit(spider2, (spider1_x, spider1_y))
				if pinchos2.pinchos.puntuacion >= 600 and pinchos2.pinchos.puntuacion <= 1000:
					screen.blit(spider1, (spider2_x, spider2_y))
				elif pinchos2.pinchos.puntuacion >= 1200 and pinchos2.pinchos.vidas == 1:
					screen.blit(spider2, (spider2_x, spider2_y))
				if huesos >= 0 and huesos < 50:
					screen.blit(hueso1, (hueso1_x, hueso1_y))
					screen.blit(hueso1, (hueso2_x, hueso2_y))
					screen.blit(hueso1, (hueso3_x, hueso3_y))
					screen.blit(hueso1, (hueso4_x, hueso4_y))
				if huesos >= 50 and huesos < 100:
					screen.blit(hueso2, (hueso1_x, hueso1_y))
					screen.blit(hueso2, (hueso2_x, hueso2_y))
					screen.blit(hueso2, (hueso3_x, hueso3_y))
					screen.blit(hueso2, (hueso4_x, hueso4_y))
				if huesos >= 100 and huesos < 150:
					screen.blit(hueso3, (hueso1_x, hueso1_y))
					screen.blit(hueso3, (hueso2_x, hueso2_y))
					screen.blit(hueso3, (hueso3_x, hueso3_y))
					screen.blit(hueso3, (hueso4_x, hueso4_y))
				if huesos >= 150:
					screen.blit(hueso4, (hueso1_x, hueso1_y))
					screen.blit(hueso4, (hueso2_x, hueso2_y))
					screen.blit(hueso4, (hueso3_x, hueso3_y))
					screen.blit(hueso4, (hueso4_x, hueso4_y))
					if huesos >= 200:
						huesos = 0
				if animacion >= 0 and animacion < 200:
					screen.blit(esqueleto1, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto1, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto1, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto1, (esqueleto4_x, esqueleto4_y))
				if animacion >= 200 and animacion < 400:
					screen.blit(esqueleto2, (esqueleto1_x, esqueleto1_y))
					screen.blit(esqueleto2, (esqueleto2_x, esqueleto2_y))
					screen.blit(esqueleto2, (esqueleto3_x, esqueleto3_y))
					screen.blit(esqueleto2, (esqueleto4_x, esqueleto4_y))
					if animacion == 399:
						animacion = 0
			#NIVEL 9 DOS BOLAS
			if level == 9:
				plataforma.puntuacion = 0
				if z == 1:
					bola1.x = plataforma.x
					bola1.y = plataforma.y
					numero_bolas += 1
					dibujo = 1
					z = 2
				if not pause:
					bola1.Movimiento()
				bola1.Golpear_personaje(plataforma)
				bloque1_1.Rebotar(bola1, plataforma)
				bloque2_1.Rebotar(bola1, plataforma)
				bloque3_1.Rebotar(bola1, plataforma)
				bloque4_1.Rebotar(bola1, plataforma)
				bloque5_1.Rebotar(bola1, plataforma)
				bloque6_1.Rebotar(bola1, plataforma)
				bloque7_1.Rebotar(bola1, plataforma)
				bloque8_1.Rebotar(bola1, plataforma)
				bloque9_1.Rebotar(bola1, plataforma)
				bloque10_1.Rebotar(bola1, plataforma)
				bloque11_1.Rebotar(bola1, plataforma)
				bloque12_1.Rebotar(bola1, plataforma)
				bloque13_1.Rebotar(bola1, plataforma)
				bloque14_1.Rebotar(bola1, plataforma)
				bloque15_1.Rebotar(bola1, plataforma)
				bloque16_1.Rebotar(bola1, plataforma)
				bloque17_1.Rebotar(bola1, plataforma)
				bloque18_1.Rebotar(bola1, plataforma)
				bloque19_1.Rebotar(bola1, plataforma)
				bloque20_1.Rebotar(bola1, plataforma)
				bloque21_1.Rebotar(bola1, plataforma)
				bloque22_1.Rebotar(bola1, plataforma)
				bloque23_1.Rebotar(bola1, plataforma)
				bloque24_1.Rebotar(bola1, plataforma)
				bloque25_1.Rebotar(bola1, plataforma)
				bloque1_2.Rebotar(bola1, plataforma)
				bloque2_2.Rebotar(bola1, plataforma)
				bloque3_2.Rebotar(bola1, plataforma)
				bloque4_2.Rebotar(bola1, plataforma)
				bloque5_2.Rebotar(bola1, plataforma)
				bloque6_2.Rebotar(bola1, plataforma)
				bloque7_2.Rebotar(bola1, plataforma)
				bloque8_2.Rebotar(bola1, plataforma)
				bloque9_2.Rebotar(bola1, plataforma)
				bloque10_2.Rebotar(bola1, plataforma)
				bloque11_2.Rebotar(bola1, plataforma)
				bloque12_2.Rebotar(bola1, plataforma)
				bloque13_2.Rebotar(bola1, plataforma)
				bloque14_2.Rebotar(bola1, plataforma)
				bloque15_2.Rebotar(bola1, plataforma)
				bloque16_2.Rebotar(bola1, plataforma)
				bloque17_2.Rebotar(bola1, plataforma)
				bloque18_2.Rebotar(bola1, plataforma)
				bloque19_2.Rebotar(bola1, plataforma)
				bloque20_2.Rebotar(bola1, plataforma)
				bloque21_2.Rebotar(bola1, plataforma)
				bloque22_2.Rebotar(bola1, plataforma)
				bloque23_2.Rebotar(bola1, plataforma)
				bloque24_2.Rebotar(bola1, plataforma)
				bloque25_2.Rebotar(bola1, plataforma)
				bloque1_3.Rebotar(bola1, plataforma)
				bloque2_3.Rebotar(bola1, plataforma)
				bloque3_3.Rebotar(bola1, plataforma) 
				bloque4_3.Rebotar(bola1, plataforma)
				bloque5_3.Rebotar(bola1, plataforma)
				bloque6_3.Rebotar(bola1, plataforma)
				bloque7_3.Rebotar(bola1, plataforma)
				bloque8_3.Rebotar(bola1, plataforma)
				bloque9_3.Rebotar(bola1, plataforma)
				bloque10_3.Rebotar(bola1, plataforma)
				bloque11_3.Rebotar(bola1, plataforma)
				bloque12_3.Rebotar(bola1, plataforma)
				bloque13_3.Rebotar(bola1, plataforma)
				bloque14_3.Rebotar(bola1, plataforma)
				bloque15_3.Rebotar(bola1, plataforma)
				bloque16_3.Rebotar(bola1, plataforma)
				bloque17_3.Rebotar(bola1, plataforma)
				bloque18_3.Rebotar(bola1, plataforma)
				bloque19_3.Rebotar(bola1, plataforma)
				bloque20_3.Rebotar(bola1, plataforma)
				bloque21_3.Rebotar(bola1, plataforma)
				bloque22_3.Rebotar(bola1, plataforma)
				bloque23_3.Rebotar(bola1, plataforma)
				bloque24_3.Rebotar(bola1, plataforma)
				bloque25_3.Rebotar(bola1, plataforma)
				if bola1.y >= 720 and z == 2:
					plataforma.vidas -= 1
					z = 1
				if bola.y >= 720:
					bola.x = plataforma.x + 60
					bola.y = plataforma.y - 20
					add_bola = True
				if numero_bloques <= 0:
					level = 10
					numero_bloques = 75
					plataforma.puntuacion = 0
					change_level = True
				if ball >= 0 and ball < 25:
					screen.blit(ball1, (bola1.x, bola1.y))
				if ball >= 25 and ball < 50:
					screen.blit(ball2, (bola1.x, bola1.y))
				if ball >= 50 and ball < 75:
					screen.blit(ball3, (bola1.x, bola1.y))
				if ball >= 75:
					screen.blit(ball4, (bola1.x, bola1.y))
					if ball >= 100:
						ball = 0
			#LEVEL 10 FINAL BOSS (GUSANO GIGANTE)
			if level == 10:
				dibujo = 0
				animacion += 1
				bloque1_3.y = 100
				bloque2_3.y = 100
				bloque3_3.y = 100
				bloque4_3.y = 100
				bloque5_3.y = 100
				bloque6_3.y = 100
				bloque7_3.y = 100
				bloque8_3.y = 100
				bloque9_3.y = 100
				bloque10_3.y = 100
				bloque11_3.y = 100
				bloque12_3.y = 100
				bloque13_3.y = 100
				bloque14_3.y = 100
				bloque15_3.y = 100
				bloque16_3.y = 100
				bloque17_3.y = 100
				bloque18_3.y = 100
				bloque19_3.y = 100
				bloque20_3.y = 100
				bloque21_3.y = 100
				bloque22_3.y = 100
				bloque23_3.y = 100
				bloque24_3.y = 100
				bloque25_3.y = 100
				bloque8_3.bomba.y = bloque8_1.bomba.y + 100
				bloque17_3.bomba.y = bloque17_1.bomba.y + 100
				numero_bloques = 72
				if not pause:
					bloque8_1.LanzarBomba(plataforma)
					bloque17_1.LanzarBomba(plataforma)
					bloque1_2.LanzarBomba(plataforma)
					bloque25_2.LanzarBomba(plataforma)
					bloque12_2.LanzarBomba(plataforma)
					bloque13_2.LanzarBomba(plataforma)
					bloque8_3.LanzarBomba(plataforma)
					bloque17_3.LanzarBomba(plataforma)
				if numero_gusanos == 1:
					aleatorio1 = randrange(1,25)
					aleatorio2 = randrange(1,25)
					if plataforma.puntuacion >= 1000:
						aleatorio1 = randrange(7,17)
						aleatorio2 = 17
					if aleatorio1 != aleatorio2:
						gusano1_x = aleatorio1*50 - 35
						gusano2_x = aleatorio2*50 - 35
						numero_gusanos = 2
				if not pause:
					Gusanos(plataforma, bola, aleatorio1, aleatorio2)
				if plataforma.puntuacion >= 5000:
					PantallaChica(plataforma, bola)
					screen.blit(gusano1, (250, 50))
					screen.blit(gusano1, (900, 50))
					if z == 1 or z == 3:
						bola.y = plataforma.y
						bola.x = plataforma.x
						z = 4
				barra_vida(screen, 540, 175, (100 - (plataforma.puntuacion/100)))
				if animacion >= 0 and animacion < 100:
					screen.blit(gusano1, (gusano1_x, gusano1_y))
					screen.blit(gusano1, (gusano2_x, gusano2_y))
					screen.blit(boss1, (0, 0))
				if animacion >= 100 and animacion < 200:
					screen.blit(gusano2, (gusano1_x, gusano1_y))
					screen.blit(gusano2, (gusano2_x, gusano2_y))
					screen.blit(boss2, (0, 0))
				if animacion >= 200 and animacion < 300:
					screen.blit(gusano1, (gusano1_x, gusano1_y))
					screen.blit(gusano1, (gusano2_x, gusano2_y))
					screen.blit(boss3, (0, 0))
				if animacion >= 300 and animacion < 400:
					screen.blit(gusano2, (gusano1_x, gusano1_y))
					screen.blit(gusano2, (gusano2_x, gusano2_y))
					screen.blit(boss4, (0, 0))
				if animacion >= 400 and animacion < 500:
					screen.blit(gusano1, (gusano1_x, gusano1_y))
					screen.blit(gusano1, (gusano2_x, gusano2_y))
					screen.blit(boss1, (0, 0))
				if animacion >= 500 and animacion < 600:
					screen.blit(gusano2, (gusano1_x, gusano1_y))
					screen.blit(gusano2, (gusano2_x, gusano2_y))
					screen.blit(boss2, (0, 0))
				if animacion >= 600 and animacion < 700:
					screen.blit(gusano1, (gusano1_x, gusano1_y))
					screen.blit(gusano1, (gusano2_x, gusano2_y))
					screen.blit(boss7, (0, 0))
				if animacion >= 700 and animacion < 800:
					screen.blit(gusano2, (gusano1_x, gusano1_y))
					screen.blit(gusano2, (gusano2_x, gusano2_y))
					screen.blit(boss8, (0, 0))
					if animacion == 799:
						animacion = 0
				if plataforma.puntuacion >= 10000: #10000??
					level = 11
					numero_bloques = 75
					change_level = True
			#FIN
			if level == 11:
				screen.fill((8, 2, 13))
				screen.blit(win, (400, 75))

			if plataforma.vidas <= 0:
					topo_boss_y = 0
					minitopo1_y = 680
					pinchos1.pinchos.y = 680
					bloque5_3.rayo.y = 50
					bloque13_3.rayo.y = 50
					bloque21_3.rayo.y = 50
					plataforma.y = 700
					barra_y = 175
					change_level = True
			if numero_bolas == 0 and level != 11:
				plataforma.vidas -= 1
				plataforma.x = 550
				bola.x = plataforma.x + 60
				bola.y = plataforma.y - 20
				bola.direcciony = -1
				add_bola = True
				numero_bolas = 1
		elif finish == True:
			saveloadmanager.save_game_data([level], ['level'])
			quit()
			exit()
		for evento in event.get():
			if evento.type==QUIT:
				saveloadmanager.save_game_data([level], ['level'])
				quit()
				exit()
			if evento.type==KEYDOWN:
				if evento.key == K_ESCAPE:
					saveloadmanager.save_game_data([level], ['level'])
					if pause:
						pause = False
					else:
						pause = True
				
				if evento.key == K_x:
					saveloadmanager.save_game_data([level], ['level'])
					quit()
					exit()

				if evento.key == K_1: #BAJAR VOLUMEN
					if (level == 1 or level == 6) and musica1.get_volume() > 0.0:
						musica1.set_volume(musica1.get_volume() - 0.1)
					if (level == 2 or level == 7) and musica2.get_volume() > 0.0:
						musica2.set_volume(musica2.get_volume() - 0.1)
					if (level == 3 or level == 8) and musica3.get_volume() > 0.0:
						musica3.set_volume(musica3.get_volume() - 0.1)
					if level == 4 and musica4.get_volume() > 0.0:
						musica4.set_volume(musica4.get_volume() - 0.1)
					if level == 5 and musica_boss1.get_volume() > 0.0:
						musica_boss1.set_volume(musica_boss1.get_volume() - 0.1)
					if level == 9 and musica5.get_volume() > 0.0:
						musica5.set_volume(musica5.get_volume() - 0.1)
					if level == 10 and musica_boss2.get_volume() > 0.0:
						musica_boss2.set_volume(musica_boss2.get_volume() - 0.1)

				if evento.key == K_2: #SUBIR VOLUMEN
					if (level == 1 or level == 6) and musica1.get_volume() > 0.0:
						musica1.set_volume(musica1.get_volume() + 0.1)
					if (level == 2 or level == 7) and musica2.get_volume() > 0.0:
						musica2.set_volume(musica2.get_volume() + 0.1)
					if (level == 3 or level == 8) and musica3.get_volume() > 0.0:
						musica3.set_volume(musica3.get_volume() + 0.1)
					if level == 4 and musica4.get_volume() > 0.0:
						musica4.set_volume(musica4.get_volume() + 0.1)
					if level == 5 and musica_boss1.get_volume() > 0.0:
						musica_boss1.set_volume(musica_boss1.get_volume() + 0.1)
					if level == 9 and musica5.get_volume() > 0.0:
						musica5.set_volume(musica5.get_volume() + 0.1)
					if level == 10 and musica_boss2.get_volume() > 0.0:
						musica_boss2.set_volume(musica_boss2.get_volume() + 0.1)

				if evento.key == K_0: #MUTE
					if level == 1 or level == 6:
						musica1.set_volume(0.0)
					if level == 2 or level == 7:
						musica2.set_volume(0.0)
					if level == 3 or level == 8:
						musica3.set_volume(0.0)
					if level == 4:
						musica4.set_volume(0.0)
					if level == 5:
						musica_boss1.set_volume(0.0)
					if level == 9:
						musica5.set_volume(0.0)
					if level == 10:
						musica_boss2.set_volume(0.0)
				
				if evento.key == K_9: #DESMUTE
					if level == 1 or level == 6:
						musica1.set_volume(1.0)
					if level == 2 or level == 7:
						musica2.set_volume(1.0)
					if level == 3 or level == 8:
						musica3.set_volume(1.0)
					if level == 4:
						musica4.set_volume(1.0)
					if level == 5:
						musica_boss1.set_volume(1.0)
					if level == 9:
						musica5.set_volume(1.0)
					if level == 10:
						musica_boss2.set_volume(1.0)
		if pause:
			draw_pause(marco_pausa)					
		display.update()
		display.flip()
def options(): #OPTIONS
	global musica_menu
	while True:
		screen.fill((16, 4, 26))
		mouse_pos = mouse.get_pos()
		
		MOVE_TEXT = main_font.render('MOVE:', True, (152, 110, 194))
		MOVE_RECT = MOVE_TEXT.get_rect(center=(100,75))
		MUSIC_TEXT = main_font.render('MUSIC:', True, (152, 110, 194))
		MUSIC_RECT = MUSIC_TEXT.get_rect(center=(112.5,350))

		LEFT_TEXT = main_font.render('LEFT:', True, (194, 184, 204))
		LEFT_RECT = LEFT_TEXT.get_rect(center=(150,150))
		RIGHT_TEXT = main_font.render('RIGHT:', True, (194, 184, 204))
		RIGHT_RECT = RIGHT_TEXT.get_rect(center=(162.5,225))

		LOW_TEXT = main_font.render('LOW:   1', True, (194, 184, 204))
		LOW_RECT = LOW_TEXT.get_rect(center=(175,425))
		UP_TEXT = main_font.render('UP:       2', True, (194, 184, 204))
		UP_RECT = UP_TEXT.get_rect(center=(175,500))
		UNMUTE_TEXT = main_font.render('UNMUTE:   9', True, (194, 184, 204))
		UNMUTE_RECT = UNMUTE_TEXT.get_rect(center=(640,425))
		MUTE_TEXT = main_font.render('MUTE:         0', True, (194, 184, 204))
		MUTE_RECT = MUTE_TEXT.get_rect(center=(640,500))

		EXIT_BUTTON = Button(image=transform.scale(image.load("bouncy_images/rect.png"), (200, 100)), pos=(640,650), text_input='EXIT', font=main_font, base_color=(255, 255, 255), hovering_color=(194, 184, 204))
		
		screen.blit(flecha_left, (275,100))
		screen.blit(flecha_right, (275,175))
		screen.blit(MOVE_TEXT, MOVE_RECT)
		screen.blit(MUSIC_TEXT, MUSIC_RECT)
		screen.blit(LEFT_TEXT, LEFT_RECT)
		screen.blit(RIGHT_TEXT, RIGHT_RECT)
		screen.blit(LOW_TEXT, LOW_RECT)
		screen.blit(UP_TEXT, UP_RECT)
		screen.blit(UNMUTE_TEXT, UNMUTE_RECT)
		screen.blit(MUTE_TEXT, MUTE_RECT)
		
		for button in [EXIT_BUTTON]:
			button.changeColor(mouse_pos)
			button.update(screen)

		for evento in event.get():
			if evento.type == QUIT:
				quit()
				exit()
			if evento.type == KEYDOWN:
				if evento.key == K_1 and musica_menu.get_volume() > 0.0:
					musica_menu.set_volume(musica_menu.get_volume() - 0.1)
				if evento.key == K_2 and musica_menu.get_volume() > 0.0:
					musica_menu.set_volume(musica_menu.get_volume() + 0.1)
				if evento.key == K_0:
					musica_menu.set_volume(0.0)
				if evento.key == K_9:
					musica_menu.set_volume(1.0)
			if evento.type == MOUSEBUTTONDOWN:
				if EXIT_BUTTON.checkForInput(mouse_pos):
					main_menu()
		display.update()

def main_menu(): #MAIN MENU SCREEN
	global loading_finished, loading_progress, musica_menu
	volume_musica_menu = 0
	if volume_musica_menu == 0:
		musica_menu = mixer.Sound('bouncy_images/musica/musica_menu.ogg')
		volume_musica_menu = 1
	while True:
		if volume_musica_menu == 1:
			musica_menu.set_volume(0.5)
			volume_musica_menu = 2
		musica_menu.play()

		screen.blit(background, (0,0))
		mouse_pos = mouse.get_pos()

		MENU_TEXT = main_font.render('BOUNCY TOMB', True, (152, 110, 194))
		MENU_RECT = MENU_TEXT.get_rect(center=(640,75))

		PLAY_BUTTON = Button(image=transform.scale(image.load("bouncy_images/rect.png"), (200, 100)), pos=(640,200), text_input='PLAY', font=main_font, base_color=(255, 255, 255), hovering_color=(194, 184, 204))
		OPTIONS_BUTTON = Button(image=transform.scale(image.load("bouncy_images/rect.png"), (200, 100)), pos=(640,300), text_input='OPTIONS', font=main_font, base_color=(255, 255, 255), hovering_color=(194, 184, 204))
		EXIT_BUTTON = Button(image=transform.scale(image.load("bouncy_images/rect.png"), (200, 100)), pos=(640,400), text_input='EXIT', font=main_font, base_color=(255, 255, 255), hovering_color=(194, 184, 204))

		screen.blit(MENU_TEXT, MENU_RECT)

		for button in [PLAY_BUTTON, OPTIONS_BUTTON, EXIT_BUTTON]:
			button.changeColor(mouse_pos)
			button.update(screen)

		for evento in event.get():
			if evento.type == QUIT:
				quit()
				exit()
			if evento.type == KEYDOWN:
				if evento.key == K_1 and musica_menu.get_volume() > 0.0:
					musica_menu.set_volume(musica_menu.get_volume() - 0.1)
				if evento.key == K_2 and musica_menu.get_volume() > 0.0:
					musica_menu.set_volume(musica_menu.get_volume() + 0.1)
				if evento.key == K_0:
					musica_menu.set_volume(0.0)
				if evento.key == K_9:
					musica_menu.set_volume(1.0)
			if evento.type == MOUSEBUTTONDOWN:
					if PLAY_BUTTON.checkForInput(mouse_pos):
						font_bar = font.SysFont('roboto', 100)
						clock = time.Clock()
						work = 50000000
						loading_bg = transform.scale(image.load('bouncy_images/loading_bg.png'), (760, 150))
						loading_bg_rect = loading_bg.get_rect(center=(640,360))
						loading_bar = image.load('bouncy_images/loading_bar.png')
						loading_bar_rect = loading_bar.get_rect(midleft=(280,360))
						loading_finished = False
						loading_progress = 0
						loading_bar_width = 8
						def doWork():
							global loading_finished, loading_progress
							for i in range(work):
								math_equation = 523687 / 789456 * 89456
								loading_progress = i
							loading_finished = True

						finished = font_bar.render('Done!', True, (255,255,255))
						finished_rect = finished.get_rect(center=(640,360))
						Thread(target=doWork).start()
						while True:
							for evento in event.get():
								if evento.type == QUIT:
									quit()
									exit()
		
							screen.fill((8, 2, 13))

							if not loading_finished:
								loading_bar_width = int(loading_progress / work * 720)
								loading_bar = transform.scale(loading_bar, (loading_bar_width,150))
								loading_bar_rect = loading_bar.get_rect(midleft=(280,360))

								screen.blit(loading_bg, loading_bg_rect)
								screen.blit(loading_bar, loading_bar_rect)
							else:
								musica_menu.stop()
								play()

							display.update()
							clock.tick(60)
					if OPTIONS_BUTTON.checkForInput(mouse_pos):
						options()
					if EXIT_BUTTON.checkForInput(mouse_pos):
						quit()
						exit()

		display.update()
main_menu()