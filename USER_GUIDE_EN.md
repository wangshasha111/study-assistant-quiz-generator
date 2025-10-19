# 📚 Study Assistant - User Guide

## 🎯 Introduction

Study Assistant is an AI-powered learning assistant that can:
- 📄 Extract content from PDFs or text
- 📝 Automatically generate study summaries
- ❓ Create interactive quiz questions
- 💾 Download study materials in PDF/TXT format
- 📊 Admin dashboard for tracking user learning data

---

## 🚀 Quick Start

### 1. Launch the Application

**Method 1: Double-click (Easiest)**
```bash
Double-click run.command file
```

**Method 2: Command Line**
```bash
# Navigate to project directory
cd project_study_assistant_quiz_generation

# Activate virtual environment
source venv/bin/activate

# Start application
streamlit run app.py
```

Application opens in browser: `http://localhost:8501`

### 2. Basic Workflow

#### Step 1: Upload Study Material
- Select input method in sidebar:
  - **Upload PDF**: Upload PDF file
  - **Paste Text**: Paste text content directly

#### Step 2: Configure Settings
- **OpenAI API Key**: Enter your API key (or use debug mode)
- **Model Selection**: Choose GPT model (default: gpt-3.5-turbo)
- **Number of Questions**: Set quiz question count (3-10)
- **Creativity**: Adjust temperature parameter (0.0-1.0)

#### Step 3: Generate Content
Click **🚀 Generate Summary & Quiz** button

#### Step 4: View Results
- **Left**: 📋 Study Summary
- **Right**: 📝 Interactive Quiz

#### Step 5: Complete Quiz
1. Select answers for each question
2. Click **📤 Submit Quiz** to submit
3. View score and detailed explanations
4. Optional: Click **🔄 Retake Quiz** to retry

#### Step 6: Download Materials
- **📄 Download as Text**: Download TXT format
- **📕 Download as PDF**: Download PDF format (includes quiz results)

---

## 🐛 Debug Mode (Free Testing)

No API Key required, uses mock data to test all features.

### How to Enable
1. Find **🐛 Debug Mode** in sidebar
2. Toggle **Enable Debug Mode** switch
3. Click **🐛 Generate Mock Data (Debug)** button

### Debug Mode Features
- ✅ No API Key needed
- ✅ No payment required
- ✅ Instant results
- ✅ Full feature testing
- ✅ Uses Prompt Engineering sample data

---

## 👤 User Features

### Enter Username (Optional)
Fill in **👤 Your Name** field in sidebar to help admin track your progress.

### Interactive Quiz
- **Select Answers**: Click radio buttons
- **Submit Quiz**: Click submit when done
- **View Results**:
  - ✅ Correct answer: Green display
  - ❌ Wrong answer: Red display with correct answer
  - ⚠️ Unanswered: Yellow warning
- **Score Statistics**:
  - Score (X/Total)
  - Percentage
  - Answered count
  - Grade (Excellent/Good/Keep Learning)

### Switch Modes
- **Interactive Mode** (default): Can select and submit answers
- **View Mode**: Display all answers directly

Click top-right button to switch:
- **✏️ Take Quiz**: Switch to interactive mode
- **👁️ View Mode**: Switch to view mode

---

## 📊 Admin Features

### Login to Admin Dashboard

1. Click **📊 Admin Dashboard** in sidebar
2. Enter admin password (default: `admin123`)
3. Click **🔓 Login**

### Admin Panel Features

#### 1. Overall Statistics
- Total sessions
- Total generations
- Quiz completions
- Average quiz score
- Active users (24h)

#### 2. Sessions List
- View all user sessions
- Search: by session ID, username, IP address
- Filter: show last N sessions
- Export: download CSV format

#### 3. Session Details
Select specific session to view:
- User info (username, IP, User Agent)
- Generation records (time, file, model, content length)
- Quiz results (score, percentage, detailed answers)
- Export: download JSON format

#### 4. Logout
Click **🚪 Logout** in sidebar to exit admin panel

---

## 🔐 Admin Password Management

### View Current Password
```bash
cat .env
```

### Reset Password

**Method 1: Using Reset Tool (Recommended)**
```bash
python3 reset_admin_password.py
```
Follow prompts to enter new password, tool validates password strength.

**Method 2: Direct Edit**
```bash
# Edit .env file
nano .env

# Modify this line
ADMIN_PASSWORD=your_new_password

# Save and restart application
```

**Method 3: Quick Command Line**
```bash
echo "ADMIN_PASSWORD=new_password" > .env
```

### Disable Admin Dashboard
```bash
# Remove or comment out password
echo "# ADMIN_PASSWORD=" > .env
```

---

## 💾 Download Features

### TXT Format
- Complete summary
- All quiz questions and answers
- Quiz results (if completed)
- Formatted text, easy to read

### PDF Format
- Professional layout
- Color-coded (correct/wrong answers)
- Highlighted quiz results
- Includes timestamp
- Printable, shareable

---

## ❓ FAQ

### Q: Forgot admin password?
A: Check .env file: `cat .env`

### Q: How to test features for free?
A: Enable debug mode, no API Key needed

### Q: Can I modify quiz after submission?
A: Yes, click "🔄 Retake Quiz" to retry

### Q: Do downloads include quiz results?
A: Yes, if quiz submitted, downloads include detailed results

### Q: Can I switch to Chinese?
A: Current version is Chinese interface, see 用户指南.md

### Q: How to stop application?
A: Press `Ctrl+C` in terminal running Streamlit

### Q: Why can't I access Admin Dashboard?
A: Need to set ADMIN_PASSWORD environment variable

### Q: Where is data stored?
A: SQLite database file: `study_assistant.db`

---

## 🔧 Troubleshooting

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Issue: Port Already in Use

**Solution:**
```bash
# Find process using port
lsof -ti:8501

# Kill process
kill -9 $(lsof -ti:8501)

# Or use different port
streamlit run app.py --server.port 8502
```

### Issue: Admin Dashboard Error

**Solution:**
```bash
# Check if password is set
cat .env

# Reset password
python3 reset_admin_password.py
```

### Issue: API Key Error

**Solution:**
1. Use debug mode for testing
2. Verify API Key is correct
3. Confirm OpenAI account has credits

### More Issues?
See full troubleshooting docs or reinstall:
```bash
# Complete reset
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 📋 Quick Command Reference

```bash
# Start application
source venv/bin/activate && streamlit run app.py

# Test configuration
python3 test_admin_config.py

# Reset password
python3 reset_admin_password.py

# Stop application
Press Ctrl+C

# View admin password
cat .env

# Install dependencies
pip install -r requirements.txt
```

---

## 📞 Get Help

- **Technical Docs**: `TECHNICAL_GUIDE_EN.md`
- **Chinese Version**: `用户指南.md`
- **Project Home**: README.md

---

**Version**: 1.0  
**Last Updated**: October 19, 2025  
**Support**: Python 3.8+, Streamlit 1.29.0+
