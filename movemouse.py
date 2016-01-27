#!/usr/bin/env python

import time
import pyautogui

def main():

	while True:
        	position = pyautogui.position()
		time.sleep(60)
		if position == pyautogui.position():
			pyautogui.moveRel(0,-1)
			pyautogui.moveRel(0,1)

main()
