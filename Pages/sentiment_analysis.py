import streamlit as st #type: ignore
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore
import matplotlib.pyplot as plt # type: ignore
import preprocessor, helper

if "chat_data" in st.session_state:
    # Check if chat data is available
    df = st.session_state["chat_data"]
    st.title("📈 Sentiment Analysis")
    # display unique users
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Select user", user_list, key='user')

    pos_sent, neg_sent, neu_sent = helper.sentiment_analysis(selected_user,df)

    # add button to show analysis
    if st.sidebar.button("Show Analysis"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<h4 style='color: #ff7f50;'>Positive Sentiment</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #2575fc;'>{pos_sent}</h4>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<h4 style='color: #ff7f50;'>Negative Sentiment</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #2575fc;'>{neg_sent}</h4>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<h4 style='color: #ff7f50;'>Neutral Sentiment</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #2575fc;'>{neu_sent}</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.header("📊 User's Sentiment")
            X = round((df['users'].value_counts()/df['messages'].shape[0]*100),2).reset_index().rename(columns={'users':'Name of Group Members','count':'Activity Percentage'})
            st.dataframe(X)
        with col2:
            st.header("Sentiment Grapgh 📈")
            labels = ['Positive', 'Negative', 'Neutral']
            values = [pos_sent,neg_sent,neu_sent]
            colors = ['green', 'red','yellow']
            fig, ax = plt.subplots()
            ax.bar(labels, values, color=colors)
            ax.set_xlabel("Sentiment", color='green', fontsize=15, fontweight='bold')
            ax.set_title("Sentiment Analysis", color='green', fontsize=20, fontweight='bold')
            ax.set_ylabel("Sentiment Score", color='green', fontsize=15, fontweight='bold')
            st.pyplot(fig)
        
        # user messages in chat
        st.header(f"Total messages of {selected_user} 📜")
        user_df = df[df['users'] == selected_user].copy()

        # Drop rows with empty or null messages
        user_df = user_df[user_df['messages'].notnull() & (user_df['messages'].str.strip() != '')]
        st.dataframe(user_df[['messages','day','month','year']])
        
        
else:
    st.warning("⚠️ Please upload a file first from the Upload section.")
