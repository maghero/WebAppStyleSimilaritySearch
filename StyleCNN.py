import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import backend as K
import numpy as np
import os
from PIL import Image
import json
from Parameters import Parameters

base_path = './'

class StyleCNN:

    # modelPath = base_path + 'RetiAllenate/fine-tuned/style/my_model'
    modelPath = 'styleCNN/my_model'
    inputTargetSize = (Parameters.IMG_WIDTH, Parameters.IMG_HEIGHT)
    styleExtractedFeaturesPath = base_path + 'extractedFeatures/actualImage.json'
    extractedFeaturesFileName = 'style_deep_feature.json'
    model = None

    # Used only to create the classes dictionary
    categories_path = '../DATASET_STYLE/train/'
    categories_names = {0: 'abstract_expressionism', 1: 'baroque', 2: 'constructivism',
                        3: 'cubbism', 4: 'impressionism', 5: 'neo-classical', 6: 'popart',
                        7: 'postimpressionism', 8: 'realism', 9: 'renaissance',
                        10: 'romanticism', 11: 'surrealism', 12: 'symbolism'}

    def __init__(self, index_extract_layer=-2):
        self.preprocessFunction = tf.keras.applications.resnet.preprocess_input
        self.model = tf.keras.models.load_model(self.modelPath)
        self.feature_model = tf.keras.Model(inputs=self.model.input, outputs = self.model.layers[index_extract_layer].output)

        if self.categories_names == None:
            self.categories_names = {}
            #Create the dictionary for the classes
            index = 0
            for file in os.listdir(self.categories_path):
                self.categories_names[index] = file
                index += 1

            print(self.categories_names)



    def extractFeatures(self, imagePath):
        # feature_vector = {}
        # self.model.summary()
        print('extracting the Features for the image: ' + imagePath)
        imageName = imagePath.split('\\')[-1]
        floatArray = None
        categories = None
        with Image.open(imagePath).resize(self.inputTargetSize) as image:
            arr_image = np.asarray(image)
            if len(arr_image.shape) != 3:
                image = image.convert('RGB')
                arr_image = np.asarray(image)
                # image.show()

            arr_image = (np.expand_dims(arr_image, 0))
            intermediate_output = self.feature_model.predict(self.preprocessFunction(arr_image))
            floatArray = np.array(intermediate_output)
            categories = np.array(self.model.layers[-1](intermediate_output))

        valuesToReturn = 2
        if categories.max() > 0.9:
            valuesToReturn = 1
        elif np.sum(categories>0.2) > 2:
            valuesToReturn = 3

        imageCategories = {}
        for i in range(valuesToReturn):
            index = categories.argmax()
            imageCategories[self.categories_names[index]] = categories[0][index]
            categories[0][index] = -1

        return [floatArray[0].tolist(), imageCategories]
