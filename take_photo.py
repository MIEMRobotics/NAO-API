import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.resolutionMap = {
            '160 x 120': 0,
            '320 x 240': 1,
            '640 x 480': 2,
            '1280 x 960': 3
        }
        self.cameraMap = {
            'Top': 0,
            'Bottom': 1
        }

        self.recordFolder = "/home/nao/recordings/cameras/"

    def onLoad(self):
        self.bIsRunning = False
        try:
            self.photoCapture = ALProxy( "ALPhotoCapture" )
        except Exception as e:
            self.photoCapture = None
            self.logger.error(e)

    def onUnload(self):
        pass

    def onInput_onStart(self):
        if( self.bIsRunning ):
            return
        self.bIsRunning = True
        resolution = self.resolutionMap[self.getParameter("Resolution")]
        cameraID = self.cameraMap[self.getParameter("Camera")]
        fileName = self.getParameter("File Name")
        if self.photoCapture:
            self.photoCapture.setResolution(resolution)
            self.photoCapture.setCameraID(cameraID)
            self.photoCapture.setPictureFormat("jpg")
            self.photoCapture.takePicture( self.recordFolder, fileName )
        self.bIsRunning = False
        self.onStopped()
