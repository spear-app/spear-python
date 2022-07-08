# !pip uninstall keras -y
# !pip uninstall keras-nightly -y
# !pip uninstall keras-Preprocessing -y
# !pip uninstall keras-vis -y
# !pip uninstall h5py -y
# !pip uninstall tensorflow
# pip install librosa
# !pip install keras==2.0.8
# !pip install h5py==2.10.0
# !pip install tensorflow==1.13.2
# !pip install  keras-preprocessing
import librosa
import numpy as np
from tensorflow.keras.models import load_model

def extract_feature(file_name):
   
    try:
        audio_data, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T,axis=0)
        
    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None, None

    return np.array([mfccsscaled])
  
  
  def print_prediction(file_name):

    prediction_feature = extract_feature(file_name) 
    predicted_vector = model.predict_classes(prediction_feature)
    if predicted_vector[0] == 0:
        return "The predicted class is: doorbell \n"
    elif predicted_vector[0]== 1:
        return "The predicted class is: knock \n" 
      
      
model = load_model('weights.best.basic_mlp.hdf5')
