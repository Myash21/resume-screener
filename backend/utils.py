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
    You are an HR assistant helping to analyze job descriptions and candidate resumes in PDF documents.

    Job Description:
    {job_description}
    
    Candidate Resumes:
    {context}

    After ranking the candidates, answer any specific questions HR might have about the candidates in a clear and precise manner.

    Question:

    {question}
    """

    try:
        # Initialize Chroma with embeddings to perform similarity search
        db = Chroma(
            persist_directory="chroma",
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            ),
        )

        # Perform a similarity search for the provided job description
        results = db.similarity_search_with_score(job_description, k=10)

        # Generate context text from the search results
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

        # Generate the prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            job_description=job_description, context=context_text, question=question
        )

        # Call the Generative AI model to generate the response
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY")
        )
        response = model.invoke(prompt)

        # Return the content of the response
        if hasattr(response, "content"):
            return response.content.strip()
        return str(response).strip()

    except Exception as e:
        logging.error(f"Error in query_rag: {e}")
        return "An error occurred while processing the query."
