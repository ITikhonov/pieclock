#!/usr/bin/env python

import screenlets
from screenlets import Screenlet
from screenlets.options import IntOption, BoolOption, TimeOption, FloatOption
from screenlets.options import StringOption, FontOption, ColorOption
from screenlets.services import ScreenletService

from math import pi
from datetime import datetime
from gobject import timeout_add

def deg(a): return a*(pi/180)

def pie(ctx,a,r,c):
	a=deg(a[0]-90),deg(a[1]-90)
	ctx.set_source_rgb(*c)
	ctx.arc(0,0,r[0], a[0],a[1])
	ctx.arc_negative(0,0,r[1], a[1],a[0])
	ctx.fill()

class PieClockScreenlet (Screenlet):
	__name__	= 'PieClockScreenlet'
	__version__	= '0.0'
	__author__	= 'Ivan Tikhonov'
	__desc__	= 'Pie Clocks'

	def __init__ (self, parent_window=None, **keyword_args):
		"""Create a new ClockScreenlet instance."""
		# call super (we define to use our own service here)
		Screenlet.__init__(self,**keyword_args)
		self.__timeout = timeout_add(500, self.update)
	
	def on_init (self):
		print "OK - Clock has been initialized."
		self.add_default_menuitems()

	def update(self):
		self.redraw_canvas()
		return True

	def on_draw (self, ctx):
		ctx.scale(self.scale,self.scale)
		ctx.scale(self.width/2,self.height/2)
		ctx.translate(1,1)

		now=datetime.now()


		pie(ctx,(15*(now.hour+now.minute/60.0),360),(0.7,0.9),(0.0,1.0,0.0))
		pie(ctx,(6*(now.minute+now.second/60.0),360),(0.4,0.6),(0.0,1.0,0.0))
		pie(ctx,(6*(now.second+now.microsecond/1000000.0),360),(0.1,0.3),(0.0,1.0,0.0))


			
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	# create new session
	import screenlets.session
	screenlets.session.create_session(PieClockScreenlet)

