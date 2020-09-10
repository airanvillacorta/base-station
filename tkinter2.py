#encoding: utf-8
from Tkinter import *
import ttk
import parameters as param

label_c_dat = None
label_c_pos = None
label_c_pos2 = None
label_m_dat = None
label_m_pos = None
label_dif = None
label_counter = None

raiz = None
stop = False

def update_label():
	def loop():
		global label_m_dat, label_m_pos, label_c_dat, label_c_pos, label_c_pos2, label_dif, label_counter, stop
		
		label_c_dat.config(text = "Camera - Location information for " + str(param.nCamera) + " events.")
		label_c_pos.config(text = " -> xRed: " + str(param.bxRed) + " cpdRed: " + str(param.cpdRed) + " xBlue: " + str(param.bxBlue) + " cpdBlue: " + str(param.cpdBlue) + " xGreen: " + str(param.bxGreen) + " cpdGreen: " + str(param.cpdGreen))
		label_c_pos2.config(text = " -> fTheta: " + str(param.fThetaFromCamera) + " fX: " + str(param.fXFromCamera) + " fZ: "  + str(param.fZFromCamera))
		label_m_dat.config(text = "Robot - Fiducial location information for " + str(param.nRobot) + " events.")
		label_m_pos.config(text = " -> fTheta: " + str(param.fTheta) + " fX: " + str(param.fX) + " fZ: "  + str(param.fZ))
		label_dif.config(text = "Difference of robot and camera data -> fTheta: " + str(param.dif_fTheta) + " fX: " + str(param.dif_fX) + " fZ: " + str(param.dif_fZ))
		label_counter.config(text = "Buffers Procesados: " + str(param.counter))

		label_m_pos.after(1000, loop)
		if stop:
			return False
	if loop() == False:
		pass

def close_window():
	global raiz
	param.close = True

def gui():
	global label_m_dat, label_m_pos, label_c_dat, label_c_pos, label_c_pos2, label_dif, label_counter, raiz

	raiz = Tk()
	raiz.geometry('1000x190')
	raiz.title('Show Values')

	label_c_dat = Label(raiz, justify=LEFT, text="Camera - Location information for 0 events.", anchor="nw")
	label_c_dat.pack(fill=X)
	label_c_dat.place(x=25, y=15)
	label_c_pos = Label(raiz, justify=LEFT, text=" -> xRed: nan cpdRed: nan xBlue: nan cpdBlue: nan xGreen: nan cpdGreen: nan", anchor="nw")
	label_c_pos.pack(fill=X)
	label_c_pos.place(x=25, y=35)
	label_c_pos2 = Label(raiz, justify=LEFT, text=" -> fTheta: nan fX: nan fZ: nan", anchor="nw")
	label_c_pos2.pack(fill=X)
	label_c_pos2.place(x=25, y=55)
	label_m_dat = Label(raiz, justify=LEFT, text="Robot - Fiducial location information for 0 events.", anchor="nw")
	label_m_dat.pack(fill=X)
	label_m_dat.place(x=25, y=75)
	label_m_pos = Label(raiz, justify=LEFT, text=" -> fTheta: nan fX: nan fZ: nan", anchor="nw")
	label_m_pos.pack(fill=X)
	label_m_pos.place(x=25, y=95)
	label_dif = Label(raiz, justify=LEFT, text="Difference of robot and camera data -> fTheta: nan fX: nan fZ: nan", anchor="nw")
	label_dif.pack(fill=X)
	label_dif.place(x=25, y=115)
	label_counter = Label(raiz, justify=LEFT, text="Buffers Procesados: 0", anchor="nw")
	label_counter.pack(fill=X)
	label_counter.place(x=25, y=135)

	#ttk.Button(raiz, text='Quit', command=quit).pack(side=BOTTOM, fill=X, padx=5, pady=5)
	ttk.Button(raiz, text='Stop simulation', command=close_window).pack(side=BOTTOM, fill=X, padx=5, pady=5)

	update_label()
	raiz.mainloop()


