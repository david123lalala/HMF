import pickle 
import re
import numpy as np
import pickle


#get function name
def get_all_function_name(all_function_list):
    function_all_name=[]
    function_regex = r"function\s+(\w+)\s*\("
    for i in range(len(all_function_list)):
        tmp_function_names = re.findall(function_regex, all_function_list[i][0])
        function_all_name.append(tmp_function_names)
    return function_all_name


# split_function
def split_function(filepath):
    function_list = []
    # function_line_number=[]
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    flag = -1  
    #line的number
    # line_number=-1 

    for line in lines:
        # line_number += 1
        text = line.strip()
        #delete the comments
        if '/' in text:
            text=text.split('/')
            text=text[0]
        if len(text) > 0 and text != "\n":
            #or text.split()[0] == "constructor"
            if text.split()[0] == "function" or text.split()[0]=='function()' or text.split()[0] == "constructor":
                function_list.append([text])
                flag += 1
                # function_line_number.append(line_number)
            elif len(function_list) > 0 and ("function" or "constructor" in function_list[flag][0]):
                function_list[flag].append(text)
    return function_list

def find_call_value(file_path):
    all_function_list=split_function(file_path)


    all_function_list_name=get_all_function_name(all_function_list)
    call_value_list=[]
    # get_call_value_function_list=[]  

    #forward function and backford function
    forward_function_list=[]
    backward_function_list=[]

    otherFunction_list=[]

    target='.call.value'

    #find call.value keywords
    for i in range(len(all_function_list)):
        count=0
        for j in range(len(all_function_list[i])):
            tmp=all_function_list[i][j]
            if re.search(target,tmp,flags=0):
                count +=1
                call_value_list.append(all_function_list[i])
                break
        if count==0:
            otherFunction_list.append(all_function_list[i])
    


    # get backward function
    for i in range(len(call_value_list)):
        tmplist=call_value_list[i][0].split(' ')
        # pattern = r'\b(\w+)\(\)'
        # pattern = r'\b\w'+re.escape(function_name)+r'\(\)'
        if len(tmplist)>=2:
            tmp=tmplist[1]
            function_tmp=tmp.split('(')
            function_name=function_tmp[0]
            pattern = r'\b\w'+re.escape(function_name)+r'\(\)'
            for j in range(len(otherFunction_list)):
                for k in range(1,len(otherFunction_list[j])):
                    otherfunction=otherFunction_list[j][k]
                    if re.search(function_name,otherfunction,flags=0):
                        tmp_fun_name=re.findall(pattern, otherfunction)
                        if tmp_fun_name in all_function_list_name:
                            if otherFunction_list[j] not in backward_function_list:
                                backward_function_list.append(otherFunction_list[j])
                        break
    
    # get forward function
    for i in range(len(otherFunction_list)):
        tmplist=otherFunction_list[i][0].split(' ')
        # pattern = r'\b(\w+)\(\)'
        if len(tmplist)>=2:
            tmp=tmplist[1]
            function_tmp=tmp.split('(')
            function_name_tmp=function_tmp[0]
            pattern = r'\b\w'+re.escape(function_name_tmp)+r'\(\)'
            for j in range(len(call_value_list)):
                for k in range(1,len(call_value_list[j])):
                    tmp_call_value_function=call_value_list[j][k]
                    if re.search(function_name_tmp,tmp_call_value_function,flags=0):
                        tmp_fun_name=re.findall(pattern, otherfunction)
                        if tmp_fun_name in all_function_list_name:
                            if otherFunction_list[i] not in forward_function_list:
                                forward_function_list.append(otherFunction_list[i])
                        break
    
    # return call_value_list,get_call_value_function_list
    return call_value_list,backward_function_list,forward_function_list

    


if __name__ == "__main__":
    have_call_value_text_number= np.loadtxt("file_number.txt", delimiter=',')
    
    # count_call_value_0=0
    # count_call_value_1=0
    final_count=0
    count_call_vale_list_0=[]
    
    

    for i in range(len(have_call_value_text_number)):
        # print(have_call_value_text_number[i])

        # source_file_path='/root/project/SmartCNN/tool/re_clean_reentrancy/'+str(int(have_call_value_text_number[i]))+'.sol'
        source_file_path='data/re_clean_reentrancy/'+str(int(have_call_value_text_number[i]))+'.sol'
        save_file_path_pkl='data/reentrancy_back_forward/'+str(int(have_call_value_text_number[i]))+'.pkl'
        save_file_path_txt='data/reentrancy_back_forward/'+str(int(have_call_value_text_number[i]))+'.txt'
        
        save_file_path_single_pkl='data/reentrancy_single/'+str(int(have_call_value_text_number[i]))+'.pkl'
        save_file_path_single_txt='data/reentrancy_single/'+str(int(have_call_value_text_number[i]))+'.txt'

        call_value_list_result,backward_function_list,forward_function_list=find_call_value(source_file_path)
        
        if len(call_value_list_result)==1 and len(forward_function_list)==1 and len(backward_function_list)==1 :
            final_count+=1
            print(have_call_value_text_number[i])

        #save txt
        new_call_value=np.asarray(call_value_list_result+backward_function_list+forward_function_list)
        np.savetxt(save_file_path_txt,new_call_value,fmt='%s')
        #save pkl
        with open(save_file_path_pkl,'wb') as f:
            pickle.dump(call_value_list_result+backward_function_list+forward_function_list,f)
    
        with open(save_file_path_single_pkl,'wb') as f:
            pickle.dump(call_value_list_result,f)
        
        new_call_value_single=np.asarray(call_value_list_result)
        np.savetxt(save_file_path_single_txt,new_call_value_single,fmt='%s')


   



