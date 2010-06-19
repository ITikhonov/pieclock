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

from calendar import monthrange,isleap

def deg(a): return a*(pi/180)

def circle(ctx,parts,r,w,c,v,b=10,d=0.5):
	ctx.set_operator(OPERATOR_OVER)
	wl=360.0/parts
	for i in range(0,parts):
		dr=1-d*(i%2)
		pie(ctx,(wl*i,wl*i+wl-b),(r,r+w*dr),c)
	ctx.set_operator(OPERATOR_DEST_OUT)
	pie(ctx, (0,wl*int(v) + (wl-b)*(v-int(v)) ), (r-0.01,r+w+0.01),(1.0,1.0,1.0,0.8))

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

		self._color_yd = (0.0,0.0,0.0)
		self._color_md = (0.2,0.2,0.0)
		self._color_wd = (0.5,0.0,1.0)
		self._color_hr = (0.0,0.5,1.0)
		self._color_mn = (0.0,0.5,0.0)
		self._color_sc = (0.8,0.8,0.8)

		now=datetime.now()

		mr=monthrange(now.year,now.month)[1]
		dr=365+isleap(now.year)

		circle(ctx, 4,  0.9,0.1, self._color_yd, (now-datetime(now.year,1,1)).days/float(dr/4.0),2,d=0)
		circle(ctx, mr,  0.775,0.1, self._color_md, now.day+now.hour/24.0+now.minute/(24*60.0), 4, 0.2)
		circle(ctx, 7,  0.65,0.1, self._color_wd, now.weekday()+now.hour/24.0+now.minute/(24*60.0),d=0)
		circle(ctx, 24, 0.35,0.15, self._color_hr, now.hour+now.minute/60.0, 4, 0.2)
		circle(ctx, 3, 0.2,0.1, self._color_mn, now.minute/20.0,d=0)
		circle(ctx, 2, 0.01,0.1, self._color_sc, (now.second + now.microsecond/1000000.0)/30.0,d=0)


if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(PieClockScreenlet)

