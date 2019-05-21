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
        import requests
        path_to_file = r"/home/nao/recordings/cameras/image.jpg"
        def post(file_type, path_to_file):
            url = "http://18.222.114.115:8080/"
            file = {file_type: open(path_to_file, 'rb')}
            response = requests.post(url, files=file)
            a=response.text
            self.tts.say(str(a))
        post('image', path_to_file)
        self.onStopped()

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box
