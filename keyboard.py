# -*-coding:utf-8 -*-
class Keyboard(object):
    def __init__(self, number, channel, inst_num,
        volume, reverb, velocity, baseNote, sust):
        self.number = number
        self.channel = channel
        self.inst_num = inst_num
        self.volume = volume
        self.reverb = reverb
        self.velocity = velocity
        self.baseNote = baseNote
        self.pressed = dict()
        self.sust = 0
        self.noteOf = dict()

    def config(self, midi):
        midi.player.set_instrument(self.inst_num, self.channel)
        #midi.player.write_short() # Do not understand here

    def key_up(self, midi, keyname, note):
        if self.pressed[keyname] > 0: # Only turn it OFF if it is ON 
            self.pressed[keyname] -= 1
            if self.pressed[keyname] <= 0:
                midi.player.note_off(note, self.velocity, self.channel)

    def key_down(self, midi, keyname, note):
        self.key_up(midi, keyname, note) # If it's already ON, turn it OFF first
        midi.player.note_on(note, self.velocity, self.channel)
        self.pressed[keyname] += (1 + self.sust)