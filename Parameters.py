import time

class Parameters:

	#CNN Parameters
	IMG_WIDTH = 224
	IMG_HEIGHT = 224

	#Image Source Folder
	SRC_FOLDER = "Images"

    #Query Image source
	QRY_IMAGE = SRC_FOLDER + "/query.jpg"

	#Features Storage File
	STORAGE_FILE = "./extractedFeatures/STYLE/style_paint_deep_feature.json"

	#Feature Source Folder
	SRC_FEATURE = "../extractedFeatures/actualImage.json"

	#k-Nearest Neighbors
	K = 30

	#Number of images to get from elastic search
	NUM_IMAGES = 100

	#Pivots File
	PIVOTS_FILE = "out/paintings.pivots.dat";

	#Number Of Pivots
	NUM_PIVOTS = 100

	#Top K pivots For Indexing
	TOP_K_IDX = 10

	#Top K pivots For Searching
	TOP_K_QUERY = 10

	#Lucene Index
	INDEX_NAME = "paintings"

    #Elasticsearch Configuration
	elastic_config = 'http://127.0.0.1:9200/'

	#HTML Output Parameters
	# BASE_URI = "file:///" + SRC_FOLDER + "/"
	BASE_URI =  SRC_FOLDER + "/"
	RESULTS_HTML = "templates/deep.seq.html"
	RESULTS_HTML_ELASTIC = "templates/deep.elastic.html"
	RESULTS_HTML_REORDERED = "templates/deep.reordered.html"

    #currentTime
	current_milli_time = lambda: int(round(time.time() * 1000))
