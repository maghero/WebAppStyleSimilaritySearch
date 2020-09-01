from Parameters import Parameters
from ElasticImgSearching import ElasticImgSearching
from StyleCNN import StyleCNN
from ArtistCNN import ArtistCNN
from Output import Output
from ImgDescriptor import ImgDescriptor

from flask import Flask
from flask import request, redirect, send_from_directory, send_file
from flask import render_template, make_response

from functools import wraps, update_wrapper
from datetime import datetime

#The search engine connected to elasticsearch
imgSearch = ElasticImgSearching(Parameters.PIVOTS_FILE, Parameters.TOP_K_QUERY)
#The neural network used to extract features and style categorization
styleCNN = StyleCNN()
#The neural network used for artist categorization
artistCNN = ArtistCNN()
#Done to suppress the warnings during the normal runtime of the application
#included in the set_up stage
styleCNN.extractFeatures(Parameters.QRY_IMAGE)
artistCNN.extractCategories(Parameters.QRY_IMAGE)

app = Flask(__name__, static_url_path='')
#Necessary otherwise the server will return always the same page for the search, even if an the image searched is changed
app.config['TEMPLATES_AUTO_RELOAD'] = True #DO NOT REMOVE
#In a real application deployment just use always an unique name for the query image such as the IP address of who made the search plus some timestamp
@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    return response

@app.route('/', methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        if request.files:
            image = request.files["image"]
            image.save(Parameters.QRY_IMAGE)

            imgFeatures, imgCategories = styleCNN.extractFeatures(Parameters.QRY_IMAGE)
            imgArtists = artistCNN.extractCategories(Parameters.QRY_IMAGE)

            query = ImgDescriptor(imgFeatures, Parameters.QRY_IMAGE.split('/')[-1])
            # print("Image Descriptor of Query Created")
            # print(query)

            time = -Parameters.current_milli_time()
            res = imgSearch.search(query, Parameters.K)
            time += Parameters.current_milli_time()

            print("Search time: " + str(time) + " ms")

            # Output.toHTML(res, Parameters.BASE_URI, Parameters.RESULTS_HTML_ELASTIC);

            # Uncomment for the optional step
            res = imgSearch.reorder(query, res)
            Output.toHTML(res, Parameters.BASE_URI, Parameters.RESULTS_HTML_REORDERED, Parameters.QRY_IMAGE, imgCategories, imgArtists, str(time))

            #Redirect to the search results
            return redirect("deep.reordered.html")

    return render_template("index.html")


@app.route("/deep.seq.html")
def seq():
    return render_template("/deep.seq.html")

# @nocache
@app.route("/deep.reordered.html")
def elastic_reordered():
    return render_template("/deep.reordered.html")

@app.route("/Images/<path:path>")
def send_im(path):
    return send_from_directory('Images', path)

@app.route("/favicon.ico")
def favicon():
    filename = 'site/icon.svg'
    return send_file(filename, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')# debug=True)
