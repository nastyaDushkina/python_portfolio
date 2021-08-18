log_config = {
    'version': 1,
    'formatters': {
        'console_formatter': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
        'file_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'mode': 'w+',
            'datefmt': '%d-%m-%Y %H:%M',
        },
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'file_formatter',
            'filename': 'chat_bot_log.log',
            'encoding': 'utf-8',
            'delay': 'False',
        },
    },
    'loggers': {
        'file_logger': {
            'handlers': ['file_handler', ],
            'level': 'DEBUG',
        },
        'console_logger': {
            'handlers': ['console_handler', ],
            'level': 'INFO'
        },
    },
}
