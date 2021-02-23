import pyglet
from libraries.wavelengthToRGB.wavelengthToRGB import wavelengthToRGB

class pygletVertex:
    def __init__(self, batch, numVertices, vertexArray):
        self.numVertices = numVertices
        self.vertexArray = vertexArray
        
        visibleForegroundWavelenth = 680
        RGBValue = wavelengthToRGB(visibleForegroundWavelenth, 1)
        self.polygonColor = [RGBValue[0], RGBValue[1], RGBValue[2], 255]

    def initialDraw(self, batch):
        
        vertexList = self.updateBatch(batch)
        return vertexList

    def changeVertices(self, batch, numVertices, vertexArray):
        self.numVertices = numVertices
        self.vertexArray = vertexArray

        vertexList = self.updateBatch(batch)
        return vertexList

    def movePolygon(self, batch, direction, moveAmount):
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

        vertexList = self.updateBatch(batch)
        return vertexList

    def changeColor(self, batch, RGBValue):
        self.polygonColor = [RGBValue[0], RGBValue[1], RGBValue[2], 255]

        vertexList = self.updateBatch(batch)
        return vertexList


    def scalePolygon(self, batch, scalingFactor):
        for i in range(len(self.vertexArray)):
            # in order to scale the model, we can scale it with respect to the origin, ie bottom left of the screen window generated
            self.vertexArray[i] = scalingFactor * self.vertexArray[i]
            self.vertexArray[i] = int(self.vertexArray[i])

        vertexList = self.updateBatch(batch)
        return vertexList

    def updateBatch(self, batch):
        vertexList = batch.add(self.numVertices, pyglet.gl.GL_LINE_LOOP, None,('v2i', self.vertexArray), ('c4B', self.polygonColor*self.numVertices))
        return vertexList
