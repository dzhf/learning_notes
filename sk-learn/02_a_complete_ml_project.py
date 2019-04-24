#!/usr/local/bin/python3
import sys
import numpy
import pandas as pd
import tarfile
import os
from six.moves import urllib
import matplotlib.pyplot as plt

DOWNLOAD_URL = 'https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.tgz'
SAVE_DIR = 'datasets/housing'
SAVE_FILE = 'housing.tgz'

def fetch_housing_data(download_url = DOWNLOAD_URL, save_dir = SAVE_DIR,
        save_file = SAVE_FILE):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    save_url = os.path.join(save_dir, save_file)
    if os.path.isfile(save_url):
        print('file already download')
        return
    urllib.request.urlretrieve(download_url, save_url)
    tar_fd = tarfile.open(save_url)
    tar_fd.extractall(save_dir)
    tar_fd.close()

def read_housing_data(file_dir=SAVE_DIR, filename=SAVE_FILE):
    file_url = os.path.join(file_dir,filename)
    print(file_url)
    housing_data = pd.read_csv(file_url,sep=',',header=0)
    return housing_data

# 获取并读取数据源
fetch_housing_data()
housing_data = read_housing_data(filename='housing.csv')

# 查看数据的整体属性
print(housing_data.head())
housing_data.info()
print(housing_data['ocean_proximity'].value_counts())
print(housing_data.describe())
housing_data.hist(bins=50,figsize=(20,15))
plt.show()
