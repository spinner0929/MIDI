# -*- coding: utf-8 -*-
import pygame.midi
from pychord import note_to_chord

pygame.init()
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
i = pygame.midi.Input(input_id)
print("input MIDI:%d" % input_id)
print ("starting")

going = True
pre_status = 156 
inputs = []

def convert(list):  # 数値をノート名に変換する関数
    NOTE_NAME = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # octave = (number // 12) - 1
    note_list = [str(NOTE_NAME[i % 12]) for i in list]
    return note_list

while going:
    if i.poll():
        midi_events = i.read(10)  # midi_events = [[[status,note,velocity,channel],timestamp],...]
        if(midi_events[0][0][1] == 96):  # C7 押下で終了
            going = False
        elif(midi_events[0][0][0] == 156):  # 鍵盤を押下したとき
            inputs.append(midi_events[0][0][1])
        elif(midi_events[0][0][0] == 140): # 鍵盤を離したとき
            if(pre_status == 156): # 鍵盤を押下していたとき
                inputs.sort()
                notes = convert(inputs)
                notes_list = sorted(set(notes), key=notes.index)
                print(notes_list, note_to_chord(notes_list))
            inputs = []
        pre_status = midi_events[0][0][0]  # 前の status を保存する

i.close()
pygame.midi.quit()
pygame.quit()
exit()