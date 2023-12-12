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

    #ren的项目
    # 没有数据均衡的code gadget(ren的项目)
    # CodeBert模型
    # vector_file_path = 'vector/codebert_code_gadget/codebert_reentrancy_single_fragment_vectors.npy'
    # vector_file_path = 'vector/1_ren_no_data_augmentation/vec_codebert.npy'
    # vector_filename = 'codebert_'+'reentrancy_cd_dd'+ "_fragment_vectors.npy"
    # vector_filename = 'codebert_'+'reentrancy_source_code'+ "_fragment_vectors.npy"
    # vector_file_path = 'vector/1_ren_no_data_augmentation/codebert_reentrancy_forward_backward.npy'

    #没有数据均衡的codebert模型（code gadget）
    # vector_file_path='vector/codebert_code_gadget_no_data_augmentation/codebert_code_gadget_no_data_augmentation.npy'
    
    #没有数据均衡的roberta模型(code gadget)
    # vector_file_path = 'vector/1_ren_no_data_augmentation/vec_roberta.npy'

    #bert模型
    # vector_filename = 'vector/bert/bert_'+'reentrancy_back_forward'+ "_fragment_vectors.npy"

    #codeberta模型
    # vector_filename = 'vector/codeberta/codeberta_'+'reentrancy_back_forward'+ "_fragment_vectors.npy"


    
    ##fu的项目
    #数据均衡的code gadget（fu的项目）
    ##将code_gadget和data_flow融合在一起
    # vector_file_path='vector/codebert_code_gadget_and_data_flow/codebert_combined_code_gadget_data_flow.npy'

    #数据均衡且去掉重复数据的code gadget(fu的项目)
    # vector_file_path='vector/2_fu_data_augmentation/no_simility/codebert_reentrancy_no_simility.npy'

    ##timestamp
    #与任的合作
    # vector_file_path='vector/1_ren_no_data_augmentation/timestamp/codebert_timestamp_for_back.npy'
    # vector_file_path='vector/1_ren_no_data_augmentation/timestamp/codebert_timestamp_single.npy'
    # vector_file_path='vector/1_ren_no_data_augmentation/timestamp/codebert_timestamp_source_code.npy'

    # vector_file_path='vector/1_ren_no_data_augmentation/timestamp/roberta_timestamp_for_back.npy'


    #和fu合作
    #code gadget_with_data_flow
    # vector_file_path='vector/2_fu_data_augmentation/reeentrancy/codebert_reentrancy_with_data_flow_4000.npy'
    # vector_file_path='vector/2_fu_data_augmentation/reeentrancy/codebert_reentrancy_1000.npy'
    # vector_file_path='vector/2_fu_data_augmentation/reeentrancy/codebert_reentrancy_5000.npy'
    # vector_file_path='vector/2_fu_data_augmentation/reeentrancy/bert_reentrancy_with_data_flow_4000.npy'
    # vector_file_path='vector/2_fu_data_augmentation/reeentrancy/codebert_reentrancy_501.npy'
    # vector_file_path='vector/2_fu_data_augmentation/reeentrancy/codebert_reentrancy_677.npy'
    # vector_file_path='vector/2_fu_data_augmentation/reeentrancy/codebert_data_flow_10000.npy'


    #需要和GPT结合的训练样本(只包含错误漏洞样本)
    # vector_gpt_file_path='vector/1_ren_no_data_augmentation/reentrancy_only_vul/only_vul_back_forward.npy'
    # vector_gpt_file_path='vector/1_ren_no_data_augmentation/reentrancy_only_vul/only_vul_source_code.npy'
    # vector_gpt_file_path='vector/1_ren_no_data_augmentation/reentrancy_only_vul/only_vul_single.npy'


    #chatGPT增强的数据均衡
    vector_file_path='2023_12_data_augmentation_LLM/vector/combined_vector.npy'




    print(vector_file_path)
    print('进行到第2步')
    #读取训练样本的数据
    #读取file的数据
    with open(vector_file_path, 'rb') as f:
        df = numpy.load(vector_file_path,allow_pickle=True)
    #转为pandas格式
    df_pandas=pandas.DataFrame(df)

    # df_pandas['val'] = df_pandas['val'].astype(str)


    #读取gpt训练样本的数据
    # with open(vector_gpt_file_path, 'rb') as f:
    #     df_gpt = numpy.load(vector_gpt_file_path,allow_pickle=True)
    # #转为pandas格式
    # df_pandas_gpt=pandas.DataFrame(df_gpt)

    
    #fu的合作论文
    #codeBert模型
    # file_name='codebert_reentrancy_single'
    # file_name='codebert_reentrancy_back_forward'
    # file_name='codebert_reentrancy_cd_dd'
    # file_name='codebert_reentrancy_source_code'

    #Roberta模型
    # file_name='roberta_codebert_code_gadget'

    #bert模型
    # file_name='bert_reentrancy_back_forward'
    
    #codeberta模型
    # file_name='codeberta_reentrancy_back_forward'

    #fu的合作论文
    #将code_gadget和data_flow
    # file_name='codebert_reentrancy_code_gadget_data_flow'
    # file_name='codebert_reentrancy_with_data_flow_4000'
    # file_name='bert_reenrtancy_with_data_flow_4000'
    # file_name='codebert_reentrancy_10000'
    # file_name='codebert_reentrancy_1000'
    # file_name='codebert_reentrancy_5000'
    # file_name='codebert_reentrancy_501'
    # file_name='codebert_reentrancy_677'

    #使用chatGPT进行数据增强的例子
    file_name='codebert_chatGPT_reentrancy'


    ##timestamp的实验数据
    ##和ren的合作
    # file_name='codebert_timestamp_for_back'
    # file_name='codebert_timestamp_single'
    # file_name='codebert_timestamp_base'

    # file_name='roberta_timestamp_for_back'

    print(df_pandas)
     
    start_time=time.time()
    model =Transformer_CNN_Model(df_pandas,file_name)
    print('进行到第4步')
    model.train()
    model.test()
    # model.GPT_test(df_pandas_gpt)


    end_time=time.time()
    print('进行到第5步')

    training_time=end_time-start_time
    print("Training time: {:.2f} seconds".format(training_time))



if __name__ == "__main__":
    print('进行到第0步')
    main()