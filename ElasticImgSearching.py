from ImgDescriptor import ImgDescriptor
from Parameters import Parameters
from FeaturesStorage import FeaturesStorage
from StyleCNN import StyleCNN
from Output import Output
from Fields import Fields
from Pivots import Pivots
from elasticsearch import helpers, Elasticsearch

import json


class ElasticImgSearching:

	# RestHighLevelClient
    client = None

	# Pivots
    pivots = None

	# int
    topKSearch = None

	# Map< String,ImgDescriptor >
    imgDescMap = None


    def __init__(self, pivotsFile, topKSearch):
		# Initialize pivots,imgDescMap,  REST
        self.pivots = Pivots(pivotsFile);
        self.topKSearch = topKSearch;
        self.imgDescMap = FeaturesStorage.loadMap(Parameters.STORAGE_FILE)

		# RestClientBuilder builder = RestClient.builder(new HttpHost("localhost", 9200, "http"));
		# client = new RestHighLevelClient(builder);
        self.client = Elasticsearch([Parameters.elastic_config])

    def close(self):
		# close REST client
        self.client.close();

    def search(self, queryF, k):
        # input imgDescriptor, int
        # return List<ImgDescriptor>
        res = []

		# convert queryF to text
        text = self.pivots.features2Text(queryF, k);
		# call composeSearch to get SearchRequest object
        object = self.composeSearch(text, k);
		# print("SOMETHING");
		# print(object);
		# perform elasticsearch search ------------------------------------------
		# searchResponse = self.client.search(object, RequestOptions.DEFAULT);
        searchResponse = self.client.search(index=Parameters.INDEX_NAME, body=object, size=k);
		# LOOP to fill res
        for hit in searchResponse['hits']['hits']:
            id = hit['_id']
            # print(hit)
            # for each result retrieve the ImgDescriptor from imgDescMap and call setDist to set the score
            img = ImgDescriptor(None, id)
            img.setDist(hit['_score'])
            res.append(img);

        return res;

	# SearchRequest
    def composeSearch(self, query, k):
		# Initialize SearchRequest and set query and k
        finalQuery = {
            "query": {
                "match": {
                    "img": query
                }
            }
        }
        ######################### DUBITO #####################################
        return json.dumps(finalQuery)
		# QueryBuilder simpleQuery = QueryBuilders.multiMatchQuery(query, Fields.IMG);
		# SearchSourceBuilder sb = new SearchSourceBuilder();
		# sb.size(k);
		# sb.query(simpleQuery);
        #
		# SearchRequest sr = new SearchRequest(Parameters.INDEX_NAME);
		# sr.types("doc");
		# sr.source(sb);
	    # return sr;

    def reorder(self, queryF, res):
        # ImgDescriptor queryF, List<ImgDescriptor> res
        # return List<ImgDescriptor>
		# LOOP
		# for each result evaluate the distance with the query, call  setDist to set the distance, then sort the results
        for imgDescriptor in res:
            features = self.imgDescMap[imgDescriptor.getId()]
            imgDescriptor.setFeatures(features)
            imgDescriptor.distance(queryF)

        res.sort()
        return res


if __name__ == '__main__':

    imgSearch = ElasticImgSearching(Parameters.PIVOTS_FILE, Parameters.TOP_K_QUERY)

    # Image Query File
    imgQuery = Parameters.SRC_FOLDER + "/NICOLAS_POUSSIN_30.jpg"

    cnn = StyleCNN()
    #Image Query File
    imgFeatures, _ = cnn.extractFeatures(imgQuery)

    query = ImgDescriptor(imgFeatures, imgQuery.split('/')[-1]);

    time = -Parameters.current_milli_time()
    res = imgSearch.search(query, Parameters.K);
    time += Parameters.current_milli_time();

    print("Search time: " + str(time) + " ms"); #103 ms

    Output.toHTML(res, Parameters.BASE_URI, Parameters.RESULTS_HTML_ELASTIC);

    # Uncomment for the optional step
    res = imgSearch.reorder(query, res);
    Output.toHTML(res, Parameters.BASE_URI, Parameters.RESULTS_HTML_REORDERED);
