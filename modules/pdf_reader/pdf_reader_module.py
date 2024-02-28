import os
import PyPDF2
from fuzzywuzzy import fuzz
from config import DEFAULT_PDF_FOLDER
import re
class PDF_READER:
    def __init__(self):
        self.pdf_folder_path = DEFAULT_PDF_FOLDER
        self.main_match = None
        self.no_answer_message = "No answer"

    def update_variables(self,passed_match):
        self.main_match = passed_match
        return self.main_match
    
    def return_answer(self):
        self.update_variables(None)
        file_list = os.listdir(self.pdf_folder_path)
        if(len(file_list)!=0):
            user_query = str(input("\n\nEnter your question: \n\n"))
            user_query = str(user_query).strip().lower()
            if(user_query):
                for file in file_list:
                    file = str(file)
                    if(file.endswith(".pdf")):
                        file_path = os.path.join(self.pdf_folder_path, file)
                        with open(file_path, 'rb') as file:
                            reader = PyPDF2.PdfFileReader(file)
                            num_pages = reader.numPages
                            
                            best_match = None
                            best_score = 0
                            
                            for page_num in range(num_pages):
                                page = reader.getPage(page_num)
                                text = page.extractText()
                                
                                if user_query in str(text).lower():
                                    score = fuzz.partial_ratio(user_query, str(text).lower().replace('\n', ' ').replace('\r', '').strip())
                                    if score > best_score:
                                        best_match = str(text).lower().replace('\n', ' ').replace('\r', '').strip()
                                        best_score = score
                                        self.update_variables(best_match)
                try:
                    return [self.main_match,user_query]
                except:
                    return [self.no_answer_message,user_query]
            else:
                self.return_answer()
        else:
            print("\n\nYou have no pdf files, add some\n\n")
            return False
        
       
