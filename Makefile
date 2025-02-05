
# Variables
DOCKER_IMAGE_NAME = namereplacer
DATA_DIR = /data
INPUT_FILE = $(DATA_DIR)/input.txt
OUTPUT_FILE = $(DATA_DIR)/output.txt
MAPPING_FILE = namereplacer/fetchers/mapping.csv

# Build the wheel first
docker-build:
	poetry build
	docker build -t $(DOCKER_IMAGE_NAME) .

# Docker commands with volume mounting
sync_data:
	docker run --rm -v $(PWD)/data:$(DATA_DIR) $(DOCKER_IMAGE_NAME) \
		python -c "from namereplacer.fetchers.main import fetch_github_data; fetch_github_data(\"https://raw.githubusercontent.com/amephraim/nlp/master/texts/J.%20K.%20Rowling%20-%20Harry%20Potter%201%20-%20Sorcerer's%20Stone.txt\")"



run_replace:
	docker run --rm -v $(PWD)/data:$(DATA_DIR) $(DOCKER_IMAGE_NAME) \
		python -c "from namereplacer.fetchers.main import file_processor; file_processor('$(INPUT_FILE)', False)"

dry_run_replace:
	docker run --rm -v $(PWD)/data:$(DATA_DIR) $(DOCKER_IMAGE_NAME) \
		python -c "from namereplacer.fetchers.main import file_processor; file_processor('$(INPUT_FILE)', True)"

run_count:
	docker run --rm -v $(PWD)/data:$(DATA_DIR) $(DOCKER_IMAGE_NAME) \
		python -c "from namereplacer.fetchers.main import word_count; word_count('$(INPUT_FILE)', '$(target_word)')"