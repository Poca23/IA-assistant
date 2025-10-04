# 🤖 Claire-IA Conversational AI

A complete conversational AI with multi-domain knowledge management, built with Python and Streamlit. Features real-time learning, CRUD operations, and advanced data import/export capabilities.

## ✨ Features

### Core Capabilities
- **Interactive Chat Interface** - Clean, responsive multi-tab web interface
- **Real-time Learning** - AI learns new responses during conversations
- **Persistent Memory** - Conversations and learned responses saved in JSON
- **Knowledge Base Management** - Complete CRUD operations for knowledge entries
- **Live Statistics** - Track conversations, learned responses, and knowledge base metrics
- **Mobile-Friendly** - Responsive design for all devices

### Advanced Features
- **Multi-Domain Knowledge** - Organized by categories (General/Personal) and subcategories
- **JSON Import/Export** - Mass data upload with validation and preview
- **CRUD Operations** - Create, Read, Update, Delete knowledge entries in real-time
- **Smart Organization** - Automatic categorization and tagging system
- **Data Persistence** - All changes saved instantly to JSON storage

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **AI/ML**: scikit-learn, TF-IDF vectorization
- **Frontend**: Streamlit (Multi-tab interface)
- **Data Storage**: JSON with structured knowledge base
- **Deployment**: Streamlit Cloud

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip package manager
```

### Installation
```bash
# Clone repository
git clone <your-repo-url>
cd ia-conversationnelle

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Locally
```bash
streamlit run app/main.py
```
Open your browser to http://localhost:8501

## 📁 Project Structure
```
ia-conversationnelle/
├── app/
│   ├── brain.py          # AI core logic
│   ├── memory.py         # Data persistence
│   ├── interface.py      # Streamlit multi-tab UI
│   ├── main.py           # Entry point
│   ├── learning.py       # Learning module
│   ├── knowledge.py      # CRUD operations for knowledge base
│   └── import_handler.py # JSON import/export handler
├── data/
│   ├── conversations.json    # Stored conversations
│   └── knowledge/           # Knowledge base directory
│       ├── general/         # General knowledge
│       │   ├── culture.json
│       │   ├── sciences.json
│       │   └── technologies.json
│       └── personal/        # Personal knowledge
│           ├── cuisine.json
│           ├── admin.json
│           ├── sante.json
│           └── budget.json
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```

## 🎯 Interface Overview

### 1️⃣ Chat Tab
- Real-time conversational interface
- AI responses with learning capability
- Message history persistence

### 2️⃣ Knowledge Base Tab
- Browse knowledge by category and subcategory
- **Create**: Add new entries with question/answer/tags
- **Read**: View all entries organized by domain
- **Update**: Edit entries in real-time with instant save
- **Delete**: Remove entries with confirmation dialog
- **Search**: Filter by tags and categories

### 3️⃣ Statistics Tab
- Total conversations tracked
- Learned responses count
- Knowledge base metrics
- Category distribution

### 4️⃣ Management Tab
- Import JSON files (mass data upload)
- Export knowledge base (backup creation)
- Clear conversation history
- System maintenance tools

## 🎓 How to Use

### Teaching the AI (Chat Interface)
1. Open the sidebar in the chat tab
2. Enter a question in the "Question" field
3. Enter the desired response in the "Response" field
4. Click "🎓 Learn" - The AI will remember this for future conversations

### Managing Knowledge Base
1. Navigate to **Knowledge Base** tab
2. Select category (General/Personal) and subcategory
3. **Add Entry**: Use the creation form at top
4. **Edit Entry**: Click edit button, modify fields, save
5. **Delete Entry**: Click delete, confirm action

### Importing Data
1. Navigate to **Management** tab
2. Click "Import JSON" section
3. Upload your JSON file (must match standard format)
4. Preview entries before import
5. Confirm to merge with existing knowledge

### Exporting Data
1. Navigate to **Management** tab
2. Select export scope (category/subcategory)
3. Click "Export" button
4. Download generated JSON file

## 📊 JSON Format Standard
```json
{
  "entries": [
    {
      "id": "unique_id",
      "question": "Question or topic",
      "answer": "Response or content",
      "tags": ["tag1", "tag2"],
      "created": "2025-01-15",
      "updated": "2025-01-15"
    }
  ],
  "metadata": {
    "category": "culture",
    "total_entries": 1,
    "last_updated": "2025-01-15"
  }
}
```

## 🏗️ Architecture

- **AIBrain**: Core conversation logic with ML-based response matching
- **Memory**: JSON-based storage for conversations and learned responses
- **KnowledgeBase**: Complete CRUD operations with category management
- **Interface**: Streamlit multi-tab app with chat, knowledge, stats, and management
- **Learning**: Module for adding new question-answer pairs
- **ImportHandler**: JSON file validation and mass data import

## 🔧 Development

### Run Tests
```bash
python -m app.test_memory    # Test memory module
python -m app.test_brain     # Test AI brain
python -m app.test_learning  # Test learning module
python -m app.test_knowledge # Test CRUD operations
```

### Project Principles
- **Modular Design** - Each file ≤ 50 lines (except interface.py)
- **Simple Architecture** - No unnecessary complexity
- **Responsive UI** - Mobile-first approach with Streamlit
- **Real-time Operations** - Immediate saves and updates
- **Data Integrity** - Validation at every step

### Git Workflow
```bash
# After completing a feature
git add .
git commit -m "feat: [description]"
git push origin main
```

## ✅ Current Status (Phase 4 - Day 25)

### Completed Features
- ✅ Core AI brain with ML logic
- ✅ Persistent JSON storage
- ✅ Multi-tab Streamlit interface (4 tabs)
- ✅ Complete CRUD operations tested and validated
- ✅ Real-time editing with instant save
- ✅ JSON import/export functionality
- ✅ Knowledge base with 13+ active entries
- ✅ Category/subcategory organization
- ✅ Mobile-responsive design

### In Progress
- 🔲 Advanced bidirectional synchronization (Days 26-27)
- 🔲 Enhanced statistics with graphs (Days 29-30)
- 🔲 Advanced maintenance tools (Days 31-32)

## 🌐 Live Demo
🚀 [Try Claire-IA Live](https://ia-assistant-vbvo2b2thrpcvr9azgfrv7.streamlit.app/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👩‍💻 Author
**Claire** - Full-Stack Developer (DWWM)  
Building intelligent applications with Python, JavaScript, Java, PHP  
*Expertise: AI/ML, Web Development, DevOps*

## 🏷️ Version
**v1.4** - Claire-IA with Complete CRUD Operations  
*Tag: v1-Claire-IA-CRUD-Complete*

---

⭐ If you found this project helpful, please give it a star!

**Hardware**: ThinkPad P53 (i7, 32GB RAM)  
**OS**: Ubuntu 24.04 LTS  
**Stack**: Python, Streamlit, scikit-learn, JSON