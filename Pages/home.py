import streamlit as st #type:ignore
from PIL import Image

st.title("Home Page")


st.markdown("""
# 👋 Welcome to WhatsApp Chat Analysis!

Unlock the hidden stories in your WhatsApp conversations. This interactive dashboard helps you:

- Analyze chat activity and trends
- Visualize your most used words and emojis
- Explore sentiment and engagement

---

## Get Started

1. Go to the **Upload File** page
2. Upload your exported WhatsApp chat file
3. Dive into the analytics!

---

> _Your data stays private and is never stored._

<small>Created by Vivek Nath Tiwari</small>
""", unsafe_allow_html=True)