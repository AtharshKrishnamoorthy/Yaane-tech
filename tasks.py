from crewai import Task
from agents import (
    guard_agent, sanitization_agent, classification_agent,
    legal_expert_agent,content_agent)

def create_tasks(user_input: str) -> list:
    verify_task = Task(
        description=f"""
        Verify if this input is crime-related: {user_input}
        If it's not crime-related, return a warning message.
        If it is crime-related, return the verified information.
        
        Format your response as:
        {{
            "is_crime": boolean,
            "details": string
        }}
        """,
        agent=guard_agent,
        expected_output="""
        {
            "is_crime": boolean,
            "details": string
        }
        """
    )

    sanitize_task = Task(
        description="""
        Remove any sensitive or personal information from the verified crime information.
        Maintain the essential details while protecting privacy.
        
        Format your response as:
        Thought: [your reasoning]
        Action: [what you're doing]
        Final Answer: [sanitized text]
        """,
        agent=sanitization_agent,
        expected_output="""
        Thought: [reasoning about sanitization process]
        Action: [description of sanitization actions]
        Final Answer: [sanitized text without sensitive information]
        """
    )

    classify_task = Task(
        description="""
        Classify the sanitized crime information into appropriate categories.
        
        Format your response as:
        {
            "main_category": string,
            "subcategory": string,
            "confidence": float (0-1),
            "explanation": string
        }
        """,
        agent=classification_agent,
        expected_output="""
        {
            "main_category": string,
            "subcategory": string,
            "confidence": float (between 0 and 1),
            "explanation": string
        }
        """
    )

    legal_analysis_task = Task(
        description="""
        Provide comprehensive legal information following the LegalResponse model structure.
        Include all required fields with detailed information.
        """,
        agent=legal_expert_agent,
        expected_output="""
        {
            "applicable_laws": [list of relevant laws],
            "jurisdiction": string,
            "severity_level": string,
            "potential_penalties": [list of possible penalties],
            "precedent_cases": [
                {
                    "case_name": string,
                    "relevance": string,
                    "outcome": string
                }
            ],
            "legal_considerations": string,
            "recommended_actions": [list of recommendations]
        }
        """
    )

    content_task = Task(
      description="""
       Generate a comprehensive user guide based on the legal analysis and classification provided.
       Create a clear, well-structured document that explains the legal situation and provides guidance.
       Your response should be in natural language paragraphs, divided into clear sections.
       
       Use the following input:
       - Sanitized crime information
       - Crime classification results
       - Legal analysis details
       
       Structure your response with these sections:
   
       1. Situation Overview
       Provide a clear summary of the situation and its legal implications.
       
       2. Understanding Your Rights
       Explain the relevant legal rights, obligations, and protections available.
       
       3. Recommended Actions
       Detail both immediate and long-term steps the user should take, presented in 
       a clear, sequential manner.
       
       4. Legal Process Guide
       Explain what to expect during the legal process, including timelines, 
       procedures, and potential outcomes.
       
       5. Applicable laws and Penalities
       Describe the laws applicale for the crime in India including the IPC sections and the penalities of the crime.
       
       5. Preventive Measures
       Suggest ways to prevent similar situations in the future, including best 
       practices and safety measures.
       
       6. Additional Support
       List available resources, including helpline numbers, legal aid services, 
       and relevant organizations that can provide assistance.
       
       Format Requirements:
       - Use clear headings for each section
       - Write in plain language, avoiding legal jargon where possible
       - Include specific examples where relevant
       - Add bullet points only for lists of resources or specific steps
       - Maintain a supportive and informative tone throughout
       """,
       agent=content_agent,
       expected_output="""
       A well-structured document with clear sections, written in natural language 
       paragraphs. Each section should be clearly marked with headers and contain 
       detailed, actionable information written in an accessible style.
       
       Example Format:
   
       ### Situation Overview
       [Paragraph explaining the situation...]
   
       ### Understanding Your Rights
       [Detailed explanation of legal rights and obligations...]
   
       ### Recommended Actions
       [Clear description of steps to take...]
   
       ### Legal Process Guide
       [Explanation of what to expect...]
       
       ### Applicable laws and Penalities
       [Describing the appliclable laws (inlcuding the IPC Scetions) and the penalities for the crime...]
   
       ### Preventive Measures
       [Suggestions for future prevention...]
   
       ### Additional Support
       [List of resources and contact information...]
       """
    ) 

    return [verify_task, sanitize_task, classify_task,
    legal_analysis_task,content_task]
    
    