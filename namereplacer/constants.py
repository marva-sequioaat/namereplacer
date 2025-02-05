from importlib.resources import files
API_URL="https://raw.githubusercontent.com/amephraim/nlp/master/texts/J.%20K.%20Rowling%20-%20Harry%20Potter%201%20-%20Sorcerer's%20Stone.txt"
CSV_FILE = files('namereplacer.fetchers').joinpath('mapping.csv')