from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        
        return 'There was an error searching your task'

    else:#page refreshed/ reloaded so will output the template.
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)