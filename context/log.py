import logging
import os
from context.color import col_info, col_warning, col_error, col_connect

logfile_path = os.path.join( os.getcwd(), '.', 'file.log' )

if(not os.path.isfile(logfile_path)):
    with open(logfile_path,'w') as fp:
        pass

logging.basicConfig(filename=logfile_path, filemode='w',level=logging.INFO)

def log_connect(method,host):
    msg = method+" "+host
    logging.info(msg)
    col_connect(method,host)

def log_info(msg):
    logging.info(msg)
    col_info(msg)

def log_warning(msg):
    logging.warning(msg)
    col_warning(msg)

def log_error(msg):
    logging.error(msg)
    col_error(msg)