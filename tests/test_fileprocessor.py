import pytest
import os
from unittest.mock import mock_open, patch, MagicMock
from namereplacer.fetchers.main import fetch_github_data, file_processor, word_count
import requests
# Test data we'll use across multiple tests
SAMPLE_TEXT = "Hello John, how are you John? JOHN is here."
SAMPLE_CSV = "original,replacement\nJohn,David\nMary,Jane"

# Tests for fetch_github_data function
def test_fetch_github_data_successful():
    """Test successful GitHub data fetch"""
    # Mock the requests.get response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Sample content"
    
    # Using patch to mock both requests.get and open()
    with patch('requests.get', return_value=mock_response):
        with patch('builtins.open', mock_open()) as mock_file:
            result = fetch_github_data("https://example.com/file.txt")
    
    # Check if file was written correctly
    mock_file().write.assert_called_once_with("Sample content")
    assert result == "/data/input.txt"

def test_fetch_github_data_failed_request():
    """Test failed GitHub request"""
    # Mock a failed request
    with patch('requests.get', side_effect=requests.RequestException("Network error")):
        result = fetch_github_data("https://example.com/file.txt")
    
    assert result is None

# Tests for file_processor function
def test_file_processor_normal():
    """Test normal operation of file processor"""
    # Mock reading the CSV file and input file
    with patch('builtins.open', mock_open(read_data=SAMPLE_CSV)) as mock_csv:
        # When open is called with input.txt, return our sample text
        mock_csv.side_effect = [
            mock_open(read_data=SAMPLE_CSV).return_value,  # For CSV file
            mock_open(read_data=SAMPLE_TEXT).return_value,  # For input file
            mock_open().return_value  # For output file
        ]
        
        file_processor("/data/input.txt")

def test_file_processor_dry_run():
    """Test file processor in dry run mode"""
    # Similar setup as normal test but with dry_run=True
    with patch('builtins.open', mock_open(read_data=SAMPLE_CSV)) as mock_csv:
        mock_csv.side_effect = [
            mock_open(read_data=SAMPLE_CSV).return_value,
            mock_open(read_data=SAMPLE_TEXT).return_value
        ]
        
        file_processor("/data/input.txt", dry_run=True)
        
        # Check that output file was not created
        assert not any(call.args[0] == "/data/output.txt" for call in mock_csv.call_args_list)

# Tests for word_count function
def test_word_count_existing_word():
    """Test counting a word that exists in the text"""
    test_content = "apple banana apple APPLE orange"
    
    with patch('builtins.open', mock_open(read_data=test_content)):
        count = word_count("/data/input.txt", "apple")
        
    assert count == 3  # Should count 'apple', 'APPLE'

def test_word_count_missing_word():
    """Test counting a word that doesn't exist in the text"""
    test_content = "apple banana orange"
    
    with patch('builtins.open', mock_open(read_data=test_content)):
        count = word_count("/data/input.txt", "grape")
        
    assert count == 0

def test_word_count_empty_file():
    """Test counting words in an empty file"""
    with patch('builtins.open', mock_open(read_data="")):
        count = word_count("/data/input.txt", "apple")
        
    assert count == 0