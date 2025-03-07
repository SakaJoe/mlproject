# For exception handling
import sys
# import logging
from src.logger import logging

# Function that outputs the details of the error, it takes in the following parameters: error (the actual error itself), error_detail (details of the error) 
def error_message_details(error,error_details:sys):
    # returns 3 types of information, we are only interested in the last information. The last information tells on which file the exception has occured and on which specific line
    _,_,exc_tb=error_details.exc_info()
    
    # Returns the file name
    file_name=exc_tb.tb_frame.f_code.co_filename
    
    error_message="Error occured in python script name [{0}] in line number [{1}] and the error message is [({2}]".format(file_name, exc_tb.tb_lineno, str(error))
    
    return error_message

# A class called CustomException which inherits from parent Exception
class CustomException(Exception):
    # Initialize the class with error message and error details
    def __init__(self, error_message, error_details:sys):
        # calls the init method from the parent class Exception and passes 'error_message' to it
        super().__init__(error_message)
        # Error message is attained by calling the function error_message_details
        self.error_message=error_message_details(error_message,error_details=error_details)
        
    def __str__(self):
        return self.error_message    
    
    

    