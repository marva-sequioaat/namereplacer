# NameReplacer

## Overview

NameReplacer is a Python tool designed to fetch text content from a GitHub repository and perform name replacements based on a predefined mapping. It provides functionality to download text files, replace names, and perform various text analysis operations.

## Features

- Fetch text content from GitHub repositories
- Replace names in text based on a CSV mapping file
- Perform dry-run replacements to preview changes
- Count word occurrences
- Docker-based deployment for easy setup and execution

## Prerequisites

- Docker
- Make
- Poetry (for development)
- Python 3.11+

## Installation

### Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/marva-sequioaat/namereplacer.git
cd namereplacer
```

2. Build the Docker image:
```bash
make docker-build
```

## Usage

### Makefile Commands

- `make sync_data`: Download the input text file from a specified GitHub URL
- `make run_replace`: Replace names in the input file and generate output
- `make dry_run_replace`: Preview name replacements without modifying the file
- `make run_count target_word=<any name you want to search>`: Analyze word statistics in the input file

### Docker Commands

All commands are run using Docker with volume mounting to the `/data` directory.

#### Fetch Content
```bash
make sync_data
```
This will download the specified text file to `/data/input.txt`

#### Replace Names
```bash
# Perform actual replacements
make run_replace

# Preview replacements without modifying the file
make dry_run_replace
```

#### Word Count
```bash
make run_count
```

## Configuration

### Mapping CSV

Create a CSV file (`mapping.csv`) with the following structure:
```
Original Name,Replacement Name
Harry,John
Hermione,Emma
Ron,Mike
```

### Customization

- Modify `namereplacer/constants.py` to change default paths or URLs


### Docker Development

1. Build the image:
```bash
make docker-build
```

2. Run commands inside the Docker container

## Error Handling

The tool includes comprehensive error handling for:
- Network requests
- File I/O operations
- CSV parsing
- Name replacements

Errors are logged with detailed information to aid troubleshooting.
