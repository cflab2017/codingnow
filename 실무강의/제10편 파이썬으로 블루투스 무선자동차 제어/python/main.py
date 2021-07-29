import serial
import keyboard as ky
# pip install serial
# pip install pyserial
# pip uninstall serial
###########################################
eventToValue = {
    "esc":0x40,     "space":0x40,
    "left":0x01,    "right":0x02,
    "up":0x04,      "down":0x08,
}
###########################################
seri = serial.Serial(port='COM10', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS) 
###########################################
def sendToAruino(key):
    comm = "KEY={:02x}".format(key)
    print('Send : ', comm)
    comm += '\n\n'
    seri.write(bytes(comm, encoding='ascii'))
###########################################
def eventProcess():
    eventPre = ''
    while True:
        event = ky.read_key()
        if event != eventPre:
            eventPre = event
            try:
                sendToAruino(eventToValue[event])
                if event == "esc":  # 종료
                    return
            except:
                pass                        
###########################################
eventProcess()
#종료 후
seri.close()
print('Finish')
###########################################







# if event == "esc":
#     sendToAruino(0x40)
#     return
# if event == "space":
#     sendToAruino(0x40)
# if event == "up":
#     sendToAruino(0x04)
# if event == "down":
#     sendToAruino(0x08)
# if event == "left":
#     sendToAruino(0x01)
# if event == "right":
#     sendToAruino(0x02)
