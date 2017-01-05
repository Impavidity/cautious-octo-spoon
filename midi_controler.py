import pygame.midi

class Midi(object):
    def __init__(self):
        self.player = None

    def setup(self):
        # Midi init 
        pygame.midi.init()
        synthReady = False
        while (not synthReady):
            for i in range(0, pygame.midi.get_count()):
                if ("Synth" in pygame.midi.get_device_info(i)[1]):
                    self.player = pygame.midi.Output(i)
                    synthReady = True
                    print "Bind to Fluidsynth successfully"

    def close(self):
        self.player.close()

    def setInstrument(self, instrument, channel):
        self.player.set_instrument(instrument, channel)
'''
    def noteOff(self, note, channel):
        self.player.node_off(note, 127, channel)

    def turnDown(self):
        del self.player
        pygame.midi.quit()
'''
