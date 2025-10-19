"""
Sample Study Material Generator
Creates a sample PDF for testing the Study Assistant Quiz Generator
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

def create_sample_pdf():
    """
    Create a sample study material PDF about Prompt Engineering for Agents
    """
    filename = "sample_study_material.pdf"
    
    # Create document
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='darkblue',
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Body style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=12,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16
    )
    
    # Add title
    title = Paragraph("Prompt Engineering for Agents", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Add subtitle
    subtitle = Paragraph("A Comprehensive Study Guide", styles['Heading3'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.3*inch))
    
    # Introduction section
    intro_heading = Paragraph("Introduction to Prompt Engineering", heading_style)
    elements.append(intro_heading)
    
    intro_text = """
    Prompt engineering involves designing and refining inputs to language models to achieve desired outputs. 
    In the context of agents, prompt engineering allows for better control over how an agent interacts with 
    the environment and solves specific tasks. This is particularly useful in domains like robotics and 
    conversational AI. By adjusting the structure and content of the prompts, users can enhance an agent's 
    performance on specific tasks.
    """
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Key Concepts section
    concepts_heading = Paragraph("Key Concepts in Prompt Engineering", heading_style)
    elements.append(concepts_heading)
    
    concepts_text = """
    <b>1. Prompt Structure:</b> The way a prompt is structured significantly impacts the quality of the output. 
    Well-structured prompts include clear instructions, context, and examples when necessary. A good prompt 
    should be specific, unambiguous, and aligned with the desired outcome.
    <br/><br/>
    <b>2. Context Window:</b> Language models have a limited context window, which is the amount of text they 
    can process at once. Effective prompt engineering requires understanding this limitation and crafting prompts 
    that fit within the context window while providing sufficient information.
    <br/><br/>
    <b>3. Few-Shot Learning:</b> This technique involves providing the model with a few examples of the desired 
    output format within the prompt. Few-shot learning helps the model understand the task better and generate 
    more accurate responses without requiring extensive fine-tuning.
    """
    elements.append(Paragraph(concepts_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Applications section
    applications_heading = Paragraph("Applications in Agent-Based Systems", heading_style)
    elements.append(applications_heading)
    
    applications_text = """
    In agent-based systems, prompt engineering plays a crucial role in defining agent behavior and decision-making 
    processes. Agents are autonomous entities that perceive their environment and take actions to achieve specific 
    goals. The prompts given to these agents determine how they interpret information and respond to different situations.
    <br/><br/>
    <b>Conversational AI:</b> In conversational AI systems, prompts help define the personality, tone, and knowledge 
    base of the agent. By carefully crafting prompts, developers can create agents that provide helpful, accurate, 
    and contextually appropriate responses to user queries.
    <br/><br/>
    <b>Robotics:</b> In robotics applications, prompt engineering helps translate high-level human instructions into 
    actionable commands for robots. This enables more intuitive human-robot interaction and allows non-expert users 
    to control complex robotic systems effectively.
    <br/><br/>
    <b>Task Planning:</b> Agents often need to break down complex tasks into manageable steps. Prompt engineering 
    can guide this decomposition process, helping agents create effective action plans and adapt to changing circumstances.
    """
    elements.append(Paragraph(applications_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Best Practices section
    practices_heading = Paragraph("Best Practices for Prompt Engineering", heading_style)
    elements.append(practices_heading)
    
    practices_text = """
    <b>1. Be Specific:</b> Vague prompts lead to unpredictable outputs. Always provide clear, specific instructions 
    about what you want the model to do. Include details about format, style, and content expectations.
    <br/><br/>
    <b>2. Iterate and Refine:</b> Prompt engineering is an iterative process. Start with a basic prompt and refine 
    it based on the outputs you receive. Small changes in wording can significantly impact results.
    <br/><br/>
    <b>3. Use Constraints:</b> When appropriate, include constraints in your prompts to guide the model's output. 
    These might include length restrictions, format requirements, or content limitations.
    <br/><br/>
    <b>4. Provide Context:</b> Give the model sufficient background information to understand the task. Context helps 
    the model generate more relevant and accurate responses.
    <br/><br/>
    <b>5. Test Edge Cases:</b> Always test your prompts with various inputs, including edge cases, to ensure robust 
    performance across different scenarios.
    """
    elements.append(Paragraph(practices_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Challenges section
    challenges_heading = Paragraph("Challenges and Considerations", heading_style)
    elements.append(challenges_heading)
    
    challenges_text = """
    Despite its effectiveness, prompt engineering faces several challenges. One major challenge is the brittleness 
    of prompts—small changes in wording can lead to dramatically different outputs. This makes it difficult to create 
    robust, reliable systems.
    <br/><br/>
    Another challenge is the lack of interpretability. It's often unclear why a particular prompt works well or poorly, 
    making systematic improvement difficult. Researchers are working on methods to better understand and predict prompt 
    effectiveness.
    <br/><br/>
    Token limits present another constraint. Complex tasks may require extensive context, but models have finite context 
    windows. Engineers must balance providing sufficient information with staying within these limits.
    <br/><br/>
    Finally, prompt engineering requires domain expertise. Creating effective prompts demands understanding both the 
    technical capabilities of language models and the specific requirements of the application domain.
    """
    elements.append(Paragraph(challenges_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Future Directions section
    future_heading = Paragraph("Future Directions", heading_style)
    elements.append(future_heading)
    
    future_text = """
    The field of prompt engineering continues to evolve rapidly. Emerging techniques include automatic prompt generation, 
    where algorithms optimize prompts based on desired outcomes. Meta-learning approaches allow models to learn how to 
    interpret prompts more effectively.
    <br/><br/>
    Multi-modal prompting, which combines text with images, audio, or other data types, represents another frontier. 
    This enables more sophisticated agent behaviors and richer human-AI interaction.
    <br/><br/>
    As language models become more powerful and accessible, prompt engineering will likely become an essential skill 
    for developers, researchers, and end-users alike. Understanding these principles will be crucial for building 
    effective AI-powered applications and agent-based systems.
    """
    elements.append(Paragraph(future_text, body_style))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Sample PDF created successfully: {filename}")
    return filename

if __name__ == "__main__":
    try:
        create_sample_pdf()
    except ImportError:
        print("❌ Error: reportlab is not installed.")
        print("Install it using: pip install reportlab")
        print("\nAlternatively, here's a simple text version you can use:")
        print("\n" + "="*50)
        
        sample_text = """
PROMPT ENGINEERING FOR AGENTS
A Comprehensive Study Guide

Introduction to Prompt Engineering

Prompt engineering involves designing and refining inputs to language models to achieve desired outputs. 
In the context of agents, prompt engineering allows for better control over how an agent interacts with 
the environment and solves specific tasks. This is particularly useful in domains like robotics and 
conversational AI. By adjusting the structure and content of the prompts, users can enhance an agent's 
performance on specific tasks.

Key Concepts in Prompt Engineering

1. Prompt Structure: The way a prompt is structured significantly impacts the quality of the output. 
Well-structured prompts include clear instructions, context, and examples when necessary.

2. Context Window: Language models have a limited context window. Effective prompt engineering requires 
understanding this limitation and crafting prompts that fit within the context window.

3. Few-Shot Learning: This technique involves providing the model with a few examples of the desired 
output format within the prompt.

Applications in Agent-Based Systems

In conversational AI systems, prompts help define the personality, tone, and knowledge base of the agent. 
In robotics applications, prompt engineering helps translate high-level human instructions into actionable 
commands for robots.
"""
        print(sample_text)
        print("="*50)
