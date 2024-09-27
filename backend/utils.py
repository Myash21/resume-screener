import os
import logging
from typing import List, Tuple
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv


load_dotenv()


def query_rag(job_description: str) -> Tuple[str, List[str]] | str:
    PROMPT_TEMPLATE = """
    Here is the job description provided:

    {job_description}

    ---

    Answer the following question based on the above context. If the question is a greeting, farewell, or expression of thanks, respond warmly and personally without referencing the context. For queries unrelated to legal content, reply with: "I’m sorry, but I can’t assist with that." Please ensure your response is descriptive and informative based on the context.

    Question: {question}
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
        prompt = prompt_template.format(context=context_text, question=question)

        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY")
        )
        response = model.invoke(prompt)

        if hasattr(response, "content"):
            return response.content.strip()
        return str(response).strip(), context_links

    except Exception as e:
        logging.error(f"Error in query_rag: {e}")
        return "An error occurred while processing the query."
