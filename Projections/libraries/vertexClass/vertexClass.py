import pyglet
from libraries.wavelengthToRGB.wavelengthToRGB import wavelengthToRGB

class pygletVertex:
    def __init__(self, batch, numVertices, vertexArray):
        self.batch = batch
        self.numVertices = numVertices
        self.vertexArray = [None]*numVertices*2
        self.vertexArray = vertexArray
        
        visibleForegroundWavelenth = 680
        RGBValue = wavelengthToRGB(visibleForegroundWavelenth, 1)
        self.polygonColor = [RGBValue[0], RGBValue[1], RGBValue[2], 255]

    def changeVertices(self,numVertices,vertexArray):
        self.numVertices = numVertices
        self.vertexArray = vertexArray

        self.updateBatch()
        return self.batch

    def changeDirection(self, direction, moveAmount):
        if direction == 'up':
            for i in range(len(self.vertexArray)):
                if i % 2 == 1:
                    self.vertexArray[i] += moveAmount
        if direction == 'down':
            for i in range(len(self.vertexArray)):
                if i % 2 == 1:
                    self.vertexArray[i] -= moveAmount
        if direction == 'left':
            for i in range(len(self.vertexArray)):
                if i % 2 == 0:
                    self.vertexArray[i] -= moveAmount
        if direction == 'right':
            for i in range(len(self.vertexArray)):
                if i % 2 == 0:
                    self.vertexArray[i] += moveAmount

        self.updateBatch()
        return self.batch

    def changeColor(self,RGBValue):
        self.polygonColor = [RGBValue[0], RGBValue[1], RGBValue[2], 255]

        self.updateBatch()
        return self.batch

    def updateBatch(self):
        self.batch = None
        self.batch = pyglet.graphics.Batch()
        self.batch.add(self.numVertices, pyglet.gl.GL_POLYGON, None, ('v2i',self.vertexArray), ('c4B',self.polygonColor*self.numVertices))

    def initialDraw(self):
        self.updateBatch()
        return self.batch
