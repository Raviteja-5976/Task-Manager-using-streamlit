import streamlit as st

st.caption('Webapp Made by Raviteja')
st.title('GDSC TASK MANAGEMENT')

st.header('Select Your Domain Page')

# Define custom CSS styles to center-align and enlarge the buttons
button_style = """
    <style>
    .stButton > button {
        width: 100%;
        font-size: 20px;
        text-align: center;
    }
    </style>
"""

# Display the CSS style
st.markdown(button_style, unsafe_allow_html=True)

# Create centered and enlarged buttons
st.button('GDSC LEAD LOGIN')
st.button('ANDROID DOMAIN LOGIN')
st.button('CLOUD DOMAIN LOGIN')
st.button('COMPETITIVE CODING DOMAIN LOGIN')
st.button('MACHINE LEARNING DOMAIN LOGIN')
st.button('WEB DEVELOPMENT DOMAIN LOGIN')
st.button('FLUTTER DOMAIN LOGIN')
st.button('MANAGEMENT DOMAIN LOGIN')
st.button('DESIGN DOMAIN LOGIN')
st.button('MARKETING DOMAIN LOGIN')
st.button('SOCIAL MEDIA DOMAIN LOGIN')
st.button('CONTENT WRITING DOMAIN LOGIN')
