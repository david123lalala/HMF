import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
import numpy
import pickle
import pandas
import os

# from gensim.models import Word2Vec

#code gadget的file_path
back_forward_code_gadget_path='data/exp_data/reentrancy_back_forward/'
single_code_gadget_path='data/exp_data/reentrancy_single/'
cd_dd_path='data/exp_data/dd_cd_reentrancy/'
source_code_path='data/exp_data/reentrancy_source_code_pkl/'

def get_vectors():
    # upload codebert_base
    model_name = "microsoft/codebert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    #file_number
    contract_number= np.loadtxt("file_number.txt", delimiter=',')
    #file_val
    vul_result= np.loadtxt("file_val", delimiter=',')

    vectors=[]
    count=0

    for k in range(len(contract_number)):
        code_all=''
        count += 1
        print("Processing fragments...", count, end="\r")
        tmp_path=single_code_gadget_path+str(int(contract_number[k]))+'.pkl'

        with open(tmp_path, 'rb') as f:
            tmp_file = pickle.load(f)

        for i in range(len(tmp_file)):
            for j in range(len(tmp_file[i])):
                code_all=code_all+tmp_file[i][j]
                
        # tokenizer
        inputs = tokenizer(code_all,max_length=100,return_tensors="pt",truncation=True,padding='max_length')
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state
        embeddings=embeddings.detach().numpy()
        print(type(embeddings))

        row = {"vector": embeddings, "val": int(vul_result[k])}
        vectors.append(row)
    df = pandas.DataFrame(vectors)

    return df

def main():
    # vector_filename = '/root/123/'+'codebert_'+'reentrancy_back_forward'+ "_fragment_vectors"
    vector_filename = '/root/123/'+'codebert_'+'reentrancy_single'+ "_fragment_vectors"
    # vector_filename = '/root/123/'+'codebert_'+'reentrancy_cd_dd'+ "_fragment_vectors"
    # vector_filename = '/root/123/'+'codebert_'+'reentrancy_source_code'+ "_fragment_vectors"

    final_vector=[]
    find_vector_filename=vector_filename+'.npy'

    if os.path.exists(find_vector_filename):
        df = np.load(find_vector_filename, allow_pickle=True)
    else:
        df = get_vectors()

        np.save(vector_filename, df)


if __name__ == "__main__":
    main()

