FROM python:3.11-slim

WORKDIR /app

COPY dist/namereplacer-0.1.0-py3-none-any.whl /tmp/
RUN pip install /tmp/namereplacer-0.1.0-py3-none-any.whl

RUN mkdir -p /data

# Set the default command
CMD ["python","namereplacer"]