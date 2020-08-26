from ImgDescriptor import ImgDescriptor
from Parameters import Parameters
from FeaturesStorage import FeaturesStorage
from SeqImageSearch import SeqImageSearch

import random

# import java.io.File;
# import java.io.IOException;
# import java.util.ArrayList;
# import java.util.Collections;
# import java.util.List;

class Pivots:

	seqPivots = SeqImageSearch()

	def __init__(self, pivotsFile):
		#Load the pivots file
		self.seqPivots.open(pivotsFile)

	def makeRandomPivots(ids, nPivs):
		pivots = None

		#LOOP
		#Create nPivs random pivots and add them in the pivots List
		#Use the position in the list as identifier not the name
		random.shuffle(ids)
		pivots = ids[0:nPivs]

		return pivots


	def features2Text(self, imgF, topK):
        #ImgDescriptor imgF, int topK, return String
		featureAsString = '';
		#perform a sequential search to get the topK most similar pivots
		searchResult = self.seqPivots.search(imgF, topK)
		#LOOP
		for descriptor in searchResult:
			for i in range(topK):
				featureAsString += descriptor.getId()
			featureAsString += '\n'
			topK -= 1
		#compose the text string using pivot ids

		return featureAsString

if __name__ == '__main__':
    ids = FeaturesStorage.load(Parameters.STORAGE_FILE);
    pivs = Pivots.makeRandomPivots(ids, Parameters.NUM_PIVOTS);
    FeaturesStorage.store(pivs, Parameters.PIVOTS_FILE);
