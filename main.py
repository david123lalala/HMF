import numpy as np
import pickle
import pandas
import os
import numpy
import time

from model.transformer_cnn import Transformer_CNN_Model

from parser import parameter_parser

ags = parameter_parser()



def main():

    #vector_path
    vector_file_path=''
    vector_gpt_file_path=''

    with open(vector_file_path, 'rb') as f:
        df = numpy.load(vector_file_path,allow_pickle=True)
    df_pandas=pandas.DataFrame(df)

    #gpt_train_data
    with open(vector_gpt_file_path, 'rb') as f:
        df_gpt = numpy.load(vector_gpt_file_path,allow_pickle=True)
    df_pandas_gpt=pandas.DataFrame(df_gpt)

    file_name='codebert_reentrancy'

    start_time=time.time()
    model =Transformer_CNN_Model(df_pandas,file_name)
    model.train()
    model.test()
    model.GPT_test(df_pandas_gpt)
    
    end_time=time.time()

    training_time=end_time-start_time
    print("Training time: {:.2f} seconds".format(training_time))


if __name__ == "__main__":
    main()