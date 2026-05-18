import pygame  # use pygame instead

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()  # initializes pygame


class SoundPlayer(pygame.mixer.Sound): # a class storing the path to an audio file which can play this audio file
    def __init__(self, path):
        super().__init__(path)
        self.not_stopped = False

    def playSound(self):
        try:
            self.not_stopped = True
            self.play()
        except:
            print("Unable to play audio")

    def playSoundUntilStopped(self): # plays sound until stopSound method is called
        try:
            self.not_stopped = True
            self.play(loops=-1)
        except:
            print("Unable to play audio")


    def stopSound(self): # stops the sound playing
        try:
            self.stop()
            self.not_stopped = False
        except:
            print("Couldn't stop sound")

    def isPlaying(self): # returns whether the sound is playing currently
        return not self.not_stopped