import streamlit as st
import os
import pdfplumber
import tempfile
import asyncio
import sys
import nest_asyncio

# Fix for event loop issues in Streamlit
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Allow nested event loops (fixes the main issue)
nest_asyncio.apply()

# Import for Groq and HuggingFace
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.documents import Document
import time

# Direct Groq API Key (Replace with your actual Groq API Key)
GROQ_API_KEY = "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"  # Replace with your actual Groq API Key

if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_xxxxxxx"):
    st.error("❌ No valid GROQ_API_KEY found. Please replace the placeholder API key with your actual key.")
    st.stop()  # Stop the app if no API key is found

# Page configuration
st.set_page_config(
    page_title="Satyukt Virtual Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for agriculture theme
st.markdown(
    """
    <style>
    /* Main app styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }

    /* Welcome box styling */
    .welcome-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        text-align: center;
        color: white;
    }

    .logo-title {
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    .welcome-subtitle {
        font-size: 1.2em;
        margin-bottom: 20px;
        opacity: 0.9;
    }

    .feature-grid {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
        flex-wrap: wrap;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        min-width: 150px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .feature-emoji {
        font-size: 2em;
        margin-bottom: 10px;
    }

    .feature-text {
        font-size: 0.9em;
        font-weight: 500;
    }

    /* Chat interface styling */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        max-height: 500px;
        overflow-y: auto;
    }

    .user-message {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 15px;
        border-radius: 18px 18px 5px 18px;
        margin: 10px 0;
        margin-left: 50px;
        box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
    }

    .bot-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #333;
        padding: 15px;
        border-radius: 18px 18px 18px 5px;
        margin: 10px 0;
        margin-right: 50px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #4CAF50;
    }

    .message-label {
        font-weight: 600;
        font-size: 0.9em;
        margin-bottom: 5px;
    }

    .user-label {
        color: #2E7D32;
        text-align: right;
        margin-right: 50px;
    }

    .bot-label {
        color: #1976D2;
        margin-left: 50px;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #4CAF50;
        padding: 12px 20px;
        font-size: 16px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #45a049;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #45a049 0%, #4CAF50 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }

    /* Selectbox styling */
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #4CAF50;
        padding: 8px 12px;
    }

    /* Spinner styling */
    .thinking-spinner {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 15px;
        margin: 10px 0;
    }

    .spinner-text {
        margin-left: 10px;
        color: #4CAF50;
        font-weight: 600;
    }

     /* Sidebar styling */
     .css-1d391kg {
         background: linear-gradient(180deg, #4CAF50 0%, #2E7D32 100%);
     }

    .css-1d391kg .css-1v0mbdj {
        color: green;
    }

    /* Hide streamlit menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Language selector */
    .language-selector {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }

    .language-label {
        color: red;
        font-weight: 600;
        margin-bottom: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for language selection
with st.sidebar:
    st.markdown('<div class="language-selector">', unsafe_allow_html=True)
    st.markdown('<div class="language-label">🌍 Select Language / भाषा चुनें</div>', unsafe_allow_html=True)

    languages = [
        "English", "हिंदी", "ಕನ್ನಡ", "தமிழ்", "తెలుగు", "বাংলা", "मराठी", "ગુજરાતી", "ਪੰਜਾਬੀ"
    ]
    selected_lang = st.selectbox("Select Language", languages, key="language_selector")

    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar info
    st.markdown("---")
    st.markdown("### 🌾 About Satyukt 🌾")
    st.markdown("**Virtual Assistant** powered by AI and Satellite Intelligence")
    st.markdown("**Services:**")
    st.markdown("- 🛰️ Crop Monitoring")
    st.markdown("- 📊 Risk Analytics")
    st.markdown("- 💰 Insurance Claims")
    st.markdown("- 🏦 Agricultural Credit")

    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("📧 contact@satyukt.com")
    st.markdown("📱 +91 8970095700")

# Main welcome container
st.markdown(
    """
    <div class="welcome-container">
        <div class="logo-title">🌾 Satyukt Virtual Assistant🌾</div>
        <div class="welcome-subtitle">Empowering Agriculture with Satellite Intelligence & AI Technology</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Feature cards section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div style="background: rgba(76, 175, 80, 0.1); padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
            <div style="font-size: 2em; margin-bottom: 10px;">🛰️</div>
            <div style="font-weight: 600;">Satellite Monitoring</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="background: rgba(33, 150, 243, 0.1); padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
            <div style="font-size: 2em; margin-bottom: 10px;">📊</div>
            <div style="font-weight: 600;">Risk Analysis</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style="background: rgba(255, 152, 0, 0.1); padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
            <div style="font-size: 2em; margin-bottom: 10px;">🤖</div>
            <div style="font-weight: 600;">AI Assistant</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div style="background: rgba(139, 195, 74, 0.1); padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
            <div style="font-size: 2em; margin-bottom: 10px;">🌾</div>
            <div style="font-weight: 600;">Crop Insights</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Dictionary for contact messages in different languages
contact_messages = {
    "English": "🤝 Let me connect you with our agricultural experts! Please contact contact@satyukt.com or call +91 8970095700 for specialized assistance.",
    "हिंदी": "🤝 मैं आपको हमारे कृषि विशेषज्ञों से जोड़ता हूँ! विशेष सहायता के लिए कृपया contact@satyukt.com पर संपर्क करें या +91 8970095700 पर कॉल करें।",
    "ಕನ್ನಡ": "🤝 ನಮ್ಮ ಕೃಷಿ ತಜ್ಞರೊಂದಿಗೆ ನಿಮ್ಮನ್ನು ಸಂಪರ್ಕಿಸುತ್ತೇನೆ! ವಿಶೇಷ ಸಹಾಯಕ್ಕಾಗಿ contact@satyukt.com ಗೆ ಸಂಪರ್ಕಿಸಿ ಅಥವಾ +91 8970095700 ಗೆ ಕರೆ ಮಾಡಿ.",
    "தமிழ்": "🤝 எங்கள் விவசாய நிபுணர்களுடன் உங்களை இணைக்கிறேன்! சிறப்பு உதவிக்கு contact@satyukt.com ஐ தொடர்பு கொள்ளவும் அல்லது +91 8970095700 ஐ அழைக்கவும்.",
    "తెలుగు": "🤝 మా వ్యవసాయ నిపుణులతో మిమ్మల్ని కనెక్ట్ చేస్తాను! ప్రత్యేక సహాయం కోసం దయచేసి contact@satyukt.com ని సంప్రదించండి లేదా +91 8970095700 కు కాల్ చేయండి.",
    "বাংলা": "🤝 আমি আপনাকে আমাদের কৃষি বিশেষজ্ঞদের সাথে সংযুক্ত করব! বিশেষ সহায়তার জন্য অনুগ্রহ করে contact@satyukt.com এ যোগাযোগ করুন অথবা +91 8970095700 নম্বরে কল করুন।",
    "मराठी": "🤝 मी तुम्हाला आमच्या कृषी तज्ञांशी जोडतो! विशेष मदतीसाठी कृपया contact@satyukt.com वर संपर्क साधा किंवा +91 8970095700 वर कॉल करा.",
    "ગુજરાતી": "🤝 હું તમને અમારા કૃષિ નિષ્ણાતો સાથે જોડું છું! વિશેષ સહાયતા માટે કૃપા કરીને contact@satyukt.com નો સંપર્ક કરો અથવા +91 8970095700 પર કૉલ કરો.",
    "ਪੰਜਾਬੀ": "🤝 ਮੈਂ ਤੁਹਾਨੂੰ ਸਾਡੇ ਖੇਤੀਬਾੜੀ ਮਾਹਿਰਾਂ ਨਾਲ ਜੋੜਦਾ ਹਾਂ! ਵਿਸ਼ੇਸ਼ ਸਹਾਇਤਾ ਲਈ ਕਿਰਪਾ ਕਰਕੇ contact@satyukt.com 'ਤੇ ਸੰਪਰਕ ਕਰੋ ਜਾਂ +91 8970095700 'ਤੇ ਕਾਲ ਕਰੋ।"
}

# Enhanced prompt template with language support
prompt = ChatPromptTemplate.from_template(
    f"""
You are a helpful, multilingual AI assistant specializing in agriculture. Answer questions using only the information provided in the PDF context below.

- Respond in {selected_lang} language.
- Keep replies short, human-like, and helpful.
- If the answer is partially available, share only what's known — no guessing.
- If the answer is missing, reply in the user's language with the following contact message:
  "{contact_messages.get(selected_lang, contact_messages['English'])}"
- Do not say phrases like "according to the context" or "not found in the PDF".
- Focus on agriculture-related guidance and support.

    <context>
    {{context}}
    </context>
    Question: {{input}}
    """
)

# Initialize session state for caching
if "llm_initialized" not in st.session_state:
    st.session_state.llm_initialized = False
    
if "embeddings_initialized" not in st.session_state:
    st.session_state.embeddings_initialized = False

# Function to safely initialize LLM with error handling
# Function to safely initialize LLM with error handling
def get_llm():
    if not st.session_state.llm_initialized:
        try:
            st.session_state.llm = ChatGroq(
                model="llama3-70b-8192",  # <-- Replaced with a current model
                api_key=GROQ_API_KEY,
                temperature=0.7,
                max_tokens=1000
            )
            st.session_state.llm_initialized = True
        except Exception as e:
            st.error(f"Error initializing Groq LLM: {e}")
            return None
    return st.session_state.llm if st.session_state.llm_initialized else None

# Function to initialize embeddings - COMPLETELY OFFLINE
def get_embeddings():
    if not st.session_state.embeddings_initialized:
        try:
            with st.spinner("📥 Loading embedding model (first time only)..."):
                st.session_state.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
                st.session_state.embeddings_initialized = True
        except Exception as e:
            st.error(f"Error initializing HuggingFace embeddings: {e}")
            return None
    
    return st.session_state.embeddings if st.session_state.embeddings_initialized else None

def is_out_of_context(answer, current_selected_lang):
    # This function checks if the answer matches the pre-defined contact message
    # or contains keywords indicating out-of-context response.
    contact_message_template = contact_messages.get(current_selected_lang, contact_messages['English']).lower()

    # Check for direct match (case-insensitive)
    if answer.strip().lower() == contact_message_template:
        return True

    # Check for common "out of context" phrases/keywords
    keywords = [
        "i'm sorry", "i don't know", "not sure", "out of context",
        "invalid", "no mention", "cannot", "unable", "not available",
        "जानकारी उपलब्ध नहीं", "मुझे नहीं पता", "संदर्भ में नहीं",  # Hindi examples
        "ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ", "ನನಗೆ ಗೊತ್ತಿಲ್ಲ",  # Kannada examples
        "தகவல் இல்லை", "எனக்குத் தெரியாது",  # Tamil examples
    ]
    return any(k in answer.lower() for k in keywords)

def extract_text_with_pdfplumber(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_page_text = page.extract_text()
                if extracted_page_text:
                    text += extracted_page_text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""
    return text

def initialize_vector_db(pdf_file):
    # Only initialize if vector_store is not already in session_state
    if "vector_store" not in st.session_state:
        try:
            loading_placeholder = st.empty()
            loading_placeholder.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: center; padding: 20px; background: #f8f9fa; border-radius: 15px; margin: 10px 0;">
                    <div style="font-size: 24px; margin-right: 10px;">🤖</div>
                    <div style="color: #4CAF50; font-weight: 600;">Initializing Satyukt Assistant... Please wait</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Save the uploaded PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_file.read())
                pdf_path = temp_file.name

            # Extract text from the temporary PDF
            text_data = extract_text_with_pdfplumber(pdf_path)

            # Remove the temporary file after extraction
            os.unlink(pdf_path)

            if not text_data.strip():
                st.error("📄 PDF appears empty or unreadable after extraction.")
                loading_placeholder.empty()
                return False

            # Create a Document object from the extracted text
            doc = Document(page_content=text_data)

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
            chunks = text_splitter.split_documents([doc])

            # Initialize HuggingFace Embeddings (completely offline)
            embeddings = get_embeddings()
            if embeddings is None:
                loading_placeholder.empty()
                return False

            # Create the vector store from the document chunks and embeddings
            st.session_state.vector_store = DocArrayInMemorySearch.from_documents(
                chunks, embeddings
            )

            loading_placeholder.empty()  # Clear the loading message
            return True

        except Exception as e:
            st.error(f"❌ Error initializing assistant: {str(e)}")
            if loading_placeholder:
                loading_placeholder.empty()
            return False
    return True  # Already initialized

# Initialize the Groq LLM
llm = get_llm()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize message sent flag
if "message_sent" not in st.session_state:
    st.session_state.message_sent = False

# Auto-load PDF for RAG context
default_pdf_path = "SatyuktQueries.pdf"
if os.path.exists(default_pdf_path):
    class DummyFile:
        def __init__(self, path):
            self.path = path

        def read(self):
            with open(self.path, "rb") as f:
                return f.read()

    pdf_input_from_user = DummyFile(default_pdf_path)

    if initialize_vector_db(pdf_input_from_user):
        if "initial_greeting_shown" not in st.session_state:
            st.success(
                "✅ Hi there! 👋 Satyukt Virtual Assistant is ready to assist you! Ask me anything about agriculture, farming, or our services.")
            st.session_state.initial_greeting_shown = True
    else:
        st.error(f"❌ Could not initialize assistant with '{default_pdf_path}'. Check PDF content.")
else:
    st.error(
        f"❌ PDF file '{default_pdf_path}' not found in the project directory. Please ensure it's in the same directory as your Streamlit app.")

# Enhanced Chat Interface
if "vector_store" in st.session_state and llm:
    st.markdown("### 💬 Chat with Satyukt Virtual Assistant")

    # Display chat history with enhanced styling
    chat_container_key = f"chat_container_{len(st.session_state.chat_history)}"
    st.markdown(f'<div class="chat-container" id="{chat_container_key}">', unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f'<div class="message-label user-label">🧑‍🌾 You</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-label bot-label">🤖 Satyukt</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bot-message">{msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # JavaScript to scroll chat container to bottom
    st.markdown(
        f"""
        <script>
            var chatContainer = document.getElementById('{chat_container_key}');
            if (chatContainer) {{
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }}
        </script>
        """,
        unsafe_allow_html=True
    )

    # Input section with form for Enter key support
    st.markdown("### Ask your question:")

    # Create a form to handle Enter key submission
    with st.form(key='chat_form', clear_on_submit=True):
        user_prompt = st.text_input(
            "Type your question here...",
            placeholder=f"Ask me anything in {selected_lang}... 🌾",
            key="user_input_form"
        )

        # Form submit button (this handles Enter key)
        submitted = st.form_submit_button("Send 🚀")

        # Handle form submission (Enter key or button click)
        if submitted and user_prompt:
            if user_prompt.strip():
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_prompt})

                # Show thinking animation
                with st.spinner("🤔 Satyukt is thinking..."):
                    try:
                        # Create the document chain
                        document_chain = create_stuff_documents_chain(llm, prompt)

                        # Create retriever from the vector store
                        retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})

                        # Create the retrieval chain
                        retrieval_chain = create_retrieval_chain(retriever, document_chain)

                        # Invoke the retrieval chain with the user's prompt
                        response = retrieval_chain.invoke({'input': user_prompt})
                        answer = response['answer']

                        # Check for out-of-context response
                        if is_out_of_context(answer, selected_lang):
                            answer = contact_messages.get(selected_lang, contact_messages['English'])

                        # Add AI response to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})

                    except Exception as e:
                        error_msg = f"🔧 Sorry, I encountered a technical issue: {e}. Please try again or contact our support team."
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

                    # Refresh the app to show new messages
                    st.rerun()

            else:
                st.warning("⚠️ Please enter a question before sending.")

        elif submitted and not user_prompt:
            st.warning("⚠️ Please enter a question before sending.")

else:
    st.info("🔄 Initializing Satyukt Virtual Assistant... Please wait a moment.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🌾 <strong>Satyukt AI - Smart Farming Assistant</strong> | Powered by Satellite Intelligence & AI</p>
        <p>Serving Farmers, Agri-banks, Insurers & Governments across India 🇮🇳</p>
    </div>
    """,
    unsafe_allow_html=True
)

