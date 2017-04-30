#Receive Bluetooth Controller events and translate them into key-presses

from bluetooth import *
import os
import time

connected = False
os.system("echo 0 > /home/pi/connected")

#from evdev import UInput, ecodes as e
#ui = UInput()

import uinput
events = (uinput.BTN_A, uinput.BTN_B, uinput.BTN_X, uinput.BTN_Y, uinput.BTN_TL, uinput.BTN_TR, uinput.BTN_SELECT, uinput.BTN_START, uinput.BTN_DPAD_UP, uinput.BTN_DPAD_DOWN, uinput.BTN_DPAD_LEFT, uinput.BTN_DPAD_RIGHT)
device = uinput.Device(events)

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ]
                    )

import select

while True:
    print("Waiting for connection...")
    client_sock, client_info = server_sock.accept()
    client_sock.setblocking(0)
    print("Accepted connection!")
    connected = True
    os.system("echo 1 > /home/pi/connected")

    try:
        lease = time.clock()
        while True:
            if time.clock() > lease + 0.0005:
                connected = False
                os.system("echo 0 > /home/pi/connected")
                print "b"
                break
            ready = select.select([client_sock], [], [], 1)
            if ready[0]:
                data = client_sock.recv(12)
            else:
                data = ""
            if len(data) == 0:
                connected = False
                os.system("echo 0 > /home/pi/connected")
                print "a"
                break
            print(data + "|")
            daetalist = list(data)
            for d in daetalist:
                if d == "R":
                    #ui.write(e.EV_KEY, e.KEY_R, 1)
                    device.emit(uinput.BTN_DPAD_RIGHT, 1)
                if d == "r":
                    #ui.write(e.EV_KEY, e.KEY_R, 0)
                    device.emit(uinput.BTN_DPAD_RIGHT, 0)
                if d == "L":
                    #ui.write(e.EV_KEY, e.KEY_L, 1)
                    device.emit(uinput.BTN_DPAD_LEFT, 1)
                if d == "l":
                    #ui.write(e.EV_KEY, e.KEY_L, 0)
                    device.emit(uinput.BTN_DPAD_LEFT, 0)
                if d == "U":
                    #ui.write(e.EV_KEY, e.KEY_U, 1)
                    device.emit(uinput.BTN_DPAD_UP, 1)
                if d == "u":
                    #ui.write(e.EV_KEY, e.KEY_U, 0)
                    device.emit(uinput.BTN_DPAD_UP, 0)
                if d == "D":
                    #ui.write(e.EV_KEY, e.KEY_D, 1)
                    device.emit(uinput.BTN_DPAD_DOWN, 1)
                if d == "d":
                    #ui.write(e.EV_KEY, e.KEY_D, 0)
                    device.emit(uinput.BTN_DPAD_DOWN, 0)
                if d == "A":
                    #ui.write(e.EV_KEY, e.KEY_A, 1)
                    device.emit(uinput.BTN_A, 1)
                if d == "a":
                    #ui.write(e.EV_KEY, e.KEY_A, 0)
                    device.emit(uinput.BTN_A, 0)
                if d == "B":
                    #ui.write(e.EV_KEY, e.KEY_B, 1)
                    device.emit(uinput.BTN_B, 1)
                if d == "b":
                    #ui.write(e.EV_KEY, e.KEY_B, 0)
                    device.emit(uinput.BTN_B, 0)
                if d == "X":
                    #ui.write(e.EV_KEY, e.KEY_X, 1)
                    device.emit(uinput.BTN_X, 1)
                if d == "x":
                    #ui.write(e.EV_KEY, e.KEY_X, 0)
                    device.emit(uinput.BTN_X, 0)
                if d == "Y":
                    #ui.write(e.EV_KEY, e.KEY_Y, 1)
                    device.emit(uinput.BTN_Y, 1)
                if d == "y":
                    #ui.write(e.EV_KEY, e.KEY_Y, 0)
                    device.emit(uinput.BTN_Y, 0)
                if d == "Q":
                    #ui.write(e.EV_KEY, e.KEY_Q, 1)
                    device.emit(uinput.BTN_START, 1)
                if d == "q":
                    #ui.write(e.EV_KEY, e.KEY_Q, 0)
                    device.emit(uinput.BTN_START, 0)
                if d == "W":
                    #ui.write(e.EV_KEY, e.KEY_W, 1)
                    device.emit(uinput.BTN_SELECT, 1)
                if d == "w":
                    #ui.write(e.EV_KEY, e.KEY_W, 0)
                    device.emit(uinput.BTN_SELECT, 0)
                if d == "S":
                    #ui.write(e.EV_KEY, e.KEY_S, 1)
                    device.emit(uinput.BTN_TL, 1)
                if d == "s":
                    #ui.write(e.EV_KEY, e.KEY_S, 0)
                    device.emit(uinput.BTN_TL, 0)
                if d == "F":
                    #ui.write(e.EV_KEY, e.KEY_F, 1)
                    device.emit(uinput.BTN_TR, 1)
                if d == "f":
                    #ui.write(e.EV_KEY, e.KEY_F, 0)
                    device.emit(uinput.BTN_TR, 0)
                if d == ".":
                    lease = time.clock()
    except IOError:
        connected = False
        os.system("echo 0 > /home/pi/connected")

client_sock.close()
server_sock.close()
ui.close()
