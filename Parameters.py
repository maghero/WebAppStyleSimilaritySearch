import time

class Parameters:

	# //DEEP parameters
	# public static final String DEEP_PROTO = "data/caffe/train_val.prototxt";
	# public static final String DEEP_MODEL = "data/caffe/bvlc_reference_caffenet.caffemodel";
	# public static final double[] MEAN_VALUES = {104, 117, 123, 0};
    #
	# public static final String DEEP_LAYER = "fc7";
	# public static final int IMG_WIDTH = 227;
	# public static final int IMG_HEIGHT = 227;


	#Image Source Folder
	SRC_FOLDER = "Images"

    #Query Image source
	QRY_IMAGE = SRC_FOLDER + "/query.jpg"

	#Features Storage File
	STORAGE_FILE = "../extractedFeatures/STYLE/style_paint_deep_feature.json"

	#Feature Source Folder
	SRC_FEATURE = "../extractedFeatures/actualImage.json"

	#k-Nearest Neighbors
	K = 30;

	#Pivots File
	PIVOTS_FILE = "out/paintings.pivots.dat";

	#Number Of Pivots
	NUM_PIVOTS = 100;

	#Top K pivots For Indexing
	TOP_K_IDX = 10;

	#Top K pivots For Searching
	TOP_K_QUERY = 10;

	#Lucene Index
	INDEX_NAME = "paintings";

    #Elasticsearch Configuration
	elastic_config = 'http://127.0.0.1:9200/'
    # {
	# 	'host': 'localhost',
    #     'scheme': "http",
	# 	'port': 9200,
	# }

	#HTML Output Parameters
	# BASE_URI = "file:///" + SRC_FOLDER + "/"
	BASE_URI =  SRC_FOLDER + "/"
	RESULTS_HTML = "templates/deep.seq.html"
	RESULTS_HTML_ELASTIC = "templates/deep.elastic.html"
	RESULTS_HTML_REORDERED = "templates/deep.reordered.html"

    #currentTiem
	current_milli_time = lambda: int(round(time.time() * 1000))
