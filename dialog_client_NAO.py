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
        import time
        import socket

        def sock_create(ip,port):
            sock = socket.socket()
            sock.connect((ip, port))
            return sock

        def sock_send_voice(path_to_file,sock):

            f=open(path_to_file,'rb')
            l=f.read()
            length = len(l)
            sock.send(str(length))# отправляем длину строки
            f.close()

            f=open(path_to_file,"rb")
            l=f.read(1024) # отправляем строку
            while (l):
                sock.send(l)
                l = f.read(1024)
            f.close()

        def sock_recv_str(sock,self):
            data=sock.recv(1024)
            self.tts = ALProxy('ALTextToSpeech')
            self.tts.say(data)

        def record_audio(self):
            self.tts = ALProxy('ALAudioDevice')
            self.tts.flushAudioOutputs()
            self.tts.startMicrophonesRecording("/home/nao/recordings/microphones/recording.ogg")
            time.sleep(2)
            self.tts.stopMicrophonesRecording()


        def micro_check_record(sock,self):
            import time
            i=0
            self.leds = ALProxy("ALLeds")
            while i<200:
                self.tts=ALProxy('ALAudioDevice')
                self.tts.enableEnergyComputation()
                if self.tts.getFrontMicEnergy()>1000:
                    self.leds.fadeRGB("AllLeds", 'green', 0.1)
                    print(self.tts.getFrontMicEnergy())
                    record_audio(self)
                    self.leds.fadeRGB("AllLeds", 'white', 0.1)
                    sock_send_voice(path_to_file,sock)
                    sock_recv_str(sock,self)
                    i=0#обнуление счетчика чтобы слушать 5 секунд
                time.sleep(0.25)
                i+=1
                print(sock)

        path_to_file = r"/home/nao/recordings/microphones/recording.ogg"
        ip='172.18.161.148'
        port=9900
        sock = sock_create(ip,port)
        micro_check_record(sock,self)
        sock.close()
        self.onStopped()

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box
