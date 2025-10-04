# 🤖 Claire-IA Conversational AI

A complete conversational AI with multi-domain knowledge management, built with Python and Streamlit. Features real-time learning, advanced CRUD operations, bidirectional synchronization, and comprehensive data import/export capabilities.

## ✨ Features

### Core Capabilities
- **Interactive Chat Interface** - Clean, responsive multi-tab web interface
- **Real-time Learning** - AI learns new responses during conversations
- **Persistent Memory** - Conversations and learned responses saved in JSON
- **Knowledge Base Management** - Complete CRUD operations for knowledge entries
- **Live Statistics** - Track conversations, learned responses, and knowledge base metrics
- **Mobile-Friendly** - Responsive design for all devices

### Advanced Features (Phase 4-5)
- **Multi-Domain Knowledge** - Organized by categories (General/Personal) and subcategories
- **Simple JSON Import** - Direct file upload with instant integration
- **Advanced Import** - Validation, preview, duplicate detection, intelligent merge
- **Filtered Export** - Export by category, tags, or date range with preview
- **Complete Backup** - Automatic ZIP backup with metadata and restore functionality
- **Bidirectional Sync** - Smart merge or replace modes with integrity validation
- **Operation Logs** - Automatic history tracking for all import/export operations
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
# or use quick launch script
./run.sh
```
Open your browser to http://localhost:8501

## 📁 Project Structure
```
ia-conversationnelle/
├── app/
│   ├── brain.py           # ✅ AI core logic (ML)
│   ├── memory.py          # ✅ Data persistence
│   ├── interface.py       # ✅ Streamlit 4-tab UI
│   ├── main.py            # ✅ Entry point
│   ├── learning.py        # ✅ Learning module
│   ├── knowledge.py       # ✅ CRUD operations for KB
│   ├── sync_import.py     # ✅ Advanced import with validation
│   ├── sync_export.py     # ✅ Export & backup system
│   └── test_*.py          # ✅ Unit tests (7 files, ~90% coverage)
├── data/
│   ├── conversations.json     # Stored conversations
│   ├── knowledge/             # Knowledge base directory
│   │   ├── general/           # General knowledge
│   │   │   ├── culture.json
│   │   │   ├── sciences.json
│   │   │   └── technologies.json
│   │   └── personal/          # Personal knowledge
│   │       ├── cuisine.json
│   │       ├── admin.json
│   │       ├── sante.json
│   │       └── budget.json
│   ├── backups/               # Automatic ZIP backups
│   └── exports/               # Filtered JSON exports
├── requirements.txt           # Dependencies
├── run.sh                     # Quick launch script
└── README.md                  # Documentation
```

## 🎯 Interface Overview

### 1️⃣ Chat Tab
- Real-time conversational interface
- AI responses with ML-based matching
- Message history persistence
- Sidebar learning panel for quick teaching

### 2️⃣ Knowledge Base Tab
- Browse knowledge by category and subcategory
- **Create**: Add new entries with question/answer/tags
- **Read**: View all entries organized by domain
- **Update**: Edit entries in real-time with instant save
- **Delete**: Remove entries with confirmation dialog
- **Search**: Filter by tags and categories

### 3️⃣ Statistics Tab
- 💬 Total conversations tracked
- 🎓 Learned responses count
- 📚 Knowledge base entries metrics
- 📈 Evolution graphs (Phase 5 - in development)

### 4️⃣ Management Tab
- **Simple Import**: Direct JSON upload
- **Advanced Import**: Validation + preview + duplicate detection + merge
- **Filtered Export**: Export by category/tags/dates with preview
- **Complete Backup**: Automatic ZIP with metadata
- **Restore**: Merge or replace modes with validation
- **Clear History**: Reset conversations with confirmation
- **Operation Logs**: View import/export history

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

### Simple Import (Quick Upload)
1. Navigate to **Management** tab → "📥 Simple Import"
2. Upload your JSON file
3. Instant integration - no preview

### Advanced Import (Recommended)
1. Navigate to **Management** tab → "🔄 Advanced Import"
2. Upload JSON file (automatic validation)
3. **Preview**: Review entries before import
4. **Duplicate Detection**: System identifies existing entries
5. **Intelligent Merge**: Choose to skip, update, or create
6. **Confirm**: Apply changes with full logs

### Filtered Export
1. Navigate to **Management** tab → "📤 Export"
2. **Filter Options**:
   - Category (General/Personal/All)
   - Tags (multi-select)
   - Date range (from/to)
3. **Preview**: See export summary before download
4. Click "Download JSON" - filtered file ready

### Complete Backup
1. Navigate to **Management** tab → "💾 Backup"
2. Click "Create Complete Backup"
3. System generates ZIP with:
   - All conversations.json
   - Complete knowledge base
   - Metadata (date, entries count)
4. Download ZIP automatically

### Restore from Backup
1. Navigate to **Management** tab → "🔄 Restore"
2. Upload backup ZIP file
3. **Choose Mode**:
   - **Merge**: Combine with existing data
   - **Replace**: Full system reset
4. System validates integrity
5. Confirm restore operation

## 📊 JSON Format Standard

### Knowledge Entry Format
```json
{
  "entries": [
    {
      "id": "unique_id_123",
      "question": "Question or topic",
      "answer": "Response or content",
      "tags": ["tag1", "tag2"],
      "created": "2025-01-15T10:30:00",
      "updated": "2025-01-27T14:20:00"
    }
  ],
  "metadata": {
    "category": "culture",
    "subcategory": "general",
    "total_entries": 1,
    "last_updated": "2025-01-27T14:20:00"
  }
}
```

### Backup ZIP Structure
```
backup_20250127_143000.zip
├── conversations.json
├── knowledge/
│   ├── general/
│   │   ├── culture.json
│   │   ├── sciences.json
│   │   └── technologies.json
│   └── personal/
│       ├── cuisine.json
│       ├── admin.json
│       ├── sante.json
│       └── budget.json
└── metadata.json  # Backup info
```

## 🏗️ Architecture

### Core Modules
- **AIBrain** (`brain.py`): ML-based conversation logic with TF-IDF vectorization
- **Memory** (`memory.py`): JSON storage with backup mechanisms
- **KnowledgeBase** (`knowledge.py`): Complete CRUD with category management
- **Interface** (`interface.py`): 4-tab Streamlit app (Chat/KB/Stats/Management)
- **Learning** (`learning.py`): Question-answer pair teaching system

### Advanced Modules (Phase 4-5)
- **SyncImport** (`sync_import.py`): 
  - File validation
  - Duplicate detection
  - Intelligent merge logic
  - Preview system
- **SyncExport** (`sync_export.py`):
  - Filtered export by criteria
  - ZIP backup generation
  - Restore with merge/replace
  - Metadata management

## 🔧 Development

### Run Tests
```bash
python -m app.test_memory       # Test memory module
python -m app.test_brain        # Test AI brain
python -m app.test_learning     # Test learning module
python -m app.test_knowledge    # Test CRUD operations
python -m app.test_sync_import  # Test import system
python -m app.test_sync_export  # Test export/backup
python -m app.test_interface    # Test UI components
```

### Project Principles
- **Modular Design** - Each file ≤ 150 lines (except interface.py extended)
- **Simple Architecture** - No unnecessary complexity
- **Responsive UI** - Mobile-first approach with Streamlit
- **Real-time Operations** - Immediate saves and updates
- **Data Integrity** - Validation at every step
- **Professional Practices** - 6W methodology (Who/What/When/Where/Why/hoW)

### Git Workflow
```bash
# After completing a feature
git add .
git commit -m "feat: [phase] - [description]"
git push origin main

# Tagging releases
git tag -a v1.1.1 -m "Phase 4 complete - Advanced import/export"
git push origin v1.1.1
```

## ✅ Current Status (Day 27 - Phase 4 COMPLETE)

### ✅ Completed Features (Days 1-27)

#### Phase 1-3: Core System
- ✅ AI brain with ML logic (scikit-learn)
- ✅ Persistent JSON storage
- ✅ Multi-tab Streamlit interface (4 tabs)
- ✅ Complete CRUD operations
- ✅ Real-time editing with instant save
- ✅ 26+ conversations tracked
- ✅ 13+ knowledge base entries active

#### Phase 4: Advanced Import/Export (Days 26-27)
- ✅ Simple Import: Direct JSON upload
- ✅ Advanced Import: 
  - File validation
  - Preview with statistics
  - Duplicate detection
  - Intelligent merge
- ✅ Filtered Export:
  - Category/tags/date filters
  - Preview before download
- ✅ Complete Backup:
  - Automatic ZIP generation
  - Metadata inclusion
- ✅ Restore System:
  - Merge/Replace modes
  - Integrity validation
- ✅ Operation Logs: Auto-tracking

### 📊 Metrics (Day 27)
| Metric | Value |
|--------|-------|
| Python Modules | 15 files |
| Lines of Code | ~1,620 |
| Unit Tests | 7 files |
| Test Coverage | ~90% |
| Active KB Entries | 13+ |
| Conversations | 26+ |
| Backups Available | 1+ |

### 🎯 Next Phase: Analytics Dashboard (Days 28-35)

#### Day 28A - Module Analytics
- 🔲 Create `app/analytics.py`
- 🔲 General statistics methods
- 🔲 Time series analysis
- 🔲 Tag distribution
- 🔲 Category breakdown
- 🔲 Usage metrics

#### Days 29-30 - Visual Charts
- 🔲 Activity graphs (day/week/month)
- 🔲 Tag popularity charts
- 🔲 Category distribution pie charts
- 🔲 Learning curve visualization

#### Days 31-32 - Integration
- 🔲 Update Stats tab with graphs
- 🔲 Export analytics reports
- 🔲 Historical trends

## 🌐 Live Demo
🚀 **[Try Claire-IA Live](https://ia-assistant-vbvo2b2thrpcvr9azgfrv7.streamlit.app/)**

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

**Hardware**: ThinkPad P53 (Intel i7, 32GB RAM)  
**OS**: Ubuntu 24.04 LTS  
**IDE**: VS Code, PyCharm

## 🏷️ Version History
- **v1.1.1** (Day 27) - Advanced Import/Export Complete ✅
- **v1.1** (Day 25) - CRUD Operations Complete
- **v1.0** (Day 15) - Initial Release
- *Tag: v1-Claire-IA*

---

⭐ **If you found this project helpful, please give it a star!**

📈 **Status**: Phase 4 Complete | Phase 5 (Analytics) Starting Day 28  
🎯 **Progress**: 60% Complete | 40% Remaining (Analytics + Advanced Maintenance)