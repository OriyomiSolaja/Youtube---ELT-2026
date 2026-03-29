import json
from datetime import date
import logging

#create logger object
logger = logging.getLogger(__name__)

def load_data():
    
    file_path = f"./data/YT_data_{date.today()}.json" 
    
    #log action we are performing using logger.info in a try except block
    try:
        logger.info(f"Processing file: YT_data{date.today()}")
        
        with open(file_path, 'r', encoding='utf-8') as raw_data:
            data = json.load(raw_data)
            
        return data
    except FileNotFoundError:
        logger.error(f"File not found:{file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file : {file_path}")
        raise
    

        