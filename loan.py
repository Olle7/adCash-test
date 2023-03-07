from flask import Flask, request, redirect, Response, render_template#, send_file
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main_page():
    return render_template("hello.html")

@app.route("/test",methods=["GET","POST"])
def test():
    return "hello2"
if __name__ == '__main__':
    app.run(debug=True)