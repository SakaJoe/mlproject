# For logging, ensuring that any execution is logged

import logging
import os
from datetime import datetime

# Define log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the logs folder path
logs_path = os.path.join(os.getcwd(), "logs")  # Just the folder path

# Create the logs folder if it does not exist
os.makedirs(logs_path, exist_ok=True)  

# Define the full file path and stores the log file inside the folder
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE) 

# Configure logging stating where the logs go, how they are formatted and what level is recorded
logging.basicConfig(
    filename=LOG_FILE_PATH, # Saves log messages to this file
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO, # Only log messages with INFO level and above
)

