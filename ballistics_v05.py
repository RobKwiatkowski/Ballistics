import math
import matplotlib.pyplot as plt
import os

def plotter(question, x_axis, y_axis, style = "b"):
	while True:
		q1 = raw_input(question)
		if q1=="y":
			plt.plot(x_axis,y_axis, style)
			plt.xlabel("Distance [m]")
			plt.ylabel("Height [m]")
			plt.ylim(ymin=0)
			plt.show()
			break
		elif q1=="n":
			break
		else:
			print "yes or no?"
			continue

path = os.path.dirname(os.path.abspath(__file__))

#time
t = [0]

#coordinates
x = [0]
y = [0]

#constants
GRAVITY 	= 9.81 		    # m/s2
TIME_STEP 	= 0.05		    # s
DENSITY		= 1.225			# kg/m3

#displaying program's name
print "BALLISTIC TRAJECTORY CALCULATOR"

#user's inputs
while True:
	try:
		mass = float(raw_input("Mass (default 0.004) [kg]: ") or "0.004")
		if mass <=0:
			print "Mass has to be bigger than 0! \n"
			continue
			
		V_init = float(raw_input("Inital velocity (default 200) [m/s]: ") or "200")
		if V_init <=0:
			print "Velocity has to be bigger than 0! \n"
			continue
			
		angle_degs = float(raw_input("Shooting angle (default 45) [deg]: ") or "45")
		if angle_degs <=0 or angle_degs >90:
			print "Shooting angle has to be bigger in the range (0,90>! \n"
			continue
			
		area = float(raw_input("Area (default 0.000024) [m2]: ") or "0.000024")
		if area <=0:
			print "Area has to be bigger than 0! \n"
			continue
			
		c_drag = float(raw_input("Coefficient of drag (default 0.5): ") or "0.5")
		if c_drag <=0:
			print "Coefficient of drag has to be bigger than 0! \n"
			continue
		break

	except ValueError:
		print "Only numbers are allowed!"

angle_rads = math.radians(angle_degs)			#converts deg to radians
V_x_init = V_init*math.cos(angle_rads)			#initial x velocity
V_y_init = V_init*math.sin(angle_rads)			#initial y velocity

Vel_x = V_x_init 							#stores the current x velocity
Vel_y = V_y_init 							#stores the current y velocity
distance = 0							#stores the current distance
height = 0								#stores the current height
time = 0								#stores the current time

#Terminal velocity calculations
TERMINAL = math.sqrt(2*mass*GRAVITY/(c_drag*area*DENSITY))

#no drag initial values
Vel_x_ref = V_x_init
Vel_y_ref = V_y_init
d_ref = 0
h_ref = 0
x_ref = [0]
y_ref = [0]

#creating file to store the results
f = open(path + "\data.txt","w")

#ascent calculations with drag
while Vel_y>=0:

    if angle_degs == 90:
		Vel_x = 0
		V_x_init = 0
    else:
        Vel_x = TERMINAL**2*V_x_init/(TERMINAL**2+GRAVITY*V_x_init*time)
	
    A = V_y_init-TERMINAL*math.tan(GRAVITY*time/TERMINAL)
    B = TERMINAL+V_y_init*math.tan(GRAVITY*time/TERMINAL)
    Vel_y = TERMINAL*A/B
    
    #updating coordinates
    C = (TERMINAL**2+GRAVITY*V_x_init*time)/TERMINAL**2
    distance = TERMINAL**2/GRAVITY*math.log(C)
    D = (V_y_init**2+TERMINAL**2)/(Vel_y**2+TERMINAL**2)
    height = TERMINAL**2/(2*GRAVITY)*math.log(D)
    
    #writing the results
    x.append(distance)
    y.append(height)
    
    f.write("Time: " + str(time).ljust(5) + " Distance: " + str(round(distance,2)).ljust(8) + " Height:  " + str(round(height,2)).ljust(5) + "\n")
    
    #updating simulation time
    time = time+TIME_STEP
    t.append(time)
    
#descent calculations with drag

h_max = height

time_fall = 0       #descending time

while height>0:

    if angle_degs == 90:
		Vel_x = 0
		distance = 0
    else:
        Vel_x = TERMINAL**2*V_x_init/(TERMINAL**2+GRAVITY*V_x_init*time)
    
    Vel_y = GRAVITY*time_fall
    
    C = (TERMINAL**2+GRAVITY*V_x_init*time)/TERMINAL**2
    distance = distance + Vel_x*TIME_STEP
    
    D = 0.5*DENSITY*c_drag*area
    height = height - math.sqrt(TERMINAL)*math.tanh(math.sqrt(GRAVITY*D/mass)*time_fall)

    
    x.append(distance)
    y.append(height)
    
    time = time + TIME_STEP
    time_fall = time_fall + TIME_STEP
    t.append(time)

#no drag section

time_ref = 0

while Vel_y_ref>=0:
	time_ref = time_ref + TIME_STEP
	if angle_degs == 90:
		Vel_x = 0
		d_ref = 0
	else:
		d_ref = Vel_x_ref*time_ref
	
	Vel_y_ref = V_y_init - GRAVITY*time_ref
	h_ref = h_ref + Vel_y_ref*TIME_STEP
	
	x_ref.append(d_ref)
	y_ref.append(h_ref)

h_ref_max = h_ref
time_ref_fall = 0

while h_ref>0:
	Vel_y_ref = GRAVITY*time
	if angle_degs == 90:
		Vel_x = 0
		d_ref = 0
	else:
		d_ref = Vel_x_ref*time_ref
	
	h_ref = h_ref_max - GRAVITY*time_ref_fall**2/2
	x_ref.append(d_ref)
	y_ref.append(h_ref)
	
	time_ref = time_ref + TIME_STEP
	time_ref_fall = time_ref_fall + TIME_STEP

f.close()

print "\n CALCULATIONS COMPLETED SUCCESFULLY \n"

print "Terminal velocity is: " + str(TERMINAL) + " m/s"
print "Maximum height is: " + str(h_max) + " m \n"

#plotting graphs

plotter("Print the trajectory with drag? (y/n)",x,y)
plotter("Print the trajectory without drag? (y/n)",x_ref,y_ref, "g")


while True:
	q2 = raw_input("Overlay both trajectories? (y/n)")
	if q2=="y":
		plt.plot(x,y, "b", x_ref,y_ref, "g--")
		plt.xlabel("Distance [m]")
		plt.ylabel("Height [m]")
		plt.ylim(ymin=0)
		plt.show()
		break
	elif q2=="n":
		break
	else:
		print "yes or no?"
		continue

        
        
        
        
        
        
        
        
        
        
        

