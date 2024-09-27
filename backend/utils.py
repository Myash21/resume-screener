import os
import logging
from typing import List, Tuple
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv


load_dotenv()


def query_rag(job_description: str, question: str) -> Tuple[str, List[str]] | str:
    PROMPT_TEMPLATE = """
    You are an HR assistant helping to analyze job descriptions in various PDF documents. Extract key information such as job title, required skills, qualifications, years of experience, responsibilities, and location. If the job description matches the following criteria, please summarize the details:

    Job Title: {job_description}
    Candidate Resumes: {context}
    
    Answer the following question asked by your HR in a description and precise way.

    Question:

    {question}
    """
    try:
        db = Chroma(
            persist_directory="chroma",
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            ),
        )

        results = db.similarity_search_with_score(job_description, k=5)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            job_description=job_description, context=context_text, question=question
        )

        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY")
        )
        response = model.invoke(prompt)

        if hasattr(response, "content"):
            return response.content.strip()
        return str(response).strip()

    except Exception as e:
        logging.error(f"Error in query_rag: {e}")
        return "An error occurred while processing the query."


def main() -> None:
    temp_jd = """
This is a remote position.

About Acowale:

Welcome to Acowale—a startup backed by giants like Microsoft, Zoho, and Freshworks. We’re shaping India’s tech future, with a 4.8 Glassdoor rating and a 100% happy team. Join us, and be part of something extraordinary.

About the Role:

We’re looking for a Frontend Developer Intern to build sleek, responsive web applications. You'll work directly with our product team on developing our upcoming apps, Acodash and Acozap. This role offers the opportunity to learn from industry experts, gain hands-on experience, and potentially secure a full-time position. You'll be directly working with our Founders, CTO and COE.

Requirements

What You’ll Do:

    Develop responsive web applications. 
    Write clean, maintainable code. 
    Collaborate with the product team on Acodash and Acozap. 
    Work full-time, starting with a training period. 
    Contribute to innovative frontend solutions. 

Skills Required:

    Proficiency in React.js, HTML, CSS, and Python. 
    Experience with frontend frameworks, including React.js and Tailwind CSS. 
    Understanding of responsive design principles. 
    Familiarity with version control systems like GIT. 

"""
    temp_question = "Tell me if Yash Mhaskar is suitable for the given job description"
    print(query_rag(job_description=temp_jd, question=temp_question))


if __name__ == "__main__":
    main()
