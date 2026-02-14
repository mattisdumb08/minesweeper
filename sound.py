import pygame as pg

pg.mixer.init()

globalVolume = 1

pg.mixer.set_num_channels(16)


class ChannelWrapper:

    def __init__(self, id):
        self.channelObject = pg.mixer.Channel(id)

    def playAll(self):

        nextSound = self.channelObject.get_queue()

        while nextSound != None:

            nextSound.play()

            nextSound = self.channelObject.get_queue()
    
    def queue(self , newSound : pg.mixer.Sound):
        self.channelObject.queue(newSound)

soundEffectsChannel = ChannelWrapper(0)

def playYippee():

    yippeeSound = pg.mixer.Sound("Yippee.mp3")
    yippeeSound.set_volume(globalVolume)

    yippeeSound.play()

    # soundEffectsChannel.queue(yippeeSound)