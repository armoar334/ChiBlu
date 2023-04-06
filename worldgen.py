#!/usr/bin/env python3

def add_square(w_map, xtop, ytop, width, height, char):
		for xin in range(xtop, xtop + width):
			for yin in range(ytop, ytop + height):
				w_map[xin][yin] = str(char)

		return w_map


