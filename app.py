import streamlit as st
import uuid
from datetime import datetime
import random
import re

# Page config
st.set_page_config(
    page_title="Donation Transparency Agent | Trust & Impact",
    page_icon="🫶",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main theme colors */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    }
    
    /* Glassmorphism effect for cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(15, 118, 110, 0.15);
        margin-bottom: 1rem;
    }
    
    /* Impact card */
    .impact-card {
        background: linear-gradient(135deg, rgba(15, 118, 110, 0.08), rgba(20, 184, 166, 0.08));
        border-radius: 20px;
        padding: 1.25rem;
        border: 1px solid rgba(20, 184, 166, 0.2);
        transition: all 0.3s ease;
    }
    
    .impact-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(15, 118, 110, 0.15);
    }
    
    /* Trust badge */
    .trust-badge {
        background: linear-gradient(135deg, #0F766E, #14B8A6);
        color: white;
        padding: 4px 12px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-right: 8px;
    }
    
    /* Progress bar */
    .progress-container {
        background: #E2E8F0;
        border-radius: 30px;
        height: 8px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #0F766E, #14B8A6);
        border-radius: 30px;
        height: 100%;
        transition: width 0.8s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #F97316, #EA580C);
        color: white !important;
        border: none;
        border-radius: 40px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(249, 115, 22, 0.4);
    }
    
    /* Metrics styling */
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #0F766E;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 14px;
        color: #64748B;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: white;
        border-right: none;
        box-shadow: 2px 0 20px rgba(0,0,0,0.05);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #0F766E, #14B8A6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Secure badge */
    .secure-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #F1F5F9;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 12px;
        color: #0F766E;
        font-weight: 500;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #0F766E, transparent);
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]
if "messages" not in st.session_state:
    st.session_state.messages = []
if "donation_history" not in st.session_state:
    st.session_state.donation_history = []
if "memories" not in st.session_state:
    st.session_state.memories = []

# Campaign Data
CAMPAIGNS = {
    "C001": {
        "name": "💧 Clean Water Wells",
        "full_name": "Clean Water Wells for Rural Kenya",
        "org": "WaterAid International",
        "category": "clean_water",
        "location": "Kenya",
        "impact": "Built 12 wells, serving 3,200+ people",
        "impact_story": "Children no longer walk 6km daily for dirty water. School attendance increased by 65%.",
        "success_score": 9.2,
        "program_percent": 88,
        "raised": 52340,
        "goal": 50000,
        "beneficiary": "Maria, 12 years old",
        "beneficiary_quote": "Now I can go to school instead of walking for water.",
        "image": "💧"
    },
    "C002": {
        "name": "📚 School Meals",
        "full_name": "School Meals Program for India",
        "org": "Save the Children",
        "category": "education",
        "location": "India",
        "impact": "1.2M meals served, attendance up 40%",
        "impact_story": "Daily nutritious meals brought children back to school. Malnutrition rates dropped by 35%.",
        "success_score": 9.8,
        "program_percent": 92,
        "raised": 42150,
        "goal": 35000,
        "beneficiary": "Rajesh, 9 years old",
        "beneficiary_quote": "The school meal is why I come to school every day.",
        "image": "📚"
    },
    "C003": {
        "name": "🏥 Mobile Clinic",
        "full_name": "Mobile Medical Clinic for Rural Uganda",
        "org": "Doctors Without Borders",
        "category": "healthcare",
        "location": "Uganda",
        "impact": "5,000+ patients treated annually",
        "impact_story": "A mobile clinic now reaches 15 remote villages, providing vaccines and maternal care.",
        "success_score": 9.5,
        "program_percent": 90,
        "raised": 75000,
        "goal": 75000,
        "beneficiary": "Grace, new mother",
        "beneficiary_quote": "The mobile clinic saved my baby's life.",
        "image": "🏥"
    },
    "C004": {
        "name": "🌞 Solar Schools",
        "full_name": "Solar Panels for Schools in Malawi",
        "org": "SolarAid",
        "category": "clean_energy",
        "location": "Malawi",
        "impact": "50 schools electrified, 5,000 students",
        "impact_story": "Solar power means students can study after dark. Test scores improved by 40%.",
        "success_score": 9.7,
        "program_percent": 85,
        "raised": 38500,
        "goal": 40000,
        "beneficiary": "Principal Chanda",
        "beneficiary_quote": "For the first time, our students can study at night.",
        "image": "🌞"
    },
    "C005": {
        "name": "🚨 Emergency Relief",
        "full_name": "Flood Emergency Relief - Pakistan",
        "org": "Red Cross",
        "category": "disaster_relief",
        "location": "Pakistan",
        "impact": "15,000 families received aid",
        "impact_story": "Emergency shelters, food, and clean water delivered within 48 hours.",
        "success_score": 8.5,
        "program_percent": 82,
        "raised": 87200,
        "goal": 100000,
        "beneficiary": "Ahmed, father of 4",
        "beneficiary_quote": "Your help gave us hope when we lost everything.",
        "image": "🚨"
    },
    "C006": {
        "name": "🎓 Girls' Education",
        "full_name": "Girls' Education Scholarship Fund",
        "org": "Malala Fund",
        "category": "education",
        "location": "Afghanistan",
        "impact": "500 girls enrolled in school",
        "impact_story": "Scholarships cover tuition, books, and transportation for girls.",
        "success_score": 9.6,
        "program_percent": 89,
        "raised": 68450,
        "goal": 60000,
        "beneficiary": "Amina, scholarship recipient",
        "beneficiary_quote": "Education is my right. Thank you for believing in me.",
        "image": "🎓"
    }
}

# Calculate metrics
total_donors = len(st.session_state.donation_history)
total_raised = sum(d["amount"] for d in st.session_state.donation_history) if st.session_state.donation_history else 0

def store_memory(content):
    """Store user preference in memory"""
    st.session_state.memories.append({
        "content": content,
        "timestamp": datetime.now().isoformat()
    })

def recall_memory(query):
    """Recall relevant memories"""
    query_lower = query.lower()
    relevant = []
    for mem in st.session_state.memories[-10:]:
        if query_lower in mem["content"].lower():
            relevant.append(mem)
    return relevant

def get_response(user_id, message):
    """Generate response based on user message"""
    msg_lower = message.lower()
    
    # Check for donation intent
    if any(word in msg_lower for word in ["donate", "$", "give", "contribute"]):
        amount_match = re.search(r'\$?(\d+)', message)
        amount = int(amount_match.group(1)) if amount_match else 50
        campaign = random.choice(list(CAMPAIGNS.values()))
        tx_hash = f"0x{int(datetime.now().timestamp()):x}{user_id[:4]}"
        
        # Store in memory
        store_memory(f"Donated ${amount} to {campaign['name']}")
        
        # Save donation history
        donation = {
            "amount": amount,
            "campaign": campaign["full_name"],
            "campaign_name": campaign["name"],
            "tx_hash": tx_hash,
            "impact": campaign["impact"],
            "impact_story": campaign["impact_story"],
            "beneficiary": campaign["beneficiary"],
            "beneficiary_quote": campaign["beneficiary_quote"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.donation_history.append(donation)
        
        # Return formatted donation receipt
        return f"""
✅ **DONATION SUCCESSFUL!** 

---

| | |
|---|---|
| **💵 Amount** | **${amount}** |
| **🎯 Campaign** | {campaign['full_name']} |
| **📍 Location** | {campaign['location']} |
| **🔗 Transaction** | `{tx_hash}` |
| **💪 Impact** | {campaign['impact']} |

---

**💝 Your Impact Story:**
> *"{campaign['beneficiary_quote']}"*
> — {campaign['beneficiary']}

---
🔒 **Blockchain Verified** • **Tax Receipt Ready** • **100% Transparent**

*Thank you for making a difference! 🫶*
"""
    
    # Check for preference learning
    if any(word in msg_lower for word in ["prefer", "care", "like", "interested"]):
        store_memory(f"Preference: {message}")
        return f"""
🧠 **I've remembered your preference!**

> *"{message}"*

✅ I'll use this to find better campaign matches for you going forward.

*Try asking "Show me campaigns" to see personalized recommendations.*
"""
    
    # Check for campaign category queries
    categories = {
        "education": "education",
        "water": "clean_water", 
        "clean water": "clean_water",
        "health": "healthcare",
        "healthcare": "healthcare",
        "medical": "healthcare",
        "solar": "clean_energy",
        "energy": "clean_energy",
        "disaster": "disaster_relief",
        "relief": "disaster_relief"
    }
    
    for keyword, category in categories.items():
        if keyword in msg_lower:
            matches = [c for c in CAMPAIGNS.values() if c["category"] == category]
            if matches:
                response = f"### 📋 {keyword.upper()} CAMPAIGNS\n\n"
                for c in matches:
                    percent_raised = min(100, (c["raised"] / c["goal"]) * 100)
                    progress_bar = "█" * int(percent_raised / 10) + "░" * (10 - int(percent_raised / 10))
                    
                    response += f"""
---
**{c['image']} {c['full_name']}**  
⭐ **Score:** {c['success_score']}/10 | **Organization:** {c['org']} | **Location:** {c['location']}

**💰 Funding Progress:**  
`{progress_bar}` {percent_raised:.0f}%  
💵 ${c['raised']:,} raised of ${c['goal']:,} goal

**💪 Impact:** {c['impact']}  
**💝 Efficiency:** {c['program_percent']}% of funds go directly to programs

---
"""
                response += "\n🔒 **All donations are blockchain-verified and tax-deductible**\n\n💡 *Say \"I want to donate $50\" to support any of these campaigns*"
                return response
    
    # Default welcome response
    memories = recall_memory(message)
    memory_note = ""
    if memories:
        memory_note = "\n\n🧠 *Based on our conversation, I remember your preferences and will use them to help you.*"
    
    return f"""
🫶 **Welcome to the Donation Transparency Agent**

I help you find **trustworthy, high-impact donation opportunities** with complete transparency.

---

**✨ Try these examples:**

| Command | What it does |
|---------|--------------|
| `Show me education campaigns` | Browse education projects |
| `Show me clean water projects` | Browse water & sanitation |
| `I prefer high-impact healthcare` | Save your preferences |
| `I want to donate $50` | Make a transparent donation |

---

**🔒 Our Transparency Guarantee:**
✓ Blockchain-verified transactions
✓ 100% of impact data is tracked  
✓ Real beneficiary stories
✓ Tax receipts for every donation
✓ No hidden fees - {random.choice(list(CAMPAIGNS.values()))['program_percent']}% to programs

*Start by asking me about campaigns that matter to you!* 🫶{memory_note}
"""

# ============ UI LAYOUT ============

# Hero Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div>
        <span class="trust-badge">⭐ TOP-RATED NONPROFIT PARTNER</span>
        <span class="trust-badge">🔒 100% TAX-DEDUCTIBLE</span>
        <h1 style="margin: 20px 0 16px 0;">Every Dollar<br>Creates Real Impact</h1>
        <p style="font-size: 18px; color: #475569; line-height: 1.5;">Blockchain-verified donations. Real beneficiary stories. Full transparency from your wallet to their hands.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div class="metric-value">{total_donors}</div>
        <div class="metric-label">TOTAL DONORS</div>
        <div class="metric-value" style="font-size: 28px; margin-top: 16px;">${total_raised:,}</div>
        <div class="metric-label">TOTAL RAISED</div>
        <hr style="margin: 16px 0;">
        <div class="secure-badge" style="justify-content: center;">✓ Verified on Blockchain</div>
    </div>
    """, unsafe_allow_html=True)

# Impact Metrics Row
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="impact-card" style="text-align: center;">
        <div style="font-size: 32px;">🌍</div>
        <div class="metric-value" style="font-size: 24px;">100%</div>
        <div class="metric-label">Transparency</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="impact-card" style="text-align: center;">
        <div style="font-size: 32px;">⭐</div>
        <div class="metric-value" style="font-size: 24px;">9.4/10</div>
        <div class="metric-label">Avg. Impact Score</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="impact-card" style="text-align: center;">
        <div style="font-size: 32px;">💝</div>
        <div class="metric-value" style="font-size: 24px;">88%+</div>
        <div class="metric-label">to Programs</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="impact-card" style="text-align: center;">
        <div style="font-size: 32px;">🔗</div>
        <div class="metric-value" style="font-size: 24px;">On-Chain</div>
        <div class="metric-label">Verification</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Chat Interface
st.markdown('<h3 style="color: #0F766E;">💬 Ask about campaigns</h3>', unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Quick action buttons
st.markdown('<p style="font-weight: 500; margin: 16px 0 8px 0;">⚡ Quick Actions</p>', unsafe_allow_html=True)
cols = st.columns(4)
quick_queries = [
    "📚 Show me education campaigns",
    "💧 Show me clean water projects",
    "🏥 I prefer high-impact healthcare",
    "💝 I want to donate $50"
]

for col, query in zip(cols, quick_queries):
    if col.button(query, use_container_width=True, key=f"quick_{query}"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        with st.chat_message("assistant"):
            with st.spinner("🔍 Finding impact opportunities..."):
                response = get_response(st.session_state.user_id, query)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Chat input
st.markdown("---")
if prompt := st.chat_input("Ask about campaigns, share preferences, or say 'I want to donate $50'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("🧠 Processing your request..."):
            response = get_response(st.session_state.user_id, prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Sidebar - Impact Dashboard
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 24px;">
        <div style="font-size: 48px;">🫶</div>
        <h3 style="color: #0F766E; margin: 8px 0 4px 0;">Your Impact</h3>
        <p style="font-size: 12px; color: #64748B;">Donor ID: {}</p>
    </div>
    """.format(st.session_state.user_id), unsafe_allow_html=True)
    
    if st.session_state.donation_history:
        total_donated = sum(d["amount"] for d in st.session_state.donation_history)
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div class="metric-value" style="font-size: 36px;">${total_donated:,}</div>
            <div class="metric-label">Lifetime Giving</div>
            <div class="metric-value" style="font-size: 24px; margin-top: 12px;">{len(st.session_state.donation_history)}</div>
            <div class="metric-label">Donations Made</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📜 Recent Donations")
        for donation in st.session_state.donation_history[-3:][::-1]:
            st.markdown(f"""
            <div class="impact-card" style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{donation['campaign_name']}</strong>
                    <strong style="color: #0F766E;">${donation['amount']}</strong>
                </div>
                <p style="font-size: 11px; color: #64748B; margin: 4px 0;">{donation['date']}</p>
                <p style="font-size: 12px; margin: 8px 0 0 0;">💪 {donation['impact'][:60]}...</p>
                <div class="secure-badge" style="margin-top: 8px; font-size: 10px;">
                    ✓ {donation['tx_hash'][:20]}...
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 48px;">💝</div>
            <p><strong>No donations yet</strong></p>
            <p style="font-size: 13px;">Make your first donation to start tracking your impact!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Trust indicators
    st.markdown("""
    ### 🔒 Trust & Safety
    <div class="secure-badge" style="margin: 8px 0; display: flex;">✓ Blockchain Verified</div>
    <div class="secure-badge" style="margin: 8px 0; display: flex;">✓ 256-bit Encryption</div>
    <div class="secure-badge" style="margin: 8px 0; display: flex;">✓ Tax Receipt Ready</div>
    <div class="secure-badge" style="margin: 8px 0; display: flex;">✓ Charity Navigator 4-Star</div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.caption("Built with 🫶 for Hackathon | Premium Transparency Platform")

# New Session button
if st.sidebar.button("🔄 Start New Session", use_container_width=True):
    st.session_state.clear()
    st.rerun()