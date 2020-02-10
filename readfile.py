import pandas as pd 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from math import pi
import seaborn as sns
import sklearn as sklearn
#matplotlib inline 
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

data_df = pd.read_csv('matches_csv/testmatch.csv')

data_df.shape()
