
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg 
import numpy as np 
import time
import array as arr
 

#initiated circle and app title
win =pg.GraphicsLayoutWidget(show=True, title='Analog CPU Thermometer')
init_window_size = 800 
win.resize(init_window_size, init_window_size) 
pg.setConfigOptions(antialias=True) 
graph = win.addPlot() 
graph.showAxis('bottom', False) 
graph.showAxis('left', False) 
graph.setAspectLocked(lock=True) 
graph.setMouseEnabled(x=False, y=False) 
radius = 1 
x = radius * np.cos(np.linspace(0, 2 * np.pi, 1000)) 
y = abs(radius * np.sin(np.linspace(0, 2 * np.pi, 1000))) 
graph.plot(x, y,pen=pg.mkPen(width=6))
graph.plot(x,y-y-0.5,pen=pg.mkPen(width=6))#linear
#linear
#initiated scale
for k in range(-50,51):
    line_length = 0.1 if k % 10 == 0 else 0.05 
    line_width = 4 if k % 10 == 0 else 2 
    color = (255,0,0) if k % 10 == 0 else (255,255,255) 
    x1 = np.sin(np.radians(360 * (k / 200))) * radius 
    x2 = np.sin(np.radians(360 * (k / 200))) * (radius - line_length)
    y1 = np.cos(np.radians(360 * (k/ 200))) * radius 
    y2 = np.cos(np.radians(360 * (k / 200))) * (radius - line_length)
    pen = pg.mkPen(width=line_width,color=color) 
    pen.setCapStyle(QtCore.Qt.RoundCap) 
    graph.plot([x1, x2], [y1,y2], pen=pen )
    
#initiated variables of scale
font_size = 32
cel_texts = []
for cel in range(1, 12, 1):
    x = np.sin(np.radians(360 * ((10*cel-60) / 200))) * radius * 0.8
    y =np.cos(np.radians(360 * ((10*cel-60) / 200))) * radius * 0.8
    text=str((cel-1)*10)
    cel_text = pg.TextItem(text[0:3], anchor=(0.25, 0.25))
    cel_text.setPos(x, y)
    font = QtGui.QFont() 
    font.setPixelSize(font_size) 
    cel_text.setFont(font)
    graph.addItem(cel_text)
    cel_texts.append(cel_text)

#text below hand
temperature_str = "Core0 Temperature, Celsius scale"
temperature_text = pg.TextItem(text=temperature_str, anchor=(0.5, 0.5))
temperature_text.setPos(0, -radius / 10)
font = QtGui.QFont() 
font.setPixelSize(int(font_size / 2)) 
temperature_text.setFont(font)
graph.addItem(temperature_text)

temperature_str = "Core1 Temperature, Celsius scale"
temperature_text = pg.TextItem(text=temperature_str, anchor=(0.5, 0.5))
temperature_text.setPos(0, -0.7)
font.setPixelSize(int(font_size / 2)) 
temperature_text.setFont(font)
graph.addItem(temperature_text)
#hand
pen = pg.mkPen(width=6,color = (255,0,0))
pen.setCapStyle(QtCore.Qt.RoundCap)    
t_hand_plot = graph.plot(pen=pen)


def set_t(temp,temp2):
    #hand core 0
    deg_t=((temp-50)/200)*360
    x_t = np.sin(np.radians(deg_t)) * radius * 0.7
    y_t = np.cos(np.radians(deg_t)) * radius * 0.7
    t_hand_plot.setData([0, x_t], [0, y_t])
    #hand core 1
    '''
    deg_t2=((temp2-50)/200)*360
    x_t2 = np.sin(np.radians(deg_t2)) * radius * 0.7
    y_t2 = np.cos(np.radians(deg_t2)) * radius * 0.7
    t2_hand_plot.setData([0, x_t2], [0, y_t2])
    '''
    
    t2_hand_plot=graph.plot([-1.1,1.1],[-0.35,-0.35],pen=pg.mkPen(width=50,color=(0,0,0)))#linear
    
    for k in range(int(temp2-5),int(temp2+6)):
        line_length = 0.1 if k % 5 == 0 else 0.05 
        pen = pg.mkPen(width=2,color = (255,0,0)) if k % 5 == 0 else pg.mkPen(width=2,color = (255,255,255)) 
        m=int(k-temp2)
        n=m+4
        pen.setCapStyle(QtCore.Qt.RoundCap)    
        #t2_hand_plot =graph.plot(pen=pen)
        
        x1 = (m)/5
        x2 = (m)/5
        y1 = -0.5+line_length
        y2 = -0.5-line_length
        if k<0:
        	t2_hand_plot=graph.plot([x1, x2], [-0.6,-0.4], pen=pg.mkPen(width=2.5,color = (0,0,0)))
        elif m==0 and not k % 5 == 0:
        	graph.plot([0,0],[-0.4,-0.6],pen=pg.mkPen(width=6))
        	t2_hand_plot=graph.plot([x1, x2], [y1,y2], pen=pg.mkPen(width=2,color = (0,0,0)) )
        else:
                t2_hand_plot=graph.plot([x1, x2], [-0.6,-0.4], pen=pg.mkPen(width=2.5,color = (0,0,0)))
                t2_hand_plot=graph.plot([x1, x2], [y1,y2], pen=pen )
        if k % 5 == 0:
           text=str(k)
           p=0.04 if k>9 else 0.02
           cel_text = pg.TextItem(text[0:3], anchor=(0.25, 0.25))
           cel_text.setPos(x1-p, -0.3)
           font = QtGui.QFont() 
           font.setPixelSize(font_size) 
           cel_text.setFont(font)
           graph.addItem(cel_text)
           cel_texts.append(cel_text)
         
    time.sleep(0.1)

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
	
	


upT=QtCore.QTimer() 
upT.timeout.connect(update_temp)
upT.start(50) 


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([]) 
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
