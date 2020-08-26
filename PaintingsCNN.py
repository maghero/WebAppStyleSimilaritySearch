import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import backend as K
import numpy as np
import os
from PIL import Image
import json
# base_path = '../'

class StyleCNN:

    # modelPath = base_path + 'RetiAllenate/fine-tuned/style/my_model'
    modelPath = 'styleCNN/my_model'
    inputTargetSize = (224, 224)
    styleExtractedFeaturesPath = base_path + 'extractedFeatures/actualImage.json'
    extractedFeaturesFileName = 'style_deep_feature.json'
    model = None
    functor = None
    # Used only to create the classes dictionary
    # categories_path = '../DATASET_STYLE/train/'
    categories_names = {0: 'abstract_expressionism', 1: 'baroque', 2: 'constructivism',
                        3: 'cubbism', 4: 'impressionism', 5: 'neo-classical', 6: 'popart',
                        7: 'postimpressionism', 8: 'realism', 9: 'renaissance',
                        10: 'romanticism', 11: 'surrealism', 12: 'symbolism'}

    def __init__(self, index_extract_layer=-2):
        self.preprocessFunction = tf.keras.applications.resnet.preprocess_input
        self.model = tf.keras.models.load_model(self.modelPath)
        self.feature_model = tf.keras.Model(inputs=self.model.input, outputs = self.model.layers[index_extract_layer].output)
        print(self.model.layers[index_extract_layer].output)
        print(self.model.layers[-1].output)
        # self.classes_model = K.function([self.model.layers[index_extract_layer].output], [self.model.layers[-1].output])
        # self.classes_model = self.model.layers[-1](self.feature_model.output)
        # print(self.classes_model)
        # self.model.summary()
        if self.categories_names == None:
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
            # floatArray = np.array(self.model.predict(self.preprocessFunction(arr_image)))
            intermediate_output = self.feature_model.predict(self.preprocessFunction(arr_image))
            floatArray = np.array(intermediate_output)

            #Compute the specific style categories
            # categories = self.classes_model(intermediate_output)
            categories = np.array(self.model.layers[-1](intermediate_output))
            #
            # feature_vector[imageName] = floatArray[0].tolist()
            # print(feature_vector)

        valuesToReturn = 2
        if categories.max() > 0.9:
            valuesToReturn = 1
        elif np.sum(categories>0.2) > 2:
            valuesToReturn = 3

        imageCategories = {}
        for i in range(valuesToReturn):
            index = categories.argmax()
            # print(categories)
            # print(index)
            # print(self.categories_names[index])
            # print(categories[0][index])
            imageCategories[self.categories_names[index]] = categories[0][index]
            categories[0][index] = -1

        return [floatArray[0].tolist(), imageCategories]
