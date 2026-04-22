from pypdf import PdfReader
from typing import List
from qdrant_client import QdrantClient


def read_single_pdf(file_path: str) -> str:
    output = []
    try:
        with open(file_path, "rb") as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                output.append(page.extract_text())
    except Exception as e:
        print(f"Error reading PDF '{file_path}': {str(e)}")
    return " ".join(output)


def get_score(resume_string: str, job_description_string: str) -> float:
    """
    Calculate similarity score between resume and job description.
    Returns a float score between 0 and 1.
    """
    documents: List[str] = [resume_string]
    client = QdrantClient(":memory:")
    client.set_model("BAAI/bge-base-en")
    client.add(collection_name="demo_collection", documents=documents)
    search_result = client.query(
        collection_name="demo_collection", query_text=job_description_string
    )
    if search_result:
        return round(search_result[0].score * 100, 2)
    return 0.0
