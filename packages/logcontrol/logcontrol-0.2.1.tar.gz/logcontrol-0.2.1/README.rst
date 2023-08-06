**logcontrol:** A logger manager for Python programs

It provides:  
  * Centralized control of log level (per-group)  

Original use case:  
  * Python GUI program containing many packages and modules  
  * Each source file that logs creates a proper logger for use within that file

    * e.g. logger = logging.getLogger(\_\_name__)

    * This allows a good logging hierarchy for control at a central point  
  * I wanted to simplify enabling debug level for specific packages or groups  
  
Installation:  
  * pip install logcontrol  
  
    (Tested for Python >=3.6.5 on Linux (Ubuntu) and Windows 7/10)

Usage:
    * example (where otherpackage and anotherpackage are example names)::

        # imports of fictitious packages
        import otherpackage
        import anotherpackage

        import logging
        import logcontrol

        # Register loggers you wish to control.
        # You can have user-friendly names for the groups if you wish:
        logcontrol.register_logger(otherpackage.logger, group='Other Package')

        # Set output file for the root logger:
        logcontrol.set_log_file('main_log.txt')

        # Enable specific log levels per-group:
        logcontrol.set_level(logging.DEBUG, group='Other Package')

        # Make specific groups log to console while debugging:
        logcontrol.log_to_console(group='Other Package')

        # You can even disable or enable propagation per-group:
        logcontrol.disable_propagation(group='Other Package')
        logcontrol.enable_propagation(group='Other Package')

        # Loggers added to the same group will get the same configuration.
        # This would automatically set DEBUG level and attach the console logging handler:
        logcontrol.register_logger(anotherpackage.module.logger, group='Other Package')

        # You can get a dict of group names with level names (good for populating a debug/log control popup):
        logcontrol.group_level_names()

        # For convenience, the predefined log levels are available:
        #     - as integers via logcontrol.log_level_integers
        #     - as strings via logcontrol.log_level_strings
        #
        # This makes it easy to display them in a combo box for users to choose.

