import os

from chainchomplib.data import PathProvider


class LogsWriterHandler:

    INFO_LOG_NAME = 'info.log'
    DEBUG_LOG_NAME = 'debug.log'
    WARNING_LOG_NAME = 'warning.log'
    ERROR_LOG_NAME = 'error.log'
    CRITICAL_LOG_NAME = 'critical.log'

    @staticmethod
    def initiate_log_files():
        if not os.path.isdir(PathProvider.log_folder()):
            return False

        try:
            info_log = open(os.path.join(PathProvider.log_folder(), LogsWriterHandler.INFO_LOG_NAME), 'x')
        except OSError:
            print('Info log already created. Moving on...')
        else:
            info_log.close()

        try:
            debug_log = open(os.path.join(PathProvider.log_folder(), LogsWriterHandler.DEBUG_LOG_NAME), 'x')
        except OSError:
            print('Debug log already created. Moving on...')
        else:
            debug_log.close()

        try:
            warning_log = open(os.path.join(PathProvider.log_folder(), LogsWriterHandler.WARNING_LOG_NAME), 'x')
        except OSError:
            print('Warning log already created. Moving on...')
        else:
            warning_log.close()

        try:
            error_log = open(os.path.join(PathProvider.log_folder(), LogsWriterHandler.ERROR_LOG_NAME), 'x')
        except OSError:
            print('Error log already created. Moving on...')
        else:
            error_log.close()

        try:
            critical_log = open(os.path.join(PathProvider.log_folder(), LogsWriterHandler.CRITICAL_LOG_NAME), 'x')
        except OSError:
            print('Critical log already created. Moving on...')
        else:
            critical_log.close()

        return True
