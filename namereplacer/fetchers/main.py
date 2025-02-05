import logging
import requests
import csv
from importlib.resources import files
import re
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
def fetch_github_data(link):
    headers = {
            'Accept': 'application/vnd.github.raw+json'
        }
    response=requests.get(link)
    
    input_file="input.txt"
    if response.status_code==200:
        file_content=response.text
        
        with open(input_file,"w",encoding="utf-8") as file:
            file.write(file_content)
            logger.info("successfully write content to the file")
    return input_file

def file_processor(input):
    
    CSV_FILE =  files('namereplacer.fetchers').joinpath('mapping.csv')
    with open(CSV_FILE,"r",encoding="utf-8") as file:
        content=csv.reader(file)
        next(content)
        replace_dic={}
        name_to_be_replaced=[]
        for row in content:
            print(row)
            name_to_be_replaced.append(row[0])
            replace_dic[row[0]]=row[1]
            
        print("replacing dic",replace_dic)
            
    with open(input,"r",encoding="utf-8") as f:
        lines=f.read()
        
        for name,replace_name in replace_dic.items():
            lines=re.sub(re.escape(name),replace_name,lines,flags=re.IGNORECASE)
    with open("output.txt","w",encoding="utf-8") as f:
            f.write(lines)
            
            
if __name__=="__main__":

    api_url="https://raw.githubusercontent.com/amephraim/nlp/master/texts/J.%20K.%20Rowling%20-%20Harry%20Potter%201%20-%20Sorcerer's%20Stone.txt"
    result=fetch_github_data(api_url)
    file_processor(result)