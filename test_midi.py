# -*- coding: utf-8 -*-
import pygame.midi

pygame.init()
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
print("input MIDI:%d" % input_id)
i = pygame.midi.Input(input_id)

print ("starting")
print ("full midi_events:[[[status,data1,data2,data3],timestamp],...]")

count = 0
while True:
    if i.poll():
        midi_events = i.read(10)  # MIDIの入力待ち
        print("full midi_events:" + str(midi_events))  # 入力情報を表示
        count += 1
    if count >= 14:  # 14イベントで終了 
        break

i.close()
pygame.midi.quit()
pygame.quit()
exit()
