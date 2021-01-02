from nayy_run import *
from gevent import pywsgi
import logging
import logging.handlers as handlers


logger = logging.getLogger('MainProgram')
logger.setLevel(10)  # 级别
logHandler = handlers.RotatingFileHandler('log.log', maxBytes=1000000, backupCount=1)  # 纪录设置
logger.addHandler(logHandler)
logger.info("Logging configuration done")  # 纪录开头


server = pywsgi.WSGIServer(('0.0.0.0', 80), app, log=logger, error_log=logger)
server.serve_forever()




