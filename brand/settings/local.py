from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.getenv("DEBUG", False) == "True"
DEBUG = True

# if DEBUG :
#     MIDDLEWARE += [ "debug_toolbar.middleware.DebugToolbarMiddleware" ]
#
# if DEBUG :
#     import socket
#
#     hostname , _ , ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ ip[ : ip.rfind(".") ] + ".1" for ip in ips ] + [
#         "127.0.0.1" ,
#         "10.0.2.2" ,
#     ]
