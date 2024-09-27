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
    You are an assistant helping to analyze job descriptions and candidate resumes in PDF documents.

    Job Description:
    {job_description}
    
    Candidate Resumes:
    {context}

    Answer any specific questions HR might have about the candidates in a clear and precise manner.

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

        results = db.similarity_search_with_score(
            job_description, k=len(db.get()["ids"])
        )

        context_text = " ".join([doc.page_content for doc, _score in results])

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
Job Description

Airbus Innovation Centre - India & South Asia is responsible for industrializing disruptive technologies by tapping into the strong engineering competencies centre while also leveraging and co-creating with the vibrant external ecosystems such as big Tech Enterprises, mature startups/MSMEs, national labs & universities and strategic partners (customers, suppliers etc.)

The technology areas that the Innovation Centre focus on are - Artificial Intelligence, Industrial Automation, Unmanned Air Systems, Connectivity, Space Tech, Autonomy, Decarbonization Technologies etc. among others.

Airbus Innovation Centre in India is 1 among 3 Innovation Centres globally for Airbus with a strong focus on A.I. and Digital Engineering. We build products from the ground up with the help of stakeholders from within Engineering and Digital competence centres (in addition to the external stakeholders mentioned above) to deliver operational excellence and contribute to the Innovation & Technology roadmap of the organization.

We are seeking a highly skilled and motivated Front-End Development Intern to join our team. The ideal candidate will have a strong background in TypeScript, React, and modern front-end development practices. This is a fantastic opportunity to gain hands-on experience and contribute to cutting-edge projects within a dynamic environment.

Job Description

Front-End Development Intern (TypeScript & React)

Key Responsibilities

    Develop responsive, high-quality front-end code using TypeScript and React.
    Implement and manage state using React's built-in hooks and advanced hooks 
    Utilize TypeScript to enforce type safety, ensuring robust and maintainable code.
    Work with React Router for handling navigation and managing application routes.
    Optimize component performance by leveraging React’s optimization techniques.
    Collaborate with product managers, data scientists, and other stakeholders to understand user needs and business requirements.
    Assist in the creation and maintenance of reusable components and component libraries using best practices in React.
    Ensure all code adheres to industry best practices, is accessible, and meets company standards.
    Debug and resolve front-end issues, leveraging browser dev tools and React DevTools.
    Integrate and consume RESTful APIs, managing data flow with state management solutions like Redux or Context API.

Qualifications

    Currently pursuing a degree in Computer Science, Software Engineering, or a related field, or a recent graduate.
    Proficiency with TypeScript and React is required.
    Basic understanding of HTML, CSS, and JavaScript.
    Familiarity with front-end build tools and package managers such as Webpack, Babel, npm, or Yarn.
    Experience with RESTful API integration and asynchronous programming.
    Strong problem-solving skills and attention to detail.
    Willingness to learn and adapt to new tools, frameworks, and technologies.
    Good communication skills and the ability to work collaboratively in a team environment.
    Experience with version control systems like Git is a plus.

This job requires an awareness of any potential compliance risks and a commitment to act with integrity, as the foundation for the Company’s success, reputation and sustainable growth.
"""

    temp_question = (
        "Tell me the best candidates suitable for the provided job description."
    )
    print(query_rag(job_description=temp_jd, question=temp_question))


if __name__ == "__main__":
    main()
