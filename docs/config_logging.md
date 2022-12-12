# IO-AVSTATS - Configuration - Logging

In **IO-AVSTATS** the Python standard module for logging is used - details can be found [here](https://docs.python.org/3/library/logging.config.html){:target="_blank"}.

The file `logging_cfg.yaml` controls the logging behaviour of the application. 

## Default content:

    version: 1
    
    formatters:
      simple:
        format: "%(asctime)s [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d %(message)s"
      extended:
        format: "%(asctime)s [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d \n%(message)s"
    
    handlers:
      console:
        class: logging.StreamHandler
        level: INFO
        formatter: simple
    
      file_handler:
        class: logging.FileHandler
        level: INFO
        filename: logging_io-avstats.log
        formatter: extended
    
    loggers:
      io-avstats:
        handlers: [ console ]
    root:
      handlers: [ file_handler ]
