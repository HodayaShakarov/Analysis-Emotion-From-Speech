
import streamlit as st
from predict_page import show_predict_page

import base64

# main_bg = "yourimage.png"# this is your image
# main_bg_ext = "png"

# this is how to make it as a background
# st.markdown(
#     f"""
#     <style>
#     .reportview-container {{
#         background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://res.cloudinary.com/sign-language/image/upload/v1635956951/video/%D7%AA%D7%9E%D7%95%D7%A0%D7%AA_%D7%A8%D7%A7%D7%A2_%D7%9C%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98_l2btt4.png")
    }
   .sidebar .sidebar-content {
        background: url("url_goes_here")
    }
    </style>
    """,
    unsafe_allow_html=True
)

show_predict_page()








