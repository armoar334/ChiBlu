#!/usr/bin/env python3

import time
import curses
from curses import wrapper

from objects import *
from worldgen import *

def draw_tiles(screen, w_map, y_off, x_off):
	for xin in range(80):
		for yin in range(22):
			screen.addstr(yin, xin, w_map[xin + x_off][yin + y_off])

	return screen

def draw_entities(screen, entities, y_off, x_off):
	for temp in entities:
		if x_off <= temp.x < x_off + 80:
			if y_off <= temp.y < y_off + 22:
				screen.addstr(temp.y - y_off, temp.x - x_off, temp.icon, curses.color_pair(temp.color))
	return screen


def main(screen):
		# Setup
		if curses.LINES < 24 or curses.COLS < 80:
			return 'Your terminal needs to be at least 24x80, yours is {}x{}'.format(curses.LINES, curses.COLS)

		curses.use_default_colors()
		curses.curs_set(0)

		for i in range(0, 7):
			curses.init_pair(i, i, -1)

		# Draw offset
		x_off = 0
		y_off = 0

		# World size
		xw_max = 100
		yw_max = 100

		# Player
		player = entity(1, 1, 'decker', '5', '5', '@', 2)

		entities = []
		entities.append(entity(10, 15, 'razor', '5', '5', 'r', 1))
		entities.append(entity(3, 3, 'cyborg', '5', '5', 'C', 2))
		entities.append(entity(80, 80, 'cyborg', '5', '5', 'C', 2))


		# World map array
		w_map = [['' for _ in range(xw_max)] for _ in range(yw_max)]

		w_map = add_square(w_map, 0, 0, 10, 5, '#')
		w_map = add_square(w_map, 1, 1, 8, 3, '.')

		main_loop = True
		
		while main_loop:
			screen = draw_tiles(screen, w_map, y_off, x_off)
			screen = draw_entities(screen, entities, y_off, x_off)

			# Player
			screen.addstr(player.y - y_off, player.x - x_off, player.icon, curses.color_pair(player.color))
			
			# Bottom bar
			screen.addstr(22, 0, '+{}+'.format('-' * 78 ))
			screen.addstr(23, 0, '|{}|'.format(' ' * 78 ))
			screen.addstr(24, 0, '+{}+'.format('-' * 78 ))
			
			screen.refresh()

			key = screen.getch()

			match key:
				case 113:
					main_loop = False		
				case curses.KEY_UP:
					player.move(0, -1)
				case curses.KEY_DOWN:
					player.move(0, 1)
				case curses.KEY_LEFT:
					player.move(-1, 0)
				case curses.KEY_RIGHT:
					player.move(1, 0)

			player.sanitise(xw_max, yw_max)

			for temp in entities:
				temp.random_move()
				temp.sanitise(xw_max, yw_max)

			# Offset
			if 39 < player.x < xw_max - 39:
				x_off = player.x - 40

			if 10 < player.y < yw_max - 10:
				y_off = player.y - 11

			screen.erase()
			
		return 'Thanks for playing!'

print(wrapper(main))
