from namereplacer.fetchers.main import fetch_github_data,file_processor
from namereplacer.constants import API_URL
"""main function which calls the functions which fetch content from github and replace names"""
def main():
    api_url=API_URL
    result=fetch_github_data(api_url)
     #function replace the name with replace_name and write to the output file
    file_processor(result,False)
    #function dry run the above without replacing the name
    file_processor(result,True)
    
if __name__=="__main__":
    main()