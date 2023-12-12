import pandas
import numpy as np
import random
import pickle
import json

#random token
def get_random_token(file_list):

    data_random_token_left=[]
    data_random_token_right=[]
    
    final_list=[]

    tmp_line=''

    for i in range(len(file_list)):
        for j in range(len(file_list[i])):
            tmp_line=tmp_line+file_list[i][j]+' '

    tmp_random_token=[]
    line=tmp_line.split(' ')
    for i in range (0,3):
        #tmp_random
        tmp_sample=random.sample(line,5)
        sample=' '.join(tmp_sample)
        tmp_random_token.append(sample)

    for i in range(len(tmp_random_token)):
        data_random_token_left.append(tmp_line+tmp_random_token[i])
        data_random_token_right.append(tmp_random_token[i]+tmp_line)

    random_token=data_random_token_left+data_random_token_right

    # for i in range(len(random_token)):
    #     if random_token[i] not in final_list:
    #         final_list.append(random_token[i])
    # return final_list

    return random_token

#replace_special_token
def get_special_token(file_list):

    tmp_line=''
    for i in range(len(file_list)):
        for j in range(len(file_list[i])):
            tmp_line=tmp_line+file_list[i][j]+' '
    
    tokens=tmp_line.split(' ')

    embedding_function_list=['function','italian','emerging','andrea','wrote','letters']
    embedding_public_list=['public','morris','think','the','warren','visual']
    embedding_if_list=['if','think','knew','how','linux','emerging']

    # embedding_function_list=['function','italian','emerging']
    # embedding_public_list=['public','morris','think']
    # embedding_if_list=['if','think','knew']

    final_token=[]

    for j in range(0,5):
        special_token=[]
        for i in range(len(tokens)):
            if tokens[i]=='function':
                tmp_token=random.choice(embedding_function_list)
                special_token.append(tmp_token)
            elif tokens[i]=='public':
                tmp_token=random.choice(embedding_public_list)
                special_token.append(tmp_token)
            elif tokens[i]=='if':
                tmp_token=random.choice(embedding_if_list)
                special_token.append(tmp_token)
            else:
                special_token.append(tokens[i])
        tmp_tokens=' '.join(special_token)
        # if tmp_token not in final_token:
        final_token.append(tmp_tokens)

    return final_token

#random sentence
def get_random_sentence(file_list):   
    data_sentence_left=[]
    data_sentence_right=[]

    # final_set=set()
    final_list=[]

    tmp_list=[]
    for i in range(len(file_list)):
        for j in range(len(file_list[i])):
            tmp_list.append(file_list[i][j])

    random_sentence=[]

    for k in range(0,3):
        tmp_sentence=random.choice(tmp_list)
        random_sentence.append(tmp_sentence)

    tmp_list=' '.join(tmp_list)

    for i in range(len(random_sentence)):
        data_sentence_left.append(random_sentence[i]+' '+tmp_list)
        data_sentence_right.append(tmp_list+' '+random_sentence[i])

    sentence_list=data_sentence_left+data_sentence_right

    return sentence_list

        
def get_data_augmentation(file_list):

    random_token=get_random_token(file_list)

    special_token=get_special_token(file_list)

    random_sentence=get_random_sentence(file_list)

    data_augmentation=random_token+special_token+random_sentence

    return data_augmentation


def get_total_data_augmentation():

    #upload file_number
    file_number=np.loadtxt("data/exp_data/final_reentrancy_get_opcode_number.txt", delimiter=',')
    file_val=np.loadtxt('data/exp_data/final_reentrancy_oyente.txt',delimiter=',')

    print('len(file_number)',len(file_number))
    print('len(file_oyente)',len(file_val))

    #save_data
    data_json=[]
    data_json_save_path='data_augmentation/da_reentrancy/data_json.json'

    #save_balanced_dataset
    data_augmentation=[]
    data_augmentatio_path='data_augmentation/da_reentrancy/code_gadget.json'

    #count_0_1
    data_0_1=[]

    for i in range(len(file_number)):
        flag=int(file_val[i])
        tmp_file_path='data/exp_data/reentrancy_back_forward/'+str(int(file_number[i]))+'.pkl'
        tmp_file_number=str(int(file_number[i]))+'.sol'

        with open(tmp_file_path,'rb') as file:
            tmp_file=pickle.load(file)

        if flag==1:
            tmp={'file_name':tmp_file_number,'file':tmp_file,'file_val':flag}
            data_json.append(tmp)
            data_0_1.append(flag)
            tmp_data_augmentation=get_data_augmentation(tmp_file)

            for j in range(len(tmp_data_augmentation)):
                tmp_2={'file_name':tmp_file_number,'file':str(tmp_data_augmentation[j]),'file_val':flag}
                data_augmentation.append(tmp_2)
                data_0_1.append(flag)

        else:
            tmp={'file_name':tmp_file_number,'file':tmp_file,'file_val':flag}
            data_json.append(tmp)
            data_0_1.append(flag)

    print('len(data_augmentation)',len(data_augmentation))
    print('data_json',len(data_json))
    
    #save_data
    data_save_file=data_json+data_augmentation


    print('data_save_file',len(data_save_file))

    with open(data_augmentatio_path,'w') as file:
        json.dump(data_save_file,file)

    print('data_0_1.count(1)',data_0_1.count(1))
    print('data_0_1.count(0)',data_0_1.count(0))

    return data_save_file

def main():

    code_gadget_file=get_total_data_augmentation()

    data_flow_file_path='data_augmentation/da_reentrancy/data_flow_from_AST.json'

    with open (data_flow_file_path,'rb') as f:
        data_flow_file=json.load(f)

    count_data_flow=0

 
    save_file=[]
    save_file_path='data_augmentation/da_reentrancy/code_gadget_with_data_flow.json'

    for i in range(len(code_gadget_file)):
        data_flow=[]
        for j in range(len(data_flow_file)):
            if code_gadget_file[i]['file_name']==data_flow_file[j]['file_name']:
                data_flow=data_flow_file[j]['file_data_flow']
                count_data_flow=count_data_flow+1
        tmp={'file_name':code_gadget_file[i]['file_name'],'code_gadget':code_gadget_file[i]['file'],'data_flow':data_flow,'file_val':code_gadget_file[i]['file_val']}
        save_file.append(tmp)

    print('count_data_flow',count_data_flow)
    print('len(save_file)',len(save_file))

    with open(save_file_path,'w') as file:
        json.dump(save_file,file)


if __name__ == "__main__":
    main()