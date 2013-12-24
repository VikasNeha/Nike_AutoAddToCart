# Embedded file name: Utilities\myLogger.pyo
import logging
import config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename=config.get_main_dir() + 'logger.log', filemode='w')
logger = logging.getLogger('MainLogs')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logger.log')
fh.setLevel(logging.ERROR)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)