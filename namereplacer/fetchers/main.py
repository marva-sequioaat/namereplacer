import logging
import requests
import csv
from namereplacer.constants import CSV_FILE,API_URL
import re
from collections import defaultdict
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

"""Fetches txt file content from github and writ to an input file"""
def fetch_github_data(link):
   
    try:
        response=requests.get(link)
        
        input_file="/data/input.txt"
        if response.status_code==200:
            file_content=response.text
            try:
                with open(input_file,"w",encoding="utf-8") as file:
                    file.write(file_content)
                    logger.info("successfully wrote content to the file")
                return input_file
            except IOError as e:
                logger.error(f"Error writing to file: {e}")
                return None

    except requests.RequestException as e:
        logger.error(f"Failed to fetch data: {e}")
        return None

def file_processor(input,dry_run=False):
    """
    Reads a mapping CSV file and replaces specified names in the input file.
    Saves the modified content to 'output.txt'.
    """
   
    try:
        with open(CSV_FILE,"r",encoding="utf-8") as file:
            content=csv.reader(file)
            next(content) # Skip header
            replace_dic={}
            
            for row in content:
                replace_dic[row[0]]=row[1]
                
    except IOError as e:
        logger.error(f"Error reading CSV file {CSV_FILE}: {e}")
        return None

    try:

        stats=defaultdict(int)    
        with open(input,"r",encoding="utf-8") as f:
            lines=f.read()
            
            for name,replace_name in replace_dic.items():
                count = len(re.findall(re.escape(name), lines, flags=re.IGNORECASE))
                stats[name] += count
                lines=re.sub(re.escape(name),replace_name,lines,flags=re.IGNORECASE)
            
        if not dry_run:
            with open("/data/output.txt","w",encoding="utf-8") as f:
                    f.write(lines)
            logger.info("Content wrote to output file successfully")
        else:
            logger.info("No content replaced.")
        logger.info(f"name count:{stats}")
        
    except IOError as e:
        logger.error(f"Error reading/writing files: {e}")
        return None        


def word_count(input, target_word):
    """count number of occurence of a word in the input.txt"""
    try:
        with open(input, "r", encoding="utf-8") as f:
            text = f.read()
            words = text.split()
            
            # Convert all words to lowercase for case-insensitive comparison
            words = [word.lower() for word in words]
            target_word = target_word.lower()
            
            # Count occurrences of the target word
            count = words.count(target_word)
            if count>0:
                logger.info(f"Occurrences of '{target_word}': {count}")
            else:
                logger.info("Word not found")
            return count
    except IOError as e:
        logger.error(f"Error reading file: {e}")
        return 0



    




