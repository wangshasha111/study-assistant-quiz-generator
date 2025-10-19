# 📚 Study Assistant - Quiz Generator

A lightweight, AI-powered study assistant that helps students create effective quizzes for self-assessment. Built with Streamlit and LangChain, this application summarizes study material and generates multiple-choice quiz questions without requiring external databases or vector storage.

## 🌟 Features

- **PDF Text Extraction**: Upload PDF documents and automatically extract text using PyPDF2
- **Smart Summarization**: Get concise bullet-point summaries of study material
- **Quiz Generation**: Automatically generate multiple-choice questions with 4 options
- **Customizable**: Adjust number of questions, AI model, and creativity level
- **No External Dependencies**: Works standalone without vector databases or RAG systems
- **User-Friendly Interface**: Clean, intuitive Streamlit UI
- **Downloadable Results**: Export summaries and quizzes as text files

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Local Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd project_study_assistant_quiz_generation
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your API key** (Optional - can also enter in the app)
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Open your browser** to `http://localhost:8501`

## 🌐 Deploying to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Create a GitHub repository and push this project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file path (`app.py`)
5. Click "Deploy"

### Step 3: Configure Secrets

In Streamlit Cloud, add your OpenAI API key:

1. Go to your app's dashboard
2. Click "Settings" → "Secrets"
3. Add your secrets in TOML format:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```
4. Click "Save"

Your app will automatically redeploy with the secrets configured!

## 📖 Usage Guide

### Uploading Study Material

**Option 1: Upload PDF**
1. Select "Upload PDF" in the input method
2. Click "Browse files" and select your PDF document
3. The app will extract and display the text

**Option 2: Paste Text**
1. Select "Paste Text" in the input method
2. Copy and paste your study material into the text area

### Generating Quiz

1. **Configure settings** in the sidebar:
   - Enter your OpenAI API key
   - Select AI model (GPT-3.5-turbo recommended for cost-effectiveness)
   - Choose number of questions (3-10)
   - Adjust creativity/temperature (0.7 recommended)

2. **Click "Generate Summary & Quiz"**

3. **Review results**:
   - View the summarized bullet points
   - Read through the generated quiz questions
   - Download results as a text file

## 🎯 Example

### Input:
**Topic:** Prompt Engineering for Agents

**Study Material:**
```
Prompt engineering involves designing and refining inputs to language models to 
achieve desired outputs. In the context of agents, prompt engineering allows for 
better control over how an agent interacts with the environment and solves specific 
tasks. This is particularly useful in domains like robotics and conversational AI. 
By adjusting the structure and content of the prompts, users can enhance an agent's 
performance on specific tasks.
```

### Output:

**Summary:**
- Prompt engineering refines inputs to language models for better output control
- In agent-based systems, it helps control agent behavior and task performance
- Useful in robotics and conversational AI

**Quiz Questions:**
1. What is the primary goal of prompt engineering in agent-based systems?
   - a) To optimize agent memory
   - b) To refine inputs for better output control ✓
   - c) To improve agent hardware
   - d) To increase computational power

2. In which domain is prompt engineering most commonly used for enhancing agent performance?
   - a) Image recognition
   - b) Conversational AI ✓
   - c) Data processing
   - d) Video editing

## 🛠️ Technology Stack

- **Streamlit**: Web application framework
- **LangChain**: LLM orchestration and prompt management
- **OpenAI GPT**: Language model for generation
- **PyPDF2**: PDF text extraction
- **Python-dotenv**: Environment variable management

## 📁 Project Structure

```
project_study_assistant_quiz_generation/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── sample_material.pdf   # Sample study material (optional)
```

## 🔧 Configuration Options

### Sidebar Settings

- **OpenAI API Key**: Your OpenAI API key for accessing GPT models
- **Model Selection**: Choose between GPT-3.5-turbo, GPT-4, or GPT-4-turbo
- **Number of Questions**: Generate 3-10 quiz questions
- **Temperature**: Control creativity (0.0 = focused, 1.0 = creative)

### Environment Variables (Optional)

Create a `.env` file:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
```

## 💡 Tips for Best Results

1. **Study Material Quality**: Provide clear, well-structured content for better summaries
2. **Length**: Works best with 500-5000 words of content
3. **Model Selection**: 
   - Use GPT-3.5-turbo for quick, cost-effective results
   - Use GPT-4 for higher quality and more accurate questions
4. **Temperature**: Keep at 0.7 for balanced creativity and accuracy
5. **Number of Questions**: 5-7 questions work best for most topics

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🙋 Support

If you encounter any issues or have questions:
1. Check the configuration in the sidebar
2. Verify your OpenAI API key is valid
3. Ensure your PDF is text-based (not scanned images)
4. Check the browser console for errors

## 🎓 Educational Context

This project was developed as part of a course on "Introduction to LangChain for Agentic Systems". It demonstrates:
- Practical application of LangChain for educational purposes
- Lightweight alternatives to RAG systems
- Prompt engineering for specific tasks
- Building deployable AI applications with Streamlit

## 🚀 Future Enhancements

Potential improvements:
- [ ] Support for multiple file formats (DOCX, TXT, etc.)
- [ ] Question difficulty levels
- [ ] True/False and fill-in-the-blank questions
- [ ] Quiz taking mode with score tracking
- [ ] Export to different formats (PDF, JSON, etc.)
- [ ] Multi-language support
- [ ] Flashcard generation

---

**Built with ❤️ using Streamlit, LangChain, and OpenAI**

No external databases required! 🚀
