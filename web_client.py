
import os
from flask import Flask


app = Flask(__name__)

@app.route("/")
def test():
    return "welcome"



@app.route("/test")
def html():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir_path, "index.html")
    print(path)
    with open(path,"r") as f:
        return f.read()


if __name__ == "__main__":
    app.run("127.0.0.1", port=8000)

