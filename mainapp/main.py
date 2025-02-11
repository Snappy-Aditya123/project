import streamlit as st

# Set Streamlit Page Config
st.set_page_config(page_title="AI Job Assistant", page_icon="🤖", layout="wide")

# --- Initialize Session State ---
if "stage" not in st.session_state:
    st.session_state.stage = "onboarding"  # Start at onboarding
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "cv_uploaded" not in st.session_state:
    st.session_state.cv_uploaded = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_section" not in st.session_state:
    st.session_state.current_section = "chatbot"  # Default to chatbot

# --- Onboarding Section ---
if st.session_state.stage == "onboarding":
    st.title("👋 Welcome to AI Job Assistant")

    # Collect user details
    name = st.text_input("Enter your name:", placeholder="John Doe")
    location = st.text_input("Enter your location:", placeholder="e.g., London, UK")
    experience_level = st.selectbox("Experience Level:", ["Entry Level", "Mid Level", "Senior Level"])

    # Collect job interest (Only One)
    job_interest = st.text_input("What is your job interest?", placeholder="e.g., Data Scientist")

    # Button to proceed
    if st.button("Save & Continue"):
        if name.strip() and location.strip() and job_interest.strip():
            st.session_state.user_data = {
                "name": name,
                "location": location,
                "experience": experience_level,
                "job_interest": job_interest,
            }
            st.session_state.stage = "cv_upload"  # Move to CV Upload
        else:
            st.warning("⚠️ Please fill in all the required fields!")

# --- CV Upload Section ---
elif st.session_state.stage == "cv_upload":
    st.title("📄 Upload Your CV (Optional)")
    st.write("Uploading your CV will help the AI provide better job recommendations.")

    uploaded_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])
    
    col1, col2 = st.columns(2)
    with col1:
        if uploaded_file:
            st.session_state.cv_uploaded = True
            st.success("✅ CV Uploaded Successfully!")

    with col2:
        if st.button("Skip"):
            st.session_state.stage = "main"  # Move to main app

    if uploaded_file or st.session_state.cv_uploaded:
        if st.button("Continue"):
            st.session_state.stage = "main"

# --- Main Application Layout ---
elif st.session_state.stage == "main":
    # Create Three Layout Columns (Left Sidebar, Main Section, Right Sidebar)
    col1, col2, col3 = st.columns([1, 2, 1])  

    # --- Left Sidebar: Navigation + Profile ---
    with col1:
        st.sidebar.title("Navigation")
        nav_option = st.sidebar.radio("Go to:", ["💬 Chatbot", "📊 CV Analysis"])

        st.sidebar.markdown("---")
        st.sidebar.subheader(f"👤 {st.session_state.user_data['name']}")
        st.sidebar.text(f"📍 {st.session_state.user_data['location']}")
        st.sidebar.text(f"🎯 Interest: {st.session_state.user_data['job_interest']}")

    # --- Center Section: Chatbot / CV Analysis ---
    with col2:
        if nav_option == "💬 Chatbot":
            st.title("💬 AI Job Assistant Chatbot")
            st.write("Chat with the AI Assistant to explore job opportunities and career guidance.")

            # Display Chat History
            for chat in st.session_state.chat_history:
                with st.chat_message(chat["role"]):
                    st.write(chat["content"])

            # Chat Input
            user_input = st.chat_input("Type your message...")
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                bot_response = "🔹 This is a placeholder response. AI will generate a real response here."
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

        elif nav_option == "📊 CV Analysis":
            st.title("📊 CV Analysis")
            
            if not st.session_state.cv_uploaded:
                st.warning("⚠️ You have not uploaded a CV. Please upload one in the sidebar.")
            else:
                st.success("✅ Your CV is being analyzed...")
                st.subheader("📝 CV Insights")
                st.write("AI-generated insights will appear here based on your CV.")

                # Example Placeholder Insights
                st.write("- **Strengths:** Python, Deep Learning, Data Analysis")
                st.write("- **Weaknesses:** Lacks cloud computing skills")
                st.write("- **Job Suitability Score:** 85% match for Data Scientist roles")
                
                st.subheader("📌 Suggested Improvements")
                st.write("- Consider learning AWS for better cloud integration.")
                st.write("- Add more projects showcasing real-world ML applications.")

    # --- Right Sidebar: Job Recommendations ---
    with col3:
        st.markdown("### 🔍 Job Recommendations")
        st.write("Here are some jobs related to your interest:")

        # Placeholder Jobs (Replace with API-based jobs later)
        job_listings = [
            {"title": "Data Scientist", "company": "Google", "location": "San Francisco"},
            {"title": "Machine Learning Engineer", "company": "Amazon", "location": "New York"},
            {"title": "AI Researcher", "company": "OpenAI", "location": "Remote"},
        ]

        for job in job_listings:
            with st.expander(f"🔹 {job['title']} at {job['company']} ({job['location']})"):
                st.write("📌 Job Description: AI will fetch real details here.")
                st.button("Apply Now", key=job["title"])

# --- Footer ---
st.markdown("---")
st.caption("🚀 AI-powered Job Assistant")
