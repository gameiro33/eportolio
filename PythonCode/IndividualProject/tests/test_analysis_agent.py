import pytest
import os
from analysisAgent import analyze_file

@pytest.mark.integration
def test_analyze_file_integration():
    # Ensure the OpenAI API key is set
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OpenAI API key not found. Skipping integration test.")

    # Test the analyze_file function with a real API call
    file_content = "This is a test file content for integration testing."
    result = analyze_file(file_content)
    
    # Check if the result contains expected elements
    assert "Criminal Likelihood score:" in result
    assert "/10" in result
    assert len(result) > 20  # Ensure we got a substantial response

    file_content = ""
    result = analyze_file(file_content)
    assert "The file you specified is empty, please check it." in result