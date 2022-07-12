#
import numpy as np 
import time
import pygame

radius = 1 

pygame.display.set_caption('CPU thermometr')#name of window
#wndow size
x_max=600
y_max=600

pygame.init()  
screen = pygame.display.set_mode((x_max, y_max))  
#pygame.draw.lines(screen,(55,255,255),False, x)
font = pygame.font.SysFont(None, 24)
done = False
def skala():

	for k in range(0,101):
		x1 =int((x_max/2-50)* np.cos(k/100*np.pi)+x_max/2)
		y1=int((y_max/2-50)* -abs(np.sin(k/100*np.pi)) +y_max/2)
		x2 =int((x_max/2-50)* np.cos((k+1)/100*np.pi)+x_max/2)
		y2=int((y_max/2-50)* -abs(np.sin((k+1)/100*np.pi)) +y_max/2)
		#print('x='+str(x1)+'____'+str(x2)+';    y='+str(y1)+'____'+str(y2))
		pygame.draw.line(screen,(255,255,255), (x1,y1),(x2,y2),width=5)
		if k%20 ==0:
			x3 =int((x_max/2-80)* np.cos(k/100*np.pi)+x_max/2)
			y3=int((y_max/2-80)* -abs(np.sin(k/100*np.pi)) +y_max/2)
			pygame.draw.line(screen,(255,0,0), (x1,y1),(x3,y3),width=5)
			text= font.render(str(abs(100-k)), True, (255,255,255))
			screen.blit(text, (x3-10, y3))
		elif (k+10)%20 ==0:
			x3 =int((x_max/2-70)* np.cos(k/100*np.pi)+x_max/2)
			y3=int((y_max/2-70)* -abs(np.sin(k/100*np.pi)) +y_max/2)
			pygame.draw.line(screen,(255,255,255), (x1,y1),(x3,y3),width=5)
			#text= font.render(str(abs(100-k)), True, (255,255,255))
			#screen.blit(text, (x3-10, y3))
		
		
		
def set_t(temp0,temp1):
	r_text = font.render('CPU Core0 temperature, Celcius deg ', True, (255,255,255))
	screen.blit(r_text, (0, y_max/16*9))
	r_text = font.render('CPU Core1 temperature, Celcius deg ', True, (255,255,255))
	screen.blit(r_text, (0, y_max/16*13))
	r_text = font.render('CPU core0: '+str(temp0)+", core1: "+str(temp1), True, (255,255,255))
	screen.blit(r_text, (0, y_max-24))
	deg_t=((temp0-50)/200)*360   
	x_t = -int(-np.sin(np.radians(deg_t)) * (x_max/2-100))+x_max/2
	y_t =-int (np.cos(np.radians(deg_t)) * (y_max/2-100))+y_max/2
	x_t1 = -int(-np.sin(np.radians(deg_t+90)) * 10)
	y_t2 =-int (np.cos(np.radians(deg_t+90)) * 10)
	#pygame.draw.line(screen,(100,255,255), (x_max/2,y_max/2),(x_t ,y_t),width=5)
	pygame.draw.polygon(screen,(0,100,255), points=[(x_max/2-x_t1,y_max/2-y_t2),(x_t,y_t),(x_max/2+x_t1,y_max/2+y_t2)])
	pygame.draw.line(screen,(255,255,255), (50,3*y_max/4),(x_max-50 ,3*y_max/4),width=5)
	pygame.draw.polygon(screen,(0,100,255), points=[(x_max/2,3*y_max/4),(x_max/2+20,3*y_max/4-20),(x_max/2-20,3*y_max/4-20)])
	for k in range(int(temp1-10),int(temp1+11)):
		m=int(k-temp1)
		n=m+4
		line_length = 4 if k % 10 == 0 else 2
		x1 = (m)/10*(x_max/2-50)+x_max/2
		
		y1 = 3*y_max/4+line_length*5
		y2 = 3*y_max/4-line_length*5
		if k>=0 and not k % 10 == 0:
			pygame.draw.line(screen,(255,255,255), (x1,y1),(x1,y2),width=line_length)
		elif k>=0 and k % 10 == 0:
			pygame.draw.line(screen,(255,0,0), (x1,y1),(x1,y2),width=line_length)
			text= font.render(str(int(k)), True, (255,255,255))
			screen.blit(text, (x1-10, y1+2))
#read temperature
def update_temp():
	
    #read temperature core 0
	fileName = ("/sys/class/thermal/thermal_zone0/temp")
	fw = open(fileName,"r")
	temp = int(fw.read())/1000
	fw.close()
    #read temperature core 1
	fileName = ("/sys/class/thermal/thermal_zone1/temp")
	fw = open(fileName,"r")
	temp1 = int(fw.read())/1000
	fw.close()
	set_t(temp,temp1)
	#print(temp1)
	
	

while done==False:
	pressed = pygame.key.get_pressed()
	for event in pygame.event.get():  
		if event.type == pygame.QUIT or (pressed[pygame.K_q]):   #quit window 
			done = True
	pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, x_max, y_max))#clear window
	skala()
	update_temp()
	#set_t(100,100)
	pygame.display.flip()
	time.sleep(0.1)

