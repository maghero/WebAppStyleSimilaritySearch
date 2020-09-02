from ImgDescriptor import ImgDescriptor
from Parameters import Parameters

import os
import json

class FeaturesStorage:

    def store(ids, storageFile):
        ''''
        List<ImgDescriptor> ids, String storageFile
        '''
        if not os.path.exists(storageFile):
            parentFolder= '/'.join(storageFile.split('/')[:-1])
            if not os.path.exists(parentFolder):
                os.makedirs(parentFolder)

        descriptorsToSave = {}
        for id in ids:
            descriptorsToSave[id.getId()] = id.getFeatures() #it should already be a list

        with open(storageFile, 'w') as file_out:
            file_out.write(json.dumps(descriptorsToSave))

    def load(storageFile):
        storedToLoad = {}
        with open(storageFile, 'r') as file_input:
            storedToLoad = json.loads(file_input.read())

        ids = []
        for id in storedToLoad:
            ids.append(ImgDescriptor(storedToLoad[id], id))
        return ids

    def loadMap(storageFile):
        storedToLoad = {}
        with open(storageFile, 'r') as file_input:
            storedToLoad = json.loads(file_input.read())
        return storedToLoad
