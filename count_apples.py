from scene import *
import ui
import sound
import random
import math
import statistics


apples = ['emj:Green_Apple', 'emj:Red_Apple']
min_apple_size = 35.0
max_apple_size = 65.0
one_apple_space = 75.0
tile_size = 50.0
margin_indent = 120.0



class Tile(SpriteNode):
	def __init__(self, number, *args, **kwargs):
		SpriteNode.__init__(self, 'pzl:Button1', *args, **kwargs)
		button_font = ('Avenir Next', 20)
		self.number = number
		self.title_label = LabelNode(str(number), font=button_font, color='black', position=(0, 1), parent=self)
		


class ApplePile(Node):
	def __init__(self, *args, **kwargs): 
		Node.__init__(self, *args, **kwargs)
		self.apples_number = random.choice([1,2])
		self.apples = []
		self.diameter = self.apples_number * one_apple_space * 0.75
		self.highlight_pile('green')
		
	
	def highlight_pile(self, color):
		circle = ui.Path.oval(0, 0, self.diameter,  			
																		self.diameter)
		circle.line_width = 3
		self.circle = ShapeNode(circle, stroke_color='green', fill_color='B1DEE1', parent=self)
		#self.circle.position = 0.0, 0.0
		if color == 'green':
			sound.play_effect('8ve:8ve-beep-hightone')
		else:
			sound.play_effect('game:Error')
		
		
		
	#randomly choose the place of apple pile on the screen
	#def place_apple(self, scr_width, scr_height):
		
		
		
	def calc_pos(self):
		position_x, position_y = 0.0, 0.0
		for a in self.apples:
			position_x = a.position.x
			position_y += a.position.y
		position_x = position_x/self.number
		position_y = position_y/self.number
		self.position.x += position_x
		self.position.y += position_y
	
		
	''' def	if_touched(self, touch_loc):
		if ((touch_loc.x < self.apples[0].position.x + one_apple_space) and
				(touch_loc.x > self.apples[0].position.x - one_apple_space)):
			if ((touch_loc.y < self.apples[0].position.y + one_apple_space) and
					(touch_loc.y > self.apples[0].position.y - one_apple_space)):
				return True
		else: 
			return False '''
			
	
				
		
class MyScene(Scene):
	def __init__(self, max_tile, *args, **kwargs):
		Scene.__init__(self)
		self.cur_number = 0
		self.max_tile = max_tile
		self.tiles = []
		self.piles = []
	
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
		self.place_piles()
		
	
	def touch_began(self, touch):
		touch_loc = self.point_from_scene(touch.location)
		for t in self.tiles:
			#if a button is clicked, highlight it
			if touch_loc in t.frame:
				sound.play_effect('8ve:8ve-tap-resonant')
				t.texture = Texture('pzl:Button2')
				t.size = (tile_size, tile_size)
				self.cur_number = t.number
				#unhighlight all other buttons
				for t in self.tiles:
					if touch_loc not in t.frame:
						t.texture = Texture('pzl:Button1')
						t.size = (tile_size, tile_size)
			''' if (self.cur_number != 0):
				for p in self.piles:
					if p.if_touched(touch_loc):
						if (p.number == self.cur_number):
							p.highlight_pile('green')
						else:
							p.highlight_pile('red') '''
							
							
	def place_piles(self):
		fail = 0
		while fail < 200:
			collided = False
			x = random.randrange(margin_indent, self.size.x - margin_indent)
			y = random.randrange(margin_indent, self.size.y - margin_indent)
			for p in self.piles:
				if ((abs(p.position.x - x) <  one_apple_space) or (abs(p.position.y - y) < one_apple_space)):
					fail += 1
					collided = True
			if not collided:
				pile = ApplePile(parent=self)
				pile.position = x, y
				self.piles.append(pile)
				fail = 0
				
						
if __name__ == '__main__':
	run(MyScene(2))
