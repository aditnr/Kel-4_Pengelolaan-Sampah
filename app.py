import streamlit as st
from util.parser import JSONParser

parser = JSONParser()
parser.parse("data/intents.json")

st.set_page_config(
    page_title="EcoChat - Asisten Pintar Pengelolaan Sampah",
    page_icon="♻️",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 15px;
        padding: 15px;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 5px 10px rgba(0,0,0,0.1);
    }
    
    [data-theme="light"] .chat-message.user {
        background-color: #f0f9ff;
        color: #1a1a1a;
    }
    
    [data-theme="light"] .chat-message.assistant {
        background-color: #e1f5e1;
        color: #1a1a1a;
    }
    
    [data-theme="dark"] .chat-message.user {
        background-color: #2d3748;
        color: #ffffff;
    }
    
    [data-theme="dark"] .chat-message.assistant {
        background-color: #1a472a;
        color: #ffffff;
    }
            
    .eco-tip {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    [data-theme="light"] .eco-tip {
        background-color: #e1f5e1;
        color: #1a1a1a;
    }
    
    [data-theme="dark"] .eco-tip {
        background-color: #1a472a;
        color: #ffffff;
    }
    
    [data-theme="light"] .welcome-container {
        background-color: #ffffff;
        color: #1a1a1a;
    }
    
    [data-theme="dark"] .welcome-container {
        background-color: #2d3748;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

def get_theme():
    try:
        return "dark" if st.get_theme() == "dark" else "light"
    except:
        return "light"

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.image("assets/03.png")
    st.markdown("### Tentang EcoChat")
    st.write("EcoChat adalah asisten pintar yang siap membantu Anda memahami pengelolaan sampah yang baik dan benar.")
    
    st.markdown("### Fitur Utama")
    st.write("• Informasi pengolahan sampah")
    st.write("• Tips daur ulang")
    st.write("• Panduan composting")
    st.write("• Edukasi lingkungan")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown("""
        <h1 style='text-align: center; color: var(--text-color);'>
            🌱 EcoChat - Asisten Pintar Pengelolaan Sampah 🌍
        </h1>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"""
            <div class='chat-message welcome-container'>
                <h3>Selamat datang di EcoChat! 👋</h3>
                <p>Saya siap membantu Anda dengan informasi seputar:</p>
                <ul>
                    <li>Cara memilah sampah</li>
                    <li>Metode pengolahan sampah</li>
                    <li>Tips reduce, reuse, recycle</li>
                    <li>Dan banyak lagi!</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.container():
            role = message["role"]
            content = message["content"]
            st.markdown(f"""
                <div class='chat-message {role}'>
                    <strong>{'Anda' if role == "user" else '🤖 EcoChat'}:</strong><br>
                    {content}
                </div>
            """, unsafe_allow_html=True)

    user_input = st.chat_input(
        "💭 Ketik pertanyaan Anda di sini...",
        key="chat_input"
    )

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        response = parser.get_response(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()

    if st.button('🔄 Mulai Percakapan Baru', key='reset'):
        st.session_state.messages = []
        st.rerun()

if st.session_state.messages:
    eco_tips = [
        "💡 Tahukah Anda? Satu botol plastik membutuhkan waktu hingga 450 tahun untuk terurai secara alami. Mari mulai membawa botol minum sendiri!",
        "💡 Gunakan kantong belanja kain daripada kantong plastik sekali pakai. Ini membantu mengurangi sampah plastik yang mencemari lingkungan.",
        "💡 Pisahkan sampah organik dan anorganik untuk memudahkan proses daur ulang dan mengurangi volume sampah di tempat pembuangan.",
        "💡 Gantilah lampu pijar dengan lampu LED yang lebih efisien dan tahan lama, sehingga membantu mengurangi konsumsi energi.",
        "💡 Kurangi penggunaan kertas dengan beralih ke dokumen digital. Ini dapat menghemat pohon dan mengurangi limbah.",
        "💡 Hindari membeli produk dengan kemasan berlebihan. Pilih produk dengan kemasan ramah lingkungan dan lebih sedikit plastik.",
        "💡 Daur ulang sampah elektronik! Jangan buang perangkat elektronik yang rusak, bawa ke tempat daur ulang agar tidak mencemari tanah.",
        "💡 Mulailah menggunakan kendaraan umum, sepeda, atau berjalan kaki untuk mengurangi emisi karbon dan polusi udara.",
        "💡 Pilih produk makanan yang menggunakan kemasan ramah lingkungan, atau lebih baik lagi, pilih produk tanpa kemasan sama sekali!",
        "💡 Manfaatkan air hujan untuk menyiram tanaman di halaman rumah Anda, ini membantu mengurangi penggunaan air bersih.",
    ]

    import random
    selected_eco_tip = random.choice(eco_tips)

    st.markdown(f"""
        <div class='eco-tip'>
            <strong>{selected_eco_tip}</strong>
        </div>
    """, unsafe_allow_html=True)
