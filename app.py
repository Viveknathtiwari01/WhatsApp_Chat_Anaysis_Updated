import streamlit as st #type: ignore

st.set_page_config(
    page_title="Streamlit-Demo", 
    page_icon = "🎗️" )

# --- add logo for all pages ---
st.logo("assets/logo.png")
st.sidebar.markdown("<h5 style='text-align: center; color: #ff7f50;'>WhatsApp Chat Analysis</h5>", unsafe_allow_html=True)

 # --- Page Setup ---
chat_analysis_page = st.Page(
    page = "Pages/chat_analysis.py",
    title = "Chat Analysis",
    icon = "📊",
)
sentiment_analysis_page = st.Page(
    page = "Pages/sentiment_analysis.py",
    title = "Sentiment Analysis",
    icon = "📈"
)

about_page  = st.Page(
    page = "Pages/about.py",
    title = "About Us",
    icon = "📖",
    default = False
) 

home_page = st.Page(
    page = "Pages/home.py",
    title = "Home Page",
    icon = "🏠",
    default = True

)

contact_page = st.Page(
    page = "Pages/contact.py",
    title = "Contact Us",
    icon = "📞",
)

upload_page = st.Page(
    page = "Pages/upload_file.py",
    title = "Upload File",
    icon = "📤",
 )

# --- NAvigation Setup ---
#pg = st.navigation(pages=[home_page, about_page, contact_page, dashboard_page])

pg  =st.navigation(
    {
        'info':[about_page],
        'upload':[upload_page],
        'Statistic':[chat_analysis_page, sentiment_analysis_page],
        'Project':[home_page, contact_page]
    }
)


# --- Run Navigation ---

pg.run()