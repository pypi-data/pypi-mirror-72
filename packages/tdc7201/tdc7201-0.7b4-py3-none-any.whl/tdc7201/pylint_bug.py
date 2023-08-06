#!/usr/bin/python3

""" Reproducible pylint bug."""

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)	# Use header pin numbers, not GPIO numbers.
