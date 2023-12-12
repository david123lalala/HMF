import numpy as np
# from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import train_test_split
from sklearn.utils import compute_class_weight
from keras.utils import to_categorical
from keras.models import Sequential,Model
# from tensorflow.keras.models import Model
from keras.layers import Embedding,Conv1D,GlobalMaxPooling1D,Dropout,Dense,GlobalAveragePooling1D,Input,LSTM 
from keras.optimizers import Adamax
from sklearn.metrics import confusion_matrix
from parser import parameter_parser
import matplotlib.pyplot as plt
import sys
from  model.transformer_attention import MultiHeadSelfAttention,TransformerBlock
import tensorflow as tf

from imblearn.over_sampling import SMOTE


args = parameter_parser()



class Transformer_CNN_Model:
    def __init__(self, data, name="", batch_size=args.batch_size, lr=args.lr, epochs=args.epochs, dropout=args.dropout,kernel_size=args.kernel_size,kernel_num=args.kernel_num):
        
        vectors = np.stack(data.iloc[:, 0].values)
        print('vectors.shape',vectors.shape)

        labels = data.iloc[:, 1].values
        print('labels.shape',labels.shape)

        vectors=np.reshape(vectors,(vectors.shape[0],vectors.shape[2],vectors.shape[3]))
        print('vectors.shape',vectors.shape)

    
        vec_first=vectors.shape[0]
        print('vec_first',vec_first)
        vec_secend=vectors.shape[1]
        print('vec_secend',vec_secend)
        vec_third=vectors.shape[2]
        print('vec_third',vec_third)



        x_train, x_test, y_train, y_test = train_test_split(vectors, labels,
                                                            test_size=0.2, stratify=labels)
        final_x_test, final_x_val, final_y_test, final_y_val = train_test_split(x_test, y_test,
                                                            test_size=0.5)

        print('x_train.shape',x_train.shape)
        print('len(x_train)',len(x_train))


        self.x_train = x_train
        self.x_test = final_x_test
        self.x_val= final_x_val

        self.y_train = to_categorical(y_train)
        self.y_test = to_categorical(final_y_test)
        self.y_val = to_categorical(final_y_val)

        print('self.x_train.shape',self.x_train.shape)
        print('self.y_train.shape',self.y_train.shape)

        self.name = name
        self.dropout=dropout
        self.batch_size = batch_size
        self.epochs = epochs
        self.kernel_size=kernel_size
        self.filter=kernel_num
        self.class_weight = compute_class_weight(class_weight='balanced', classes=[0, 1], y=labels)
    

        embed_dim = vec_third  # Embedding size for each token
        num_heads = 4 # Number of attention heads
        ff_dim = 32  # Hidden layer size in feed forward network inside transformer

        embed_input = Input(shape=(vec_secend,vec_third))
        x = TransformerBlock(embed_dim, num_heads, ff_dim)(embed_input)
        x = Conv1D(filters=self.filter,kernel_size=self.kernel_size,padding='VALID', strides = 1, activation='relu',name='conv')(x)
        x = GlobalAveragePooling1D()(x)
        x = Dense(20, activation="relu")(x)
        x = Dropout(0.1)(x)
        output = Dense(2, activation="softmax")(x)
        model = Model(inputs=embed_input, outputs=output,name="transformer_cnn") 
        adamax = Adamax(lr)
        model.compile(optimizer=adamax, loss='categorical_crossentropy', metrics=['accuracy'])
        self.model = model


    def train(self):
        history =self.model.fit(self.x_train, self.y_train, batch_size=self.batch_size, epochs=self.epochs,class_weight=self.class_weight,validation_data=(self.x_val, self.y_val))
        self.model.save('model/train_model/reentrancy_detect_model.h5')
        # self.model.summary()

    def test(self):
        values = self.model.evaluate(self.x_test, self.y_test, batch_size=self.batch_size)
        # print("Accuracy: ", values[1])
        predictions = (self.model.predict(self.x_test, batch_size=self.batch_size)).round()
        # predictions = (predictions >= self.threshold)


        tn, fp, fn, tp = confusion_matrix(np.argmax(self.y_test, axis=1), np.argmax(predictions, axis=1)).ravel()
        #表示预测正确的数值
        print("validation Accuracy: ", (tp + tn) / (tp + tn + fp + fn))
        print('validation  False positive rate(FPR): ', fp / (fp + tn))
        print('validation  False negative rate(FNR): ', fn / (fn + tp))
        recall = tp / (tp + fn)
        print('validation Recall(TPR): ', recall)
        precision = tp / (tp + fp)
        print('validation Precision: ', precision)
        print('validation F1 score: ', (2 * precision * recall) / (precision + recall))



    def GPT_test(self,gpt_data):
    
        print('GPT_test')
        vectors = np.stack(gpt_data.iloc[:, 0].values)
        labels = gpt_data.iloc[:, 1].values
        print('vectors.shape',vectors.shape)

        print('labels',labels)

        #preprocess the labels and vectors
        vectors=np.reshape(vectors,(vectors.shape[0],vectors.shape[2],vectors.shape[3]))
        labels= to_categorical(labels)

        #first attention_1
        print('get_weight_from_model')
        attention_weights_1=self.model.layers[1].output

        visualization_model_1 = Model(inputs=self.model.input, outputs=attention_weights_1)

        attention_weights_1 = visualization_model_1.predict(vectors)

        plt.matshow(attention_weights_1[0], cmap='viridis')  
        # plt.matshow(attention_weights_1[0], cmap='YlGnBu') 
        plt.xlabel('Input Text')
        plt.ylabel('Attention Weights')
        plt.savefig('tool/visualization/attention_1.png')


        #secend attention_2
        print('get_weight_from_model')
        attention_weights_2=self.model.layers[2].output

        visualization_model_2 = Model(inputs=self.model.input, outputs=attention_weights_2)

        attention_weights_2 = visualization_model_2.predict(vectors)

        np.save("tool/attention_weight/aw_numpy/attention_weights.npy", attention_weights_2)

        # attention_weights_2.shape (52, 99, 6)
        # attention_weights_2[0].shape (99, 6)
        print('attention_weights_2,type',type(attention_weights_2))
        print('attention_weights_2.shape',attention_weights_2.shape)
        print('attention_weights_2[0].shape',attention_weights_2[0].shape)

        plt.colorbar()
        plt.matshow(attention_weights_2[0], cmap='viridis')  
        # plt.matshow(attention_weights_2[0], cmap='YlGnBu') 
        plt.xlabel('Kernel numbers')
        plt.ylabel('Code gadget tokens')
        plt.savefig('tool/visualization/attention_2.png')


        values = self.model.evaluate(vectors, labels, batch_size=self.batch_size)
        
        # print("Accuracy: ", values[1])
        predictions = (self.model.predict(vectors, batch_size=self.batch_size)).round()
        # predictions = (predictions >= self.threshold)

        print('predictions',predictions)

        print('predictions_np_argmax',np.argmax(predictions, axis=1))
        # print(predictions.shape)

        tn, fp, fn, tp = confusion_matrix(np.argmax(labels, axis=1), np.argmax(predictions, axis=1)).ravel()

        print('reuslt of GPT')
        print("validation Accuracy: ", (tp + tn) / (tp + tn + fp + fn))

    