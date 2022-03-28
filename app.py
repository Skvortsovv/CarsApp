from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        req = request.form
        return render_template('create.html')
    return render_template('create.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
