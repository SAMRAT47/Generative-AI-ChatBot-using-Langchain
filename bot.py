"""
Professional Multi-Provider AI Chatbot with Streamlit
Created by Samrat Roychoudhury

This application provides a unified interface for multiple AI providers:
- OpenAI (GPT models)
- Google Gemini (Gemini models)
- Groq (Fast inference with Llama/Mixtral)
- Ollama (Local models)

Structure:
1. Configuration & Setup
2. Provider & Model Management
3. UI Styling Functions
4. Sidebar Configuration
5. Chat Interface
6. Message Handling
"""

from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
import base64
import os
import streamlit.components.v1 as components

# Load environment variables from .env file
load_dotenv()

# ============================================
# SECTION 1: CONFIGURATION & SETUP
# ============================================

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="GENAI-Chatbot by Samrat",
    page_icon="⚛",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Provider and model configuration dictionary
# This maps each provider to their available models
PROVIDER_CONFIG = {
    "OpenAI": {
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4-turbo"],
        "import_path": "langchain_openai",
        "class_name": "ChatOpenAI",
        "env_key": "OPENAI_API_KEY"
    },
    "Google Gemini": {
        "models": ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.5-pro"],
        "import_path": "langchain_google_genai",
        "class_name": "ChatGoogleGenerativeAI",
        "env_key": "GOOGLE_API_KEY"
    },
    "Groq": {
        "models": ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        "import_path": "langchain_groq",
        "class_name": "ChatGroq",
        "env_key": "GROQ_API_KEY"
    },
    "Ollama": {
        "models": ["llama3.3", "gemma3", "mistral-small3.2", "phi4"],
        "import_path": "langchain_ollama",
        "class_name": "ChatOllama",
        "env_key": None  # Ollama doesn't need API key, runs locally
    }
}


# ============================================
# SECTION 2: PROVIDER & MODEL MANAGEMENT
# ============================================

def get_llm_instance(provider, model_name, temperature, max_tokens):
    """
    Dynamically creates and returns an LLM instance based on provider selection.

    Args:
        provider (str): The AI provider name (e.g., "OpenAI", "Groq")
        model_name (str): The specific model to use
        temperature (float): Controls randomness (0.0 to 1.0)
        max_tokens (int): Maximum response length

    Returns:
        LLM instance: A configured language model object
    """
    try:
        config = PROVIDER_CONFIG[provider]

        # Check if API key is required and available
        if config["env_key"] and not os.getenv(config["env_key"]):
            st.error(f"⚠️ {config['env_key']} not found in environment variables!")
            st.info("💡 Add your API key to the .env file")
            return None

        # Dynamic import of the appropriate LLM class
        module = __import__(config["import_path"], fromlist=[config["class_name"]])
        LLMClass = getattr(module, config["class_name"])

        # Create common parameters
        common_params = {
            "model": model_name,
            "temperature": temperature,
        }

        # Add max_tokens only for providers that support it
        if provider != "Ollama":
            common_params["max_tokens"] = max_tokens

        # Return configured LLM instance
        return LLMClass(**common_params)

    except ImportError as e:
        st.error(f"⚠️ Please install: pip install {config['import_path'].replace('_', '-')}")
        return None
    except Exception as e:
        st.error(f"⚠️ Error initializing {provider}: {str(e)}")
        return None


# ============================================
# SECTION 3: UI STYLING FUNCTIONS
# ============================================

def encode_image_to_base64(image_file):
    """
    Converts an image file to base64 encoding for CSS embedding.

    Args:
        image_file (str): Path to the image file

    Returns:
        str or None: Base64 encoded string or None if file doesn't exist
    """
    if image_file and os.path.exists(image_file):
        with open(image_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def apply_main_background(image_file, visibility_alpha=0.28):
    """
    Sets the main app background with gradient overlay.
    Creates a professional look with customizable transparency.
    """
    encoded = encode_image_to_base64(image_file)
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


def apply_sidebar_styling(image_file, overlay_alpha=0.20, radius=18):
    """
    Applies custom styling to the sidebar with optional background image.
    Creates a modern, glass-morphism effect.
    """
    encoded = encode_image_to_base64(image_file)
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


def apply_global_styles():
    """
    Applies global CSS styles for a professional, modern look.
    Styles include: chat bubbles, input fields, dropdowns, and buttons.
    """
    st.markdown("""
        <style>
        /* ========== HEADER & CONTAINER ========== */
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stAppViewContainer"] { background: transparent; }

        /* ========== CHAT MESSAGE BUBBLES ========== */
        .stChatMessage {
            background-color: rgba(255,255,255,0.92) !important;
            border-radius: 14px !important;
            padding: 1rem !important;
            margin: 0.6rem 0 !important;
            box-shadow: 0 6px 18px rgba(0,0,0,0.12) !important;
            color: #111 !important;
            border: 1px solid rgba(0,0,0,0.06) !important;
        }

        /* Color-coded borders for user vs assistant */
        .stChatMessage[data-testid*="user"] { 
            border-left: 5px solid #667eea !important; 
        }
        .stChatMessage[data-testid*="assistant"] { 
            border-left: 5px solid #764ba2 !important; 
        }

        /* Ensure text is always readable */
        .stChatMessage, .stChatMessage * { 
            color: #0f1720 !important; 
            -webkit-text-fill-color: #0f1720 !important; 
        }

        .stChatMessage a { 
            color: #0b61ff !important; 
            text-decoration: underline !important; 
        }

        /* ========== SIDEBAR SELECTBOX STYLING ========== */
        /* Main selectbox container */
        [data-testid="stSidebar"] .stSelectbox > div > div {
            background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04)) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(8px) !important;
            padding: 8px 12px !important;
        }

        /* Label above selectbox */
        [data-testid="stSidebar"] .stSelectbox label {
            color: rgba(255,255,255,0.95) !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            margin-bottom: 8px !important;
        }

        /* Selected value text - MAKE IT VISIBLE */
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
            color: white !important;
        }

        /* Selected text inside the box */
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span {
            color: white !important;
            font-weight: 600 !important;
        }

        /* Dropdown arrow */
        [data-testid="stSidebar"] .stSelectbox svg {
            fill: white !important;
        }

        /* ========== SIDEBAR SLIDER STYLING ========== */
        [data-testid="stSidebar"] .stSlider label {
            color: rgba(255,255,255,0.95) !important;
            font-weight: 600 !important;
        }

        [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
            background: rgba(255,255,255,0.1) !important;
        }

        /* ========== SIDEBAR NUMBER INPUT STYLING ========== */
        [data-testid="stSidebar"] .stNumberInput label {
            color: rgba(255,255,255,0.95) !important;
            font-weight: 600 !important;
        }

        [data-testid="stSidebar"] .stNumberInput input {
            background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04)) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 10px !important;
            color: white !important;
            padding: 8px 12px !important;
        }

        /* ========== SIDEBAR BUTTONS ========== */
        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] .stDownloadButton > button {
            width: 100% !important;
            background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04)) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            color: white !important;
            padding: 12px 16px !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            box-shadow: 0 8px 22px rgba(0,0,0,0.28) !important;
            backdrop-filter: blur(8px) !important;
            transition: all 0.15s ease;
            font-size: 0.95rem !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover,
        [data-testid="stSidebar"] .stDownloadButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.35) !important;
            background: linear-gradient(180deg, rgba(255,255,255,0.12), rgba(255,255,255,0.06)) !important;
        }

        /* ========== CHAT INPUT STYLING ========== */
        .stChatInputContainer {
            border-radius: 16px !important;
            padding: 12px !important;
            background: rgba(255,255,255,0.95) !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.18) !important;
            border: 2px solid rgba(255,255,255,0.08) !important;
        }

        .stChatInput input {
            border-radius: 10px !important;
            padding: 12px !important;
            background: rgba(255,255,255,0.9) !important;
            border: 1px solid rgba(0,0,0,0.08) !important;
            color: #111 !important;
            font-size: 1rem !important;
        }

        .stChatInput input::placeholder {
            color: rgba(0,0,0,0.45) !important;
        }

        /* ========== METRICS STYLING ========== */
        [data-testid="stSidebar"] .stMetric {
            background: rgba(255,255,255,0.05) !important;
            padding: 12px !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
        }

        [data-testid="stSidebar"] .stMetric label {
            color: rgba(255,255,255,0.85) !important;
            font-weight: 600 !important;
        }

        [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
            color: white !important;
            font-weight: 700 !important;
        }

        /* ========== SPACING ========== */
        [data-testid="stSidebar"] > div:first-child {
            padding-bottom: 120px !important;
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================
# SECTION 4: APPLY ALL STYLING
# ============================================

# Create images directory if it doesn't exist
image_dir = "images"
if not os.path.exists(image_dir):
    os.makedirs(image_dir, exist_ok=True)

# Apply all styling functions
apply_main_background(os.path.join(image_dir, "chatbot_bg.jpg"), visibility_alpha=0.28)
apply_sidebar_styling(os.path.join(image_dir, "sidebar_bg.jpg"), overlay_alpha=0.20, radius=18)
apply_global_styles()

# ============================================
# SECTION 5: TITLE & HEADER
# ============================================

st.markdown('<div style="position:relative; z-index:9999;">', unsafe_allow_html=True)
st.title("🤖 Multi-Provider AI Chatbot")
st.markdown(
    "<p style='text-align:center; color: rgba(255,255,255,0.92); margin-top:-8px;'>"
    "Support for OpenAI, Gemini, Groq & Ollama | Created by Samrat Roychoudhury"
    "</p>",
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SECTION 6: SESSION STATE INITIALIZATION
# ============================================

# Initialize chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize provider selection if it doesn't exist
if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = "Groq"  # Default provider

# ============================================
# SECTION 7: SIDEBAR CONFIGURATION
# ============================================

with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # STEP 1: Provider Selection
    selected_provider = st.selectbox(
        "AI Provider",
        options=list(PROVIDER_CONFIG.keys()),
        index=list(PROVIDER_CONFIG.keys()).index(st.session_state.selected_provider),
        help="Choose your AI provider",
        key=f"provider_{st.session_state.get('provider_key', 0)}"
    )

    # Update session state if provider changed
    if selected_provider != st.session_state.selected_provider:
        st.session_state.selected_provider = selected_provider
        st.session_state.selected_model = PROVIDER_CONFIG[selected_provider]["models"][0]
        st.rerun()

    # STEP 2: Model Selection (dynamic based on provider)
    available_models = PROVIDER_CONFIG[selected_provider]["models"]
    current_model = st.session_state.get('selected_model', available_models[0])
    model_index = available_models.index(current_model) if current_model in available_models else 0

    selected_model = st.selectbox(
        "Model",
        options=available_models,
        index=model_index,
        help=f"Model from {selected_provider}",
        key=f"model_{st.session_state.get('model_key', 0)}"
    )

    # Update session state with selected model
    if selected_model != st.session_state.get('selected_model'):
        st.session_state.selected_model = selected_model
        st.rerun()

    st.markdown("---")
    st.markdown("### 🎛️ Generation Parameters")

    # Temperature control
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness: 0 is focused, 1 is creative"
    )

    # Max tokens control
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=4096,
        value=1024,
        step=100,
        help="Maximum length of the response"
    )

    st.markdown("---")

    # Chat Statistics
    if st.session_state.chat_history:
        st.markdown("### 🔎 Chat Statistics")
        user_msgs = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        assistant_msgs = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])

        col1, col2 = st.columns(2)
        with col1:
            st.metric("User", user_msgs)
        with col2:
            st.metric("AI", assistant_msgs)

        st.metric("Total Messages", len(st.session_state.chat_history))

    st.markdown("---")
    st.markdown("### 🔗 Actions")

    # Clear chat button
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        components.html("<script>window.location.reload()</script>", height=0)

    # Export chat button
    if st.session_state.chat_history:
        chat_text = "\n\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in st.session_state.chat_history
        ])
        st.download_button(
            label="⬇ Export Chat",
            data=chat_text,
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.button("⬇ Export Chat", disabled=True, use_container_width=True)

# ============================================
# SECTION 8: CHAT INTERFACE
# ============================================

# Display chat history
chat_container = st.container()
with chat_container:
    if not st.session_state.chat_history:
        st.info(f"👋 Hello! I'm powered by **{selected_provider} - {selected_model}**. How can I help you today?")

    for message in st.session_state.chat_history:
        role = message.get("role", "assistant")
        avatar = "🤵🏻" if role == "user" else "🛸"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

# ============================================
# SECTION 9: MESSAGE HANDLING
# ============================================

# Chat input
user_prompt = st.chat_input("Type your message here...", key="chat_input")

if user_prompt:
    # Display user message
    with st.chat_message("user", avatar="🤵🏻"):
        st.markdown(user_prompt)

    # Add to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Generate AI response
    with st.chat_message("assistant", avatar="🛸"):
        placeholder = st.empty()
        full_response = ""

        try:
            # Get LLM instance
            llm = get_llm_instance(selected_provider, selected_model, temperature, max_tokens)

            if llm:
                # Prepare messages for the LLM
                messages = [
                    {"role": "system",
                     "content": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and engaging responses."},
                    *st.session_state.chat_history
                ]

                # Stream the response
                for chunk in llm.stream(input=messages):
                    part = getattr(chunk, "content", str(chunk))
                    full_response += part
                    placeholder.markdown(full_response + "▌")

                # Final response
                placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            else:
                placeholder.error("⚠️ Failed to initialize the language model. Please check your configuration.")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            st.info("💡 Please check your API key and internet connection.")

# ============================================
# SECTION 10: FOOTER
# ============================================

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color: rgba(255,255,255,0.92); font-size:0.9rem; padding: 12px;'>"
    "💡 <strong>Tips:</strong> Use the sidebar to switch providers and models • Export your conversations anytime<br>"
    "<em>Supports OpenAI, Google Gemini, Groq, and Ollama</em>"
    "</div>",
    unsafe_allow_html=True

)


