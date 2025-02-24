'''
This file is used for tracking events during the execution of a program
It writes logs to a file so that you can analyze them

'''
import logging 
import os
from datetime import datetime

# Create a Log File with a Timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create a logs Folder & Define Log File Path
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

# Set Up the Log File Path where the the logs will be saved
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

# Configure Logging Format
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

