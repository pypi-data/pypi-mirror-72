**freezehelper:** A Python package to simplify checks for frozen state and executable directory (such as when using PyInstaller)

It provides:  
  * attributes to check platform, freeze state, and whether running in a child or parent process

Original use case:  
  * Python program that is deployed frozen (using PyInstaller) but is run from source while developed
  * When running from source I wanted to perform extra actions/checks on startup, e.g.:

    * setting a different log level/log to console or replacing sys.excepthook

    * changing what gets run in a child process on start when using multiprocessing
  
Installation:  
  * pip install freezehelper
  
    (Tested for Python >=3.6.5 on Linux (Ubuntu) and Windows 10)

Usage:
    * quick-start overview::

        # import the package
        import freezehelper

        ## Package Attributes

        # A bool to check if running from source:
        freezehelper.from_source

        # A bool to check if frozen:
        freezehelper.frozen

        # More bool items for platform:
        freezehelper.is_linux
        freezehelper.is_mac
        freezehelper.is_windows

        # Bool items for process context:
        freezehelper.is_child_process
        freezehelper.is_main_process

        # Path string for directory containing the main executable:
        freezehelper.executable_dir

        # Path string for the main executable:
        freezehelper.executable_path

        ## Functions

        # Functions for getting directory of executable or path to main executable:
        # These accept a bool resolve_links keyword argument.
        # When True (default), any symbolic links in the path are resolved in order to get the real path.
        freezehelper.get_executable_dir()
        freezehelper.get_executable_path()


        ## Examples
        if freezehelper.frozen:
            print(f"{freezehelper.executable_path} go brrr")

        # create separate logs for parent and child processes
        import logcontrol
        import os

        log_dir = os.path.join(freezehelper.executable_dir, "logs")
        child_log_dir = os.path.join(log_dir, "workers")

        if freezehelper.is_main_process:
            log_file = os.path.join(log_dir, "main_process.log")
        else:
            log_file = os.path.join(child_log_dir, f"{os.getpid()}_worker.log")

        logcontrol.set_log_file(log_file)

