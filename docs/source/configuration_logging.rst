=====================
Configuration Logging
=====================

In **IO-AVSTATS** the Python standard module for logging is used - details can be found `here <https://docs.python.org/3/library/logging.config.html>`_.

The file ``logging_cfg.yaml`` controls the logging behaviour of the application.

Default content::

    version: 1

    disable_existing_loggers: False

    formatters:
      simple:
        format: "%(asctime)s [%(name)s] [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d %(message)s"
      extended:
        format: "%(asctime)s [%(name)s] [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d \n%(message)s"

    handlers:
      console:
        class: logging.StreamHandler
        level: INFO
        formatter: simple
      file_handler:
        class: logging.FileHandler
        level: INFO
        filename: logging_io_aero.log
        formatter: extended

    root:
      level: DEBUG
      handlers: [ console, file_handler ]

