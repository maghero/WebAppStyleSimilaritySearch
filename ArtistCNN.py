import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import backend as K
import numpy as np
import os
from PIL import Image
import json
from Parameters import Parameters

base_path = './'

class ArtistCNN:

    modelPath = 'artistCNN/my_model'
    inputTargetSize = (Parameters.IMG_WIDTH, Parameters.IMG_HEIGHT)
    model = None

    # Used only to create the classes dictionary
    categories_path = '../DATASET_ARTIST/train/'
    categories_names = {0: 'ALBRECHT_DURER', 1: 'AMEDEO_MODIGLIANI', 2: 'ANDREA_MANTEGNA', 3: 'ANDY_WARHOL', 4: 'ARSHILLE_GORKY', 5: 'CAMILLE_COROT', 6: 'CARAVAGGIO', 7: 'CASPAR_DAVID_FRIEDRICH', 8: 'CLAUDE_LORRAIN', 9: 'CLAUDE_MONET', 10: 'DANTE_GABRIEL_ROSSETTI', 11: 'DAVID_HOCKNEY', 12: 'DIEGO_VELAZQUEZ', 13: 'EDGAR_DEGAS', 14: 'EDOUARD_MANET', 15: 'EDVARD_MUNCH', 16: 'EDWARD_HOPPER', 17: 'EGON_SCHIELE', 18: 'EL_LISSITZKY', 19: 'EUGENE_DELACROIX', 20: 'FERNAND_LEGER', 21: 'FRANCISCO_DE_GOYA', 22: 'FRANCISCO_DE_ZURBARAN', 23: 'FRANCIS_BACON', 24: 'FRANS_HALS', 25: 'FRANZ_MARC', 26: 'FRA_ANGELICO', 27: 'FREDERIC_EDWIN_CHURCH', 28: 'FRIDA_KAHLO', 29: 'GENTILESCHI_ARTEMISIA', 30: 'GEORGES_BRAQUE', 31: 'GEORGES_DE_LA_TOUR', 32: 'GEORGES_SEURAT', 33: 'GEORGIA_OKEEFE', 34: 'GERHARD_RICHTER', 35: 'GIORGIONE', 36: 'GIORGIO_DE_CHIRICO', 37: 'GIOTTO_DI_BONDONE', 38: 'GUSTAVE_COURBET', 39: 'GUSTAVE_MOREAU', 40: 'GUSTAV_KLIMT', 41: 'HANS_HOLBEIN_THE_YOUNGER', 42: 'HANS_MEMLING', 43: 'HENRI_MATISSE', 44: 'HIERONYMUS_BOSCH', 45: 'JACKSON_POLLOCK', 46: 'JACQUES-LOUIS_DAVID', 47: 'JAMES_ENSOR', 48: 'JAMES_MCNEILL_WHISTLER', 49: 'JAN_VAN_EYCK', 50: 'JAN_VERMEER', 51: 'JASPER_JOHNS', 52: 'JEAN-ANTOINE_WATTEAU', 53: 'JEAN-AUGUSTE-DOMINIQUE_INGRES', 54: 'JEAN-MICHEL_BASQUIAT', 55: 'JEAN_FRANCOIS_MILLET', 56: 'JOACHIM_PATINIR', 57: 'JOAN_MIRO', 58: 'JOHN_CONSTABLE', 59: 'JOSEPH_MALLORD_WILLIAM_TURNER', 60: 'KAZIMIR_MALEVICH', 61: 'LUCIO_FONTANA', 62: 'MARC_CHAGALL', 63: 'MARK_ROTHKO', 64: 'MAX_ERNST', 65: 'NICOLAS_POUSSIN', 66: 'PAUL_CEZANNE', 67: 'PAUL_GAUGUIN', 68: 'PAUL_KLEE', 69: 'PETER_PAUL_RUBENS', 70: 'PICASSO', 71: 'PIERRE-AUGUSTE_RENOIR', 72: 'PIETER_BRUEGEL_THE_ELDER', 73: 'PIET_MONDRIAN', 74: 'RAPHAEL', 75: 'REMBRANDT_VAN_RIJN', 76: 'RENE_MAGRITTE', 77: 'ROGER_VAN_DER_WEYDEN', 78: 'ROY_LICHTENSTEIN', 79: 'SALVADOR_DALI', 80: 'SANDRO_BOTTICELLI', 81: 'THEODORE_GERICAULT', 82: 'TINTORETTO', 83: 'TITIAN', 84: 'UMBERTO_BOCCIONI', 85: 'VINCENT_VAN_GOGH', 86: 'WASSILY_KANDINSKY', 87: 'WILLEM_DE_KOONING', 88: 'WILLIAM_BLAKE', 89: 'WILLIAM_HOGARTH', 90: 'WINSLOW_HOMER'}

    def __init__(self, index_extract_layer=-1):
        self.preprocessFunction = tf.keras.applications.resnet.preprocess_input
        self.model = tf.keras.models.load_model(self.modelPath)

        if self.categories_names == None:
            #Create the dictionary for the classes
            self.categories_names = {}
            index = 0
            for file in os.listdir(self.categories_path):
                self.categories_names[index] = file
                index += 1

            print(self.categories_names)


    def extractCategories(self, imagePath):
        '''
            return the predicted artist categories
        '''
        print('finding the most similar artists for the image: ' + imagePath)
        imageName = imagePath.split('\\')[-1]
        categories = None
        total_probability = 0.0
        imageCategories = {}

        with Image.open(imagePath).resize(self.inputTargetSize) as image:
            arr_image = np.asarray(image)
            if len(arr_image.shape) != 3:
                image = image.convert('RGB')
                arr_image = np.asarray(image)
                # image.show()

            arr_image = (np.expand_dims(arr_image, 0))

            #Compute the specific artist categories
            categories = np.array(self.model.predict(self.preprocessFunction(arr_image)))

        numCat = 0
        while total_probability < 0.60 and numCat < 3:

            total_probability += categories.max()
            numCat += 1
            
            index = categories.argmax()

            imageCategories[self.categories_names[index]] = categories[0][index]

            categories[0][index] = -1

        return imageCategories
