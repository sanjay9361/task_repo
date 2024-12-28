from flask import Flask, render_template, jsonify
from scraper import scrape_trending_topics

app = Flask(_name_)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    data = scrape_trending_topics()
    return jsonify(data)

if _name_ == '_main_':
    app.run(debug=True)