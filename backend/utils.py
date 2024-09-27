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
Job Title: Python/Django Developer Internship Company: Geekrabit Private Limited Location: Wagholi, Pune Type: Unpaid Internship (6 months), In-office Reward: Stipend based on performance Geekrabit Private Limited, located in Wagholi, Pune, is offering an exciting opportunity for a Python/Django Developer Intern to join our team for a 6-month unpaid internship. This internship will provide valuable hands-on experience in a professional environment, allowing interns to enhance their skills, build their portfolios, and make meaningful contributions to real-world projects. A stipend will be awarded based on performance during the internship period.

    Collaborate with our development team to develop Python-based applications using the Django
    Write clean, efficient, and maintainable code following best practices and object-oriented programming
    Apply segmentation techniques and algorithms to support data analysis and processing within Django
    Participate in code reviews and contribute to improving code quality and consistency.
    Work closely with team members to understand project requirements and deliver solutions within
    Stay updated on industry trends and emerging technologies related to Python development and Django Responsibilities: framework. (OOP) principles. applications. deadlines. framework. Requirements:
    Pursuing or recently completed a degree in Computer Science, Engineering, or a related field.
    Strong proficiency in Python programming language.
    Understanding of object-oriented programming (OOP) concepts and design patterns.
    Familiarity with the Django framework for web development.
    Knowledge of segmentation techniques and algorithms is advantageous.
    Ability to write clean, efficient, and scalable code.
    Excellent problem-solving skills and attention to detail.
    Effective communication and collaboration skills.
    Ability to work independently and as part of a team in a fast-paced environment. Benefits:
    Hands-on experience with real-world projects in a professional setting.
    Mentorship and guidance from experienced professionals.
    Opportunity to enhance skills and build a professional portfolio.
    Networking opportunities within the company.
    Possibility of future employment opportunities based on performance.
    Internship certificate upon successful completion.
    Letter of recommendation for outstanding interns. How to Apply: Interested candidates are invited to submit their updated CV to: ashutosh.geekrabit@gmail.com kapil.geekrabit@gmail.com Geekrabit Private Limited is committed to providing equal opportunities and fostering diversity in the workplace. We encourage individuals from all backgrounds to apply. Please note that this is an unpaid internship position with a stipend awarded based on performance.


Desired Skills and Experience
PYTHON, Django, SOLID, SEGEMENTATION, OOPS, Object-Oriented Programming (OOP)
"""
    temp_question = "Give me the summary of this job description"
    print(query_rag(job_description=temp_jd, question=temp_question))


if __name__ == "__main__":
    main()
