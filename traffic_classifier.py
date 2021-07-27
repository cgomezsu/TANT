"""
v.e.s.

Traffic-Aware Network Telemetry


MIT License

Copyright (c) 2021 Cesar A. Gomez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""                   

import time
import numpy as np 
import pandas as pd
import joblib

import sklearn
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

import xgboost as xgb

import onnx
import onnxmltools
from onnxconverter_common.data_types import FloatTensorType

from onnxmltools.convert import convert_xgboost

import onnxruntime as ort

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Set Numpy random seed for reproducibility
np.random.seed(777)

df = pd.read_csv('/home/ubuntu/EmulationDataset.csv')
X = df.drop(['Label'], axis = 1)
Y = df['Label']

X = X.astype(float, errors = 'raise')      # Convert all object types into float
Y = LabelEncoder().fit_transform(Y)        # Conver labels into integers

# Data normalization
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)                     # Fit scaler only on traffic data

xgb_clf = joblib.load("/home/ubuntu/xgb_clf_9_opt2.pkl")         # Load trained model

# Convert model into ONNX
initial_type = [('float_input', FloatTensorType([None, 9]))]    # 9 features
onx = convert_xgboost(xgb_clf, initial_types=initial_type)

# Compute the predictions with ONNX Runtime
sess = ort.InferenceSession(onx.SerializeToString())
input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name

flows = 120                            # Number of flows to be emulated
max_sample = len(Y)-1

for i in range(flows):

    n = np.random.randint(0, max_sample)
    tf_class = sess.run([label_name], {input_name: X[n:n+1].astype(np.float32)})[0]    # Flow classification
    
    np.save('/home/ubuntu/tf_class.npy', tf_class)
    time.sleep(3)
