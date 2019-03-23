#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
import math

darea = Gtk.DrawingArea()
clicks = []

def paintWidget(widget, cr):
	global clicks

	size = widget.get_allocation()
	cr.set_source_rgb(0.6, 0.6, 0.6)

	cr.rectangle(0, 0, size.width, size.height)
	cr.fill()

	cr.set_source_rgb(0.6, 0, 0)
	cr.move_to(20, size.height / 2)
	
	cr.set_font_size(20)
	cr.show_text("Press any key to quit - touch to draw a point")

	cr.set_source_rgb(0, 1, 0)
	circleSize = 20

	for point in clicks:
		cr.save()
		cr.translate(point[0], point[1]);
		cr.arc(0, 0, circleSize / 2, 0, 2 * math.pi)
		cr.fill();
		cr.restore()


def mouseEventPressed(window, event):
	global clicks

	clicks.append([event.x, event.y])
	darea.queue_draw()


darea.connect("draw", paintWidget)

darea.set_events(darea.get_events() | Gdk.EventMask.BUTTON_PRESS_MASK)


darea.connect('button-press-event', mouseEventPressed)

window = Gtk.Window(title="Draw Test")
window.connect("key-press-event", Gtk.main_quit)

window.add(darea)
window.show_all()

window.fullscreen()
window.show()
window.connect("delete-event", Gtk.main_quit)
Gtk.main()



