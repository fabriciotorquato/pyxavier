import sys
import os
import pyscreenshot as ImageGrab

class App(object):

    def screenshot(self, saveFolder,name):
        path = saveFolder + "/" + name + '.png'
        im=ImageGrab.grab()
        im.save(path)
        os.chmod(path, 0o777)


