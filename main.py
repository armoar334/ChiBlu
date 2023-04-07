#!/usr/bin/env python3

import time
import curses
from curses import wrapper

from objects import *
from worldgen import *

def draw_tiles(screen, w_map, y_off, x_off):
	for xin in range(80):
		for yin in range(20):
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
		if curses.LINES < 23 or curses.COLS < 79:
			return 'Your terminal needs to be at least 24x80, yours is {}x{}'.format(curses.LINES, curses.COLS)

		curses.use_default_colors()
		curses.curs_set(0)

		for i in range(0, 7):
			curses.init_pair(i, i, -1)

		if main_menu(screen):
			game(screen)
		else:
			return

def main_menu(screen):
	# Logo
	screen.addstr(7, 26, "  ____ _     _ ")
	screen.addstr("____  _", curses.color_pair(4))
	screen.addstr(8, 26, " / ___| |__ (_)")
	screen.addstr(" __ )| |_   _", curses.color_pair(4))
	screen.addstr(9, 26, "| |   | '_ \| |")
	screen.addstr("  _ \| | | | |", curses.color_pair(4))
	screen.addstr(10, 26, "| |___| | | | |")
	screen.addstr(" |_) | | |_| |", curses.color_pair(4))
	screen.addstr(11, 26, " \____|_| |_|_|")
	screen.addstr("____/|_|\__,_|", curses.color_pair(4))

	running = True
	curr_opt = 1
	while running:
		match curr_opt:
			case 1:
				screen.addstr(14, 37, "> Start    ") # This is a bad way to clear
				screen.addstr(15, 37, "Exit      ") # I dont care tho
			case 2:
				screen.addstr(14, 37, "Start      ") # It should also be a seperate function but again, i cba
				screen.addstr(15, 37, "> Exit    ")

		key = screen.getch()

		match key:
			case curses.KEY_UP:
				curr_opt -= 1
			case curses.KEY_DOWN:
				curr_opt += 1
			case 10 | 13:
				match curr_opt:
					case 1:
						screen.erase()
						return True
					case _:
						return False
			case 113:
				return False

		if curr_opt <= 1:
			curr_opt = 1

		if curr_opt >= 2:
			curr_opt = 2


def game(screen):
		# Draw offset
		x_off = 0
		y_off = 0

		# World size
		xw_max = 100
		yw_max = 100

		# Player
		player = entity(0, 0, 'decker', '5', '5', '@', 2, 'player')
		p_move = 2 # Player movements per "turn"

		entities = []
		entities.append(entity(10, 15, 'razor', '5', '5', 'r', 1, 'Molly'))
		entities.append(entity(3, 3, 'cyborg', '5', '5', 'C', 2, 'Brian'))
		entities.append(entity(80, 80, 'cyborg', '5', '5', 'C', 2, 'Jerma985'))


		# World map array
		w_map = [['' for _ in range(xw_max)] for _ in range(yw_max)]

		w_map = add_square(w_map, 1, 1, 8, 5, '#')
		w_map = add_square(w_map, 2, 2, 6, 3, '.')

		w_map = add_square(w_map, 10, 1, 8, 5, '#')
		w_map = add_square(w_map, 11, 2, 6, 3, '.')

		w_map = add_square(w_map, 1, 7, 17, 5, '#')
		w_map = add_square(w_map, 2, 8, 15, 3, '.')

		w_map[5][5] = '.'

		main_loop = True

		frame = 0
		checked_ent = player
		while main_loop:
			frame += 1

			for temp in entities:
				if frame % p_move == 0:
					temp.random_move(w_map)
					temp.sanitise(xw_max, yw_max)
				if temp.health <= 0:
					entities.remove(temp)

			screen = draw_tiles(screen, w_map, y_off, x_off)
			screen = draw_entities(screen, entities, y_off, x_off)

			temp_px = 0
			temp_py = 0


			
			# Player
			screen.addstr(player.y - y_off, player.x - x_off, player.icon, curses.color_pair(player.color))
			
			# Bottom bar
			screen.addstr(21, 0, '+{}+'.format('-' * 78 ))
			screen.addstr(22, 0, '|{}|'.format(' ' * 78 ))
			screen.addstr(23, 0, '+{}+'.format('-' * 77 ))

			#screen.addstr(22, 1, 'x: {} y: {}'.format(player.x, player.y))
			#screen.addstr(22, 1, '{}'.format( 'O' * ( ( frame % p_move ) + 1 ) ) 
			screen.addstr(22, 1, '{}: {}'.format(checked_ent.name, checked_ent.health))
			
			screen.refresh()

			key = screen.getch()

			match key:
				case 113:
					main_loop = False		
				case curses.KEY_UP:
					temp_py = -1
				case curses.KEY_DOWN:
					temp_py = 1
				case curses.KEY_LEFT:
					temp_px = -1
				case curses.KEY_RIGHT:
					temp_px = 1

			# Kick / other interactions
			temp_ent = player.check_ent(player.x + temp_px, player.y + temp_py, entities)
			if temp_ent:
				checked_ent = temp_ent
				checked_ent.health -= 1
			else:
				player.move(temp_px, temp_py, w_map)

			player.sanitise(xw_max, yw_max)


			# Offset
			if 39 < player.x < xw_max - 39:
				x_off = player.x - 40

			if 9 < player.y < yw_max - 10:
				y_off = player.y - 10

			screen.erase()
			
		return 'Thanks for playing!'

print(wrapper(main))
