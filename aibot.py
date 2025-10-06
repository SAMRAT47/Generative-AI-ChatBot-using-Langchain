from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from datetime import datetime
import base64
from pathlib import Path

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Chatbot by Samrat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================
# BACKGROUND IMAGE LOADER
# ============================================
def get_base64_image(image_path):
    """Convert image to base64 string for CSS embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None


# Try to load background images
# Place your images in the 'assets' folder:
# - assets/background.jpg (or .jpeg/.png) for main background
# - assets/sidebar_bg.jpg (or .jpeg/.png) for sidebar background
background_image = get_base64_image("assets/background.jpeg")
sidebar_image = get_base64_image("assets/sidebar_bg.jpeg")

# ============================================
# BUILD DYNAMIC CSS
# ============================================
css_styles = """
    <style>
    /* ============================================
       HOW TO ADD CUSTOM BACKGROUND IMAGES
       ============================================

       METHOD 1: Local Images (Automatic - Recommended)
       Steps in PyCharm:
       1. Right-click project root → New → Directory → name it "assets"
       2. Place your images in the assets folder:
          - background.jpg (or .jpeg/.png) for main background
          - sidebar_bg.jpg (or .jpeg/.png) for sidebar background
       3. Restart Streamlit app (Ctrl+C then run again)
       4. Images will automatically load!

       METHOD 2: Online Image URL
       Replace the gradient line in the code below with:
       background: url('https://your-image-url.com/image.jpg') center/cover no-repeat fixed;
    */

    /* Override Streamlit defaults */
    .stApp {
        background: transparent;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Main container styling */
    .main {
"""

# Add main background (image or gradient)
if background_image:
    css_styles += f"""
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.6) 0%, rgba(118, 75, 162, 0.6) 100%),
                    url('data:image/jpeg;base64,{background_image}') center/cover no-repeat fixed;
"""
else:
    css_styles += """
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
"""

css_styles += """
        min-height: 100vh;
    }

    /* Chat container */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        color: white;
    }

    /* Make text readable in chat messages */
    .stChatMessage p, .stChatMessage div {
        color: white !important;
    }

    /* Title styling */
    .main-title {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Input box styling */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.1);
        border-top: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }

    /* Style the input field */
    .stChatInput input {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }

    .stChatInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Sidebar styling */
"""

# Add sidebar background (image or gradient)
if sidebar_image:
    css_styles += f"""
    .stSidebar {{
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0.7) 100%),
                    url('data:image/jpeg;base64,{sidebar_image}') center/cover no-repeat fixed !important;
        backdrop-filter: blur(5px);
    }}
"""
else:
    css_styles += """
    .stSidebar {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px);
    }
"""

css_styles += """

    [data-testid="stSidebarNav"] {
        background: transparent;
    }

    .stSidebar [data-testid="stMarkdownContainer"] {
        color: white !important;
    }

    /* Info box styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px);
        color: white !important;
    }

    .stAlert p {
        color: white !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    </style>
"""

# Apply the CSS
st.markdown(css_styles, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🤖 AI Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Llama 3.1 | Created by Samrat Roychoudhury</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # Model selection
    model_option = st.selectbox(
        "Select Model",
        ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
        index=0
    )

    # Temperature control
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative, lower values more focused"
    )

    # Max tokens
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=4096,
        value=1024,
        step=100
    )

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    # Chat statistics
    if "chat_history" in st.session_state and st.session_state.chat_history:
        st.markdown("### 📊 Chat Statistics")
        user_msgs = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        assistant_msgs = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])
        st.metric("User Messages", user_msgs)
        st.metric("Assistant Messages", assistant_msgs)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Initialize LLM with sidebar parameters
@st.cache_resource
def get_llm(model_name, temp):
    return ChatGroq(
        model=model_name,
        temperature=temp,
    )


llm = get_llm(model_option, temperature)

# Display chat history
chat_container = st.container()
with chat_container:
    if not st.session_state.chat_history:
        st.info("👋 Hello! I'm your AI assistant. How can I help you today?")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

# Chat input
user_prompt = st.chat_input("Type your message here...", key="chat_input")

if user_prompt:
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)

    # Add to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Generate response with spinner
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                response = llm.invoke(
                    input=[
                        {"role": "system",
                         "content": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and engaging responses."},
                        *st.session_state.chat_history
                    ]
                )
                assistant_response = response.content

                # Display response
                st.markdown(assistant_response)

                # Add to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": assistant_response
                })

            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")
                st.info("Please check your API key and internet connection.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;'>"
    "💡 Tip: Use the sidebar to customize your chat experience"
    "</div>",
    unsafe_allow_html=True
)