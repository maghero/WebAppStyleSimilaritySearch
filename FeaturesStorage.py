from ImgDescriptor import ImgDescriptor
from Parameters import Parameters

# import it.unipi.ing.mim.img.elasticsearch.ElasticImgIndexing;
#
# import java.io.File;
# import java.io.FileInputStream;
# import java.io.FileOutputStream;
# import java.io.IOException;
# import java.io.ObjectInputStream;
# import java.io.ObjectOutputStream;
# import java.util.ArrayList;
# import java.util.List;
# import java.util.Map;
#
# import com.fasterxml.jackson.core.type.TypeReference;
# import com.fasterxml.jackson.databind.ObjectMapper;

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

# 	@SuppressWarnings("unchecked")
# 	//storageFile is a json file with keys as name of the image and the value is the predict float vector
# 	public static List<ImgDescriptor> load(File storageFile) throws IOException, ClassNotFoundException {
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
# //		try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(storageFile))) {
# 		List<ImgDescriptor> ret = new ArrayList<ImgDescriptor>();
# 		try (FileInputStream fis = new FileInputStream(storageFile)) {
# 			Map<String,float[]> result = new ObjectMapper().readValue(fis,  new TypeReference<Map<String, float[]>>() {});//HashMap.class);
# //			System.out.println(result);
# 			for (String id : result.keySet()) {
# //			for (float[] values : result.values()){
# //				System.out.println(id);
# //				System.out.println(result.getClass());
# //				System.out.println(id.getClass());
# //				System.out.println(result.values().getClass());
# //				System.out.println(result.get(id));
# //
# //				float[] floatList = result.get(id);
# //				System.out.println((floatList);
# 				ImgDescriptor a = new ImgDescriptor(result.get(id), id);
# 				ret.add(a);
# 			}
# 			return ret;
# 		}catch (com.fasterxml.jackson.core.JsonParseException e) { //For the Pivots
# 			try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(storageFile))) {
# 				return (List<ImgDescriptor>) ois.readObject();
# 			}
# 		}
# 	}
#
#
# 	public static Map<String,float[]> jsonload(File storageFile) throws IOException, ClassNotFoundException {
# //		try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(storageFile))) {
# 		try (FileInputStream fis = new FileInputStream(storageFile)) {
# 			return new ObjectMapper().readValue(fis,  new TypeReference<Map<String, float[]>>() {});//HashMap.class);
# 		}
# 	}
#
#
# 	public static void main(String[] args) throws ClassNotFoundException, IOException {
# 		List<ImgDescriptor> imgDescDataset = FeaturesStorage.load(Parameters.STORAGE_FILE);
# 		for (ImgDescriptor img : imgDescDataset) {
# 			System.out.print("Id: " + img.getId() + " with Features : [ ");
# 			for (float feature : img.getFeatures()) {
# 				System.out.print(feature);
# 				System.out.print(' ');
# 			}
# 			System.out.println(']');
# 		}
# 	}
#
#
#
# }
