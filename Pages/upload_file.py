import streamlit as st #type: ignore
import preprocessor  # your preprocessor.py

st.title("📤 Upload WhatsApp Chat File")

uploaded_file = st.file_uploader("Upload your WhatsApp chat file")

if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocessor(data)

    # Save chat data to session state
    st.session_state["chat_data"] = df

    st.success("✅ File uploaded and processed successfully!")
