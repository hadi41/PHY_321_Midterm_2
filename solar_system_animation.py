import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
import time

plt.style.use('dark_background')

Au = 149597870700
yr = 31556952
day = 86400
MEarth = 5.97219 * 10**(24)

G = 6.67430 * 10**(-11) / Au**3 * MEarth * yr**2
M = 1988500 * 10**24 / MEarth

fig, ax = plt.subplots(1,1,figsize=(8,8))
plt.subplots_adjust(bottom=0.2)
plt.subplots_adjust(right=0.8)
ax.set_title('Interactive solar system')

planet_list = []

class Planet_Plot:
	def __init__(self,no,mass,r,v,name,color,size,ax_input):
		self.name = name
		self.m = mass / MEarth
		self.r_init = np.array(r)
		self.v_init = np.array(v) * yr / day
		self.r = np.array(r)
		self.v = np.array(v) * yr / day
		self.color = color
		self.size = size
		self.no = no
		self.ax = ax_input
		self.line, = ax.plot([], [], label=self.name, \
			color = self.color, linewidth=self.size/2)
		buttonplace = plt.axes([0.05 + 0.1 * (self.no - 1), \
			0.05, 0.1, 0.1])
		self.button = Button(buttonplace, label=self.name, \
			color = self.color, hovercolor='#676B72')
		self.active = True
		self.button.on_clicked(self.click)
	def click(self, event):
		if self.active:
			planet_list.remove(self)
			self.active = False
			self.line.remove()
		else:
			planet_list.append(self)
			self.active = True
			planet_list.sort(key=lambda planet: planet.no)
			self.line, = self.ax.plot([],[], \
				label=self.name, color = self.color, \
				linewidth=self.size/2)

Mercury = Planet_Plot(1,3.302 * 10**23, [0.2801,-0.2962],\
	[0.01492,0.02059],'Mercury','#C7E0DA',1,ax)
Venus = Planet_Plot(2,4.8605 * 10**24, [-0.7185,0.08856],\
	[-0.002410,-0.02019],'Venus','#FCC830',3,ax)
Earth = Planet_Plot(3,5.97219 * 10**24, [-0.9124,-0.4202],\
	[0.007034,-0.01564],'Earth','#30A0FC',3,ax)
Mars = Planet_Plot(4,6.4171 * 10**23, [-0.03949,-1.450],\
	[0.01451,0.0008661],'Mars','#FC6530',2,ax)
Jupiter = Planet_Plot(5,1.898 * 10**27, [1.292,-5.017],\
	[0.007216,0.002241],'Jupiter','#FFCE6C',6,ax)
Saturn = Planet_Plot(6,5.6834 * 10**26, [4.297,-9.046],\
	[0.004730,0.002377],'Saturn','#E6E591',5,ax)
Uranus = Planet_Plot(7,8.6813 * 10**25, [15.98,11.70],\
	[-0.002353,0.002990],'Uranus','#91F5F9',4,ax)
Neptune = Planet_Plot(8,1.02413 * 10**26, [29.31,-6.035],\
	[0.0006126,0.003093],'Neptune','#4665E3',4,ax)
Pluto = Planet_Plot(9,1.307 * 10**22, [13.28,-31.31],\
	[0.002969,-0.0005568],'Pluto','#F9CFC2',1,ax)

full_planet_list = [Mercury,Venus,Earth,Mars,Jupiter,\
	Saturn,Uranus,Neptune,Pluto]

planet_list = full_planet_list

def list_resetter():
	global full_planet_list
	full_planet_list = [Mercury,Venus,Earth,Mars,Jupiter,\
	Saturn,Uranus,Neptune,Pluto]
	return

def solar_ec(t, planet_list):
	tN = len(t)
	ts = (t[tN-1] - t[0])/(tN - 1)
	r = np.zeros((tN,len(planet_list),2))
	for mu in range(len(planet_list)):
		r[0][mu] = planet_list[mu].r
	for i in range(tN-1):
		for mu in range(len(planet_list)):
			planet1 = planet_list[mu]
			planet1.v += - G * M * planet1.r * ts \
			/ np.linalg.norm(planet1.r)**3
			for nu in range(mu+1,len(planet_list)):
				planet2 = planet_list[nu]
				aa = - G * (planet1.r - planet2.r) * ts \
				/ np.linalg.norm(planet1.r - planet2.r)**3
				planet1.v += aa * planet2.m
				planet2.v -= aa * planet1.m
		for planet in planet_list:
			planet.r += planet.v * ts
		for mu in range(len(planet_list)):
			r[i+1][mu] = planet_list[mu].r
	return r

def setup(ax_input):
	ax_input.grid()
	ax_input.legend(fancybox = True, loc = 'upper left', \
		framealpha=5, borderpad=0.5, frameon=True)
	ax_input.set_xlim([-60,60])
	ax_input.set_ylim([-60,60])
	ax_input.plot([0,0],[0,0], color='#FFF700', label='Sun', \
		marker='o', linestyle='', markersize=5)

def frame_generator(t, planet_list, ax_input):
	r = solar_ec(t, planet_list)
	r_max = 0
	for mu in range(len(planet_list)):
		planet = planet_list[mu]
		planet.line.set_xdata(r[:,mu,0])
		planet.line.set_ydata(r[:,mu,1])

sliderplace1 = plt.axes([0.92,0.2,0.03,0.6])
slider_ts = Slider(sliderplace1, 'time-step', valmin=0.001, \
	valmax=0.1, valinit=0.01, orientation = 'vertical')
sliderplace2 = plt.axes([0.85,0.2,0.03,0.6])
slider_speed = Slider(sliderplace2, 'speed', valmin=0.003, \
	valmax=10, valinit=0.5, slidermin=slider_ts, \
	orientation = 'vertical')

def reset(event):
	global full_planet_list, planet, planet_list
	list_resetter()
	time.sleep(0.5)
	for planet in full_planet_list:
		if not planet.active:
			planet.click(event)
		planet.v = planet.v_init
		planet.r = planet.r_init
	slider_ts.val = slider_ts.valinit
	slider_speed.val = slider_speed.valinit
	return

buttonplace = plt.axes([0.85,0.85,0.1,0.1])
reset_button = Button(buttonplace, 'reset', color='red', \
	hovercolor = 'yellow')
reset_button.on_clicked(reset)

animation = FuncAnimation(fig, func = lambda i : \
	frame_generator(np.arange(i,i+slider_speed.val,\
		slider_ts.val), planet_list, \
		ax), frames = 10000, interval = 30, repeat = True, \
		init_func = lambda : setup(ax))

plt.show()




