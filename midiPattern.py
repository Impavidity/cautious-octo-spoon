# -*- coding: utf-8 -*-
import midi
import time

class MidiPattern(object):
    def __init__(self, track_num):
        self.pattern = midi.Pattern()
        self.track_num = track_num
        self.trackList = list()
        self.baseTime = 0
        self.startTime = 0
        self.endTime = 0
        for i in range(track_num):
            self.trackList.append(midi.Track())

    def start_record(self):
        self.baseTime = time.time()
        self.startTime = self.baseTime
        print "Star record at time : ", self.baseTime

    def add_note(self, ctime, channel, note, velocity):
        tick = int((ctime - self.baseTime) / 0.002)
        self.baseTime = ctime
        print ctime, tick
        self.trackList[channel].append(midi.NoteOnEvent(tick=tick, channel=channel, data=[note, velocity]))

    def stop_record(self, name_id):
        for i in range(self.track_num):
            self.trackList[i].append(midi.EndOfTrackEvent(tick=1))
            self.pattern.append(self.trackList[i])
        name = str(name_id) + ".mid"
        self.endTime = time.time()
        midi.write_midifile(name, self.pattern)
        print "Stop record at time : ", time.time()
        print "Save the music to file : ", name
        print "The time is ", self.endTime-self.startTime, "s"
