import os

workers = 4
bind = "0.0.0.0:" + str(int(os.environ.get("PORT", 10000)))
