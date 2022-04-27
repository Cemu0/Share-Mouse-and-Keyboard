import mouse
import keyboard
import socket
from time import sleep
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
# HOST_ADDR = "192.168.1.10"
# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)

def getkey(data,kew) -> str:
    return data[data.find(kew)+len(kew):data.rfind("\n")]
try:
    print("slave mode")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST_ADDR, 12345))
    while 1:
        data = s.recv(128).decode("ascii")
        # print("get",data) 
        try: 
            if "K1 " in data:
                key = int(data[data.find("K1 ")+3:data.rfind("\n")])
                # print("press",key)
                #debug only, can remove in product 
                if not keyboard.is_pressed(key):
                    keyboard.press(key)

            elif "K2 " in data:
                key = int(getkey(data,"K2 "))
                # print("release",key)
                if keyboard.is_pressed(key):
                    keyboard.release(key)

            elif "M1 " in data:
                key = getkey(data,"M1 ")
                mouse.release(key)
            elif "M2 " in data:
                key = getkey(data,"M2 ")
                mouse.press(key)
            elif "M3 " in data:
                key = getkey(data,"M3 ").split(" ")
                mouse.move(int(key[0]),int(key[1]))
            elif "M4 " in data:
                key = getkey(data,"M4 ")
                mouse.wheel(key)

        except:
            pass

except:
    print("host mode")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST_ADDR, 12345))
    s.listen(10)
    cL = []

    def sendKey(event):
        # print(event)
        key = event.scan_code or event.name
        # keyboard.press(key) if event.event_type == keyboard.KEY_DOWN else keyboard.release(key)
        # print(key)
        sendpkg = "K1 " + str(key) + "\n" if event.event_type == keyboard.KEY_DOWN else "K2 " + str(key) + "\n"
        
        try:
            for c in cL:
                c.send(bytearray(sendpkg.encode()))
        except:
            pass

    def sendMouse(event):
        # print(event)
        sendpkg = ""
        if isinstance(event, mouse.ButtonEvent):
            if event.event_type == mouse.UP:
                # mouse.release(event.button) #M1
                sendpkg="M1 " + str(event.button) + "\n"
            else:
                # mouse.press(event.button) #M2
                sendpkg="M2 " + str(event.button) + "\n"

        elif isinstance(event, mouse.MoveEvent):
            # mouse.move_to(event.x, event.y) #M3
            sendpkg="M3 " + str(event.x) + " " + str(event.y) + "\n"

        elif isinstance(event, mouse.WheelEvent):
            # mouse.wheel(event.delta)
            sendpkg="M4 " + str(event.delta) + "\n"

        # print(bytearray(sendpkg.encode()))
        try:
            for c in cL:
                c.send(bytearray(sendpkg.encode()))
        except:
            pass
    
    mouse.hook(sendMouse)
    keyboard.hook(sendKey)

    def loop():
        while(1):
            c, addr = s.accept()
            print('{} connected.'.format(addr))
            cL.append(c)
        
    x = threading.Thread(target=loop, args=(), daemon=True)
    x.start()

    keyboard.wait("F5")

