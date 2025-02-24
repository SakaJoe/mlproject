'''
This file is used for exception handling

'''
import sys
import logging
from src.logger import logging


# Function extracts detailed error information when an exception occurs.
def error_message_detail(error,error_detail:sys):
    
    # _(ignored)-> Exception type, _(ignored) -> Exception value, exc_tb -> Traceback object (contains file name, line number, etc.)
    _,_,exc_tb=error_detail.exc_info()
    
    # Extracts the file where the error occured 
    file_name=exc_tb.tb_frame.f_code.co_filename
    
    # Format a custom error message
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
     file_name,exc_tb.tb_lineno,str(error) 
    )  
    return error_message   
        
  
    
# Creates a custom exception class that extends Python’s built-in Exception.
class CustomException(Exception):
    # This initializes the CustomException by storing a detailed error message.
    def __init__(self, error_message,error_detail:sys):
        # Calls the parent Exception class to initialize the error.
        super().__init__(error_message)
        
        # Calls the error_message_detail() to format a detailed error message.
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
        
    # When print(CustomException) is called, it returns the formatted error message.
    def __str__(self):
        return self.error_message
    
    
