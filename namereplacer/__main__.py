from namereplacer.fetchers.main import fetch_github_data,file_processor
from namereplacer.constants import API_URL

def main():
    api_url=API_URL
    result=fetch_github_data(api_url)
    file_processor(result)

if __name__=="__main__":
    main()