import streamlit as st
import PyPDF2
from io import BytesIO
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import re
from typing import Dict, List
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, will use system environment variables
    pass

# Import database and session tracking
from database import DatabaseManager
from session_utils import get_session_id, get_client_ip, get_user_agent

# Page configuration
st.set_page_config(
    page_title="Study Assistant - Quiz Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .summary-box {
        background-color: #E3F2FD;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .summary-box h3, .summary-box h4 {
        color: #1565C0;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .summary-box ul {
        margin-left: 1rem;
    }
    .summary-box li {
        margin-bottom: 0.3rem;
        line-height: 1.6;
    }
    .summary-box p {
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    .quiz-box {
        background-color: #F3E5F5;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .question-card {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #9C27B0;
    }
    .option {
        padding: 0.5rem;
        margin: 0.3rem 0;
        background-color: #f8f9fa;
        border-radius: 5px;
        border-left: 3px solid #ddd;
    }
    .correct-answer {
        background-color: #d4edda;
        border-left: 3px solid #28a745;
        padding: 0.5rem;
        margin-top: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .bullet-point {
        padding: 0.3rem 0;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


def parse_and_display_summary(summary: str):
    """
    Parse and display summary in a structured format
    """
    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
    st.subheader("📋 Summary")
    
    # Split by lines
    lines = summary.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if it's a header line (starts with ###, ##, or #)
        if line.startswith('#'):
            # Render as markdown header
            st.markdown(line)
        # Check if it starts with a bullet point
        elif re.match(r'^[-•*]\s*', line):
            # Keep the bullet point and render with markdown support
            st.markdown(line)
        # Check if it looks like a sub-point (starts with spaces or tabs and bullet)
        elif re.match(r'^\s+[-•*]\s*', line):
            # Keep the indentation and bullet
            st.markdown(line)
        else:
            # For other lines, add bullet point if it's substantial content
            if len(line) > 0:
                st.markdown(f"• {line}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def parse_quiz_data(quiz: str) -> list:
    """
    Parse quiz string into structured data
    
    Returns:
        list: List of dicts with question data
    """
    questions_data = []
    
    # Split questions by "Question" keyword
    questions = re.split(r'Question\s+\d+:', quiz)
    questions = [q.strip() for q in questions if q.strip()]
    
    for i, question_block in enumerate(questions, 1):
        lines = question_block.strip().split('\n')
        
        question_text = ""
        options = {}
        answer_key = ""
        answer_text = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if it's an option
            option_match = re.match(r'^([a-d])\)\s*(.+)', line, re.IGNORECASE)
            if option_match:
                key = option_match.group(1).lower()
                text = option_match.group(2).strip()
                options[key] = text
            # Check if it's the answer line
            elif re.match(r'^Answer:', line, re.IGNORECASE):
                answer_full = re.sub(r'^Answer:\s*', '', line, flags=re.IGNORECASE)
                # Extract answer key (a, b, c, or d)
                answer_match = re.match(r'^([a-d])\)', answer_full, re.IGNORECASE)
                if answer_match:
                    answer_key = answer_match.group(1).lower()
                    answer_text = answer_full
            # Otherwise, it's part of the question
            elif not options and not answer_key:
                question_text += " " + line
        
        questions_data.append({
            'id': i,
            'question': question_text.strip(),
            'options': options,
            'answer_key': answer_key,
            'answer_text': answer_text
        })
    
    return questions_data


def display_interactive_quiz(quiz: str):
    """
    Display quiz in interactive mode where users can select answers
    """
    st.markdown('<div class="quiz-box">', unsafe_allow_html=True)
    
    # Add mode toggle
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.subheader("📝 Interactive Quiz")
    with col_header2:
        if st.button("👁️ View Mode", help="Switch to view-only mode with answers"):
            st.session_state.quiz_mode = 'view'
            st.rerun()
    
    # Parse quiz data
    questions_data = parse_quiz_data(quiz)
    
    # Display each question
    for q_data in questions_data:
        q_id = q_data['id']
        
        st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f"**Question {q_id}:** {q_data['question']}")
        st.markdown("")
        
        # Create radio buttons for options
        options_list = [f"{k}) {v}" for k, v in sorted(q_data['options'].items())]
        
        # Get current answer
        current_answer = st.session_state.user_answers.get(q_id, None)
        
        # Show result if submitted
        if st.session_state.quiz_submitted:
            selected = st.radio(
                f"Select your answer:",
                options_list,
                index=None if current_answer is None else ord(current_answer) - ord('a'),
                key=f"q_{q_id}",
                disabled=True
            )
            
            # Show if correct or incorrect
            if current_answer:
                is_correct = current_answer == q_data['answer_key']
                if is_correct:
                    st.markdown(f'<div class="correct-answer">✅ Correct! Answer: {q_data["answer_text"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="background-color: #f8d7da; border-left: 3px solid #dc3545; padding: 0.5rem; margin-top: 0.5rem; border-radius: 5px; font-weight: bold;">❌ Incorrect. Correct answer: {q_data["answer_text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color: #fff3cd; border-left: 3px solid #ffc107; padding: 0.5rem; margin-top: 0.5rem; border-radius: 5px;">⚠️ Not answered. Correct answer: {q_data["answer_text"]}</div>', unsafe_allow_html=True)
        else:
            # Interactive mode
            selected = st.radio(
                f"Select your answer:",
                options_list,
                index=None if current_answer is None else ord(current_answer) - ord('a'),
                key=f"q_{q_id}"
            )
            
            # Update answer in session state
            if selected:
                answer_key = selected[0].lower()
                st.session_state.user_answers[q_id] = answer_key
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    if not st.session_state.quiz_submitted:
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📤 Submit Quiz", type="primary", use_container_width=True):
                if len(st.session_state.user_answers) == 0:
                    st.warning("⚠️ Please answer at least one question before submitting!")
                else:
                    st.session_state.quiz_submitted = True
                    
                    # Log quiz result to database
                    if st.session_state.generation_id:
                        try:
                            from database import DatabaseManager
                            from session_utils import get_session_id
                            
                            db = DatabaseManager()
                            session_id = get_session_id()
                            
                            # Calculate results
                            correct_count = sum(
                                1 for q_data in questions_data
                                if st.session_state.user_answers.get(q_data['id']) == q_data['answer_key']
                            )
                            total_count = len(questions_data)
                            answered_count = len(st.session_state.user_answers)
                            
                            # Log to database
                            db.log_quiz_result(
                                session_id=session_id,
                                generation_id=st.session_state.generation_id,
                                score=correct_count,
                                total_questions=total_count,
                                answered_count=answered_count,
                                user_answers=st.session_state.user_answers
                            )
                        except Exception as e:
                            # Don't fail if logging fails
                            pass
                    
                    st.rerun()
    else:
        # Show score
        correct_count = sum(
            1 for q_data in questions_data
            if st.session_state.user_answers.get(q_data['id']) == q_data['answer_key']
        )
        total_count = len(questions_data)
        answered_count = len(st.session_state.user_answers)
        percentage = (correct_count / total_count * 100) if total_count > 0 else 0
        
        st.markdown("---")
        st.markdown("### 📊 Quiz Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Score", f"{correct_count}/{total_count}")
        with col2:
            st.metric("Percentage", f"{percentage:.1f}%")
        with col3:
            st.metric("Answered", f"{answered_count}/{total_count}")
        with col4:
            if percentage >= 80:
                st.metric("Grade", "🌟 Excellent")
            elif percentage >= 60:
                st.metric("Grade", "👍 Good")
            else:
                st.metric("Grade", "📚 Keep Learning")
        
        # Reset button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Retake Quiz", use_container_width=True):
                st.session_state.user_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def parse_and_display_quiz(quiz: str):
    """
    Parse and display quiz questions in a structured, card-based format
    Now with view mode toggle
    """
    st.markdown('<div class="quiz-box">', unsafe_allow_html=True)
    
    # Add mode toggle
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.subheader("📝 Quiz Questions (View Mode)")
    with col_header2:
        if st.button("✏️ Take Quiz", help="Switch to interactive mode"):
            st.session_state.quiz_mode = 'interactive'
            st.session_state.user_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()
    
    # Split questions by "Question" keyword
    questions = re.split(r'Question\s+\d+:', quiz)
    questions = [q.strip() for q in questions if q.strip()]
    
    for i, question_block in enumerate(questions, 1):
        # Create a card for each question
        st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
        
        # Split into lines
        lines = question_block.strip().split('\n')
        
        # Extract question text (first non-empty line)
        question_text = ""
        options = []
        answer = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if it's an option (a), b), c), d))
            if re.match(r'^[a-d]\)', line, re.IGNORECASE):
                options.append(line)
            # Check if it's the answer line
            elif re.match(r'^Answer:', line, re.IGNORECASE):
                answer = re.sub(r'^Answer:\s*', '', line, flags=re.IGNORECASE)
            # Otherwise, it's part of the question
            elif not options and not answer:
                question_text += " " + line
        
        # Display question
        st.markdown(f"**Question {i}:** {question_text.strip()}")
        st.markdown("")  # Add spacing
        
        # Display options in a structured way
        if options:
            for option in options:
                st.markdown(f'<div class="option">{option}</div>', unsafe_allow_html=True)
        
        # Display answer
        if answer:
            st.markdown(f'<div class="correct-answer">✓ Answer: {answer}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def generate_pdf(summary: str, quiz: str) -> BytesIO:
    """
    Generate a formatted PDF with summary and quiz questions
    
    Args:
        summary: Summary text
        quiz: Quiz questions text
        
    Returns:
        BytesIO: PDF file in memory
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for the PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1E88E5'),
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#1565C0'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=16
    )
    
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['BodyText'],
        fontSize=12,
        fontName='Helvetica-Bold',
        spaceAfter=8,
        spaceBefore=10
    )
    
    option_style = ParagraphStyle(
        'OptionStyle',
        parent=styles['BodyText'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=4
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=HexColor('#28a745'),
        fontName='Helvetica-Bold',
        leftIndent=20,
        spaceAfter=6,
        spaceBefore=6
    )
    
    # Add title
    elements.append(Paragraph("📚 Study Assistant - Quiz Generator", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Add summary section
    elements.append(Paragraph("📋 Summary", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Process summary lines
    summary_lines = summary.strip().split('\n')
    for line in summary_lines:
        line = line.strip()
        if line:
            # Remove markdown bold syntax for PDF
            line = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line)
            # Handle headers
            if line.startswith('###'):
                line = re.sub(r'^###\s*', '', line)
                elements.append(Paragraph(line, heading_style))
            elif line.startswith('##'):
                line = re.sub(r'^##\s*', '', line)
                elements.append(Paragraph(line, heading_style))
            else:
                # Add bullet point if not present
                if not re.match(r'^[-•*]', line):
                    line = '• ' + line
                elements.append(Paragraph(line, body_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Add quiz section
    elements.append(Paragraph("📝 Quiz Questions", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Parse quiz questions
    questions = re.split(r'Question\s+\d+:', quiz)
    questions = [q.strip() for q in questions if q.strip()]
    
    for i, question_block in enumerate(questions, 1):
        lines = question_block.strip().split('\n')
        
        question_text = ""
        options = []
        answer = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if re.match(r'^[a-d]\)', line, re.IGNORECASE):
                options.append(line)
            elif re.match(r'^Answer:', line, re.IGNORECASE):
                answer = re.sub(r'^Answer:\s*', '', line, flags=re.IGNORECASE)
            elif not options and not answer:
                question_text += " " + line
        
        # Add question
        elements.append(Paragraph(f"<b>Question {i}:</b> {question_text.strip()}", question_style))
        
        # Add options
        for option in options:
            elements.append(Paragraph(option, option_style))
        
        # Add answer
        if answer:
            elements.append(Paragraph(f"✓ Answer: {answer}", answer_style))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # Add footer
    elements.append(Spacer(1, 0.3*inch))
    footer_text = "Generated with Study Assistant | Built with Streamlit, LangChain, and OpenAI"
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_pdf_with_results(summary: str, quiz: str, user_answers: dict = None) -> BytesIO:
    """
    Generate a formatted PDF with summary, quiz questions, and user results
    
    Args:
        summary: Summary text
        quiz: Quiz questions text
        user_answers: Dict of user answers {question_id: answer_key}
        
    Returns:
        BytesIO: PDF file in memory
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for the PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1E88E5'),
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#1565C0'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=16
    )
    
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['BodyText'],
        fontSize=12,
        fontName='Helvetica-Bold',
        spaceAfter=8,
        spaceBefore=10
    )
    
    option_style = ParagraphStyle(
        'OptionStyle',
        parent=styles['BodyText'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=4
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=HexColor('#28a745'),
        fontName='Helvetica-Bold',
        leftIndent=20,
        spaceAfter=6,
        spaceBefore=6
    )
    
    incorrect_style = ParagraphStyle(
        'IncorrectStyle',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=HexColor('#dc3545'),
        fontName='Helvetica-Bold',
        leftIndent=20,
        spaceAfter=6,
        spaceBefore=6
    )
    
    # Add title
    elements.append(Paragraph("📚 Study Assistant - Quiz Generator", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Add summary section
    elements.append(Paragraph("📋 Summary", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Process summary lines
    summary_lines = summary.strip().split('\n')
    for line in summary_lines:
        line = line.strip()
        if line:
            line = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line)
            if line.startswith('###'):
                line = re.sub(r'^###\s*', '', line)
                elements.append(Paragraph(line, heading_style))
            elif line.startswith('##'):
                line = re.sub(r'^##\s*', '', line)
                elements.append(Paragraph(line, heading_style))
            else:
                if not re.match(r'^[-•*]', line):
                    line = '• ' + line
                elements.append(Paragraph(line, body_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Parse quiz questions
    questions_data = parse_quiz_data(quiz)
    
    # Add Quiz Results Summary Box if available (before quiz questions)
    if user_answers:
        correct_count = sum(
            1 for q in questions_data
            if user_answers.get(q['id']) == q['answer_key']
        )
        total_count = len(questions_data)
        answered_count = len(user_answers)
        percentage = (correct_count / total_count * 100) if total_count > 0 else 0
        
        # Determine grade
        if percentage >= 80:
            grade = "🌟 Excellent"
            grade_color = HexColor('#28a745')
        elif percentage >= 60:
            grade = "👍 Good"
            grade_color = HexColor('#17a2b8')
        else:
            grade = "📚 Keep Learning"
            grade_color = HexColor('#ffc107')
        
        # Results heading style
        results_heading_style = ParagraphStyle(
            'ResultsHeading',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=HexColor('#dc3545'),
            spaceAfter=15,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        results_box_style = ParagraphStyle(
            'ResultsBox',
            parent=styles['BodyText'],
            fontSize=13,
            fontName='Helvetica-Bold',
            spaceAfter=6,
            leading=20
        )
        
        grade_style = ParagraphStyle(
            'GradeStyle',
            parent=styles['BodyText'],
            fontSize=14,
            textColor=grade_color,
            fontName='Helvetica-Bold',
            spaceAfter=8,
            spaceBefore=4
        )
        
        # Add prominent results section
        elements.append(Paragraph("📊 QUIZ RESULTS", results_heading_style))
        elements.append(Spacer(1, 0.05*inch))
        elements.append(Paragraph("="*70, styles['Code']))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph("<b>PERFORMANCE SUMMARY:</b>", results_box_style))
        elements.append(Paragraph(f"Score: <font color='#1E88E5'><b>{correct_count}/{total_count}</b></font> questions correct", results_box_style))
        elements.append(Paragraph(f"Percentage: <font color='#1E88E5'><b>{percentage:.1f}%</b></font>", results_box_style))
        elements.append(Paragraph(f"Answered: {answered_count}/{total_count} questions", results_box_style))
        elements.append(Paragraph(f"Grade: {grade}", grade_style))
        
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("="*70, styles['Code']))
        elements.append(Spacer(1, 0.3*inch))
    
    # Add quiz section
    elements.append(Paragraph("📝 Quiz Questions & Answers", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    for q in questions_data:
        # Add question
        elements.append(Paragraph(f"<b>Question {q['id']}:</b> {q['question']}", question_style))
        
        # Add options
        for key in sorted(q['options'].keys()):
            option_text = f"{key}) {q['options'][key]}"
            # Highlight user's answer if provided
            if user_answers and user_answers.get(q['id']) == key:
                option_text = f"<b>[YOUR ANSWER]</b> {option_text}"
            elements.append(Paragraph(option_text, option_style))
        
        # Add correct answer and status
        if user_answers:
            user_answer = user_answers.get(q['id'])
            is_correct = user_answer == q['answer_key']
            
            if is_correct:
                elements.append(Paragraph(f"✅ CORRECT - Answer: {q['answer_text']}", answer_style))
            else:
                if user_answer:
                    elements.append(Paragraph(f"❌ INCORRECT - Correct answer: {q['answer_text']}", incorrect_style))
                else:
                    elements.append(Paragraph(f"⚠️ NOT ANSWERED - Correct answer: {q['answer_text']}", answer_style))
        else:
            elements.append(Paragraph(f"✓ Answer: {q['answer_text']}", answer_style))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # Add footer
    elements.append(Spacer(1, 0.3*inch))
    footer_text = "Generated with Study Assistant | Built with Streamlit, LangChain, and OpenAI"
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text content from uploaded PDF file using PyPDF2
    
    Args:
        pdf_file: Uploaded PDF file object
        
    Returns:
        str: Extracted text content from PDF
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = ""
        
        for page in pdf_reader.pages:
            text_content += page.extract_text()
        
        return text_content.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""


def summarize_content(llm, content: str) -> str:
    """
    Summarize the study material into concise bullet points
    
    Args:
        llm: Language model instance
        content: Study material text
        
    Returns:
        str: Summarized content in bullet points
    """
    summary_template = """You are an educational assistant helping students study effectively.

Study Material:
{content}

Please summarize the above study material into clear, concise bullet points that capture the key concepts and important information. 
Focus on the main ideas and essential facts that students should remember.

Summary:"""

    summary_prompt = PromptTemplate(
        input_variables=["content"],
        template=summary_template
    )
    
    # Create chain using LCEL (LangChain Expression Language)
    summary_chain = summary_prompt | llm | StrOutputParser()
    
    try:
        summary = summary_chain.invoke({"content": content})
        return summary.strip()
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return ""


def generate_quiz_questions(llm, content: str, num_questions: int = 5) -> str:
    """
    Generate multiple-choice quiz questions based on the study material
    
    Args:
        llm: Language model instance
        content: Study material text
        num_questions: Number of questions to generate
        
    Returns:
        str: Generated quiz questions with options and answers
    """
    quiz_template = """You are an educational assistant creating quiz questions for students.

Study Material:
{content}

Based on the above study material, generate {num_questions} multiple-choice quiz questions that test understanding of the key concepts.

For each question:
1. Create a clear, specific question
2. Provide 4 answer options (a, b, c, d)
3. Make sure only one option is correct
4. Indicate the correct answer
5. Ensure questions cover different aspects of the material

Format each question exactly as follows:

Question 1: [Your question here]
a) [Option A]
b) [Option B]
c) [Option C]
d) [Option D]
Answer: [Correct option letter]) [Correct answer text]

Quiz Questions:"""

    quiz_prompt = PromptTemplate(
        input_variables=["content", "num_questions"],
        template=quiz_template
    )
    
    # Create chain using LCEL (LangChain Expression Language)
    quiz_chain = quiz_prompt | llm | StrOutputParser()
    
    try:
        questions = quiz_chain.invoke({"content": content, "num_questions": num_questions})
        return questions.strip()
    except Exception as e:
        st.error(f"Error generating quiz questions: {str(e)}")
        return ""


def get_mock_summary() -> str:
    """Return mock summary data for debugging"""
    return """### Summary of Prompt Engineering

• **Definition**:
• Prompt engineering is a practice in natural language processing (NLP) where text describes the task for AI to generate an appropriate output.

• **Prompts**:
• Detailed descriptions of desired outputs from AI models, guiding user-model interaction.
• Effectiveness hinges on the quality of prompt design.

• **Examples of Prompts**:
• **Text Prompts**: Inquiries or tasks for language models (e.g., generating articles, defining terms).
• **Code Prompts**: Requests for coding tasks (e.g., writing functions, debugging code).
• **Image Prompts**: Descriptions for generating visual content (e.g., illustrations, scenes).

• **Tips for Effective Prompt Engineering**:
• **Role Playing**: Specify the role of the model to direct the interaction.
• **Clarity**: Be concise and clear to minimize ambiguity.
• **Context**: Provide sufficient background information.
• **Iteration**: Refine prompts based on output quality."""


def get_mock_quiz() -> str:
    """Return mock quiz data for debugging"""
    return """Question 1: What is the primary goal of prompt engineering in agent-based systems?
a) To optimize agent memory
b) To refine inputs for better output control
c) To improve agent hardware
d) To increase computational power
Answer: b) To refine inputs for better output control

Question 2: In which domain is prompt engineering most commonly used for enhancing agent performance?
a) Image recognition
b) Conversational AI
c) Data processing
d) Video editing
Answer: b) Conversational AI

Question 3: What is a key characteristic of effective prompts?
a) They should be as long as possible
b) They should be vague and open-ended
c) They should be clear and specific
d) They should avoid any context
Answer: c) They should be clear and specific

Question 4: Which of the following is NOT an example of prompt engineering application?
a) Text generation
b) Code writing
c) Hardware manufacturing
d) Image generation
Answer: c) Hardware manufacturing

Question 5: What does "context window" refer to in prompt engineering?
a) The visual display of the prompt
b) The amount of text a model can process at once
c) The time taken to generate output
d) The number of users accessing the model
Answer: b) The amount of text a model can process at once"""


def main():
    """Main application function"""
    
    # Initialize database
    db = DatabaseManager()
    
    # Get session info
    session_id = get_session_id()
    client_ip = get_client_ip()
    user_agent = get_user_agent()
    
    # Initialize session state for storing results
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'quiz_mode' not in st.session_state:
        st.session_state.quiz_mode = 'interactive'  # 'interactive' or 'view'
    if 'generation_id' not in st.session_state:
        st.session_state.generation_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    # Header
    st.markdown('<h1 class="main-header">📚 Study Assistant - Quiz Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your study material and get instant summaries and quiz questions!</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration and upload
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Optional username input
        username = st.text_input(
            "👤 Your Name (Optional)",
            value=st.session_state.username or "",
            help="Enter your name to track your progress",
            placeholder="Anonymous"
        )
        if username:
            st.session_state.username = username
        
        # Update session in database
        db.create_or_update_session(
            session_id=session_id,
            username=username or None,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        st.markdown("---")
        
        # Debug Mode Toggle
        st.markdown("### 🐛 Debug Mode")
        debug_mode = st.toggle(
            "Enable Debug Mode",
            value=st.session_state.debug_mode,
            help="Use mock data instead of calling OpenAI API (saves money during testing)"
        )
        st.session_state.debug_mode = debug_mode
        
        if debug_mode:
            st.success("🐛 Debug Mode Active - Using Mock Data")
            st.info("💰 No API calls will be made")
        
        st.markdown("---")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key. Get one at https://platform.openai.com/api-keys",
            value=os.getenv("OPENAI_API_KEY", ""),
            disabled=debug_mode  # Disable when in debug mode
        )
        
        # Model selection
        model_name = st.selectbox(
            "Select Model",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "gpt-4o", "gpt-4o-mini"],
            index=0,
            help="Choose the OpenAI model to use",
            disabled=debug_mode  # Disable when in debug mode
        )
        
        # Number of questions
        num_questions = st.slider(
            "Number of Quiz Questions",
            min_value=3,
            max_value=10,
            value=5,
            help="Select how many quiz questions to generate",
            disabled=debug_mode  # Disable when in debug mode
        )
        
        # Temperature setting
        temperature = st.slider(
            "Creativity (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make output more creative but less focused",
            disabled=debug_mode  # Disable when in debug mode
        )
        
        st.markdown("---")
        
        # Upload Study Material Section
        with st.expander("📤 Upload Study Material", expanded=True):
            # Input method selection
            input_method = st.radio(
                "Choose input method:",
                ["Upload PDF", "Paste Text"],
                horizontal=False
            )
            
            study_content = ""
            uploaded_file_name = None
            uploaded_file_size = None
            
            if input_method == "Upload PDF":
                uploaded_file = st.file_uploader(
                    "Choose a PDF file",
                    type=['pdf'],
                    help="Upload a PDF containing your study material"
                )
                
                if uploaded_file is not None:
                    uploaded_file_name = uploaded_file.name
                    uploaded_file_size = uploaded_file.size
                    
                    with st.spinner("Extracting text from PDF..."):
                        study_content = extract_text_from_pdf(uploaded_file)
                        
                    if study_content:
                        st.success(f"✅ Extracted {len(study_content)} characters")
                        with st.expander("View extracted text"):
                            st.text_area("Content", study_content, height=150, key="sidebar_pdf_preview")
            else:
                study_content = st.text_area(
                    "Paste your study material:",
                    height=200,
                    placeholder="Enter or paste your study material here...",
                    key="sidebar_text_input"
                )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This Study Assistant uses LangChain and OpenAI to:
        - 📄 Extract text from PDFs
        - 📝 Summarize study material
        - ❓ Generate quiz questions
        
        No external databases required!
        """)
        
        if debug_mode:
            st.markdown("---")
            st.markdown("### 🐛 Debug Mode Info")
            st.markdown("""
            **Debug Mode is Active:**
            - ✅ No API calls made
            - ✅ No costs incurred
            - ✅ Instant mock results
            - ✅ Perfect for UI testing
            - ✅ Perfect for format testing
            
            **Mock data includes:**
            - Sample summary on Prompt Engineering
            - 5 multiple-choice questions
            - All formatting features
            """)
    
    # Main content area - Full width for content display
    st.header("🎯 Generate Quiz")
    
    # Check conditions based on debug mode
    if debug_mode:
        # In debug mode, we don't need API key or content
        can_generate = True
        if not study_content:
            st.info("ℹ️ Debug Mode: You can generate with or without study material")
    else:
        # In normal mode, need API key
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to continue.")
            can_generate = False
        elif not study_content:
            st.info("👆 Please upload a PDF or paste text in the sidebar to get started.")
            can_generate = False
        else:
            can_generate = True
    
    if can_generate or debug_mode:
        # Change button label based on mode
        button_label = "🐛 Generate Mock Data (Debug)" if debug_mode else "🚀 Generate Summary & Quiz"
        button_type = "secondary" if debug_mode else "primary"
        
        if st.button(button_label, type=button_type, use_container_width=True):
            try:
                if debug_mode:
                    # Use mock data in debug mode
                    with st.spinner("🐛 Loading mock data..."):
                        import time
                        time.sleep(1)  # Simulate some processing time
                        st.session_state.summary = get_mock_summary()
                        st.session_state.quiz = get_mock_quiz()
                    st.success("✅ Mock data loaded successfully!")
                    
                    # Log generation to database
                    generation_id = db.log_generation(
                        session_id=session_id,
                        file_name=uploaded_file_name if input_method == "Upload PDF" else None,
                        file_size=uploaded_file_size if input_method == "Upload PDF" else None,
                        content_length=len(study_content) if study_content else 0,
                        input_method=input_method.lower().replace(" ", "_"),
                        summary=st.session_state.summary,
                        quiz=st.session_state.quiz,
                        model_used="mock",
                        debug_mode=True
                    )
                    st.session_state.generation_id = generation_id
                    
                else:
                    # Normal mode - call OpenAI API
                    # Initialize LLM
                    llm = ChatOpenAI(
                        model_name=model_name,
                        temperature=temperature,
                        openai_api_key=api_key
                    )
                    
                    # Generate summary
                    with st.spinner("📝 Generating summary..."):
                        summary = summarize_content(llm, study_content)
                        st.session_state.summary = summary
                    
                    # Generate quiz questions
                    with st.spinner("❓ Generating quiz questions..."):
                        quiz = generate_quiz_questions(llm, study_content, num_questions)
                        st.session_state.quiz = quiz
                    
                    # Log generation to database
                    generation_id = db.log_generation(
                        session_id=session_id,
                        file_name=uploaded_file_name if input_method == "Upload PDF" else None,
                        file_size=uploaded_file_size if input_method == "Upload PDF" else None,
                        content_length=len(study_content),
                        input_method=input_method.lower().replace(" ", "_"),
                        summary=st.session_state.summary,
                        quiz=st.session_state.quiz,
                        model_used=model_name,
                        debug_mode=False
                    )
                    st.session_state.generation_id = generation_id
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                if not debug_mode:
                    st.info("Please check your API key and try again.")
                else:
                    st.info("An error occurred in debug mode.")
    
    # Display results if they exist in session state - side by side layout
    if st.session_state.summary and st.session_state.quiz:
        # Create two columns for Summary and Quiz
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            parse_and_display_summary(st.session_state.summary)
        
        with col_right:
            # Display quiz based on mode
            if st.session_state.quiz_mode == 'interactive':
                display_interactive_quiz(st.session_state.quiz)
            else:
                parse_and_display_quiz(st.session_state.quiz)
    elif st.session_state.summary:
        # If only summary exists, show it full width
        parse_and_display_summary(st.session_state.summary)
    elif st.session_state.quiz:
        # If only quiz exists, show it full width
        if st.session_state.quiz_mode == 'interactive':
            display_interactive_quiz(st.session_state.quiz)
        else:
            parse_and_display_quiz(st.session_state.quiz)
    
    # Download section - show only if results exist
    if st.session_state.summary and st.session_state.quiz:
        st.markdown("---")
        st.subheader("💾 Download Results")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Text download with quiz results
            quiz_results_text = ""
            if st.session_state.quiz_submitted and st.session_state.user_answers:
                questions_data = parse_quiz_data(st.session_state.quiz)
                correct_count = sum(
                    1 for q in questions_data
                    if st.session_state.user_answers.get(q['id']) == q['answer_key']
                )
                total_count = len(questions_data)
                answered_count = len(st.session_state.user_answers)
                percentage = (correct_count / total_count * 100) if total_count > 0 else 0
                
                # Grade determination
                if percentage >= 80:
                    grade = "🌟 Excellent"
                elif percentage >= 60:
                    grade = "👍 Good"
                else:
                    grade = "📚 Keep Learning"
                
                quiz_results_text = f"""

{'='*70}
                           📊 QUIZ RESULTS
{'='*70}

PERFORMANCE SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Score:           {correct_count}/{total_count} questions correct
  Percentage:      {percentage:.1f}%
  Answered:        {answered_count}/{total_count} questions
  Grade:           {grade}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DETAILED ANSWER REVIEW:
{'='*70}
"""
                for q in questions_data:
                    user_answer = st.session_state.user_answers.get(q['id'])
                    is_correct = user_answer == q['answer_key']
                    
                    if is_correct:
                        status = "✅ CORRECT"
                        status_line = "━" * 70
                    elif user_answer:
                        status = "❌ INCORRECT"
                        status_line = "━" * 70
                    else:
                        status = "⚠️  NOT ANSWERED"
                        status_line = "━" * 70
                    
                    user_answer_text = f"{user_answer.upper()}) {q['options'].get(user_answer, 'N/A')}" if user_answer else "Not answered"
                    
                    quiz_results_text += f"""
Question {q['id']}: {q['question']}
{status_line}
  Your Answer:     {user_answer_text}
  Correct Answer:  {q['answer_text']}
  Status:          {status}
{'='*70}

"""
            
            download_content = f"""╔══════════════════════════════════════════════════════════════════════╗
║              STUDY ASSISTANT - QUIZ GENERATOR                        ║
╚══════════════════════════════════════════════════════════════════════╝

{'='*70}
                              📋 SUMMARY
{'='*70}

{st.session_state.summary}

{'='*70}
                          📝 QUIZ QUESTIONS
{'='*70}

{st.session_state.quiz}
{quiz_results_text}
{'='*70}

Generated using Study Assistant
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*70}
"""
            st.download_button(
                label="📄 Download as Text",
                data=download_content,
                file_name=f"study_quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_b:
            # PDF download with quiz results
            try:
                pdf_buffer = generate_pdf_with_results(
                    st.session_state.summary,
                    st.session_state.quiz,
                    st.session_state.user_answers if st.session_state.quiz_submitted else None
                )
                st.download_button(
                    label="📕 Download as PDF",
                    data=pdf_buffer,
                    file_name=f"study_quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>Built with Streamlit, LangChain, and OpenAI | "
        "No external databases required 🚀</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
