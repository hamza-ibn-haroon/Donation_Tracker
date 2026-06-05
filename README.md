# 🫶 Donation Transparency Agent

An AI agent that helps donors find trustworthy, high-impact donation campaigns using **Hindsight persistent memory**.

## 🧠 What Makes This Special

This agent **remembers**:
- Your donation preferences across sessions
- Past campaigns you've viewed
- Your donation history with impact tracking
- Campaign success scores and financial transparency

## 🚀 Features

- **Persistent Memory**: Uses Hindsight to retain donor preferences and campaign data
- **Blockchain Verification**: Simulated on-chain transaction tracking
- **Impact Tracking**: Success scores and outcome metrics for each campaign
- **Financial Transparency**: Program vs admin spending breakdowns
- **AI-Powered Responses**: Natural language understanding with Groq

## 🛠️ Tech Stack

- **Memory Layer**: Hindsight (Vectorize)
- **AI Model**: Groq (openai/gpt-oss-120b)
- **Frontend**: Streamlit
- **Language**: Python 3.12

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/donation-transparency-agent
cd donation-transparency-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run Hindsight locally (required for full memory)
docker run -p 8888:8888 -p 9999:9999 vectorize/hindsight

# Run the app
streamlit run app.py