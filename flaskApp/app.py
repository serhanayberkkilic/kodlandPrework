import sys
from flaskApp.backend import index
from flaskApp.backend.config import app

sys.path.append('backend')

if __name__ == '__main__': 
    app.run(host="localhost", port=8000)


