from scene import *
import ui
import sound
import random
import math


apples = ['emj:Green_Apple', 'emj:Red_Apple']
min_apple_size = 35
max_apple_size = 65
one_apple_space = 80


class Tile(SpriteNode):
	def __init__(self, number, *args, **kwargs):
		SpriteNode.__init__(self, 'pzl:Button1', *args, **kwargs)
		button_font = ('Avenir Next', 20)
		self.number = number
		self.title_label = LabelNode(str(number), font=button_font, color='black', position=(0, 1), parent=self)
		

class ApplePile(Node):
	def __init__(self, *args, **kwargs): 
		Node.__init__(self, *args, **kwargs)
		self.apples = []
		circle = ui.Path.oval(0, 0, one_apple_space, one_apple_space)
		circle.line_width = 3
		self.circle = ShapeNode(circle, stroke_color='black', fill_color="B1DEE1", parent=self)
		self.choose_apple()
		
	#randomly choose red/green apple, position it inside its circle
	def choose_apple(self):
		apple = SpriteNode(apples[random.choice([0,1])], parent=self)
		r = random.uniform(apple.size.w/2, self.circle.size.w/2-apple.size.w/2)
		theta = random.uniform(0, 360)
		apple_size = random.uniform(min_apple_size, max_apple_size)
		apple.size = (apple_size, apple_size)
		apple.position = r*math.cos(theta), r*math.sin(theta)
		self.apples.append(apple)
		
		
class MyScene(Scene):
	def __init__(self, max_tile, *args, **kwargs):
		Scene.__init__(self)
		self.cur_number = 0
		self.max_tile = max_tile
		self.tiles = []
	
	def setup(self):
		self.background_color = "B1DEE1"
		tab = 0
		for i in range(1, self.max_tile+1):
			if i != 1:
				tab = 20
			tile = Tile(i, parent=self)
			tile.size = (50.0, 50.0)
			tile.position = (tile.size.w + (i-1)*tile.size.w + tab, self.size.h - tile.size.h)	
			self.tiles.append(tile)
		pile = ApplePile(parent=self)
		pile.position = 100, 100

	
	def touch_began(self, touch):
		touch_loc = self.point_from_scene(touch.location)
		for t in self.tiles:
			#if a button is clicked, highlight it
			if touch_loc in t.frame:
				sound.play_effect('8ve:8ve-tap-resonant')
				t.texture = Texture('pzl:Button2')
				t.size = (50.0, 50.0)
				self.cur_number = t.number
				#unhighlight all other buttons
				for t in self.tiles:
					if touch_loc not in t.frame:
						t.texture = Texture('pzl:Button1')
						t.size = (50.0, 50.0)

						
if __name__ == '__main__':
	run(MyScene(2))
