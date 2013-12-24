webElementTimeOut = 180
Email = None
Password = None
Keyword = None
Size = None

ProxyIP = None
ProxyUsername = None
ProxyPassword = None

import sys
import os
import imp


def main_is_frozen():
    return hasattr(sys, 'frozen') or hasattr(sys, 'importers') or imp.is_frozen('__main__')


def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(os.path.dirname(sys.executable))
    return os.path.dirname(sys.argv[0])