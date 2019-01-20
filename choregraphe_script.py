#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        #self.onStopped() #activate the output of the box
        import socket
        import requests

        self.tts = ALProxy('ALTextToSpeech')

        def post(file_type, path_to_file):
            url = "http://192.168.1.100:5000/upload_" + file_type
            file = {file_type: open(path_to_file, 'rb')}
            response = requests.post(url, files=file)
            a=response.text
            self.tts.say(str(a))

        path_to_im = r"/home/nao/recordings/microphones/recording.ogg"

        post("audio", path_to_im)
        self.onStopped()

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box

