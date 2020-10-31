# -*- coding: utf-8 -*-
import subprocess
import pygame.midi

lctn = {"15": [110,1365], "25": [280,1365], "35": [450,1365], "45": [620,1365], "55": [790,1365], "65": [960,1365], \
           "16": [110,1530], "26": [280,1530], "36": [450,1530], "46": [620,1530], "56": [790,1530], "66": [960,1530], \
           "17": [110,1695], "27": [280,1695], "37": [450,1695], "47": [620,1695], "57": [790,1695], "67": [960,1695], \
           "18": [110,1860], "28": [280,1860], "38": [450,1860], "48": [620,1860], "58": [790,1860], "68": [960,1860], \
           "19": [110,2025], "29": [280,2025], "39": [450,2025], "49": [620,2025], "59": [790,2025], "69": [960,2025]}

def convert(num, location):  # 入力を命令に変換する関数
    NOTE_NAME = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # octave = (num // 12) - 1
    note = str(NOTE_NAME[num % 12])

    # 音階名と命令の対応
    move = {"C":-9, "D":1, "E":11, "empty":-10, "F":10, "G":9, "A":-1, "B":-11}
    arrow = {"C":"↙︎", "D":"↓", "E":"↘︎", "empty":"←", "F":"→", "G":"↗︎", "A":"↑", "B":"↖︎"}
    direction = arrow[note[0]]

    # 軌跡を表す数字に応じて現在地を変更する
    if(str(location + move[note[0]]) in list(lctn.keys())):
        nloc = location + move[note[0]]
    else:
        nloc = location
    return nloc, note, direction

def touch():  #  位置情報の軌跡通りに adb でタップ&スワイプ命令する
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "3", "57", "1"))
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "3", "48", "1"))
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "1", "330", "1"))
    
def swipe(xy):
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "3", "53", str(xy[0])))
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "3", "54", str(xy[1])))
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "0", "0", "0"))
    
def finish():
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "3", "57", "4294967295"))
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "1", "330", "0"))
    subprocess.call(("adb", "shell", "sendevent", "/dev/input/event1", "0", "0", "0"))


if __name__ =='__main__':

    pygame.init()
    pygame.midi.init()
    input_id = pygame.midi.get_default_input_id()
    i = pygame.midi.Input(input_id)
    print("input MIDI:%d" % input_id)
    print ("starting")

    location = 37
    
    touch()
    try:
        while True:
            if i.poll():
                midi_events = i.read(10)  # midi_events = [[[status,note,velocity,channel],timestamp],...]
                if(midi_events[0][0][1] == 96):  # C7押下で離す
                    finish()
                    location = 37
                    touch()
                elif(midi_events[0][0][0] == 155):  # 鍵盤を押下したとき
                    output = convert(midi_events[0][0][1], location)
                    swipe(lctn[str(output[0])])
                    print(output[1], output[2])
                    location = output[0]
    except KeyboardInterrupt:
        finish()

    i.close()
    pygame.midi.quit()
    pygame.quit()
    exit()
