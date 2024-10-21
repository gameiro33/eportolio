import pytest
import os
import json
from datetime import datetime, timezone
from genMetadata import WriteMetaData

@pytest.fixture
def write_metadata():
    # Fixture to create a WriteMetaData instance for reuse in multiple tests
    return WriteMetaData("/tmp/test_directory", ["*.txt", "*.sql"])

def test_time_convert(write_metadata):
    timestamp = 1617235200  # 2021-04-01 00:00:00 UTC
    expected = "2021-04-01 00:00:00"
    assert write_metadata.timeConvert(timestamp) == expected

def test_size_format(write_metadata):
    size_bytes = 1024 * 1024  # 1 MB
    expected = "1024.00 KB"
    assert write_metadata.sizeFormat(size_bytes) == expected

def test_get_file_content(write_metadata, tmp_path):
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content)
    
    assert write_metadata.get_file_content(str(test_file)) == test_content

def test_get_file_content_error(write_metadata):
    non_existent_file = "/path/to/non/existent/file.txt"
    assert "Error reading file:" in write_metadata.get_file_content(non_existent_file)

@pytest.fixture
def mock_analyze_file(monkeypatch):
    # This fixture mocks the analyze_file function to isolate the test from external dependencies
    def mock_analyze(content):
        return "Mocked analysis result"
    monkeypatch.setattr("genMetadata.analyze_file", mock_analyze)

def test_write_stats(write_metadata, tmp_path, mock_analyze_file):
    # This test is more complex because it tests multiple components together:
    # 1. File creation
    # 2. WriteMetaData.writeStats method
    # 3. JSON file creation and content verification
    
    test_file = tmp_path / "test.txt"
    test_content = "Test content"
    test_file.write_text(test_content)
    
    write_metadata.writeStats(str(test_file), "test.txt")
    
    metadata_dir = tmp_path / "MetaData"
    json_file = metadata_dir / "data.json"
    
    # Verify that the metadata directory and JSON file are created
    assert metadata_dir.exists()
    assert json_file.exists()
    
    # Check the content of the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Verify the structure and content of the JSON data
    assert len(data) == 1
    assert data[0]['File_Name'] == "test.txt"
    assert data[0]['Content'] == "Mocked analysis result"

def test_log_file_metadata(write_metadata, tmp_path, mock_analyze_file):
    # This test is the most complex because it tests the entire workflow:
    # 1. Setting up a test directory with multiple files
    # 2. Running the logFileMetadata method
    # 3. Verifying the correct files are processed and ignored
    # 4. Checking the final JSON output
    
    write_metadata.directory = str(tmp_path)
    
    # Create test files with different extensions
    (tmp_path / "file1.txt").write_text("Content 1")
    (tmp_path / "file2.sql").write_text("Content 2")
    (tmp_path / "file3.py").write_text("Content 3")  # Should be ignored due to extension
    
    write_metadata.logFileMetadata()
    
    metadata_dir = tmp_path / "MetaData"
    json_file = metadata_dir / "data.json"
    
    # Verify that the metadata directory and JSON file are created
    assert metadata_dir.exists()
    assert json_file.exists()
    
    # Check the content of the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Verify that only the correct files were processed
    assert len(data) == 2
    assert set(item['File_Name'] for item in data) == {"file1.txt", "file2.sql"}
