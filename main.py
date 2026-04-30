import os
import streamlit as st
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# ==========================================
API_KEY = st.secrets.get(
    "ELEVENLABS_API_KEY",
    os.getenv("ELEVENLABS_API_KEY")
)
# ==========================================
# SAFETY CHECK
# ==========================================

if not API_KEY:
    st.error("❌ Missing ElevenLabs API Key")
    st.info("Add ELEVENLABS_API_KEY in Streamlit Secrets or local .env file.")
    st.stop()

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================

st.set_page_config(
    page_title="VoiceBooker | TTS Engine",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3rem;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #0052a3;
        border-color: #0052a3;
    }

    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E1E1E;
        margin-bottom: -15px;
    }

    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("### ⚙️ System Status")

    if API_KEY:
        st.success("🟢 API Key Loaded")
    else:
        st.error("🔴 API Key Missing")

    st.markdown("---")

    st.markdown("### About VoiceBooker")

    st.write(
        """
        This testing module validates the 
        **ElevenLabs Voice Synthesis** layer 
        before integrating into the main 
        LangGraph & Twilio orchestration loop.
        """
    )

    st.markdown("---")

    st.caption("Engine: `eleven_multilingual_v2`")
    st.caption("Format: `mp3_44100_128`")

# ==========================================
# MAIN INTERFACE
# ==========================================

st.markdown(
    '<p class="main-header">🎙️ VoiceBooker Synthesis Engine</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-header">Professional Text-to-Speech Generation Testing Environment</p>',
    unsafe_allow_html=True
)

# ==========================================
# AVAILABLE VOICES
# ==========================================

AVAILABLE_VOICES = {
    "George (British, Warm, Professional)": "JBFqnCBsd6RMkjVDRZzb",
    "Rachel (American, Calm, Conversational)": "21m00Tcm4TlvDq8ikWAM",
    "Drew (American, News, Authoritative)": "29vD33N1CtxCmqQRPOHJ",
    "Clyde (American, Deep, Friendly)": "2EiwWnXFnvU5JabPnv8n",
    "Callum (Transatlantic, Intense, Direct)": "N2lVS1w4EtoT3dr4eOWO"
}

# ==========================================
# LAYOUT
# ==========================================

col1, col2 = st.columns([1.2, 1], gap="large")

# ==========================================
# LEFT PANEL
# ==========================================

with col1:

    st.markdown("### 🗣️ Voice Configuration")

    selected_voice_name = st.selectbox(
        "Select Agent Voice Profile",
        list(AVAILABLE_VOICES.keys()),
        help="Choose the voice persona for your AI booking agent."
    )

    selected_voice_id = AVAILABLE_VOICES[selected_voice_name]

    st.markdown("### 📝 Script")

    text_to_speak = st.text_area(
        "Enter the text you want the agent to synthesize:",
        "Hello! Welcome to our booking system. How can I help you schedule your venue today?",
        height=180
    )

    generate_btn = st.button(
        "🚀 Generate Audio",
        use_container_width=True
    )

# ==========================================
# RIGHT PANEL
# ==========================================

with col2:

    st.markdown("### 🎧 Audio Output")

    if not generate_btn:
        st.info(
            "👈 Configure your voice profile and script on the left, then click Generate Audio."
        )

    if generate_btn:

        if not text_to_speak.strip():
            st.warning("⚠️ Please enter some text.")
        else:
            try:

                with st.spinner("⏳ Connecting to ElevenLabs Neural Engine..."):

                    client = ElevenLabs(api_key=API_KEY)

                    audio_generator = client.text_to_speech.convert(
                        text=text_to_speak,
                        voice_id=selected_voice_id,
                        model_id="eleven_multilingual_v2",
                        output_format="mp3_44100_128",
                    )

                    # Convert stream generator into bytes
                    audio_bytes = b"".join(audio_generator)

                st.success("✅ Synthesis Complete!")

                # Audio player
                st.audio(audio_bytes, format="audio/mp3")

                # Download button
                st.download_button(
                    label="⬇️ Download MP3",
                    data=audio_bytes,
                    file_name=f"VoiceBooker_{selected_voice_id}.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

            except Exception as e:
                st.error("❌ Synthesis Failed")
                st.error(f"Details: {str(e)}")
