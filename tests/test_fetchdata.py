import pytest
import requests
from unittest.mock import Mock, patch
import logging
from namereplacer.fetchers.main import fetch_github_data  
import os



# Fixture to set up a temporary file path
# Fixture to mock requests.get
@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get

# Fixture to mock file operations
@pytest.fixture
def mock_file_open():
    with patch("builtins.open") as mock_open:
        yield mock_open

# Fixture to mock successful GitHub response
@pytest.fixture
def mock_successful_response():
    """
    Creates a mock response object that simulates a successful GitHub API response
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Sample GitHub content"
    return mock_response


# Test 1: Check if the link is a string
def test_link_is_string():
    link = 123  # Not a string
    result = fetch_github_data(link)
    assert result is None, "Function should return None if the link is not a string"

        
# Test 2: Check if function handles empty string
def test_empty_string():
    """Test that function handles empty string appropriately"""
    result = fetch_github_data("")
    assert result is None

# Test 3: Test successful GitHub fetch and file write

def test_successful_fetch_and_write(mock_requests_get, mock_file_open):
    # Mock the response from requests.get
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Sample content from GitHub"
    mock_requests_get.return_value = mock_response

    # Mock the file open operation
    mock_file = Mock()
    mock_file_open.return_value.__enter__.return_value = mock_file

    # Call the function
    result = fetch_github_data("https://github.com/valid-link")

    # Assertions
    assert result == "/data/input.txt", "Function should return the correct file path"
    mock_file.write.assert_called_once_with("Sample content from GitHub"), "File content should match the fetched data"

# Test 4: Test GitHub API failure
@patch('requests.get')
def test_github_fetch_failure(mock_get):
    """Test handling of GitHub API failure"""
    # Setup mock to raise an exception
    mock_get.side_effect = requests.RequestException("API error")

    # Call function
    result = fetch_github_data("https://api.github.com/test")

    # Assert
    assert result is None

# Test 5: Test file write failure
@patch('requests.get')
@patch('builtins.open')
def test_file_write_failure(mock_open, mock_get):
    """Test handling of file write failure"""
    # Setup mocks
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Test content"
    mock_get.return_value = mock_response
    
    # Make open raise an IOError
    mock_open.side_effect = IOError("Write error")

    # Call function
    result = fetch_github_data("https://api.github.com/test")

    # Assert
    assert result is None

# Test 6: Test non-200 status code
@patch('requests.get')
def test_non_200_status(mock_get):
    """Test handling of non-200 HTTP status codes"""
    # Setup mock response with 404 status
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    # Call function
    result = fetch_github_data("https://api.github.com/test")

    # Assert
    assert result is None

# Test 7: Test valid URL format
def test_valid_url_format():
    """Test that function validates URL format"""
    result = fetch_github_data("not_a_valid_url")
    assert result is None