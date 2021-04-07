from pyglet.gl import *
from OpenGL.GLU import *
from OpenGL.GL import *
import pyglet
from libraries.wavelengthToRGB.wavelengthToRGB import wavelengthToRGB
import sys


class pygletVertex:
    def __init__(self, batch, vertexArray,wavelengthColor):
        self.numVertices = int(len(vertexArray)/2)
        self.vertexArray = vertexArray
        self.triangleArray = []
        self.vertexList = [None]
        
        RGBValue = wavelengthToRGB(wavelengthColor, 1)
        self.polygonColor = [RGBValue[0], RGBValue[1], RGBValue[2], 255]

    def initialDraw(self, batch):
        
        self.vertexList = self.updateBatch(batch)
        return self.vertexList

    def changeVertices(self, batch, vertexArray):
        self.numVertices = numVertices
        self.vertexArray = vertexArray

        self.vertexList = self.updateBatch(batch)
        return self.vertexList

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

        self.vertexList = self.updateBatch(batch)
        return self.vertexList

    def changeColor(self, batch, RGBValue):
        self.polygonColor = [RGBValue[0], RGBValue[1], RGBValue[2], 255]

        self.vertexList = self.updateBatch(batch)
        return self.vertexList


    def scalePolygon(self, batch, scalingFactor):
        for i in range(len(self.vertexArray)):
            # in order to scale the model, we can scale it with respect to the origin, ie bottom left of the screen window generated
            self.vertexArray[i] = scalingFactor * self.vertexArray[i]
            self.vertexArray[i] = int(self.vertexArray[i])

        self.vertexList = self.updateBatch(batch)
        return self.vertexList

    def triangulate(self, polygon, holes=[]):
        """
        Returns a list of triangles.
        Uses the GLU Tesselator functions!
        """
        vertices = []
        def edgeFlagCallback(param1, param2): pass

        def beginCallback(param=None):
            vertices = []

        def vertexCallback(vertex, otherData=None):
            vertices.append(vertex[:2])

        def combineCallback(vertex, neighbors, neighborWeights, out=None):
            out = vertex
            return out

        def endCallback(data=None): pass

        tess = gluNewTess()
        gluTessProperty(tess, GLU_TESS_WINDING_RULE, GLU_TESS_WINDING_ODD)
        # forces triangulation of polygons (i.e. GL_TRIANGLES) rather than returning triangle fans or strips
        gluTessCallback(tess, GLU_TESS_EDGE_FLAG_DATA, edgeFlagCallback)
        gluTessCallback(tess, GLU_TESS_BEGIN, beginCallback)
        gluTessCallback(tess, GLU_TESS_VERTEX, vertexCallback)
        gluTessCallback(tess, GLU_TESS_COMBINE, combineCallback)
        gluTessCallback(tess, GLU_TESS_END, endCallback)
        gluTessBeginPolygon(tess, 0)

        #first handle the main polygon
        gluTessBeginContour(tess)
        for point in range(len(polygon)):
            if point % 2 == 0:
                point3d = (polygon[point], polygon[point+1], 0)
            else:
                pass
            gluTessVertex(tess, point3d, point3d)
        gluTessEndContour(tess)

        #then handle each of the holes, if applicable
        if holes != []:
            for hole in holes:
                gluTessBeginContour(tess)
                for point in hole:
                    point3d = (point[0], point[1], 0)
                    gluTessVertex(tess, point3d, point3d)
                gluTessEndContour(tess)

        gluTessEndPolygon(tess)
        gluDeleteTess(tess)
        flat_list_vertices = [item for sublist in vertices for item in sublist]
        self.numVerticesTriangle = int(len(flat_list_vertices)/2)


        def cast_list(test_list, data_type):
            return list(map(data_type, test_list))

        flat_list_vertices = cast_list(flat_list_vertices, int)

        return flat_list_vertices

    def updateBatch(self, batch):
        self.triangleArray = self.triangulate(self.vertexArray)
        self.vertexList = None # prevents memory leaks
        self.vertexList = batch.add(self.numVerticesTriangle, pyglet.gl.GL_TRIANGLES, None,('v2i', self.triangleArray), ('c4B', self.polygonColor*self.numVerticesTriangle))
        return self.vertexList
