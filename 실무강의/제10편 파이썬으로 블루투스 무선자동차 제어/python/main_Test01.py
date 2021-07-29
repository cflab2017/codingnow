
import keyboard as kb
###########################################
eventToValue = {
    "esc":0x40,     
    "space":0x40,
    "left":0x01,    
    "right":0x02,
    "up":0x04,      
    "down":0x07,
}
###########################################
# while True:
#     event = kb.read_key()
#     print(event)
#     if event == 'esc':
#         break

###########################################
while True:
    event = kb.read_key()
    # print(event)
    try:
        # print(' : ', eventToValue[event])
        print(event,  '\t: ', "KEY={:02x}".format(eventToValue[event]))
    except:
        pass
    # print(event,  '\t: ', "KEY={:02x}".format(eventToValue[event]))

    if event == 'esc':
        break

###########################################
print('Finish')#종료 후
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
