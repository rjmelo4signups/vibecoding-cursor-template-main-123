import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Welcome to My App",
    page_icon="🚀",
    layout="wide"
)

# Main heading
st.title("🚀 Welcome to My App")
st.markdown("---")

# Hero section
st.markdown("""
## Hello! 👋
This is your personal landing page. Here you can showcase your projects and tools.
""")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.header("📁 My Projects")
    st.markdown("""
    - **Job Scraper**: Find job opportunities
    - **Video Downloader**: Download videos easily  
    - **Form Automation**: Automate repetitive tasks
    - **Mouse Jiggle**: Keep your computer active
    """)

with col2:
    st.header("🛠️ Quick Actions")
    if st.button("View All Projects"):
        st.success("All projects are available in your workspace!")
    
    if st.button("Get Started"):
        st.info("Choose a project from the list above to begin!")

# Add some spacing
st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)