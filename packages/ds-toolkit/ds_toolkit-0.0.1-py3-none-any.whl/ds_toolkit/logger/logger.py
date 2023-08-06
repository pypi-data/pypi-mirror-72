import logging
import sys
from datetime import datetime
from time import time, strftime, localtime
from datetime import timedelta
import os

from ds_toolkit.config import config

logs_python_folder_path = config.PYTHON_LOGS_FOLDER_PATH or os.path.dirname(__file__) + '/logs/'
log_level = config.LOG_LEVEL or logging.ERROR


# ----------------------------------------------------------------------------------------------------


def _get_handlers(logger):
	"""
	Get handlers
	Args:
		logger (BaseLogger):

	Returns:
		(list of logging.Handler): List of logging handlers.
	"""
	
	def _make_dirs(datestamp):
		"""
		Makes directories for log files.

		Args:
			datestamp (str):
		"""
		if not os.path.isdir(f'{logs_python_folder_path}debug/{datestamp}/'):
			os.makedirs(f'{logs_python_folder_path}debug/{datestamp}/')
		if not os.path.isdir(f'{logs_python_folder_path}errors/{datestamp}/'):
			os.makedirs(f'{logs_python_folder_path}errors/{datestamp}/')
	
	def _get_handlers_configs(datestamp, timestamp):
		"""
		Get list of handlers configs.

		Args:
			datestamp (str):
			timestamp (str):

		Returns:
			(list of dict): List of configs
		"""
		return [
			{
				'type': 'console',
				'level': log_level,
				'formatter': logging.Formatter(
					'\n[ Time: %(asctime)s | Line Number: #:%(lineno)4s | File Name: %(pathname)s | Function:  %(funcName)s() ] \n%(levelname)s: %(message)s',
					'%Y-%m-%d %H:%M:%s'
				)
			},
			{
				'type': 'file',
				'level': logging.DEBUG,
				'formatter': logging.Formatter(
					'\n[ Time: %(asctime)s  | PID: %(process)d | Line Number: #:%(lineno)4s ] \nFile Name: %(pathname)s \nFunction: %(funcName)s() \n%(levelname)s: %(message)s',
					'%Y-%m-%d %H:%M:%s'
				),
				'path': f'{logs_python_folder_path}debug/{datestamp}/{timestamp}.log',
				
			},
			{
				'type': 'file',
				'level': logging.ERROR,
				'formatter': logging.Formatter(
					'\n[ Time: %(asctime)s | PID: %(process)d | Line Number: #:%(lineno)4s ] \nFile Name: %(pathname)s \nFunction: %(funcName)s() \n%(levelname)s: %(message)s',
					'%Y-%m-%d %H:%M:%s'
				),
				'path': f'{logs_python_folder_path}errors/{datestamp}/{timestamp}.log'
			}
		]
	
	def _get_handler(settings):
		"""
		Builds & returns logging handler.

		Args:
			settings (dict): Handlers config dictionary

		Returns:
			(logging.Handler): Logging handler
		"""
		
		if settings['type'] == 'file':
			handler = logging.FileHandler(settings['path'])
		else:
			handler = logging.StreamHandler()
		
		handler.setLevel(settings['level'])
		handler.setFormatter(settings['formatter'])
		
		return handler
	
	def _get_handlers():
		_make_dirs(logger.date)
		handlers_configs = _get_handlers_configs(logger.date, logger.start_time)
		handlers = []
		for handlers_config in handlers_configs:
			handlers.append(_get_handler(handlers_config))
		
		return handlers
	
	return _get_handlers()


class BaseLogger(logging.Logger):
	date: str
	start_time: str
	
	def __init__(self, name):
		super().__init__(name)
	
	def _exception_handler(self, exc_type, exc_value, exc_traceback):
		if issubclass(exc_type, KeyboardInterrupt):
			sys.__excepthook__(exc_type, exc_value, exc_traceback)
			return
		self.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
	
	def runtime(self, seconds=False):
		if seconds:
			return _get_seconds_elapsed(self.start_time)
		else:
			return _get_elapsed(self.start_time)


def _add_handlers(logger):
	handlers = _get_handlers(logger)
	for handler in handlers:
		logger.addHandler(handler)


def _string_from_datetime(date, show_time=True):
	fmt = '%Y-%m-%d'
	return date.strftime(fmt + ' %H:%M:%S%f' if show_time else fmt)


def _datetime_from_string(date):
	return datetime.strptime(date, '%Y-%m-%d %H:%M:%S%f')


def _get_elapsed(start_time):
	return str(datetime.now() - _datetime_from_string(start_time))


def _get_seconds_elapsed(start_time):
	elapsed = datetime.now() - _datetime_from_string(start_time)
	return elapsed.seconds


def _init_logger(logger):
	"""
	Initialize logger
	Args:
		logger (BaseLogger):
	"""
	logger.date = datetime.strftime(datetime.now(), '%Y-%m-%d')
	logger.start_time = _string_from_datetime(datetime.now())
	logger.setLevel(logging.DEBUG)
	
	_add_handlers(logger)
	
	logger.info(f"\n{'=' * 224} \n{'-' * 90} Initializing Program | {logger.start_time} {'-' * 90} \n \n")
	sys.excepthook = logger._exception_handler


def logger():
	"""
	Returns:
		BaseLogger: Custom logger
	"""
	logging.setLoggerClass(BaseLogger)
	logger = logging.getLogger('root')
	if not len(logger.handlers):
		_init_logger(logger)
	return logger
