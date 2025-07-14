# import streamlit as st
# import os
# import pdfplumber
# import tempfile
# import random
# # Import for Google Gemini
# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain
# from langchain_community.vectorstores import DocArrayInMemorySearch
# from langchain_core.documents import Document
# from dotenv import load_dotenv
# import time


# load_dotenv()

# # Page configuration
# st.set_page_config(
#     page_title="Satyukt Virtual Assistant",
#     page_icon="🌾",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )


# google_api_keys = [
#     os.getenv("GOOGLE_API_KEY_1"),
#     os.getenv("GOOGLE_API_KEY_2"),
#     os.getenv("GOOGLE_API_KEY_3"),
#     os.getenv("GOOGLE_API_KEY_4")
# ]
# # Filter out any None values (in case some keys are not set)
# google_api_keys = [key for key in google_api_keys if key]

# if not google_api_keys:
#     st.error("❌ No valid GOOGLE_API_KEYs found. Please set at least one in your .env file.")
#     st.stop()  # Stop the app if no API keys are found

# # Custom CSS for agriculture theme
# st.markdown(
#     """
#     <style>
#     /* Main app styling */
#     .main {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         font-family: 'Segoe UI', 'Roboto', sans-serif;
#     }

#     /* Welcome box styling */
#     .welcome-container {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         border-radius: 20px;
#         padding: 30px;
#         margin: 20px 0;
#         box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
#         text-align: center;
#         color: white;
#     }

#     .logo-title {
#         font-size: 2.5em;
#         font-weight: 700;
#         margin-bottom: 10px;
#         text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
#     }

#     .welcome-subtitle {
#         font-size: 1.2em;
#         margin-bottom: 20px;
#         opacity: 0.9;
#     }

#     .feature-grid {
#         display: flex;
#         justify-content: space-around;
#         margin-top: 20px;
#         flex-wrap: wrap;
#     }

#     .feature-card {
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 15px;
#         padding: 15px;
#         margin: 10px;
#         min-width: 150px;
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(255, 255, 255, 0.2);
#     }

#     .feature-emoji {
#         font-size: 2em;
#         margin-bottom: 10px;
#     }

#     .feature-text {
#         font-size: 0.9em;
#         font-weight: 500;
#     }

#     /* Chat interface styling */
#     .chat-container {
#         background: white;
#         border-radius: 15px;
#         padding: 20px;
#         margin: 20px 0;
#         box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
#         max-height: 500px;
#         overflow-y: auto;
#     }

#     .user-message {
#         background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
#         color: white;
#         padding: 15px;
#         border-radius: 18px 18px 5px 18px;
#         margin: 10px 0;
#         margin-left: 50px;
#         box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
#     }

#     .bot-message {
#         background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
#         color: #333;
#         padding: 15px;
#         border-radius: 18px 18px 18px 5px;
#         margin: 10px 0;
#         margin-right: 50px;
#         box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
#         border-left: 4px solid #4CAF50;
#     }

#     .message-label {
#         font-weight: 600;
#         font-size: 0.9em;
#         margin-bottom: 5px;
#     }

#     .user-label {
#         color: #2E7D32;
#         text-align: right;
#         margin-right: 50px;
#     }

#     .bot-label {
#         color: #1976D2;
#         margin-left: 50px;
#     }

#     /* Input styling */
#     .stTextInput > div > div > input {
#         border-radius: 25px;
#         border: 2px solid #4CAF50;
#         padding: 12px 20px;
#         font-size: 16px;
#     }

#     .stTextInput > div > div > input:focus {
#         border-color: #45a049;
#         box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
#     }

#     /* Button styling */
#     .stButton > button {
#         background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
#         color: white;
#         border: none;
#         border-radius: 25px;
#         padding: 12px 30px;
#         font-size: 16px;
#         font-weight: 600;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
#     }

#     .stButton > button:hover {
#         background: linear-gradient(135deg, #45a049 0%, #4CAF50 100%);
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
#     }

#     /* Selectbox styling */
#     .stSelectbox > div > div > select {
#         border-radius: 10px;
#         border: 2px solid #4CAF50;
#         padding: 8px 12px;
#     }

#     /* Spinner styling */
#     .thinking-spinner {
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         padding: 20px;
#         background: #f8f9fa;
#         border-radius: 15px;
#         margin: 10px 0;
#     }

#     .spinner-text {
#         margin-left: 10px;
#         color: #4CAF50;
#         font-weight: 600;
#     }

#      /* Sidebar styling */
#      .css-1d391kg {
#          background: linear-gradient(180deg, #4CAF50 0%, #2E7D32 100%);
#      }

#     .css-1d391kg .css-1v0mbdj {
#         color: green;
#     }

#     /* Hide streamlit menu */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}

#     /* Language selector */
#     .language-selector {
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 10px;
#         padding: 10px;
#         margin: 10px 0;
#     }

#     .language-label {
#         color: red;
#         font-weight: 600;
#         margin-bottom: 5px;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Sidebar for language selection
# with st.sidebar:
#     st.markdown('<div class="language-selector">', unsafe_allow_html=True)
#     st.markdown('<div class="language-label">🌍 Select Language / भाषा चुनें</div>', unsafe_allow_html=True)

#     languages = [
#         "English", "हिंदी", "ಕನ್ನಡ", "தமிழ்", "తెలుగు", "বাংলা", "मराठी", "ગુજરાતી", "ਪੰਜਾਬੀ"
#     ]
#     selected_lang = st.selectbox("Select Language", languages, key="language_selector")

#     st.markdown('</div>', unsafe_allow_html=True)

#     # Sidebar info
#     st.markdown("---")
#     st.markdown("### 🌾 About Satyukt 🌾")
#     st.markdown("**Virtual Assistant** powered by AI and Satellite Intelligence")
#     st.markdown("**Services:**")
#     st.markdown("- 🛰️ Crop Monitoring")
#     st.markdown("- 📊 Risk Analytics")
#     st.markdown("- 💰 Insurance Claims")
#     st.markdown("- 🏦 Agricultural Credit")

#     st.markdown("---")
#     st.markdown("### 📞 Contact")
#     st.markdown("📧 contact@satyukt.com")
#     st.markdown("📱 +91‑8970095700")

# # Main welcome container
# st.markdown(
#     """
#     <div class="welcome-container">
#         <div class="logo-title">🌾 Satyukt Virtual Assistant🌾</div>
#         <div class="welcome-subtitle">Empowering Agriculture with Satellite Intelligence & AI Technology</div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# # Feature cards section
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.markdown(
#         """
#         <div style="background: rgba(76, 175, 80, 0.1); padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
#             <div style="font-size: 2em; margin-bottom: 10px;">🛰️</div>
#             <div style="font-weight: 600;">Satellite Monitoring</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# with col2:
#     st.markdown(
#         """
#         <div style="background: rgba(33, 150, 243, 0.1); padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
#             <div style="font-size: 2em; margin-bottom: 10px;">📊</div>
#             <div style="font-weight: 600;">Risk Analysis</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# with col3:
#     st.markdown(
#         """
#         <div style="background: rgba(255, 152, 0, 0.1); padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
#             <div style="font-size: 2em; margin-bottom: 10px;">🤖</div>
#             <div style="font-weight: 600;">AI Assistant</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# with col4:
#     st.markdown(
#         """
#         <div style="background: rgba(139, 195, 74, 0.1); padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
#             <div style="font-size: 2em; margin-bottom: 10px;">🌾</div>
#             <div style="font-weight: 600;">Crop Insights</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# # Dictionary for contact messages in different languages
# contact_messages = {
#     "English": "🤝 Let me connect you with our agricultural experts! Please contact contact@satyukt.com or call 8970700045 | 7019992797 for specialized assistance.",
#     "हिंदी": "🤝 मैं आपको हमारे कृषि विशेषज्ञों से जोड़ता हूँ! विशेष सहायता के लिए कृपया contact@satyukt.com पर संपर्क करें या 8970700045 | 7019992797 पर कॉल करें।",
#     "ಕನ್ನಡ": "🤝 ನಮ್ಮ ಕೃಷಿ ತಜ್ಞರೊಂದಿಗೆ ನಿಮ್ಮನ್ನು ಸಂಪರ್ಕಿಸುತ್ತೇನೆ! ವಿಶೇಷ ಸಹಾಯಕ್ಕಾಗಿ contact@satyukt.com ಗೆ ಸಂಪರ್ಕಿಸಿ ಅಥವಾ 8970700045 | 7019992797 ಗೆ ಕರೆ ಮಾಡಿ.",
#     "தமிழ்": "🤝 எங்கள் விவசாய நிபுணர்களுடன் உங்களை இணைக்கிறேன்! சிறப்பு உதவிக்கு contact@satyukt.com ஐ தொடர்பு கொள்ளவும் அல்லது 8970700045 | 7019992797 ஐ அழைக்கவும்.",
#     "తెలుగు": "🤝 మా వ్యవసాయ నిపుణులతో మిమ్మల్ని కనెక్ట్ చేస్తాను! ప్రత్యేక సహాయం కోసం దయచేసి contact@satyukt.com ని సంప్రదించండి లేదా 8970700045 | 7019992797 కు కాల్ చేయండి.",
#     "বাংলা": "🤝 আমি আপনাকে আমাদের কৃষি বিশ৻জ্ঞদের সাথে সংযুক্ত করব! বিশেষ সহায়তার জন্য অনুগ্রহ করে contact@satyukt.com এ যোগাযোগ করুন অথবা 8970700045 | 7019992797 নম্বরে কল করুন।",
#     "मराठी": "🤝 मी तुम्हाला आमच्या कृषी तज्ञांशी जोडतो! विशेष मदतीसाठी कृपया contact@satyukt.com वर संपर्क साधा किंवा 8970700045 | 7019992797 वर कॉल करा.",
#     "ગુજરાતી": "🤝 હું તમને અમારા કૃષિ નિષ્ણાતો સાથે જોડું છું! વિશેષ સહાયતા માટે કૃપા કરીને contact@satyukt.com નો સંપર્ક કરો અથવા 8970700045 | 7019992797 પર કૉલ કરો.",
#     "ਪੰਜਾਬੀ": "🤝 ਮੈਂ ਤੁਹਾਨੂੰ ਸਾਡੇ ਖੇਤੀਬਾੜੀ ਮਾਹਿਰਾਂ ਨਾਲ ਜੋੜਦਾ ਹਾਂ! ਵਿਸ਼ੇਸ਼ ਸਹਾਇਤਾ ਲਈ ਕਿਰਪਾ ਕਰਕੇ contact@satyukt.com 'ਤੇ ਸੰਪਰਕ ਕਰੋ ਜਾਂ 8970700045 | 7019992797 'ਤੇ ਕਾਲ ਕਰੋ।"
# }

# # Enhanced prompt template with language support
# prompt = ChatPromptTemplate.from_template(
#     f"""
# You are a helpful, multilingual AI assistant specializing in agriculture. Answer questions using only the information provided in the PDF context below.

# - Respond in {selected_lang} language.
# - Keep replies short, human-like, and helpful.
# - If the answer is partially available, share only what's known — no guessing.
# - If the answer is missing, reply in the user's language with the following contact message:
#   "{contact_messages.get(selected_lang, contact_messages['English'])}"
# - Do not say phrases like "according to the context" or "not found in the PDF".
# - Focus on agriculture-related guidance and support.

#     <context>
#     {{context}}
#     </context>
#     Question: {{input}}
#     """
# )

# # Initialize the Gemini LLM for chat/generation with a random API key
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=random.choice(google_api_keys))

# def is_out_of_context(answer, current_selected_lang):
#     # This function checks if the answer matches the pre-defined contact message
#     # or contains keywords indicating out-of-context response.
#     contact_message_template = contact_messages.get(current_selected_lang, contact_messages['English']).lower()

#     # Check for direct match (case-insensitive)
#     if answer.strip().lower() == contact_message_template:
#         return True

#     # Check for common "out of context" phrases/keywords
#     keywords = [
#         "i'm sorry", "i don't know", "not sure", "out of context",
#         "invalid", "no mention", "cannot", "unable", "not available",
#         "जानकारी उपलब्ध नहीं", "मुझे नहीं पता", "संदर्भ में नहीं",  # Hindi examples
#         "ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ", "ನನಗೆ ಗೊತ್ತಿಲ್ಲ",  # Kannada examples
#         "தகவல் இல்லை", "எனக்குத் தெரியாது",  # Tamil examples
#     ]
#     return any(k in answer.lower() for k in keywords)

# def extract_text_with_pdfplumber(pdf_path):
#     text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 extracted_page_text = page.extract_text()
#                 if extracted_page_text:
#                     text += extracted_page_text + "\n"
#     except Exception as e:
#         st.error(f"Error extracting text from PDF: {e}")
#         return ""
#     return text

# def initialize_vector_db(pdf_file, api_keys):
#     # Only initialize if vector_store is not already in session_state
#     if "vector_store" not in st.session_state:
#         try:
#             loading_placeholder = st.empty()
#             loading_placeholder.markdown(
#                 """
#                 <div style="display: flex; align-items: center; justify-content: center; padding: 20px; background: #f8f9fa; border-radius: 15px; margin: 10px 0;">
#                     <div style="font-size: 24px; margin-right: 10px;">🤖</div>
#                     <div style="color: #4CAF50; font-weight: 600;">Initializing Satyukt Assistant... Please wait</div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             # Save the uploaded PDF to a temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
#                 temp_file.write(pdf_file.read())
#                 pdf_path = temp_file.name

#             # Extract text from the temporary PDF
#             text_data = extract_text_with_pdfplumber(pdf_path)

#             # Remove the temporary file after extraction
#             os.unlink(pdf_path)

#             if not text_data.strip():
#                 st.error("📄 PDF appears empty or unreadable after extraction.")
#                 loading_placeholder.empty()
#                 return False

#             # Create a Document object from the extracted text
#             doc = Document(page_content=text_data)

#             # Split the document into chunks
#             text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
#             chunks = text_splitter.split_documents([doc])

#             # Initialize Gemini Embeddings with a random API key
#             st.session_state.embeddings = GoogleGenerativeAIEmbeddings(
#                 model="models/embedding-001",
#                 google_api_key=random.choice(api_keys)
#             )

#             # Create the vector store from the document chunks and embeddings
#             st.session_state.vector_store = DocArrayInMemorySearch.from_documents(
#                 chunks, st.session_state.embeddings
#             )

#             loading_placeholder.empty()  # Clear the loading message
#             return True

#         except Exception as e:
#             st.error(f"❌ Error initializing assistant: {str(e)}")
#             loading_placeholder.empty()
#             return False
#     return True  # Already initialized

# # Initialize chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Auto-load PDF for RAG context
# default_pdf_path = "SatyuktQueries.pdf"
# if os.path.exists(default_pdf_path):
#     class DummyFile:  # Create a dummy class to mimic Streamlit's UploadedFile
#         def __init__(self, path):
#             self.path = path

#         def read(self):
#             with open(self.path, "rb") as f:
#                 return f.read()

#     pdf_input_from_user = DummyFile(default_pdf_path)

#     if initialize_vector_db(pdf_input_from_user, google_api_keys):
#         if "initial_greeting_shown" not in st.session_state:
#             st.success(
#                 "✅ Hi there! 👋 Satyukt Virtual Assistant is ready to assist you! Ask me anything about agriculture, farming, or our services.")
#             st.session_state.initial_greeting_shown = True
#     else:
#         st.error(f"❌ Could not initialize assistant with '{default_pdf_path}'. Check PDF content or API keys.")
# else:
#     st.error(
#         f"❌ PDF file '{default_pdf_path}' not found in the project directory. Please ensure it's in the same directory as your Streamlit app.")

# # Enhanced Chat Interface
# if "vector_store" in st.session_state:  # Only show chat if vector store is initialized
#     st.markdown("### 💬 Chat with Satyukt Virtual Assistant")

#     # Display chat history with enhanced styling
#     chat_container_key = f"chat_container_{len(st.session_state.chat_history)}"
#     st.markdown(f'<div class="chat-container" id="{chat_container_key}">', unsafe_allow_html=True)

#     for i, msg in enumerate(st.session_state.chat_history):
#         if msg["role"] == "user":
#             st.markdown(f'<div class="message-label user-label">🧑‍🌾 You</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<div class="message-label bot-label">🤖 Satyukt</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="bot-message">{msg["content"]}</div>', unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

#     # JavaScript to scroll chat container to bottom
#     st.markdown(
#         f"""
#         <script>
#             var chatContainer = document.getElementById('{chat_container_key}');
#             if (chatContainer) {{
#                 chatContainer.scrollTop = chatContainer.scrollHeight;
#             }}
#         </script>
#         """,
#         unsafe_allow_html=True
#     )

#     # Input section
#     st.markdown("### Ask your question:")
#     user_prompt = st.text_input(
#         "Type your question here...",
#         placeholder=f"Ask me anything in {selected_lang}... 🌾",
#         key="user_input"
#     )

#     send_button = st.button("Send 🚀", key="send_btn")

#     # Handle ONLY Send button click
#     if send_button and user_prompt:
#         if user_prompt.strip():
#             # Add user message to chat history
#             st.session_state.chat_history.append({"role": "user", "content": user_prompt})

#             # Show thinking animation
#             with st.spinner("🤔 Satyukt is thinking..."):
#                 try:
#                     # Create the document chain
#                     document_chain = create_stuff_documents_chain(llm, prompt)

#                     # Create retriever from the vector store
#                     retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})

#                     # Create the retrieval chain
#                     retrieval_chain = create_retrieval_chain(retriever, document_chain)

#                     # Invoke the retrieval chain with the user's prompt
#                     response = retrieval_chain.invoke({'input': user_prompt})
#                     answer = response['answer']

#                     # Check for out-of-context response
#                     if is_out_of_context(answer, selected_lang):
#                         answer = contact_messages.get(selected_lang, contact_messages['English'])

#                     # Add AI response to chat history
#                     st.session_state.chat_history.append({"role": "assistant", "content": answer})

#                 except Exception as e:
#                     error_msg = f"🔧 Sorry, I encountered a technical issue: {e}. Please try again or contact our support team."
#                     st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

#                 # Clear input and refresh the app to show new messages
#                 st.rerun()

#         else:
#             st.warning("⚠️ Please enter a question before sending.")

#     elif send_button and not user_prompt:
#         st.warning("⚠️ Please enter a question before sending.")

# else:
#     st.info(
#         "🔄 Initializing Satyukt Virtual Assistant... Please wait a moment.")

# # Footer
# st.markdown("---")
# st.markdown(
#     """
#     <div style="text-align: center; color: #666; padding: 20px;">
#         <p>🌾 <strong>Satyukt AI - Smart Farming Assistant</strong> | Powered by Satellite Intelligence & AI</p>
#         <p>Serving Farmers, Agri-banks, Insurers & Governments across India 🇮🇳</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )






import streamlit as st
import os
import pdfplumber
import tempfile
import random
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.documents import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Satyukt Virtual Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Google API keys
google_api_keys = [
    os.getenv("GOOGLE_API_KEY_1"),
    os.getenv("GOOGLE_API_KEY_2"),
    os.getenv("GOOGLE_API_KEY_3"),
    os.getenv("GOOGLE_API_KEY_4")
]
google_api_keys = [key for key in google_api_keys if key]

if not google_api_keys:
    st.error("❌ No valid GOOGLE_API_KEYs found. Please set at least one in your .env file.")
    st.stop()

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }
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
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #4CAF50;
        padding: 8px 12px;
    }
    .language-selector {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .language-label {
        color: white;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4CAF50 0%, #2E7D32 100%);
    }
    #MainMenu, footer, header {visibility: hidden;}
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
    st.markdown("📱 +91-8970095700")

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

# Feature cards
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
        <div style="background: rgba(33, 150, 243, 0.1); padding: 20px; Releases: 1.0.0 border-radius: 10px; text-align: center; margin: 10px 0;">
            <div style="font-size: 2em; margin-bottom: 10px;">📊</div>
            <div style="font-weight: 600;">Riskહું</div>
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

# Contact messages
contact_messages = {
    "English": "🤝 Let me connect you with our agricultural experts! Please contact contact@satyukt.com or call 8970700045 | 7019992797 for specialized assistance.",
    "हिंदी": "🤝 मैं आपको हमारे कृषि विशेषज्ञों से जोड़ता हूँ! विशेष सहायता के लिए कृपया contact@satyukt.com पर संपर्क करें या 8970700045 | 7019992797 पर कॉल करें।",
    "ಕನ್ನಡ": "🤝 ನಮ್ಮ ಕೃಷಿ ತಜ್ಞರೊಂದಿಗೆ ನಿಮ್ಮನ್ನು ಸಂಪರ್ಕಿಸುತ್ತೇನೆ! ವಿಶೇಷ ಸಹಾಯಕ್ಕಾಗಿ contact@satyukt.com ಗೆ ಸಂಪರ್ಕಿಸಿ ಅಥವಾ 8970700045 | 7019992797 ಗೆ ಕರೆ ಮಾಡಿ.",
    "தமிழ்": "🤝 எங்கள் விவசாய நிபுணர்களுடன் உங்களை இணைக்கிறேன்! சிறப்பு உதவிக்கு contact@satyukt.com ஐ தொடர்பு கொள்ளவும் அல்லது 8970700045 | 7019992797 ஐ அழைக்கவும்.",
    "తెలుగు": "🤝 మా వ్యవసాయ నిపుణులతో మిమ్మల్ని కనెక్ట్ చేస్తాను! ప్రత్యేక సహాయం కోసం దయచేసి contact@satyukt.com ని సంప్రదించండి లేదా 8970700045 | 7019992797 కు కాల్ చేయండి.",
    "বাংলা": "🤝 আমি আপনাকে আমাদের কৃষি বিশ৻জ্ঞদের সাথে সংযুক্ত করব! বিশেষ সহায়তার জন্য অনুগ্রহ করে contact@satyukt.com এ যোগাযোগ করুন অথবা 8970700045 | 7019992797 নম্বরে কল করুন।",
    "मराठी": "🤝 मी तुम्हाला आमच्या कृषी तज्ञांशी जोडतो! विशेष मदतीसाठी कृपया contact@satyukt.com वर संपर्क साधा किंवा 8970700045 | 7019992797 वर कॉल करा.",
    "ગુજરાતી": "🤝 હું તમને અમારા કૃષિ નિષ્ણાતો સાથે જોડું છું! વિશેષ સહાયતા માટે કૃપા કરીને contact@satyukt.com નો સંપર્ક કરો અથવા 8970700045 | 7019992797 પર કૉલ કરો.",
    "ਪੰਜਾਬੀ": "🤝 ਮੈਂ ਤੁਹਾਨੂੰ ਸਾਡੇ ਖੇਤੀਬਾੜੀ ਮਾਹਿਰਾਂ ਨਾਲ ਜੋੜਦਾ ਹਾਂ! ਵਿਸ਼ੇਸ਼ ਸਹਾਇਤਾ ਲਈ ਕਿਰਪਾ ਕਰਕੇ contact@satyukt.com 'ਤੇ ਸੰਪਰਕ ਕਰੋ ਜਾਂ 8970700045 | 7019992797 'ਤੇ ਕਾਲ ਕਰੋ।"
}

# Prompt template
prompt = ChatPromptTemplate.from_template(
    f"""
    You are a helpful, multilingual AI assistant specializing in agriculture. Answer questions using only the information provided in the PDF context below.

    - Respond in {selected_lang} language.
    - Keep replies short, human-like, and helpful.
    - If the answer is partially available, share only what's known — no guessing.
    - If the answer is missing, reply with: "{contact_messages.get(selected_lang, contact_messages['English'])}"
    - Do not say phrases like "according to the context" or "not found in the PDF".
    - Focus on agriculture-related guidance and support.

    <context>
    {{context}}
    </context>
    Question: {{input}}
    """
)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=random.choice(google_api_keys)
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "initial_greeting_shown" not in st.session_state:
    st.session_state.initial_greeting_shown = False

# Function to extract text from PDF
def extract_text_with_pdfplumber(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "".join(page.extract_text() or "" for page in pdf.pages)
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Function to initialize vector database
def initialize_vector_db(pdf_file):
    if "vector_store" not in st.session_state:
        try:
            with st.spinner("🤖 Initializing Satyukt Assistant..."):
                # Save uploaded PDF to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(pdf_file.read())
                    pdf_path = temp_file.name

                # Extract text
                text_data = extract_text_with_pdfplumber(pdf_path)
                os.unlink(pdf_path)  # Remove temporary file

                if not text_data.strip():
                    st.error("📄 PDF is empty or unreadable.")
                    return False

                # Create document
                doc = Document(page_content=text_data)
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = text_splitter.split_documents([doc])

                # Initialize embeddings
                st.session_state.embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/embedding-001",
                    google_api_key=random.choice(google_api_keys)
                )

                # Create vector store
                st.session_state.vector_store = DocArrayInMemorySearch.from_documents(
                    chunks, st.session_state.embeddings
                )
                return True
        except Exception as e:
            st.error(f"❌ Error initializing assistant: {str(e)}")
            return False
    return True

# Check for out-of-context responses
def is_out_of_context(answer, current_selected_lang):
    contact_message = contact_messages.get(current_selected_lang, contact_messages['English']).lower()
    if answer.strip().lower() == contact_message:
        return True
    keywords = [
        "i'm sorry", "i don't know", "not sure", "out of context",
        "invalid", "no mention", "cannot", "unable", "not available",
        "जानकारी उपलब्ध नहीं", "मुझे नहीं पता", "సమాచారం అందుబాటులో లేదు",
        "তথ্য উপলব্ধ নেই", "माहिती उपलब्ध नाही", "કોઈ માહિતી ઉપલબ્ધ નથી",
        "ਕੋਈ ਜਾਣਕਾਰੀ ਉਪਲਬਧ ਨਹੀਂ", "தகவல் இல்லை", "ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ"
    ]
    return any(k in answer.lower() for k in keywords)

# Load default PDF or allow upload
default_pdf_path = "SatyuktQueries.pdf"
pdf_input_from_user = None
if os.path.exists(default_pdf_path):
    class DummyFile:
        def __init__(self, path):
            self.path = path
        def read(self):
            with open(self.path, "rb") as f:
                return f.read()
    pdf_input_from_user = DummyFile(default_pdf_path)
else:
    pdf_input_from_user = st.file_uploader("Upload a PDF file", type=["pdf"])

# Initialize vector store if PDF is available
if pdf_input_from_user:
    if initialize_vector_db(pdf_input_from_user):
        if not st.session_state.initial_greeting_shown:
            st.success("✅ Hi there! 👋 Satyukt Virtual Assistant is ready to assist you! Ask me anything about agriculture, farming, or our services.")
            st.session_state.initial_greeting_shown = True
    else:
        st.error("❌ Could not initialize assistant. Check PDF content or API keys.")

# Chat interface
if "vector_store" in st.session_state:
    st.markdown("### 💬 Chat with Satyukt Virtual Assistant")
    chat_container_key = f"chat_container_{len(st.session_state.chat_history)}"
    st.markdown(f'<div class="chat-container" id="{chat_container_key}">', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="message-label user-label">🧑‍🌾 You</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-label bot-label">🤖 Satyukt</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bot-message">{msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Scroll to bottom
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

    # Input section
    st.markdown("### Ask your question:")
    user_prompt = st.text_input(
        "Type your question here...",
        placeholder=f"Ask me anything in {selected_lang}... 🌾",
        key="user_input"
    )
    send_button = st.button("Send 🚀", key="send_btn")

    if send_button and user_prompt.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.spinner("🤔 Satyukt is thinking..."):
            try:
                document_chain = create_stuff_documents_chain(llm, prompt)
                retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 2})
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                response = retrieval_chain.invoke({'input': user_prompt})
                answer = response.get('answer', contact_messages.get(selected_lang, contact_messages['English']))
                if is_out_of_context(answer, selected_lang):
                    answer = contact_messages.get(selected_lang, contact_messages['English'])
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                answer = contact_messages.get(selected_lang, contact_messages['English'])
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
    elif send_button:
        st.warning("⚠️ Please enter a question before sending.")

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
