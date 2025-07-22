import streamlit as st # type: ignore
import preprocessor, helper
import matplotlib.pyplot as plt # type: ignore
from matplotlib import font_manager as fm
import os
st.title("📈 Chat Analysis") 

# Check if chat data is available
if "chat_data" in st.session_state:
    df = st.session_state["chat_data"]

    # Proceed with analysis
    # display unique users
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Select user", user_list, key='user')

    num_messages, num_words, num_media, num_links, emoji_count = helper.fetch_stats(df,selected_user)

    # add button to show analysis
    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"<h4 style='color: #ff7f50;'>Total Messages</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #2575fc;'>{num_messages}</h4>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<h4 style='color: #ff7f50;'>Total Words 📝</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #2575fc;'>{num_words}</h4>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<h4 style='color: #ff7f50;'>Total Shared Media📸</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #2575fc;'>{num_media}</h4>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<h4 style='color: #ff7f50;'>Total Shared Links 🌐 </h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #2575fc;'>{num_links}</h4>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<h4 style='color: #ff7f50;'>Total Shared Emojis 😄</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #2575fc;'>{emoji_count}</h4>", unsafe_allow_html=True)   
        
        if selected_user == 'Overall':
            
            X = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                st.title("🏆 Most Active Users!")
                ax.barh(X.index, X.values, color='purple')
                ax.set_xlabel("Number of Messages", color='green', fontsize=15, fontweight='bold')
                ax.set_ylabel("User's Name", color='green', fontsize=15, fontweight='bold')
                ax.set_title("Most Active Users", color='green', fontsize=20, fontweight='bold')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                total_users = df['users'].unique().shape[0]
                st.title(f"📊 Total No of Users:- {total_users}")
                X = round((df['users'].value_counts()/df['messages'].shape[0]*100),2).reset_index().rename(columns={'users':'Name of Group Members','count':'Activity Percentage'})
                
                st.dataframe(X)

        # generate word cloud
        st.title("🗣️ Word Cloud")
        df_img = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        ax.axis('off')
        st.pyplot(fig)


        col1, col2 = st.columns(2)
        with col1:
            common_words_data = helper.fetch_most_common_words(selected_user, df)

            st.title("🗣️ Most Common Words")

            if isinstance(common_words_data, str):
                st.write(common_words_data)
            else:
                st.dataframe(common_words_data)
        
        with col2:
            common_words_data = helper.fetch_most_common_words(selected_user, df)

            st.title("🗣️ Most Common Words")

            if isinstance(common_words_data, str):
                st.write(common_words_data)
            else:
                fig, ax = plt.subplots()
                ax.bar(common_words_data['Common Words'], common_words_data['Word Frequency'], color='purple')
                plt.xticks(rotation='vertical')
                ax.set_xlabel("Common Words", color='green', fontsize=15, fontweight='bold')
                ax.set_ylabel("Word Frequency", color='green', fontsize=15, fontweight='bold')
                st.pyplot(fig)
        
        # emoji analysis
        emoji_count_df = helper.fetch_most_common_emojis(selected_user, df)
        col1, col2 = st.columns(2)
        with col2:
            st.title("😄 Emoji Analysis")
            st.dataframe(emoji_count_df)
        with col1:
            # Set emoji font
            emoji_font_path = 'C:/Windows/Fonts/seguiemj.ttf'  # Segoe UI Emoji font path in Windows
            if os.path.exists(emoji_font_path):
                emoji_font = fm.FontProperties(fname=emoji_font_path)
            else:
                emoji_font = fm.FontProperties()  # Use default font

            st.title("😄 Emoji's Pie Chart")

            fig, ax = plt.subplots()

            wedges, texts, autotexts = ax.pie(
                emoji_count_df['Emoji Frequency'].head(),
                labels=emoji_count_df['Emojis'].head(),
                autopct='%0.2f%%',
                startangle=140,
                textprops={'fontsize': 16, 'fontproperties': emoji_font}
            )

            for text in texts:
                text.set_fontproperties(emoji_font)
                text.set_fontsize(20)

            for autotext in autotexts:
                autotext.set_fontsize(14)

            ax.axis('equal')
            st.pyplot(fig)
else:
    st.warning("⚠️ Please upload a WhatsApp chat file first on the 'Upload File' page.")
       
