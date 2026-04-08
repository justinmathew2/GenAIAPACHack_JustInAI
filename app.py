import streamlit as st
import requests

# 👉 Backend API URL
API_URL = "http://localhost:8000"

# 👉 Page config
st.set_page_config(page_title="JustInAI", layout="wide")

# 👉 Header
st.title("🤖 JustInAI")
st.caption("Multi-Agent AI System (Text + Image + Tools)")

# 👉 Input Section
st.subheader("💬 Enter your request")
query = st.text_input("Type something (task / question / anything)")

# 👉 Image Upload
st.subheader("📸 Upload an Image (Optional)")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", width="stretch")

# 👉 Run Button
if st.button("🚀 Run Analysis"):

    if not query and not uploaded_file:
        st.warning("Please enter a query or upload an image")
    else:
        with st.spinner("🤖 AI Agents are working..."):

            files = None
            data = {"query": query if query else "analyze this image"}

            if uploaded_file:
                files = {"file": uploaded_file.getvalue()}

            try:
                res = requests.post(
                    f"{API_URL}/analyze",
                    data=data,
                    files=files
                )

                result = res.json()

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
                st.stop()

        # 👉 Output Section
        st.subheader("📊 Result")

        if result.get("calendar_link"):
            st.markdown(f"[📅 Add to Google Calendar]({result['calendar_link']})")
            
        # 🔥 IMAGE FLOW
        if result.get("type") == "image":

            st.success("🖼 Image Analysis Completed")

            st.subheader("🔍 Analysis")
            st.write(result.get("analysis", "No analysis"))

            st.subheader("🌦 Weather")
            st.info(result.get("weather", "No weather data"))

            st.subheader("🧠 Decision")
            st.warning(result.get("decision", "No decision"))

            st.subheader("📅 Task Created")
            st.success(result.get("task", "No task"))

        # 🔥 TASK FLOW
        elif result.get("type") == "task":

            st.success(result.get("message", "Task created"))

        # 🔥 GENERAL FLOW
        else:
            st.subheader("💡 AI Response")
            response_text = result.get("response")

            if response_text:
                st.info(response_text)
            else:
                st.warning("No response generated")

# 👉 Divider
st.divider()

# 👉 Task History Section
st.subheader("📋 Task History")

if st.button("🔄 Load Tasks"):
    try:
        res = requests.get(f"{API_URL}/tasks")
        tasks = res.json()

        if len(tasks) == 0:
            st.info("No tasks yet")
        else:
            for t in tasks:
                st.success(f"✅ {t['task']}")

    except Exception as e:
        st.error(f"Error fetching tasks: {e}")

if st.button("🗑 Clear Tasks"):
    requests.get(f"{API_URL}/clear_tasks")
    st.success("All tasks cleared")

# 👉 Agent Workflow Visualization (VERY IMPORTANT FOR DEMO)
st.divider()
st.subheader("🔄 Agent Workflow")

st.markdown("""
1. 🧠 **Primary Agent** → Understands user intent  
2. 🖼 **Vision Agent** → Processes image (if provided)  
3. 📚 **Knowledge Agent** → Generates insights (Gemini AI)  
4. 🌦 **Weather Agent** → Fetches real-time data  
5. 📅 **Task Agent** → Creates tasks  
6. 💾 **Memory Agent** → Stores data in Firestore  
""")