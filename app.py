from flask import Flask, render_template, url_for, request, redirect
import miispaceDB
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        
        return 'There was an error searching your task'

    else:#page refreshed/ reloaded so will output the template.
        return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
@app.route('/signup.html', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        username = username.lower()
        password = request.form['password']
        repeatPass = request.form['repeatPassword']


        if(password != repeatPass): #check for repeat password
            try:
                return render_template('signup.html', ERROR=True, ERROR_MSG="Passwords must be the same", signedIn= isloggedIn())
            except: return "Error in repeat password"
        elif(miispaceDB.checkDuplicateUsername(username)): #check for username alreadu in db
            try:
                return render_template('signup.html', ERROR=True, ERROR_MSG="Duplicate: Choose a new username", signedIn= isloggedIn())
            except: return "Error in duplicate username"
        else:#add account to db
            miispaceDB.setupAccount(username, password)
            try:
                return signupSuccess()
            except:
                return 'There was an error searching your task'

    else:#page refreshed/ reloaded so will output the template.
        return render_template('signup.html')

@app.route('/signin', methods=['POST', 'GET'])
@app.route('/signin.html', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        username = username.lower()
        password = request.form['password']
        if(not miispaceDB.validateLogin(username, password)): #check for correctinfo
            try:
                return render_template('signin.html')
            except: return "Error in sigin"
        return redirect(url_for("mainPage"))
    else:#page refreshed/ reloaded so will output the template.
        return render_template('signin.html')

@app.route('/signupSuccess')
def signupSuccess():
    return render_template('signupSuccess.html')
if __name__ == "__main__":
    app.run(debug=True)