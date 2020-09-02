from ImgDescriptor import ImgDescriptor
from Parameters import Parameters
from FeaturesStorage import FeaturesStorage
from elasticsearch import helpers, Elasticsearch
from Pivots import Pivots
from Fields import Fields

class ElasticImgIndexing:

    #Pivots
    pivots = None

    #List<ImgDescriptor>
    imgDescDataset = None

    #int
    topKIdx = None

	#RestHighLevelClient
    client = None

    def __init__(self, pivotsFile, datasetFile, topKIdx):
		#Initialize pivots, imgDescDataset, REST
        self.pivots = Pivots(pivotsFile);
        self.imgDescDataset = FeaturesStorage.load(datasetFile);
        self.topKIdx = topKIdx;
        #The rest client needed to contact
		# RestClientBuilder builder = RestClient.builder(new HttpHost("localhost", 9200, "http"));
		# client = new RestHighLevelClient(builder);
        self.client = Elasticsearch([Parameters.elastic_config])

    def close(self):
        #close REST client
        self.client.close();

    def createIndex(self):
		#Create the Elasticsearch index
        request_body = {
    	    "settings" : {
    	        "number_of_shards": 1,
    	        "number_of_replicas": 0,
                "analysis.analyzer.first.type": "whitespace"
    	    },

            "mapping": {
                "doc": {
                  "properties": {
                    "ID": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "img": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                }
              }
    	}
        self.client.indices.create(index = Parameters.INDEX_NAME, body = request_body)


    def index(self):
		#LOOP
			#index all dataset features into Elasticsearch
        for imgDescriptor in self.imgDescDataset:
            features = self.pivots.features2Text(imgDescriptor, self.topKIdx)
            request = self.composeRequest(imgDescriptor.getId(), features)
            self.client.bulk(index = Parameters.INDEX_NAME, body = request)


    def composeRequest(self, id, imgTxt):
		#Initialize and fill IndexRequest Object with Fields.ID and Fields.IMG txt
        request = [];
        jsonMap = {}

        jsonMap[Fields.ID] = id
        jsonMap[Fields.IMG] = imgTxt

        op_dict = {
	        "index": {
	            "_index": Parameters.INDEX_NAME,
	            "_type": 'doc',
	            "_id": jsonMap[Fields.ID]
	        }
	    }

        request.append(op_dict)
        request.append(jsonMap)

        return request;


if __name__ == '__main__':
    esImgIdx = ElasticImgIndexing(Parameters.PIVOTS_FILE, Parameters.STORAGE_FILE, Parameters.TOP_K_IDX)
    print("Creating Index")
    esImgIdx.createIndex()
    esImgIdx.index()

    esImgIdx.close()
