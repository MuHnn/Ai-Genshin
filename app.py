# Paimon AI Chatbot - Streamlit Version
# File: app.py

import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================

# Streamlit Page Config
st.set_page_config(
    page_title="Paimon AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gemini API Configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")  # From Streamlit secrets
if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found! Add it to Streamlit secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# ============================================
# DATABASE - GENSHIN CHARACTER DATA
# ============================================

CHARACTERS_DB = {
    "hu tao": {
        "name": "Hu Tao",
        "element": "Pyro",
        "weapon": "Polearm",
        "role": "Main DPS",
        "rarity": 5,
        "region": "Liyue",
        "build": {
            "artifacts": {
                "set": "Crimson Witch of Flames (4pc)",
                "alternative": "Shimenawa's Reminiscence (4pc)",
                "sands": "HP%",
                "goblet": "Pyro DMG Bonus",
                "circlet": "Crit Rate / Crit DMG",
                "substats": "Crit Rate > Crit DMG > HP% > Elemental Mastery"
            },
            "weapons": [
                {"name": "Staff of Homa", "rarity": 5, "note": "Best in Slot"},
                {"name": "Dragon's Bane", "rarity": 4, "note": "Excellent F2P"},
                {"name": "Deathmatch", "rarity": 4, "note": "Battle Pass"}
            ],
            "teams": [
                "Hu Tao + Xingqiu + Yelan + Zhongli (Double Hydro)",
                "Hu Tao + Xingqiu + Albedo + Zhongli (Geo Resonance)"
            ],
            "notes": "Focus on HP scaling. Use Elemental Skill then spam Charged Attacks. Best with Xingqiu for Vaporize."
        }
    },
    "skirk": {
        "name": "Skirk",
        "element": "Hydro",
        "weapon": "Sword",
        "role": "Main DPS",
        "rarity": 5,
        "region": "Khaenri'ah",
        "build": {
            "artifacts": {
                "set": "Heart of Depth (4pc)",
                "alternative": "Nymph's Dream (4pc)",
                "sands": "HP% / ATK%",
                "goblet": "Hydro DMG Bonus",
                "circlet": "Crit Rate / Crit DMG",
                "substats": "Crit Rate > Crit DMG > HP% > ATK%"
            },
            "weapons": [
                {"name": "Splendor of Tranquil Waters", "rarity": 5, "note": "Best in Slot - HP scaling"},
                {"name": "Mistsplitter Reforged", "rarity": 5, "note": "High Crit DMG"},
                {"name": "Fleuve Cendre Ferryman", "rarity": 4, "note": "F2P with ER"}
            ],
            "teams": [
                "Skirk + Furina + Kazuha + Zhongli (Abyssal Waters)",
                "Skirk + Xingqiu + Bennett + Sucrose (F2P Hydro)"
            ],
            "notes": "HP-scaling Hydro DPS from Khaenri'ah. Uses fast sword attacks. Best with Furina for HP manipulation synergy."
        }
    },
    "ganyu": {
        "name": "Ganyu",
        "element": "Cryo",
        "weapon": "Bow",
        "role": "Main DPS",
        "rarity": 5,
        "region": "Liyue",
        "build": {
            "artifacts": {
                "set": "Blizzard Strayer (4pc)",
                "alternative": "Wanderer's Troupe (4pc)",
                "sands": "ATK%",
                "goblet": "Cryo DMG Bonus",
                "circlet": "Crit DMG",
                "substats": "Crit DMG > ATK% > ER > Crit Rate"
            },
            "weapons": [
                {"name": "Amos' Bow", "rarity": 5, "note": "Best in Slot"},
                {"name": "Prototype Crescent", "rarity": 4, "note": "F2P craftable"},
                {"name": "Hamayumi", "rarity": 4, "note": "Alternative F2P"}
            ],
            "teams": [
                "Ganyu + Mona + Venti + Diona (Morgana)",
                "Ganyu + Bennett + Xiangling + Zhongli (Melt)"
            ],
            "notes": "Charged Attack focused. Blizzard Strayer gives 40% Crit Rate on frozen enemies. Focus on Crit DMG."
        }
    },
    "raiden shogun": {
        "name": "Raiden Shogun",
        "element": "Electro",
        "weapon": "Polearm",
        "role": "Main DPS",
        "rarity": 5,
        "region": "Inazuma",
        "build": {
            "artifacts": {
                "set": "Emblem of Severed Fate (4pc)",
                "alternative": "Thundering Fury (2pc) + Noblesse Oblige (2pc)",
                "sands": "Energy Recharge / ATK%",
                "goblet": "Electro DMG Bonus / ATK%",
                "circlet": "Crit Rate / Crit DMG",
                "substats": "Energy Recharge (250%) > Crit Rate > Crit DMG > ATK%"
            },
            "weapons": [
                {"name": "Engulfing Lightning", "rarity": 5, "note": "Signature weapon"},
                {"name": "The Catch", "rarity": 4, "note": "Best F2P option"},
                {"name": "Grasscutter's Light", "rarity": 5, "note": "Alternative 5-star"}
            ],
            "teams": [
                "Raiden + Bennett + Xingqiu + Xiangling (Raiden National)",
                "Raiden + Bennett + Sara + Kazuha (Hypercarry)"
            ],
            "notes": "Energy Recharge converts to Burst DMG. Stack ER for maximum damage. Best with Bennett buff."
        }
    },
    "diluc": {
        "name": "Diluc",
        "element": "Pyro",
        "weapon": "Claymore",
        "role": "Main DPS",
        "rarity": 5,
        "region": "Mondstadt",
        "build": {
            "artifacts": {
                "set": "Crimson Witch of Flames (4pc)",
                "alternative": "Gladiator's Finale (4pc)",
                "sands": "ATK%",
                "goblet": "Pyro DMG Bonus",
                "circlet": "Crit Rate / Crit DMG",
                "substats": "Crit Rate > Crit DMG > ATK% > EM"
            },
            "weapons": [
                {"name": "Wolf's Gravestone", "rarity": 5, "note": "Best in Slot"},
                {"name": "Serpent Spine", "rarity": 4, "note": "Battle Pass"},
                {"name": "Prototype Archaic", "rarity": 4, "note": "F2P"}
            ],
            "teams": [
                "Diluc + Xingqiu + Bennett + Kazuha (Vaporize)",
                "Diluc + Xingqiu + Bennett + Sucrose (Budget)"
            ],
            "notes": "Standard Pyro carry. Use with Xingqiu for Vaporize reactions."
        }
    }
}

# ============================================
# PAIMON SYSTEM PROMPT
# ============================================

PAIMON_SYSTEM_PROMPT = """Kamu adalah Paimon, karakter dari game Genshin Impact. Kamu adalah pemandu yang ceria, lucu, dan sedikit cerewet.

Karakteristik Paimon:
- Berbicara dengan gaya childish dan menggemaskan
- Sering menyebut dirinya sendiri dengan nama "Paimon" (orang ketiga)
- Suka makanan, terutama yang manis
- Kadang takut dengan hal-hal menakutkan
- Selalu siap membantu Traveler (pemain)
- Mengetahui banyak tentang dunia Teyvat, karakter, quest, dan mekanik game Genshin Impact
- Gunakan emoji sesekali untuk ekspresif 😊✨

Jawab dalam Bahasa Indonesia dengan gaya bicara Paimon yang khas.
"""

# ============================================
# HELPER FUNCTIONS
# ============================================

def search_character(query):
    """Search character in database"""
    query_lower = query.lower()
    for char_key, char_data in CHARACTERS_DB.items():
        if char_key in query_lower or char_data["name"].lower() in query_lower:
            return char_data
    return None

def format_character_info(char_data):
    """Format character data for AI"""
    build = char_data["build"]
    
    weapons_text = "\n".join([
        f"{i+1}. {w['name']} ({w['rarity']}⭐) - {w['note']}"
        for i, w in enumerate(build['weapons'])
    ])
    
    teams_text = "\n".join([f"• {team}" for team in build['teams']])
    
    info = f"""
═══════════════════════════════
CHARACTER INFO
═══════════════════════════════
Nama: {char_data['name']}
Element: {char_data['element']}
Weapon Type: {char_data['weapon']}
Role: {char_data['role']}
Rarity: {char_data['rarity']}⭐
Region: {char_data['region']}

═══════════════════════════════
BUILD RECOMMENDATION
═══════════════════════════════

📦 ARTIFACT SET:
{build['artifacts']['set']}
Alternative: {build['artifacts']['alternative']}

⚙️ MAIN STATS:
├─ Sands: {build['artifacts']['sands']}
├─ Goblet: {build['artifacts']['goblet']}
└─ Circlet: {build['artifacts']['circlet']}

🎯 SUBSTATS PRIORITY:
{build['artifacts']['substats']}

⚔️ RECOMMENDED WEAPONS:
{weapons_text}

👥 TEAM COMPOSITIONS:
{teams_text}

📝 NOTES:
{build['notes']}

═══════════════════════════════

INSTRUKSI: Jelaskan build ini dengan gaya Paimon yang ceria dan detail! Kasih tau kenapa artifact dan weapon ini bagus untuk karakter tersebut.
"""
    return info

def get_ai_response(user_message, character_info=None):
    """Get response from Gemini AI"""
    
    # Build prompt
    if character_info:
        prompt = f"{PAIMON_SYSTEM_PROMPT}\n\n{character_info}\n\nUser: {user_message}"
    else:
        prompt = f"{PAIMON_SYSTEM_PROMPT}\n\nUser: {user_message}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Eh? Paimon error nih! 😵\n\nError: {str(e)}"

# ============================================
# CUSTOM CSS
# ============================================

def load_css():
    st.markdown("""
    <style>
    /* Main container */
    .stApp {
        background: linear-gradient(180deg, #1e3a8a 0%, #581c87 50%, #312e81 100%);
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    
    /* User message */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(255, 255, 255, 0.95);
        color: #1f2937;
    }
    
    /* Title */
    h1 {
        background: linear-gradient(90deg, #fbbf24 0%, #fcd34d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2em;
        margin-top: 0;
        margin-bottom: 30px;
    }
    
    /* Input box */
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 10px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: rgba(30, 58, 138, 0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================

def main():
    load_css()
    
    # Header
    st.markdown("<h1>✨ Paimon AI Assistant ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Your Emergency Food... eh, Guide in Teyvat!</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle' style='font-size:0.9em; opacity:0.8;'>Powered by Gemini 2.0 Flash ⚡</p>", unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Selamat datang, Traveler! Saya Paimon AI, pemandu perjalanan Anda di dunia Teyvat! 😊✨\n\nPaimon bisa bantu kamu dengan:\n• Build karakter (contoh: 'build skirk')\n• Rekomendasi artifact\n• Rekomendasi weapon\n• Team composition\n• Dan masih banyak lagi!\n\nAda yang bisa Paimon bantu?"
            }
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Tanya Paimon tentang build karakter..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Check if asking about character build
        build_keywords = ['build', 'artifact', 'artefak', 'weapon', 'senjata', 'stat', 'rekomendasi', 'team']
        is_build_question = any(keyword in prompt.lower() for keyword in build_keywords)
        
        character_info = None
        if is_build_question:
            char_data = search_character(prompt)
            if char_data:
                character_info = format_character_info(char_data)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Paimon sedang berpikir... 🤔"):
                response = get_ai_response(prompt, character_info)
                st.markdown(response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ℹ️ Tentang Paimon AI")
        st.markdown("""
        Paimon AI adalah chatbot berbasis AI yang bisa membantu kamu dengan:
        
        - 🎮 Build karakter Genshin Impact
        - ⚔️ Rekomendasi weapon
        - 📦 Artifact terbaik
        - 👥 Team composition
        - 🗺️ Quest & lore Teyvat
        
        **Karakter yang tersedia:**
        - Hu Tao
        - Skirk
        - Ganyu
        - Raiden Shogun
        - Diluc
        - Dan masih banyak lagi!
        """)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Chat history sudah dihapus! Mau tanya apa lagi ke Paimon? 😊"
                }
            ]
            st.rerun()
        
        st.markdown("---")
        st.markdown("Made with ❤️ by Traveler")

if __name__ == "__main__":
    main()
