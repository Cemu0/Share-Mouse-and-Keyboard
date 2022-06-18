import mouse
import keyboard
import socket
from time import sleep, time
import threading

class datapk():
    def encrypt(self,inp,mode):
        #mouse
        if(mode == 0):
            pass
        pass
    def action(self,inp):
        pass

# role = "HOST"
# role = "SLAVE"
HOST_ADDR = input("please enter HOST Address:")
print("PRESS F5 to exit")

# HOST_ADDR = "192.168.1.78"
# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)

def getkey(data,kew) -> str:
    if data.find(kew)+len(kew) < data.rfind("\n"):
        return data[data.find(kew)+len(kew):data.rfind("\n")]
    return data[data.find(kew)+len(kew):]
try:
    print("slave mode")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST_ADDR, 12345))
    smm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    smm.connect((HOST_ADDR, 12346))

    def keycontrol():
        last_mouse_press = 0
        last_keyboard_press = 0
        while 1:
            data = s.recv(64).decode("ascii")
            # print("get",data) 
            try: 
                if "K1 " in data:
                    key = int(data[data.find("K1 ")+3:data.rfind("\n")])
                    # print("press",key)
                    #debug only, can remove in product 
                    if(last_keyboard_press > 0):
                        keyboard.release(key)
                        last_keyboard_press = key

                    if not keyboard.is_pressed(key):
                        keyboard.press(key)

                elif "K2 " in data:
                    key = int(getkey(data,"K2 "))
                    # print("release",key)
                    last_keyboard_press = -1
                    if keyboard.is_pressed(key):
                        keyboard.release(key)

                elif "M1 " in data:
                    key = getkey(data,"M1 ")
                    last_mouse_press = -1
                    mouse.release(key)
                elif "M2 " in data:
                    key = getkey(data,"M2 ")
                    if(last_mouse_press > 0):
                        mouse.release(key)
                        last_mouse_press = key
                    mouse.press(key)
                # elif "M3 " in data:
                #     key = getkey(data,"M3 ").split(" ")
                #     mouse.move(key[0],key[1])
                elif "M4 " in data:
                    key = getkey(data,"M4 ")
                    mouse.wheel(float(key))

                # print("success run",bytearray(data.encode())) 
            except:
                # print("corrupted package",bytearray(data.encode()))
                pass
            
    def mousecontrol():
        while 1:
            data = smm.recv(64).decode("ascii")
            key = data.split(" ")
            try: 
                mouse.move(key[0],key[1])
            except:
                pass
            
    x = threading.Thread(target=keycontrol, args=(), daemon=True)
    x.start()
    x = threading.Thread(target=mousecontrol, args=(), daemon=True)
    x.start()

    
    keyboard.wait("F5")

except:
    print("host mode")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST_ADDR, 12345))
    smm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    smm.bind((HOST_ADDR, 12346))
    s.listen(10)
    smm.listen(10)
    cL = []
    cLmm = []
    global lastsend
    global exit
    exit = False
    lastsend = time()
    def sendKey(event):
        # print(event)
        key = event.scan_code or event.name
        # keyboard.press(key) if event.event_type == keyboard.KEY_DOWN else keyboard.release(key)
        # print(key)
        sendpkg = "K1 " + str(key) + "\n" if event.event_type == keyboard.KEY_DOWN else "K2 " + str(key) + "\n"
        
        try:
            pkg = bytearray(sendpkg.encode())
            for c in cL:
                c.sendall(pkg)
        except:
            pass

    def sendMouse(event):
        # print(event)
        global lastsend
        sendpkg = ""
        if isinstance(event, mouse.ButtonEvent):
            if event.event_type == mouse.UP:
                # mouse.release(event.button) #M1
                sendpkg="M1 " + str(event.button) + "\n"
            else:
                # mouse.press(event.button) #M2
                sendpkg="M2 " + str(event.button) + "\n"

        elif isinstance(event, mouse.MoveEvent):

            # mouse.move(0, 0) #M3

            if(time() - lastsend > 0.05):
                sendpkg="" + str(event.x) + " " + str(event.y) + "\n"
                lastsend = time() 

                try:
                    pkg = bytearray(sendpkg.encode())
                    for c in cLmm:
                        c.sendall(pkg)
                except:
                    pass
    
            else:
                return

        elif isinstance(event, mouse.WheelEvent):
            # mouse.wheel(event.delta)
            # print(type(event.delta))
            sendpkg="M4 " + str(event.delta) + "\n"

        # print(bytearray(sendpkg.encode()))
        try:
            pkg = bytearray(sendpkg.encode())
            for c in cL:
                c.sendall(pkg)
        except:
            pass
    
    mouse.hook(sendMouse)
    keyboard.hook(sendKey)

    def loop():
        while(1):
            c, addr = s.accept()
            print('{} connected.'.format(addr))
            cL.append(c)
    
    def loop2():
        while(1):
            c, addr = smm.accept()
            print('{} connected.'.format(addr))
            cLmm.append(c)
        
    x = threading.Thread(target=loop, args=(), daemon=True)
    x.start()
    x = threading.Thread(target=loop2, args=(), daemon=True)
    x.start()

    def getkeys():
        global exit 
        keyboard.wait("F5")
        exit = True

    x1 = threading.Thread(target=getkeys, args=(), daemon=True)
    x1.start()

    while not exit:
        sleep(1)
   

