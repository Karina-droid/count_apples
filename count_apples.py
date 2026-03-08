from scene import *
import ui
import sound
import random
import math
import statistics
A = Action


apples = ['emj:Green_Apple', 'emj:Red_Apple']
scr_height = 820.0
min_apple_size = 35.0
max_apple_size = 65.0
one_apple_space = 60.0
tile_size = 50.0
margin_indent = 80.0



class Tile(SpriteNode):
	def __init__(self, number, *args, **kwargs):
		SpriteNode.__init__(self, 'pzl:Button1', *args, **kwargs)
		button_font = ('Avenir Next', 20)
		self.number = number
		self.title_label = LabelNode(str(number), font=button_font, color='black', position=(0, 1), parent=self)

				
		
class Apple(SpriteNode):
	def __init__(self, r, angle, *args, **kwargs):
		SpriteNode.__init__(self, random.choice(apples), *args, **kwargs)
		self.r = r
		self.angle = angle
		
	
	def fall(self):
		fall_time = random.uniform(1.5, 2.5)
		actions = [A.move_by(0, -(scr_height), fall_time), A.remove()]
		self.run_action(A.sequence(actions))
			


class ApplePile(Node):
	def __init__(self, *args, **kwargs): 
		Node.__init__(self, *args, **kwargs)
		self.apples_number = random.choice([1,2])
		self.apples = []
		self.diameter = self.apples_number * max_apple_size
		self.tapped = False
		for i in range(self.apples_number):
			self.place_apple()
		
	
	def highlight_pile(self, color):
		if color != None:
			self.tapped = True
			circle = ui.Path.oval(0, 0, self.diameter,  			
																				self.diameter)
			circle.line_width = 3
			self.circle = ShapeNode(circle, stroke_color=color, fill_color='B1DEE1', parent=self)
			self.circle.blend_mode = 2
			if color == 'green':
				sound.play_effect('8ve:8ve-beep-hightone')
			elif color == 'red':
				sound.play_effect('game:Error')
		else:
			try:
				self.circle.run_action(A.fade_to(0, 1))
			except AttributeError:
				return
	
		
	def place_apple(self):
		size = random.randrange(min_apple_size, max_apple_size)
		r = random.uniform(0, self.diameter/2 - size/2)
		angle = random.uniform(0, 2*math.pi)
		for apple in self.apples:
			for i in range(1000):
				if (math.pi * apple.r * (angle/math.pi) < 1.5*max_apple_size):
					angle = random.uniform(0, 2*math.pi)
		apple = Apple(r, angle, parent=self)
		apple.size = size, size
		apple.position = r*math.cos(angle), r*math.sin(angle)
		self.apples.append(apple)
				
		
		
class MyScene(Scene):
	def __init__(self, max_tile, *args, **kwargs):
		Scene.__init__(self)
		self.cur_number = 0
		self.max_tile = max_tile
		self.tiles = []
		self.piles = []
		self.hearts = []
	
	
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
		self.place_hearts()
		
	
	def touch_began(self, touch):
		touch_loc = self.point_from_scene(touch.location)
		if self.cur_number == 0:
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
		if (self.cur_number != 0):
			for p in self.piles:
				if (abs(touch_loc.x - p.position.x) < p.diameter/2) and (abs(touch_loc.y - p.position.y) < p.diameter/2):
					if p.tapped == False:
						if (p.apples_number == self.cur_number):
							p.highlight_pile('green')
						else:
							p.highlight_pile('red')
							self.wrong()
							
							
	def place_piles(self):
		fail = 0
		while fail < 200:
			collided = False
			x = random.randrange(margin_indent, self.size.x - margin_indent)
			y = random.randrange(margin_indent, self.size.y - margin_indent)
			for p in self.piles:
				if ((abs(p.position.x - x) <  one_apple_space) or (abs(p.position.y - y) < max_apple_size)):
					fail += 1
					collided = True
			if not collided:
				pile = ApplePile(parent=self)
				pile.position = x, y
				self.piles.append(pile)
				fail = 0
				
				
	def place_hearts(self):
		for i in range(3):
			heart = SpriteNode('emj:Heart', position=(self.size.x - margin_indent - i*50, 
																									self.size.y - margin_indent/2), size=(45, 45), parent=self)
			self.hearts.append(heart)
			
	
	def wrong(self):
		heart = self.hearts.pop()
		if not self.hearts:
			self.loose()
		heart.texture = Texture('emj:Heart_Broken')
		heart.size = (45, 45)
		self.run_action(Action.wait(2))
		heart.run_action(Action.fade_to(0, 1.5))
		sound.play_effect('game:Clank')
		
		
	def loose(self):
		self.run_action(A.wait(10))
		for pile in self.piles:
			pile.highlight_pile(None)
		for pile in self.piles:
			for apple in pile.apples: 
				apple.fall()
				
					
						
if __name__ == '__main__':
	run(MyScene(2))
