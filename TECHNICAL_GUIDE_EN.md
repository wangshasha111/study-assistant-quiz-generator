# 🔧 Study Assistant - Technical Guide

## 📋 Table of Contents
1. [System Architecture](#system-architecture)
2. [Installation & Configuration](#installation--configuration)
3. [Development Guide](#development-guide)
4. [Database Management](#database-management)
5. [Troubleshooting](#troubleshooting)
6. [Version Compatibility](#version-compatibility)

---

## 🏗️ System Architecture

### Core Components

```
project_study_assistant_quiz_generation/
├── app.py                      # Main application
├── database.py                 # Database management
├── session_utils.py            # Session utilities
├── admin_auth.py               # Admin authentication
├── pages/
│   └── 1_📊_Admin_Dashboard.py # Admin panel
├── venv/                       # Virtual environment
├── study_assistant.db          # SQLite database
├── .env                        # Environment variables
└── requirements.txt            # Dependencies
```

### Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | Streamlit | 1.29.0+ |
| AI Framework | LangChain | 0.1.0+ |
| LLM API | OpenAI | 1.109.1+ |
| PDF Processing | PyPDF2 | 3.0.1+ |
| PDF Generation | ReportLab | 4.4.4+ |
| Database | SQLite3 | Built-in |
| Environment | python-dotenv | 1.0.0+ |

### Data Flow

```
User Input → PDF Extract/Text Input → LangChain Processing 
    ↓
OpenAI API (GPT Models)
    ↓
Generate Summary + Quiz → Display Results → Database Logging
    ↓
User Interaction → Submit Answers → Grading → Download PDF/TXT
```

---

## 💻 Installation & Configuration

### System Requirements

- **OS**: macOS / Linux / Windows
- **Python**: 3.8 or higher
- **RAM**: Minimum 512MB
- **Disk**: Minimum 500MB

### Initial Setup

```bash
# 1. Clone or download project
cd project_study_assistant_quiz_generation

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Configure environment
cp .env.example .env
nano .env  # Edit configuration

# 7. Start application
streamlit run app.py
```

### Environment Variables

Create `.env` file:

```bash
# OpenAI API Key (optional, can enter in app)
OPENAI_API_KEY=sk-your-api-key-here

# Admin Password (required to enable Admin Dashboard)
ADMIN_PASSWORD=your_secure_password
```

### Verify Installation

```bash
# Test Python version
python3 --version

# Test key packages
python3 -c "import streamlit; print('✓ Streamlit')"
python3 -c "import langchain; print('✓ LangChain')"
python3 -c "import openai; print('✓ OpenAI')"
python3 -c "import PyPDF2; print('✓ PyPDF2')"
python3 -c "import reportlab; print('✓ ReportLab')"

# Test configuration
python3 test_admin_config.py
```

---

## 👨‍💻 Development Guide

### Project Structure Details

#### app.py (Main Application, ~1424 lines)
- **Purpose**: Main UI and core logic
- **Key Functions**:
  - `extract_text_from_pdf()`: PDF text extraction
  - `summarize_content()`: Generate summary
  - `generate_quiz_questions()`: Generate quiz
  - `display_interactive_quiz()`: Interactive quiz
  - `generate_pdf_with_results()`: PDF generation
- **Features**:
  - LangChain LCEL pattern
  - Session state management
  - Debug mode support
  - Database integration

#### database.py (~350 lines)
- **Purpose**: SQLite database management
- **Class**: `DatabaseManager`
- **Schema**:
  ```sql
  sessions (
    session_id TEXT PRIMARY KEY,
    username TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP,
    last_activity TIMESTAMP
  )
  
  generations (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    timestamp TIMESTAMP,
    file_name TEXT,
    file_size INTEGER,
    content_length INTEGER,
    input_method TEXT,
    summary TEXT,
    quiz TEXT,
    model_used TEXT,
    debug_mode BOOLEAN
  )
  
  quiz_results (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    generation_id INTEGER,
    score INTEGER,
    total_questions INTEGER,
    percentage REAL,
    answered_count INTEGER,
    user_answers TEXT,  -- JSON
    completed_at TIMESTAMP
  )
  ```

#### session_utils.py (~70 lines)
- **Purpose**: Session tracking utilities
- **Functions**:
  - `get_session_id()`: Get Streamlit session ID
  - `get_client_ip()`: Get client IP (proxy support)
  - `get_user_agent()`: Get browser info
  - `format_file_size()`: Format file size
  - `truncate_text()`: Truncate long text

#### admin_auth.py (~120 lines)
- **Purpose**: Admin authentication
- **Functions**:
  - `get_admin_password()`: Get admin password
  - `is_admin_enabled()`: Check if admin enabled
  - `check_admin_authentication()`: Auth check
  - `logout_admin()`: Logout
  - `show_logout_button()`: Display logout button

### LangChain Integration

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=api_key
)

# Create prompt template
prompt = PromptTemplate(
    input_variables=["content"],
    template="..."
)

# LCEL chain
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"content": content})
```

### Adding New Features

#### Example: Add True/False Quiz

1. **Modify prompt template** (`app.py`)
```python
def generate_true_false_quiz(llm, content: str) -> str:
    quiz_template = """Generate True/False questions..."""
    # Implementation
```

2. **Update UI** (`app.py`)
```python
quiz_type = st.selectbox("Quiz Type", ["Multiple Choice", "True/False"])
if quiz_type == "True/False":
    quiz = generate_true_false_quiz(llm, content)
```

3. **Update database** (if needed)
```python
# Add new field to generations table
ALTER TABLE generations ADD COLUMN quiz_type TEXT;
```

### Debugging Tips

```python
# 1. Enable Streamlit debug mode
streamlit run app.py --logger.level=debug

# 2. Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")

# 3. Use st.write() for debugging
st.write("Debug:", variable)

# 4. Check session state
st.write(st.session_state)

# 5. Exception handling
try:
    # code
except Exception as e:
    st.error(f"Error: {e}")
    import traceback
    st.code(traceback.format_exc())
```

---

## 🗄️ Database Management

### View Data

```bash
# Use sqlite3
sqlite3 study_assistant.db

# SQL queries
.tables
SELECT * FROM sessions LIMIT 10;
SELECT * FROM generations WHERE debug_mode = 0;
SELECT * FROM quiz_results ORDER BY percentage DESC;
.quit
```

### Backup Database

```bash
# Create backup
cp study_assistant.db study_assistant_backup_$(date +%Y%m%d).db

# Or use SQLite command
sqlite3 study_assistant.db ".backup study_assistant_backup.db"
```

### Reset Database

```bash
# Delete database (will lose all data)
rm study_assistant.db

# Restart app, database recreates automatically
streamlit run app.py
```

### Export Data

```python
# Using DatabaseManager
from database import DatabaseManager

db = DatabaseManager()

# Export session data
db.export_session_data(session_id, "output.json")

# Get statistics
stats = db.get_statistics()
print(stats)
```

---

## 🔧 Troubleshooting

### Common Errors & Solutions

#### 1. ModuleNotFoundError

```bash
# Symptom
ModuleNotFoundError: No module named 'reportlab'

# Solution
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. TypeError: width parameter

```bash
# Symptom
TypeError: 'str' object cannot be interpreted as an integer

# Cause
Streamlit 1.29.0 doesn't support width="stretch"

# Solution
Fixed, now using use_container_width=True
```

#### 3. Database Locked

```bash
# Symptom
sqlite3.OperationalError: database is locked

# Solution
# Stop all Streamlit instances
killall streamlit
# Restart
streamlit run app.py
```

#### 4. Port in Use

```bash
# Symptom
Address already in use

# Solution 1
lsof -ti:8501 | xargs kill -9

# Solution 2
streamlit run app.py --server.port 8502
```

#### 5. OpenAI API Error

```bash
# Symptom
openai.error.AuthenticationError

# Solution
# 1. Use debug mode for testing
# 2. Verify API Key
# 3. Check account credits
```

### Complete Reset

```bash
# Stop app
killall streamlit

# Remove virtual environment
rm -rf venv

# Remove cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Remove database (optional)
rm study_assistant.db

# Reinstall
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Restart
streamlit run app.py
```

---

## 📦 Version Compatibility

### Current Versions

```
Python: 3.12
Streamlit: 1.29.0
LangChain: 0.1.0
langchain-openai: 0.0.6
OpenAI: 1.109.1
PyPDF2: 3.0.1
ReportLab: 4.4.4
python-dotenv: 1.0.0
```

### API Change History

#### Streamlit API Changes

**1.29.0** (Current)
- Uses `use_container_width=True`
- Uses `st.context.headers` (newer version)
- Backward compatible with `_get_websocket_headers()`

**1.37.0+** (Future)
- Supports `width="stretch"` parameter
- New layout components

### Upgrade Guide

```bash
# Check current version
pip list | grep streamlit

# Upgrade single package
pip install --upgrade streamlit

# Upgrade all packages
pip install --upgrade -r requirements.txt

# Lock versions (recommended for production)
pip freeze > requirements-lock.txt
```

### Compatibility Check

```bash
# Test all imports
python3 << EOF
import streamlit
import langchain
import openai
import PyPDF2
import reportlab
print("✓ All imports successful")
EOF

# Run tests
python3 test_admin_config.py

# Syntax check
python3 -m py_compile app.py
```

---

## 🚀 Deployment Guide

### Local Deployment

```bash
# Use run.command (macOS)
./run.command

# Or manual start
source venv/bin/activate
streamlit run app.py
```

### Server Deployment

```bash
# Run in background
nohup streamlit run app.py --server.headless true &

# Use specific port
streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV ADMIN_PASSWORD=change_me_in_production

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
```

### Streamlit Cloud Deployment

1. Push code to GitHub
2. Visit share.streamlit.io
3. Connect GitHub repository
4. Set environment variables in Secrets
5. Deploy

---

## 🧪 Testing

### Unit Tests

```python
# test_app.py (example)
import pytest
from app import extract_text_from_pdf, parse_quiz_data

def test_parse_quiz_data():
    quiz_text = """Question 1: Test
a) Option A
b) Option B
Answer: a) Option A"""
    
    result = parse_quiz_data(quiz_text)
    assert len(result) == 1
    assert result[0]['answer_key'] == 'a'
```

### Integration Tests

```bash
# Run test suite
pytest tests/

# Coverage testing
pytest --cov=. tests/
```

---

## 📊 Performance Optimization

### Caching Strategy

```python
# Use Streamlit cache
@st.cache_data
def load_data():
    # Cache data loading
    return data

@st.cache_resource
def init_llm():
    # Cache resource initialization
    return ChatOpenAI(...)
```

### Database Optimization

```sql
-- Add indexes
CREATE INDEX idx_sessions_created ON sessions(created_at);
CREATE INDEX idx_generations_session ON generations(session_id);
CREATE INDEX idx_quiz_session ON quiz_results(session_id);
```

---

## 📝 Development Standards

### Code Style

```bash
# Use black formatter
pip install black
black app.py

# Use flake8 linter
pip install flake8
flake8 app.py
```

### Docstrings

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        bool: Description of return value
        
    Raises:
        ValueError: Description of exception
    """
    pass
```

---

## 🔒 Security Recommendations

### Production Checklist

- [ ] Change default admin password
- [ ] Use strong password (8+ chars, mixed case, numbers, symbols)
- [ ] Don't commit .env to version control
- [ ] Regular database backups
- [ ] Restrict Admin Dashboard access
- [ ] Use HTTPS (production deployment)
- [ ] Regular dependency updates
- [ ] Monitor API usage and costs

---

## 📞 Technical Support

### Resources

- **User Guide**: `USER_GUIDE_EN.md`
- **Chinese Version**: `用户指南.md` / `技术文档.md`
- **API Docs**: LangChain / Streamlit / OpenAI official docs

### Contributing

Issues and Pull Requests welcome!

---

**Version**: 1.0  
**Last Updated**: October 19, 2025  
**Maintained by**: Study Assistant Development Team
