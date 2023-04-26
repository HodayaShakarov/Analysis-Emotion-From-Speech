#!/usr/bin/env python
# coding: utf-8
from django.conf import settings

# In[ ]:


import streamlit as st
import pickle
import numpy as np
from PIL import Image
import glob
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision
import matplotlib.pyplot as plt 
import torch
import torch.nn as nn
import torch.nn.functional as F
import SessionState
from random import randint

def show_predict_page():
    
    class ConvNet(nn.Module):
        def __init__(self, num_classes):
            super(ConvNet, self).__init__()

            self.conv1 = nn.Sequential(nn.Conv2d(1, 6, kernel_size=5, padding = 2),
                                       nn.BatchNorm2d(6),
                                       nn.ReLU(),
                                       nn.MaxPool2d(kernel_size=2, stride=2))

            self.conv2 = nn.Sequential(nn.Conv2d(6, 16, kernel_size=3, padding = 2),
                                       nn.BatchNorm2d(16),
                                       nn.ReLU(),
                                       nn.MaxPool2d(kernel_size=2, stride=2))
            self.conv3 = nn.Sequential(nn.Conv2d(16, 32, kernel_size=3, padding = 1),
                                       nn.BatchNorm2d(32),
                                       nn.ReLU(),
                                       nn.MaxPool2d(kernel_size=2, stride = 2))

            self.output = nn.Linear(2048, num_classes)

        def forward(self, x):
            out = self.conv1(x)
            out = self.conv2(out)
            out = self.conv3(out)


            out = out.reshape(-1,2048)
            #print(out.shape)
            out = self.output(out)
            #print(out.shape)
            return F.softmax(out, dim=1)

  

    alpha=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    #my_model=torch.load('model.pt')
    model = ConvNet(26)

    model.load_state_dict(torch.load('C:/Users/This_user/Downloads/project/prog/pro'))
    model.eval()


       

     


       

    
    
    
    #########################################################
        


    ss=SessionState.get(li= [])
    def display_text(bounds):
        text = []
        for x in bounds:
            
            #t = x[1]
            text.append(x)
        text = ' '.join(text)
        return text 

    #listo=[]

    st.title('Hands gesture detection')
    
#     ff=SessionState.get(l= [1,4])
#     ff.l.append(state)
#     # convert list to iterator
#     state= iter(ff.l)
#     st.write(state)

#     # the next element is the first element
#     marks_1 = next(iterator_marks)
    #print(marks_1)
      
        

    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="big-font"> Upload Image !</p>', unsafe_allow_html=True)

    state=2
#         state = str(randint(1000, 100000000))
    #if st.button("a"):
    #    state = str(np.random.rand())
    image_file = st.file_uploader("",accept_multiple_files=True,key=f'{state}')
    if image_file:
        st.markdown('Upload complete!')
#         #################
#         # Hide filename on UI
#         st.markdown('''
#             <style>
#                 .uploadedFile {display: none}
#             <style>''',
#             unsafe_allow_html=True)
################################
    #st.button("add_space",key=str(np.random.rand()))
    if st.button("Convert"):
        for i in image_file:
            
            if image_file is not None:
                

    #             img = Image.open(image_file)
                file_bytes = np.asarray(bytearray(i.read()), dtype=np.uint8)
                opencv_image = cv2.imdecode(file_bytes, 1)

                #this is your image
                img = opencv_image

                # pre processing the image and prepare it for the classification
                img = cv2.resize(img, (64,64))
                img_tensor = torch.from_numpy(img[:,:,1:2])
                img_tensor=img_tensor.reshape(1,1,64,64)


                #st.subheader('Image you Uploaded...')


                pred= model(img_tensor*1.1)

                top_p_pred, top_class_pred = pred.topk(1, dim=1) 
                #st.write(alpha[top_class_pred.item()])
                ss.li.append(alpha[top_class_pred.item()])
    
                
    if st.button("add_space"):
        ss.li.append(" ")
        state=ss.li[-2]
            #ss.li.append(listo)
    #if st.button("Text"):
    #    st.write( ss.li)

    st.write("".join(ss.li))
    #image_file=None
    

#     css = """
#     .uploadedFiles {
#         display: none;
#     }
#     """
#     # or `visibility: hidden;`

#     st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
#     files = st.sidebar.file_uploader("Choose files", accept_multiple_files=True)
    
    m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            # background-color: rgb(204, 149, 49);
              background-image: url('/bg.PNG');

        }
        </style>""", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url("https://images.app.goo.gl/LFCobouKtT7oZ7Qv7")
        }
       .sidebar .sidebar-content {
            background: url("https://images.app.goo.gl/LFCobouKtT7oZ7Qv7")
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    

    