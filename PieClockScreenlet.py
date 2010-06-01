#!/usr/bin/env python

import screenlets
from screenlets import Screenlet
from screenlets.options import IntOption, BoolOption, TimeOption, FloatOption
from screenlets.options import StringOption, FontOption, ColorOption
from screenlets.services import ScreenletService
from cairo import OPERATOR_DEST_OUT,OPERATOR_OVER

from math import pi
from datetime import datetime
from gobject import timeout_add

def deg(a): return a*(pi/180)

def pie(ctx,a,r,c):
	a=deg(a[0]-90),deg(a[1]-90)
	if len(c)==3: ctx.set_source_rgb(*c)
	else: ctx.set_source_rgba(*c)
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

		self._color_wd = (0.5,0.0,1.0)
		self._color_hr = (0.0,0.5,1.0)
		self._color_mn = (0.0,0.5,0.0)
		self._color_sc = (0.8,0.8,0.8)

		now=datetime.now()

		wl=360/7.0
		for i in range(0,7):
			pie(ctx,(wl*i,wl*i+wl-4),(0.8,0.9),self._color_wd)
		ctx.set_operator(OPERATOR_DEST_OUT)
		pie(ctx,(0,wl*now.weekday()+(wl-4)*(now.hour/24.0+now.minute/(24*60.0))),(0.7,1),(1.0,1.0,1.0,0.8))

		ctx.set_operator(OPERATOR_OVER)
		for i in range(0,24):
			pie(ctx,(15*i,15*i+11),(0.6,0.7),self._color_hr)
		ctx.set_operator(OPERATOR_DEST_OUT)
		pie(ctx,(0,15*now.hour+11*(now.minute/60.0)),(0.5,0.8),(0.0,1.0,0.0,0.8))

		ctx.set_operator(OPERATOR_OVER)
		for i in range(0,3):
			pie(ctx,(120*i,120*i+110),(0.3,0.5),self._color_mn)
		ctx.set_operator(OPERATOR_DEST_OUT)
		pie(ctx,(0,120*(now.minute/20)+(110/20.0)*((now.minute%20)+now.second/60.0)),(0.2,0.6),(0.0,1.0,0.0,0.8))

		ctx.set_operator(OPERATOR_OVER)
		pie(ctx,(6*(now.second+now.microsecond/1000000.0),360),(0.1,0.2),self._color_sc)

if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(PieClockScreenlet)

