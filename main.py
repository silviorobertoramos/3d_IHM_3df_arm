import math
from os import close, stat
from tkinter import *
from robot import Robot
from tkinter import ttk
import serial
import serial.tools.list_ports


ser = serial.Serial(timeout = None)
ser.baudrate = 115200
ser.port = 'COM25'

initial_x = 0
clicking = False

def left_click(event):
  global clicking
  clicking = True

def left_release(event):
  global clicking
  clicking = False

def left_motion(event):
  robot.angle = 0
  robot.updateTarget(event.x, event.y)
  sliders['rotate'].set(0)
  sliders['arm1'].set(robot.arms[0].angle + math.pi/2)
  sliders['arm2'].set(robot.arms[1].angle - robot.arms[0].angle)

  try:
    serial_msg = str(robot.angle) + ';' + str(robot.arms[0].angle) + ';' + str(robot.arms[1].angle) + ';'
    ser.write(serial_msg.encode())
  except:
    pass


def right_click(event):
  global initial_x, clicking
  initial_x = event.x
  clicking = True

def right_release(event):
  global clicking
  clicking = False

def right_motion(event):
  global initial_x
  robot.rotate(event.x - initial_x)
  try:
    serial_msg = str(robot.angle) + ';' + str(robot.arms[0].angle) + ';' + str(robot.arms[1].angle) + ';'
    ser.write(serial_msg.encode())
  except:
    pass

def slide_rotate(var):
  if not clicking:
    robot.updateAngle(sliders['rotate'].get())
    try:
      serial_msg = str(robot.angle) + ';' + str(robot.arms[0].angle) + ';' + str(robot.arms[1].angle) + ';'
      ser.write(serial_msg.encode())
    except:
      pass

def slide_arm1(var):
  if not clicking:
    robot.updateArm1(sliders['arm1'].get() - math.pi/2);
    try:
      serial_msg = str(robot.angle) + ';' + str(robot.arms[0].angle) + ';' + str(robot.arms[1].angle) + ';'
      ser.write(serial_msg.encode())
    except:
      pass

def slide_arm2(var):
  if not clicking:
    robot.updateArm2(sliders['arm2'].get());
    try:
      serial_msg = str(robot.angle) + ';' + str(robot.arms[0].angle) + ';' + str(robot.arms[1].angle) + ';'
      ser.write(serial_msg.encode())
    except:
      pass

def emergency_stop():
  ser.write(b'STOP')

def set_baud():
  global ser
  try:
    ser.baudrate = int(baudrate_text.get())
  except:
    print('error setting baud')


def close_serial():
  global ser
  ser.close()
  open_serial_button.config(state = NORMAL)
  baudrate_button.config(state = NORMAL)
  baudrate_text.config(state = NORMAL)
  com_combobox.config(state = NORMAL)
  close_serial_button.config(state = DISABLED)

def open_serial():
  global ser
  ser.open()
  open_serial_button.config(state = DISABLED)
  baudrate_button.config(state = DISABLED)
  baudrate_text.config(state = DISABLED)
  com_combobox.config(state = DISABLED)
  close_serial_button.config(state = NORMAL)

def choosing_com():
  com_combobox["values"] =list(serial.tools.list_ports.comports())


def selected_com(event):
  com = com_combobox.get().split(' ')
  ser.port = com[0]

# Variáveis
root = Tk()
w = 600
h = 500
canvas =  Canvas(root, width=w, heigh=h, bg='white')
robot = Robot(canvas, 150, w/2, 3*h/4)
sliders = {
  'rotate' : Scale(root, from_= - math.pi, to= math.pi, orient=HORIZONTAL, command = slide_rotate, length = 300, resolution = 0.01),
  'arm1' : Scale(root, from_= - math.pi, to= math.pi, orient=HORIZONTAL, command = slide_arm1, length = 300, resolution = 0.01),
  'arm2': Scale(root, from_= - math.pi, to= math.pi, orient=HORIZONTAL, command = slide_arm2, length = 300, resolution = 0.01)
}
labels = {
  'rotate' : Label(root, text = 'Ângulo de Rotação'),
  'arm1' : Label(root, text = 'Ângulo da Base'),
  'arm2': Label(root, text = 'Ângulo da Ponta')
}
emergency_button = Button(root, text = "Stop", command = emergency_stop, anchor = W, bg = 'red')
emergency_button.configure(width = 5, activebackground = "red")
emergency_window = canvas.create_window(10, 10, anchor=NW, window=emergency_button)
open_serial_button = Button(root, text = 'Open Serial', command = open_serial)
close_serial_button = Button(root, text = 'Close Serial', command = close_serial, state = DISABLED)
com_combobox = ttk.Combobox(root, text = '', postcommand = choosing_com, )
baudrate_text = Entry(root)
baudrate_text.insert(INSERT, '115200')
baudrate_button = Button(root, text = 'Set Baudrate', command = set_baud)

canvas.bind('<Button-1>', left_click)
canvas.bind('<ButtonRelease-1>', left_release)
canvas.bind('<B1-Motion>', left_motion)
canvas.bind('<Button-3>', right_click)
canvas.bind('<ButtonRelease-3>', right_release)
canvas.bind('<B3-Motion>', right_motion)
com_combobox.bind("<<ComboboxSelected>>", selected_com)

canvas.grid(row = 1, column = 1)
canvas.update()

sliders['rotate'].grid(row = 2, column = 1)
labels['rotate'].grid(row = 3, column = 1)
sliders['arm1'].grid(row = 4, column = 1)
labels['arm1'].grid(row = 5, column = 1)
sliders['arm2'].grid(row = 6, column = 1)
labels['arm2'].grid(row = 7, column = 1)
open_serial_button.grid(row = 2, column = 2)
close_serial_button.grid(row = 3, column = 2)
com_combobox.grid(row = 4, column = 2)
baudrate_text.grid(row = 5, column = 2)
baudrate_button.grid(row = 6, column = 2)

# Loop
root.mainloop()
