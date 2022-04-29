import mousejklertdcvcv 
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
# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)

def getkey(data,kew) -> str:
    if data.find(kew)+len(kew) < data.rfind("\n"):
        return data[data.find(kew)+len(kew):data.rfind("\n")]
    return data[data.find(kew)+len(kew):]

try:
    print("slave mode")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sfast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((HOST_ADDR, 12345))
    sfast.bind(("", 5005))

    def mouseMove():
        while 1:
            data, addr = sfast.recvfrom(64) # buffer size is 1024 bytes
            (x,y) = data.decode("ascii").split(" ")
            mouse.move(x,y)
    
    x = threading.Thread(target=mouseMove, args=(), daemon=True)
    x.start()

    while 1:
        data = s.recv(64).decode("ascii")
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

except:
    print("host mode")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST_ADDR, 12345))
    sfast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sfast.bind(("0.0.0.0", 5005))

    s.listen(10)
    cL = []
    adrL = []
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
            # mouse.move_to(event.x, event.y) #M3
            if(time() - lastsend > 0.01):
                sendpkg="M3 " + str(event.x) + " " + str(event.y) + "\n"
                lastsend = time() 
                MESSAGE = bytearray(sendpkg.encode())
                for addr in adrL:
                    sfast.sendto(MESSAGE, (str(addr), 5005))
                return 
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
            adrL.append(addr)
        
    x = threading.Thread(target=loop, args=(), daemon=True)
    x.start()

    def getkeys():
        global exit 
        keyboard.wait("F5")
        exit = True

    x1 = threading.Thread(target=getkeys, args=(), daemon=True)
    x1.start()

    while not exit:
        sleep(1)
   

