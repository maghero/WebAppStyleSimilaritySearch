import math
from functools import total_ordering

@total_ordering
class ImgDescriptor:
    normalizedVector = None#float[] image feature
    id = "" #String unique id of the image (usually file name)
    dist = -1 #Double used for sorting purposes

    def __init__(self, features, id):
        if features != None:
            norm2 = self.evaluateNorm2(features)
            self.normalizedVector = self.getNormalizedVector(features, norm2)
        self.id = id

    def getFeatures(self):
        return self.normalizedVector

    def setFeatures(self, features):
        norm2 = self.evaluateNorm2(features)
        self.normalizedVector = self.getNormalizedVector(features, norm2)


    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getDist(self):
        return self.dist

    def setDist(self, dist):
        self.dist = dist

    # Used for the total ordering
    def __eq__(self, arg0):
        return self.dist == arg0.dist

    def __lt__(self, arg0):
        return self.dist < arg0.dist

	#evaluate Euclidian distance
    def distance(self, desc):

        queryVector = desc.getFeatures()

        self.dist = 0
        for i in range(len(queryVector)):
            self.dist += (self.normalizedVector[i] - queryVector[i]) * (self.normalizedVector[i] - queryVector[i])

        self.dist = math.sqrt(self.dist)
        return self.dist

	#Normalize the vector values
    def getNormalizedVector(self, vector, norm):
        if norm != 0:
            for i in range(len(vector)):
                vector[i] = vector[i]/norm

        return vector

	#Norm 2
    def evaluateNorm2(self, vector):
        norm2 = 0

        for i in range(len(vector)):
            norm2 += (vector[i]) * (vector[i])

        return math.sqrt(norm2)
