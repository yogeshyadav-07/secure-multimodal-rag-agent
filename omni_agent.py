import streamlit as st
import os
import base64
import hashlib
import mysql.connector
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# LangChain Engine Framework Components
from langchain_mistralai import ChatMistralAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

# --- 🌐 MULTI-LANGUAGE LOCALIZATION DICTIONARY ---
LANG_DICT = {
    "English": {
        "title": "🔒 OmniAgent Enterprise Gateway",
        "caption": "Your personal AI workspace secured with MySQL Encryption.",
        "login_tab": "🔑 Login Existing User",
        "register_tab": "📝 Create New Account",
        "name": "Full Name",
        "username": "Username",
        "email": "Email Address",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "btn_login": "Sign In 🚀",
        "btn_register": "Create Account ✨",
        "err_mismatch": "❌ Passwords do not match!",
        "err_invalid": "❌ Invalid Username or Password!",
        "err_fill": "⚠️ Please fill all fields completely.",
        "err_exists": "⚠️ Username or Email already exists!",
        "success_reg": "🎉 Account successfully created! Please switch to the login tab.",
        "welcome": "Welcome back",
        "user_sidebar": "👤 User",
        "terminal_sidebar": "Logged into Secured Terminal",
        "theme_sidebar": "🌙 Dark Workspace Theme",
        "tavily_sidebar": "Activate Real-Time Web Engine (Tavily)",
        "logout_sidebar": "🚪 Logout Session",
        "main_title": "⚡ OmniAgent Pro: Multi-Modal Context Platform",
        "main_caption": "Factual Engine anchored to 2026 | Logged in as: ",
        "engine_label": "🧬 ENGINE: ",
        "chat_init": "Hello! I am your secured AI Assistant. Attach files below using the `➕` expander.",
        "attach_title": "➕ Attach Reference File Context (PDF or Image Docs)",
        "upload_label": "Upload Area Node",
        "chat_input": "Ask anything... Use the arrow on the right to send ⬆️",
        "toast_img": "Image loaded successfully!",
        "toast_pdf": "PDF Vectorized successfully!",
        "spinner_pdf": "Processing document chunks...",
        "sys_instruction": "You are OmniAgent Pro, an elite enterprise multi-modal AI assistant. Current year is 2026. Ground your answers factually."
    },
    "Hindi (हिन्दी)": {
        "title": "🔒 ओम्नीएजेंट एंटरप्राइज गेटवे",
        "caption": "आपका व्यक्तिगत एआई वर्कस्पेस जो माईएसक्यूएल एन्क्रिप्शन से सुरक्षित है।",
        "login_tab": "🔑 लॉगिन करें",
        "register_tab": "📝 नया अकाउंट बनाएं",
        "name": "पूरा नाम",
        "username": "यूज़रनेम",
        "email": "ईमेल पता",
        "password": "पासवर्ड",
        "confirm_password": "पासवर्ड की पुष्टि करें",
        "btn_login": "साइन इन करें 🚀",
        "btn_register": "अकाउंट बनाएं ✨",
        "err_mismatch": "❌ पासवर्ड मेल नहीं खाते!",
        "err_invalid": "❌ गलत यूज़रनेम या पासवर्ड!",
        "err_fill": "⚠️ कृपया सभी फ़ील्ड पूरी तरह से भरें।",
        "err_exists": "⚠️ यूज़रनेम या ईमेल पहले से मौजूद है!",
        "success_reg": "🎉 अकाउंट सफलतापूर्वक बन गया है! कृपया लॉगिन टैब पर जाएं।",
        "welcome": "आपका स्वागत है",
        "user_sidebar": "👤 यूज़र",
        "terminal_sidebar": "सुरक्षित टर्मिनल में लॉग इन हैं",
        "theme_sidebar": "🌙 डार्क वर्कस्पेस थीम",
        "tavily_sidebar": "रीयल-टाइम वेब सर्च चालू करें (Tavily)",
        "logout_sidebar": "🚪 लॉगआउट सेशन",
        "main_title": "⚡ ओम्नीएजेंट प्रो: मल्टी-मोडल कॉन्टेक्स्ट प्लेटफॉर्म",
        "main_caption": "तथ्यात्मक इंजन वर्ष 2026 | लॉग इन यूज़र: ",
        "engine_label": "🧬 इंजन: ",
        "chat_init": "नमस्ते! मैं आपका सुरक्षित एआई असिस्टेंट हूं। नीचे दिए गए `➕` एक्सपैंडर से फ़ाइलें जोड़ें।",
        "attach_title": "➕ संदर्भ फ़ाइल जोड़ें (PDF या इमेज दस्तावेज़)",
        "upload_label": "अपलोड एरिया नोड",
        "chat_input": "कुछ भी पूछें... भेजने के लिए दाईं ओर तीर का उपयोग करें ⬆️",
        "toast_img": "इमेज सफलतापूर्वक लोड हो गई!",
        "toast_pdf": "PDF सफलतापूर्वक वेक्टराइज़ हो गया!",
        "spinner_pdf": "दस्तावेज़ के टुकड़े प्रोसेस किए जा रहे हैं...",
        "sys_instruction": "आप ओम्नीएजेंट प्रो हैं, एक विशिष्ट एंटरप्राइज मल्टी-मोडल एआई सहायक। वर्तमान वर्ष 2026 है। अपने उत्तरों को तथ्यों पर आधारित रखें।"
    },
    "Hinglish": {
        "title": "🔒 OmniAgent Enterprise Gateway",
        "caption": "Aapka personal AI workspace secured with MySQL Encryption.",
        "login_tab": "🔑 Login Existing User",
        "register_tab": "📝 Naya Account Banayein",
        "name": "Pura Naam (Full Name)",
        "username": "Username",
        "email": "Email Address",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "btn_login": "Sign In 🚀",
        "btn_register": "Create Account ✨",
        "err_mismatch": "❌ Passwords match nahi kar rahe hain!",
        "err_invalid": "❌ Galat Username ya Password! Kripya check karein.",
        "err_fill": "⚠️ Kripya saari fields ko completely fill karein.",
        "err_exists": "⚠️ Username ya Email pehle se maujood hai!",
        "success_reg": "🎉 Account successfully ban gaya hai! Ab login tab par jaakar login karein.",
        "welcome": "Welcome back",
        "user_sidebar": "👤 User",
        "terminal_sidebar": "Secured Terminal mein logged in hain",
        "theme_sidebar": "🌙 Dark Workspace Theme",
        "tavily_sidebar": "Real-Time Web Engine Activate Karein (Tavily)",
        "logout_sidebar": "🚪 Logout Session",
        "main_title": "⚡ OmniAgent Pro: Multi-Modal Context Platform",
        "main_caption": "Factual Engine anchored to 2026 | Logged in as: ",
        "engine_label": "🧬 ENGINE: ",
        "chat_init": "Hello! Main aapka secured AI Assistant hoon. Niche diye `➕` expander se files attach karein.",
        "attach_title": "➕ Attach Reference File Context (PDF or Image Docs)",
        "upload_label": "Upload Area Node",
        "chat_input": "Kuch bhi puchhein... Send karne ke liye right arrow use karein ⬆️",
        "toast_img": "Image load ho gayi!",
        "toast_pdf": "PDF Vectorize ho gaya!",
        "spinner_pdf": "Document chunks process ho rahe hain...",
        "sys_instruction": "Aap OmniAgent Pro hain, ek elite enterprise multi-modal AI assistant. Current year 2026 hai. Apne answers ko factually ground karein aur Hinglish/English tone me reply karein."
    }
}

# --- ⚙️ 1. Session States & Language Setup ---
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Helper Function to get translated strings shortcode
def t(key):
    return LANG_DICT[st.session_state.lang].get(key, "")

# Initialize default chat message based on language if empty
if len(st.session_state.chat_history) == 0:
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": LANG_DICT[st.session_state.lang]["chat_init"], 
        "source": "Core LLM Brain"
    })

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "processed_file_fingerprint" not in st.session_state:
    st.session_state.processed_file_fingerprint = None
if "img_base64_cache" not in st.session_state:
    st.session_state.img_base64_cache = None

# --- 🗄️ 2. MySQL Database Functions (Port 3300) ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3300)), # Port 3300 integrated
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "password"), # Add your secret password here
            database=os.getenv("MYSQL_DB", "omni_agent_db")
        )
        return conn
    except Exception as e:
        st.error(f"⚠️ Database Connection Failed: {e}")
        return None

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def register_user(name, username, email, password):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        hashed_pw = make_hash(password)
        cursor.execute(
            "INSERT INTO users (name, username, email, password_hash) VALUES (%s, %s, %s, %s)", 
            (name, username, email, hashed_pw)
        )
        conn.commit()
        return "success"
    except mysql.connector.Error as err:
        if err.errno == 1062: # Database duplicate entry code
            return "exists"
        else:
            st.error(f"Execution Error: {err}")
            return "error"
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    hashed_pw = make_hash(password)
    # User username ya email dono me se kisi se bhi login kar sake uski utility di hai
    cursor.execute("SELECT * FROM users WHERE (username = %s OR email = %s) AND password_hash = %s", (username, username, hashed_pw))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# --- 🎨 3. Page Config & CSS Theme Control ---
st.set_page_config(page_title="Secure OmniAgent Pro", page_icon="🔒", layout="wide")

if st.session_state.theme == "Dark":
    st.markdown("<style>.stApp { background-color: #0b0f19; color: #f1f5f9; } section[data-testid='stSidebar'] { background-color: #111827 !important; }.badge-info { color: #38bdf8; font-weight: bold; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp { background-color: #f8fafc; color: #0f172a; } section[data-testid='stSidebar'] { background-color: #f1f5f9 !important; }.badge-info { color: #2563eb; font-weight: bold; }</style>", unsafe_allow_html=True)


# --- 🎫 4. AUTHENTICATION GATEWAY ---
if not st.session_state.authenticated:
    # Language Dropdown interface level par system switch karne ke liye
    cols = st.columns([8, 2])
    with cols[1]:
        selected_lang = st.selectbox("🌐 Interface Language", options=["English", "Hindi (हिन्दी)", "Hinglish"], index=["English", "Hindi (हिन्दी)", "Hinglish"].index(st.session_state.lang))
        if selected_lang != st.session_state.lang:
            st.session_state.lang = selected_lang
            st.rerun()

    st.title(t("title"))
    st.caption(t("caption"))
    
    auth_tab, register_tab = st.tabs([t("login_tab"), t("register_tab")])
    
    with auth_tab:
        login_user = st.text_input(f"{t('username')} / {t('email')}", key="login_user_input")
        login_pass = st.text_input(t("password"), type="password", key="login_pass_input")
        if st.button(t("btn_login"), use_container_width=True):
            if authenticate_user(login_user, login_pass):
                st.session_state.authenticated = True
                st.session_state.username = login_user
                st.success(f"🎉 {t('welcome')}, {login_user}!")
                st.rerun()
            else:
                st.error(t("err_invalid"))
                
    with register_tab:
        reg_name = st.text_input(t("name"), key="reg_name_input")
        reg_user = st.text_input(t("username"), key="reg_user_input")
        reg_email = st.text_input(t("email"), key="reg_email_input")
        reg_pass = st.text_input(t("password"), type="password", key="reg_pass_input")
        reg_conf = st.text_input(t("confirm_password"), type="password", key="reg_conf_input")
        
        if st.button(t("btn_register"), use_container_width=True):
            if not (reg_name and reg_user and reg_email and reg_pass and reg_conf):
                st.warning(t("err_fill"))
            elif reg_pass != reg_conf:
                st.error(t("err_mismatch"))
            else:
                status = register_user(reg_name, reg_user, reg_email, reg_pass)
                if status == "exists":
                    st.warning(t("err_exists"))
                elif status == "success":
                    st.success(t("success_reg"))
    st.stop()


# --- 🧠 5. CORE MODEL CACHING ---
@st.cache_resource
def load_foundational_layers():
    llm = ChatMistralAI(model="mistral-large-latest", temperature=0.1)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return llm, embeddings

llm, embeddings = load_foundational_layers()

def encode_image_to_b64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')


# --- 🎛️ 6. SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown(f"<h3 style='color:#10b981;'>{t('user_sidebar')}: {st.session_state.username}</h3>", unsafe_allow_html=True)
    st.caption(t("terminal_sidebar"))
    st.divider()
    
    # Active inside application language switcher node
    selected_lang_sidebar = st.selectbox("🌐 System Language", options=["English", "Hindi (हिन्दी)", "Hinglish"], index=["English", "Hindi (हिन्दी)", "Hinglish"].index(st.session_state.lang), key="sidebar_lang_select")
    if selected_lang_sidebar != st.session_state.lang:
        st.session_state.lang = selected_lang_sidebar
        # Reset the default greeting message matching state language
        st.session_state.chat_history[0] = {"role": "assistant", "content": t("chat_init"), "source": "Core LLM Brain"}
        st.rerun()
        
    st.divider()
    current_theme_toggle = st.toggle(t("theme_sidebar"), value=(st.session_state.theme == "Dark"))
    new_theme_state = "Dark" if current_theme_toggle else "Light"
    if new_theme_state != st.session_state.theme:
        st.session_state.theme = new_theme_state
        st.rerun()
        
    st.divider()
    enable_tavily = st.toggle(t("tavily_sidebar"), value=True)
    
    st.divider()
    if st.button(t("logout_sidebar"), use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.chat_history = []
        st.session_state.vector_store = None
        st.session_state.img_base64_cache = None
        st.rerun()


# --- 💬 7. MAIN APP CHAT LOOP ---
st.title(t("main_title"))
st.caption(f"{t('main_caption')} {st.session_state.username}")

# Render active chat states
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(f"<span class='badge-info'>{t('engine_label')}{msg.get('source', 'Brain')}</span>", unsafe_allow_html=True)
        st.write(msg["content"])

# Multi-modal payload attachment block
with st.expander(t("attach_title"), expanded=False):
    uploaded_file = st.file_uploader(t("upload_label"), type=["pdf", "png", "jpg", "jpeg"], label_visibility="collapsed")
    
    if uploaded_file and uploaded_file.name != st.session_state.processed_file_fingerprint:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        st.session_state.processed_file_fingerprint = uploaded_file.name
        
        if file_ext in [".png", ".jpg", ".jpeg"]:
            st.session_state.vector_store = None
            img_bits = uploaded_file.read()
            st.session_state.img_base64_cache = encode_image_to_b64(img_bits)
            st.image(Image.open(BytesIO(img_bits)), caption="Buffered Asset", width=200)
            st.toast(t("toast_img"), icon="🖼️")
            
        elif file_ext == ".pdf":
            st.session_state.img_base64_cache = None
            with st.spinner(t("spinner_pdf")):
                temp_pdf_sink = f"temp_engine_{uploaded_file.name}"
                with open(temp_pdf_sink, "wb") as f: f.write(uploaded_file.getbuffer())
                try:
                    loader = PyPDFLoader(temp_pdf_sink)
                    pages = loader.load()
                    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
                    chunks = splitter.split_documents(pages)
                    st.session_state.vector_store = Chroma.from_documents(chunks, embeddings)
                    st.toast(t("toast_pdf"), icon="✅")
                except Exception as ex: st.error(f"Vectorization fault: {ex}")
                finally:
                    if os.path.exists(temp_pdf_sink): os.remove(temp_pdf_sink)

# Query core trigger execution pipeline
if prompt_query := st.chat_input(t("chat_input")):
    st.session_state.chat_history.append({"role": "user", "content": prompt_query})
    
    with st.chat_message("user"):
        st.write(prompt_query)
        
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        badge_placeholder = st.empty()
        
        try:
            active_routing_source = "Core LLM Brain"
            system_instruction = (
                f"{t('sys_instruction')} "
                f"You are directly interacting with customer username identity: {st.session_state.username}."
            )
            
            # Pathway A: Computer Vision Engine Processing
            if st.session_state.img_base64_cache is not None:
                active_routing_source = "Computer Vision Engine"
                badge_placeholder.markdown(f"<span class='badge-info'>{t('engine_label')}{active_routing_source}</span>", unsafe_allow_html=True)
                
                vision_payload = [
                    {"type": "text", "text": f"Analyze this context asset to satisfy prompt: {prompt_query}"},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{st.session_state.img_base64_cache}"}
                ]
                
                full_stream_text = ""
                for chunk in llm.stream([HumanMessage(content=vision_payload)]):
                    full_stream_text += chunk.content
                    response_placeholder.write(full_stream_text)
                
                st.session_state.img_base64_cache = None
                st.session_state.processed_file_fingerprint = None
                
            # Pathway B: Document RAG Index / Tavily Live Context Search
            else:
                context_payload = ""
                if st.session_state.vector_store is not None:
                    active_routing_source = "Local Document RAG Index"
                    matched_nodes = st.session_state.vector_store.max_marginal_relevance_search(prompt_query, k=4)
                    context_payload += "\n\n[LOCAL PDF FACTS]:\n" + "\n\n".join([n.page_content for n in matched_nodes])
                    
                if enable_tavily:
                    query_lower = prompt_query.lower()
                    realtime_signals = ["news", "today", "current", "latest", "time", "weather", "market", "stock", "score", "date"]
                    if any(sig in query_lower for sig in realtime_signals):
                        active_routing_source = "Live Web Search (Tavily)"
                        try:
                            tavily_client = TavilySearchResults(max_results=3)
                            optimized_query = f"{prompt_query} year 2026" if "2026" not in query_lower else prompt_query
                            search_hits = tavily_client.invoke({"query": optimized_query})
                            context_payload += "\n\n[REAL-TIME LIVE 2026 INTERNET DATA]:\n" + str(search_hits)
                        except: pass
                            
                badge_placeholder.markdown(f"<span class='badge-info'>{t('engine_label')}{active_routing_source}</span>", unsafe_allow_html=True)
                if context_payload:
                    system_instruction += f"\n\nGround your logic directly on this injected layer context:\n{context_payload}"
                    
                messages_stack = [SystemMessage(content=system_instruction)]
                for past_turn in st.session_state.chat_history[-6:-1]:
                    if past_turn["role"] == "user": messages_stack.append(HumanMessage(content=past_turn["content"]))
                    else: messages_stack.append(AIMessage(content=past_turn["content"]))
                messages_stack.append(HumanMessage(content=prompt_query))
                
                full_stream_text = ""
                for chunk in llm.stream(messages_stack):
                    full_stream_text += chunk.content
                    response_placeholder.write(full_stream_text)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": full_stream_text,
                "source": active_routing_source
            })
            
        except Exception as major_error:
            st.error(f"System Error Exception: {major_error}")