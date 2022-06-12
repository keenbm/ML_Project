from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return "Starting Machine Learning"

if __name__ == '__main__':
    app.run(debug=True)