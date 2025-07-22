import streamlit as st  #type: ignore
from PIL import Image
import os

st.title("About Us")

st.markdown("""
Welcome to **WhatsApp Chat Analysis**! 🚀

This project empowers you to gain deep insights from your WhatsApp conversations. Whether you're curious about your most active friends, want to visualize your chat history, or analyze the sentiment of your messages, this tool has you covered.

### Key Features
- 📊 **Chat Statistics**: Discover your most active days, top words, and more.
- 🌥️ **Word Clouds**: Visualize your most used words.
- 😀 **Emoji Analysis**: See which emojis you use the most.
- 📈 **Sentiment Analysis**: Understand the mood of your conversations.

---
### Meet the Creator
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    st.image("assets/vivek_1.jpg", width=80)
with col2:
    st.markdown("""
**Vivek Nath Tiwari**  
_AI/ML Enthusiast & Developer_  
[Contact Me](mailto:viveknath62094@gmail.com)
""")

st.markdown("""
---
<small>Made with ❤️ using Streamlit</small>
""", unsafe_allow_html=True)
