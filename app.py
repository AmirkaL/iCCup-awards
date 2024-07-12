from flask import Flask, render_template, request, jsonify
from parser import get_iccup_awards

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_awards')
def get_awards():
    nickname = request.args.get('nickname')
    awards = get_iccup_awards(nickname)
    return jsonify(awards)

if __name__ == '__main__':
    app.run(debug=True)
