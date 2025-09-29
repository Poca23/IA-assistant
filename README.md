# 🤖 Claire-IA Conversational AI

A minimalist conversational AI built with Python and Streamlit that learns from user interactions in real-time.

## ✨ Features

- **Interactive Chat Interface** - Clean, responsive web interface
- **Real-time Learning** - AI learns new responses during conversations
- **Persistent Memory** - Conversations and learned responses saved in JSON
- **Live Statistics** - Track conversations and learned responses
- **Mobile-Friendly** - Responsive design for all devices

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **AI/ML**: scikit-learn, TF-IDF vectorization
- **Frontend**: Streamlit
- **Data Storage**: JSON
- **Deployment**: Streamlit Cloud

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip package manager
Installation
# Clone repository
git clone <your-repo-url>
cd ia-conversationnelle

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
Run Locally
python -m streamlit run app/interface.py
Open your browser to http://localhost:8501
📁 Project Structure
ia-conversationnelle/
├── app/
│   ├── brain.py          # AI core logic
│   ├── memory.py         # Data persistence
│   ├── interface.py      # Streamlit UI
│   ├── learning.py       # Learning module
│   └── main.py           # Entry point
├── data/
│   └── conversations.json # Stored conversations
├── requirements.txt      # Dependencies
└── README.md            # Documentation
🎓 How to Teach the AI

Open the sidebar in the web interface
Enter a question in the "Question" field
Enter the desired response in the "Response" field
Click "🎓 Learn" - The AI will remember this for future conversations

📊 Architecture

AIBrain: Core conversation logic with ML-based response matching
Memory: JSON-based storage for conversations and learned responses
Interface: Streamlit web app with chat interface and learning controls
Learning: Module for adding new question-answer pairs

🔧 Development
Run Tests
python -m app.memory    # Test memory module
python -m app.brain     # Test AI brain
python -m app.learning  # Test learning module
Project Principles

Modular Design - Each file ≤ 50 lines
Simple Architecture - No unnecessary complexity
Responsive UI - Mobile-first approach
Real-time Learning - Immediate response updates

🌐 Live Demo
Try Claire-IA Live (Coming soon)
🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
👩‍💻 Author
Claire - Full-Stack DeveloperBuilding intelligent applications with Python

⭐ If you found this project helpful, please give it a star!