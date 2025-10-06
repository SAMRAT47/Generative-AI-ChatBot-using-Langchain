from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from datetime import datetime
import base64
import os
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GENAI Chatbot by Samrat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Title Section
# --------------------------------------------------
st.markdown('<div style="position:relative; z-index:9999;">', unsafe_allow_html=True)
st.title("🤖 AI Chatbot")
st.markdown(
    "<p style='text-align:center; color: rgba(255,255,255,0.92); margin-top:-8px;'>"
    "Powered by Llama 3.1 | Created by Samrat Roychoudhury"
    "</p>",
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# ============================================
# IMAGE / BACKGROUND HELPERS
# ============================================
def _encode_image_to_base64(image_file):
    """Return base64 string for an image if file exists, else None."""
    if image_file and os.path.exists(image_file):
        with open(image_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def set_background(image_file, visibility_alpha=0.28):
    encoded = _encode_image_to_base64(image_file)
    if encoded:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image:
                    linear-gradient(135deg, rgba(102,126,234,{visibility_alpha}) 0%, rgba(118,75,162,{visibility_alpha}) 100%),
                    url("data:image;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            </style>
        """, unsafe_allow_html=True)


def set_sidebar_background(image_file, overlay_alpha=0.20, radius=18):
    encoded = _encode_image_to_base64(image_file)
    if encoded:
        st.markdown(f"""
            <style>
            [data-testid="stSidebar"] {{
                position: relative !important;
                border-radius: {radius}px !important;
                overflow: hidden !important;
                box-shadow: 0 8px 30px rgba(0,0,0,0.35);
                margin: 1rem 0 1rem 1rem;
            }}
            [data-testid="stSidebar"] > div:first-child {{
                background-image:
                    linear-gradient(135deg, rgba(0,0,0,{overlay_alpha}) 0%, rgba(0,0,0,{overlay_alpha}) 100%),
                    url("data:image;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                padding: 18px;
                min-height: 100vh;
            }}
            [data-testid="stSidebarNav"] {{
                background: transparent !important;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <style>
            [data-testid="stSidebar"] {{
                border-radius: {radius}px !important;
                overflow: hidden !important;
                background: linear-gradient(135deg, rgba(30,30,50,0.95) 0%, rgba(20,20,40,0.98) 100%);
            }}
            </style>
        """, unsafe_allow_html=True)


def set_input_background(image_file, overlay_alpha=0.03, radius=16):
    encoded = _encode_image_to_base64(image_file)
    if encoded:
        st.markdown(f"""
            <style>
            .stChatInputContainer {{
                border-radius: {radius}px !important;
                padding: 12px !important;
                background-image:
                    linear-gradient(0deg, rgba(255,255,255,{overlay_alpha}), rgba(255,255,255,{overlay_alpha})),
                    url("data:image;base64,{encoded}") !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                box-shadow: 0 8px 24px rgba(0,0,0,0.18) !important;
                border: 2px solid rgba(255,255,255,0.06) !important;
            }}
            .stChatInput input {{
                border-radius: {radius - 6}px !important;
                padding: 12px !important;
                background: rgba(255,255,255,0.9) !important;
                border: 1px solid rgba(0,0,0,0.08) !important;
                color: #111 !important;
                font-size: 1rem !important;
            }}
            .stChatInput input::placeholder {{
                color: rgba(0,0,0,0.45) !important;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <style>
            .stChatInputContainer {{
                border-radius: {radius}px !important;
                padding: 12px !important;
                background: rgba(255,255,255,0.95) !important;
                box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
            }}
            .stChatInput input {{
                border-radius: {radius - 6}px !important;
                padding: 12px !important;
                background: white !important;
                color: #111 !important;
            }}
            </style>
        """, unsafe_allow_html=True)


# ============================================
# Apply backgrounds (images go into images/ folder)
image_dir = "images"
if not os.path.exists(image_dir):
    os.makedirs(image_dir, exist_ok=True)

set_background(os.path.join(image_dir, "chatbot_bg.jpg"), visibility_alpha=0.28)
set_sidebar_background(os.path.join(image_dir, "sidebar_bg.jpg"), overlay_alpha=0.20, radius=18)
set_input_background(os.path.join(image_dir, "input_bg.jpg"), overlay_alpha=0.30, radius=16)


# ============================================
# GLOBAL CSS: chat bubbles, sidebar buttons (modern), metrics, etc.
st.markdown("""
    <style>
    /* keep header transparent */
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stAppViewContainer"] { background: transparent; }

    /* Chat message cards */
    .stChatMessage {
        background-color: rgba(255,255,255,0.92) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        margin: 0.6rem 0 !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12) !important;
        color: #111 !important;
        border: 1px solid rgba(0,0,0,0.06) !important;
    }
    .stChatMessage[data-testid*="user"] { border-left: 5px solid #667eea !important; }
    .stChatMessage[data-testid*="assistant"] { border-left: 5px solid #764ba2 !important; }

    /* Force dark readable text inside chat */
    .stChatMessage, .stChatMessage * { color: #0f1720 !important; -webkit-text-fill-color: #0f1720 !important; text-shadow: none !important; }
    .stChatMessage a { color: #0b61ff !important; text-decoration: underline !important; }
    .stChatMessage code, .stChatMessage pre { color: #111 !important; background-color: rgba(0,0,0,0.04) !important; }

    /* Sidebar: make contained buttons modern, stacked and centered */
    [data-testid="stSidebar"] .sidebar-actions {
        display: flex;
        flex-direction: column;
        gap: 10px;
        align-items: center;
        justify-content: center;
        padding: 12px 6px;
        margin-top: 12px;
    }

    /* style Streamlit buttons that appear inside sidebar (gives them a modern look) */
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stDownloadButton > button {
        width: calc(100% - 28px) !important;
        max-width: 240px !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        color: white !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.28) !important;
        backdrop-filter: blur(6px) saturate(120%) !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease, background 0.12s ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] .stDownloadButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.35) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04)) !important;
    }

    /* ensure sidebar has enough bottom padding */
    [data-testid="stSidebar"] > div:first-child { padding-bottom: 120px !important; }

    /* Metrics in sidebar - lighter labels */
    .stMetric label { color: rgba(255,255,255,0.9) !important; }
    .stMetric [data-testid="stMetricValue"] { color: white !important; }
    </style>
""", unsafe_allow_html=True)


# ============================================
# Sidebar content (Config + professional stacked actions)
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    model_option = st.selectbox(
        "Select Model",
        ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
        index=0
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative, lower values more focused"
    )

    max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=4096,
        value=1024,
        step=100
    )

    st.markdown("---")

    # Chat stats
    if "chat_history" in st.session_state and st.session_state.chat_history:
        st.markdown("### 🔎 Chat Statistics")
        user_msgs = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        assistant_msgs = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])
        st.metric("User Messages", user_msgs)
        st.metric("Assistant Messages", assistant_msgs)
        st.metric("Total Messages", len(st.session_state.chat_history))

    st.markdown("---")

    # Professional-stacked actions area (centered)
    st.markdown('<div class="sidebar-actions" aria-hidden="false">', unsafe_allow_html=True)

    # Clear button (stacked)
    clear_clicked = st.button("🗑️ Clear Chat", key="clear_chat_btn")

    # Export as download button (only show when chat exists)
    if st.session_state.get("chat_history"):
        chat_text = "\n\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in st.session_state.chat_history
        ])
        st.download_button(
            label="📥 Export Chat",
            data=chat_text,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_chat_history_btn"
        )
    else:
        # placeholder button (uninteractive) to show consistent layout when no chat exists
        st.button("📥 Export Chat", key="export_placeholder", disabled=True)

    # End stacked container
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("<div style='color: rgba(255,255,255,0.75); text-align:center; font-size:12px; margin-top:6px;'>Quick actions</div>", unsafe_allow_html=True)

    # Clear action: when clicked, clear and reload the page to update UI
    if clear_clicked:
        st.session_state.chat_history = []
        # Reload page (works across Streamlit versions)
        components.html("<script>window.location.reload()</script>", height=0)


# ============================================
# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================
# Initialize LLM (cached resource)
@st.cache_resource
def get_llm(model_name, temp):
    return ChatGroq(model=model_name, temperature=temp)


llm = get_llm(model_option, temperature)


# ============================================
# Render chat history (no per-message copy buttons)
chat_container = st.container()
with chat_container:
    if not st.session_state.chat_history:
        st.info("👋 Hello! I'm your AI assistant. How can I help you today?")

    for message in st.session_state.chat_history:
        role = message.get("role", "assistant")
        avatar = "👤" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])


# ============================================
# Chat input + streaming
user_prompt = st.chat_input("Type your message here...", key="chat_input")

if user_prompt:
    # display user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)

    # store user message
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # generate assistant response (stream)
    with st.chat_message("assistant", avatar="🛸"):
        placeholder = st.empty()
        full_response = ""
        try:
            for chunk in llm.stream(
                input=[
                    {"role": "system", "content": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and engaging responses."},
                    *st.session_state.chat_history
                ]
            ):
                part = getattr(chunk, "content", str(chunk))
                full_response += part
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            st.info("Please check your API key and internet connection.")


# ============================================
# Footer note
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color: rgba(255,255,255,0.95); font-size:0.9rem;'>"
    "💡 Tip: Use the sidebar to customize your experience • Use Export to download the conversation"
    "</div>",
    unsafe_allow_html=True
)

