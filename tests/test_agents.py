from app.agents.tools import search_library
from app.data.sample_documents import SAMPLE_DOCUMENTS

def test_search_library_returns_matching_source():
    result = search_library("machine learning model evaluation precision recall")
    assert "Machine Learning Model Evaluation" in result
    assert "precision" in result.lower()

def test_search_library_handles_no_match():
    result = search_library("xylophone nebula")
    assert "No matching documents" in result

def test_sample_library_has_documents():
    assert len(SAMPLE_DOCUMENTS) >= 3
