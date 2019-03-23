#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
import math

darea = Gtk.DrawingArea()
calibDataScreenPos = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
calibData = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
calibPosition = 0

def paintWidget(widget, cr):
	global calibDataScreenPos
	global calibData
	global calibPosition

	size = widget.get_allocation()
	cr.set_source_rgb(0.6, 0.6, 0.6)
	
	if calibDataScreenPos[0][0] == -1:
		paddingX = size.width / 10
		paddingY = size.height / 10
		calibDataScreenPos[0] = [paddingX, paddingY]
		calibDataScreenPos[1] = [size.width - paddingX, paddingY]
		calibDataScreenPos[2] = [paddingX, size.height - paddingY]
		calibDataScreenPos[3] = [size.width - paddingX, size.height - paddingY]

	cr.rectangle(0, 0, size.width, size.height)
	cr.fill()

	cr.set_source_rgb(0.6, 0, 0)
	cr.move_to(20, size.height / 2)
	
	cr.set_font_size(20)
	cr.show_text("Press any key to quit - touch to draw a point")

	if calibPosition > 3:
		cr.move_to(20, size.height / 2 + 50)
		cr.show_text("Touch again to Quit")

	circleSize = 50
	i = 0

	for cs in calibDataScreenPos:
		cr.save()
		if i < calibPosition:
			cr.set_source_rgb(0, 1, 0)
		elif i <= calibPosition:
			cr.set_source_rgb(1, 1, 1)
		else:
			cr.set_source_rgb(0.5, 0.5, 0.5)
			
		cr.translate(cs[0], cs[1]);
		cr.arc(0, 0, circleSize / 2, 0, 2 * math.pi)
		cr.fill();
		
		p = calibData[i]
		if p[0] >= 0:
			cr.translate(0, 50);
			cr.set_source_rgb(0, 0, 0)
			cr.show_text(str(int(p[0])) + " / " + str(int(p[1])))

		cr.restore()
		i = i + 1


def doCalibrate():
	# Hints: https://wiki.archlinux.org/index.php/Talk:Calibrating_Touchscreen
	size = darea.get_allocation()
	sw = size.width
	sh = size.height
	
	## TODO add parameter to configure device
	calibDevice = "silead_ts"

	print("\nCalibration finished.")
	print("Screen size: %i / %i" % (sw, sh))
	i = 0

	for cd in calibData:
		print("Calib Point %i: %lf / %lf" % (i, cd[0], cd[1]))
		i = i + 1

	xyAxes = 0
	
	if abs(calibData[0][0] - calibData[1][0]) < 20:
		xyAxes = 1
	elif abs(calibData[0][1] - calibData[1][1]) < 20:
		xyAxes = 2

	if xyAxes < 1:
		print("Could not assign X / Y Axes, probably bad callibration")
		return

	if xyAxes == 1:
		print("X/Y Axes are swapped!")
		
		for i in range(4):
			tmp = calibData[0][0]
			calibData[0][0] = calibData[0][1]
			calibData[0][1] = tmp

	calibrationMatrix  = "2.074595 0 0"
	calibrationMatrix += "0 2.688341 0"
	calibrationMatrix += "0 0 1"

	print("To apply permanent, store to:")
	print("/etc/X11/xorg.conf.d/99-calibration.conf")
	print("--------------------------------------------\n")
	print("Section \"InputClass\"")
	print("	Identifier	\"calibration\"")
	print("	MatchProduct	\"" + calibDevice + "\"")
	print("	Option	\"CalibrationMatrix\"	\"" + calibrationMatrix + "\"")
	print("	Driver	\"libinput\"")
	print("EndSection")
	print("\n--------------------------------------------")


def mouseEventPressed(window, event):
	global calibData
	global calibPosition

	if calibPosition >= 4:
		Gtk.main_quit()
		doCalibrate()
		return

	calibData[calibPosition][0] = event.x
	calibData[calibPosition][1] = event.y
	
	calibPosition = calibPosition + 1
	darea.queue_draw()


darea.connect("draw", paintWidget)

darea.set_events(darea.get_events() | Gdk.EventMask.BUTTON_PRESS_MASK)


darea.connect('button-press-event', mouseEventPressed)

window = Gtk.Window(title="Calibration")
window.connect("key-press-event", Gtk.main_quit)

window.add(darea)
window.show_all()

window.fullscreen()
window.show()
window.connect("delete-event", Gtk.main_quit)
Gtk.main()



