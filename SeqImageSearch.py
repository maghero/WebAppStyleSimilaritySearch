from ImgDescriptor import ImgDescriptor
from Parameters import Parameters
from FeaturesStorage import FeaturesStorage

from PaintingsCNN import StyleCNN
from Output import Output

# import java.io.File;
# import java.io.IOException;
# import java.util.Collections;
# import java.util.List;

class SeqImageSearch:

	descriptors = None #List<ImgDescriptor>

	def open(self, storageFile):
		self.descriptors = FeaturesStorage.load(storageFile)

	def search(self, queryF, k):
        #ImgDescriptor queryF, int k
        #return List<ImgDescriptor>
		time = -Parameters.current_milli_time()
		for i in range(len(self.descriptors)):
			self.descriptors[i].distance(queryF)

		time += Parameters.current_milli_time()
		print(str(time) + " ms")

		# print(self.descriptors)
		self.descriptors.sort()
		# print(self.descriptors)
		# print(len(self.descriptors));
		return self.descriptors[0:k];


if __name__ == '__main__':
    searcher = SeqImageSearch()

    print(Parameters.STORAGE_FILE)

    searcher.open(Parameters.STORAGE_FILE);

    cnn = StyleCNN()
    #Image Query File
    features = cnn.extractFeatures(Parameters.QRY_IMAGE)

    query = ImgDescriptor(features, Parameters.QRY_IMAGE.split('/')[-1])

    time = -Parameters.current_milli_time()
    res = searcher.search(query, Parameters.K);
    time += Parameters.current_milli_time();
    print("Sequential search time: " + str(time) + " ms"); #2526 ms

    Output.toHTML(res, Parameters.BASE_URI, Parameters.RESULTS_HTML);
