# main.py
from sql import *
from webpath import app

if __name__ == "__main__":
    # delete_tables()
    init()
    app.run(debug=True)