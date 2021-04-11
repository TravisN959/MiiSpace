from flask import Flask, render_template, url_for, request, redirect, session
import json
import os
from werkzeug.utils import secure_filename
import miispaceDB



app = Flask(__name__)
app.secret_key = "miispace"


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        
        return 'There was an error searching your task'

    else:#page refreshed/ reloaded so will output the template.
        return render_template('index.html',signedIn= isloggedIn())


@app.route('/signup', methods=['POST', 'GET'])
@app.route('/signup.html', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        username = username.lower()
        password = request.form['password']
        repeatPass = request.form['repeatPassword']
        phone = request.form['phone']
        name = request.form['name']

        if(password != repeatPass): #check for repeat password
            try:
                return render_template('signup.html', ERROR=True, ERROR_MSG="Passwords must be the same", signedIn= isloggedIn())
            except: return "Error in repeat password"
        elif(miispaceDB.checkDuplicateUsername(username)): #check for username alreadu in db
            try:
                return render_template('signup.html', ERROR=True, ERROR_MSG="Duplicate: Choose a new username", signedIn= isloggedIn())
            except: return "Error in duplicate username"
        else:#add account to db
            miispaceDB.setupAccount(username, password, phone, name)
            try:
                return signupSuccess()
            except:
                return 'There was an error searching your task'

    else:#page refreshed/ reloaded so will output the template.
        return render_template('signup.html',signedIn= isloggedIn())

@app.route('/signin', methods=['POST', 'GET'])
@app.route('/signin.html', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        username = username.lower()
        password = request.form['password']
        if(not miispaceDB.validateLogin(username, password)): #check for correctinfo
            try:
                return render_template('signin.html',signedIn= isloggedIn(),ERROR=True, ERROR_MSG="Password/Username Combo Error: Try Again", )
            except: return "Error in sigin"
        session["user"] = username
        return redirect(url_for("mainPage"))
    else:#page refreshed/ reloaded so will output the template.
        return render_template('signin.html',signedIn= isloggedIn(),ERROR=False, ERROR_MSG="No Error")

@app.route('/signupSuccess')
def signupSuccess():
    return render_template('signupSuccess.html',signedIn= isloggedIn())



@app.route('/mainPage', methods=['POST', 'GET'])
@app.route('/mainPage.html', methods=['POST', 'GET'])
def mainPage():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys

        account = miispaceDB.getInfo(session["user"])

        name=account["username"]## testing
        bgImage = account["bgImage"]
        pictures = account["pictures"]
        sticky_notes = account["sticky_notes"]
        calendar = account["calendar"]

        return render_template('mainPage.html',name=name, signedIn= isloggedIn(), bg = bgImage, pics =pictures, sticky = sticky_notes, calendar=calendar)
    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/stickynotes', methods=['POST', 'GET'])
@app.route('/stickynotes.html', methods=['POST', 'GET'])
def stickynotes():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys
        if request.method == 'POST':
            new_text = request.form['text']
            if(new_text==""):
                account = miispaceDB.getInfo(session["user"])
                sticky_notes = account["sticky_notes"]
                return render_template('stickynotes.html',sticky = sticky_notes,signedIn= isloggedIn())
             
            account = miispaceDB.getInfo(session["user"])
            name=account["username"]
            miispaceDB.addNote(name,new_text)
            account = miispaceDB.getInfo(session["user"])
            sticky_notes = account["sticky_notes"]
            
            return render_template('stickynotes.html',sticky = sticky_notes,signedIn= isloggedIn())
        else:
            account = miispaceDB.getInfo(session["user"])
            sticky_notes = account["sticky_notes"]
            return render_template('stickynotes.html',sticky = sticky_notes,signedIn= isloggedIn())

    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/myImages', methods=['POST', 'GET'])
@app.route('/myImages.html', methods=['POST', 'GET'])
def myImages():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys
        if request.method == 'POST':
            
            new_text = request.form['text']
            if(new_text==""):
                account = miispaceDB.getInfo(session["user"])
                pics = account["pictures"]
                return render_template('myImages.html',images = images,signedIn= isloggedIn())
                
            
            account = miispaceDB.getInfo(session["user"])
            name=account["username"]
            miispaceDB.addImage(name,new_text)
            account = miispaceDB.getInfo(session["user"])
            imagesList = account["pictures"]
            return render_template('myImages.html',images = imagesList,signedIn= isloggedIn())
        else:
            account = miispaceDB.getInfo(session["user"])
            imagesList = account["pictures"]
            return render_template('myImages.html',images = imagesList,signedIn= isloggedIn())

    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/settingsAccount', methods=['POST', 'GET'])
@app.route('/settingsAccount.html', methods=['POST', 'GET'])
def settingsPage():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys

        account = miispaceDB.getInfo(session["user"])

        username=account["username"]## testing
        phone=account["phone"]
        name=account["name"]

        

        if request.method == 'POST':
            usernameForm = request.form['username']
            nameForm = request.form['name']
            usernameForm = usernameForm.lower()
            password = request.form['password']
            repeatPass = request.form['repeatPassword']
            phoneForm = request.form['phone']
            if(password != repeatPass): #check for repeat password
                return render_template('settingsAccount.html', name=name, username=username, phone=phone,ERROR=True, ERROR_MSG="Passwords must be the same", signedIn= isloggedIn())
            else:
                if(password):
                    miispaceDB.setPassword(username, password)
            miispaceDB.setPhone(username, phoneForm)
            miispaceDB.setName(username, nameForm)
            miispaceDB.setUsername(username, usernameForm)
            session["user"] = usernameForm
            return render_template('settingsAccount.html',name=nameForm, username=usernameForm, phone=phoneForm, signedIn= isloggedIn(), ERROR=False)
        else:
            return render_template('settingsAccount.html',name=name, username=username, phone=phone, signedIn= isloggedIn())
    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/settingsAppearance', methods=['POST', 'GET'])
@app.route('/settingsAppearance.html', methods=['POST', 'GET'])
def settingsAppearancePage():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys

        account = miispaceDB.getInfo(session["user"])

        name=account["username"]## testing
        phone=account["phone"]

        return render_template('settingsAppearance.html',name=name, phone=phone, signedIn= isloggedIn())
    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/settingsAbout', methods=['POST', 'GET'])
@app.route('/settingsAbout.html', methods=['POST', 'GET'])
def settingsAboutPage():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys

        account = miispaceDB.getInfo(session["user"])

        name=account["username"]## testing
        phone=account["phone"]

        return render_template('settingsAbout.html',name=name, phone=phone, signedIn= isloggedIn())
    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/settingsHelp', methods=['POST', 'GET'])
@app.route('/settingsHelp.html', methods=['POST', 'GET'])
def settingsHelpPage():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys

        account = miispaceDB.getInfo(session["user"])

        name=account["username"]## testing
        phone=account["phone"]

        return render_template('settingsHelp.html',name=name, phone=phone, signedIn= isloggedIn())
    else:
        return render_template('signin.html', signedIn= isloggedIn())


def isloggedIn():
    if "user" in session:
        return True
    else:
        return False

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("signin"))


@app.route('/deleteNotes')
def deleteS():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys

        account = miispaceDB.getInfo(session["user"])

        name=account["username"]## testing
        miispaceDB.resetNote(name)
        account = miispaceDB.getInfo(session["user"])
        sticky_notes = account["sticky_notes"]

        return render_template('stickynotes.html',name=name, signedIn= isloggedIn(), sticky = sticky_notes)
    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/deleteImages')
def deleteI():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys

        account = miispaceDB.getInfo(session["user"])

        name=account["username"]## testing
        miispaceDB.resetImage(name)
        account = miispaceDB.getInfo(session["user"])
        pics = account["pictures"]

        return render_template('myImages.html',name=name, signedIn= isloggedIn(), images = pics)
    else:
        return render_template('signin.html', signedIn= isloggedIn())


@app.route('/deleteSpecificNote', methods=['POST', 'GET'])
def deleteSS():
    if "user" in session:#checks to see if logged in
        
        if request.method == 'POST':
            new_text = request.form['deleteSpecificNote']
            try:

                theInt = int(new_text)
                
                account = miispaceDB.getInfo(session["user"])
                
                if (theInt > len(account["sticky_notes"]) or theInt <= 0):
                    name=account["username"]## testing
                    
                    sticky_notes = account["sticky_notes"]
                    return render_template('stickynotes.html',name=name, signedIn= isloggedIn(), sticky = sticky_notes, ERROR=True, ERROR_MSG="Invalid Number!")
                    

                name=account["username"]## testing
                miispaceDB.deleteNote(name, theInt)
                account = miispaceDB.getInfo(session["user"])
                sticky_notes = account["sticky_notes"]

                return render_template('stickynotes.html',name=name, signedIn= isloggedIn(), sticky = sticky_notes)
            except:
                account = miispaceDB.getInfo(session["user"])
                name=account["username"]## testing
                sticky_notes = account["sticky_notes"]
                return render_template('stickynotes.html',name=name, signedIn= isloggedIn(), sticky = sticky_notes, ERROR=True, ERROR_MSG="Invalid Number!")
    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/deleteSpecificImage', methods=['POST', 'GET'])
def deleteSI():
    if "user" in session:#checks to see if logged in
        
        if request.method == 'POST':
            new_text = request.form['deleteSpecificImage']
            try:

                theInt = int(new_text)

                account = miispaceDB.getInfo(session["user"])
                if (theInt > len(account["pictures"]) or theInt <= 0):
                    name=account["username"]## testing
                    pics = account["pictures"]
                    return render_template('myImages.html',name=name, signedIn= isloggedIn(), images = pics, ERROR=True, ERROR_MSG="Invalid Number!")

                name=account["username"]## testing
                miispaceDB.deleteImage(name, theInt)
                account = miispaceDB.getInfo(session["user"])
                pics = account["pictures"]

                return render_template('myImages.html',name=name, signedIn= isloggedIn(), images = pics)
            except:
                account = miispaceDB.getInfo(session["user"])
                name=account["username"]## testing
                pics = account["pictures"]
                return render_template('myImages.html',name=name, signedIn= isloggedIn(), images = pics, ERROR=True, ERROR_MSG="Invalid Number!")
    else:
        return render_template('signin.html', signedIn= isloggedIn())


@app.route('/calendar', methods=['POST', 'GET'])
@app.route('/calendar.html', methods=['POST', 'GET'])
def makeCalendar():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys
        if request.method == 'POST':
            new_text = request.form['calendar']
            
            if(new_text==""):
                account = miispaceDB.getInfo(session["user"])
                calendar = account["calendar"]
                return render_template('calendar.html', calendar = calendar ,signedIn= isloggedIn())
            
            account = miispaceDB.getInfo(session["user"])
            name=account["username"]
            miispaceDB.addCalendar(name,new_text)
            account = miispaceDB.getInfo(session["user"])
            calendar = account["calendar"]
            
            return render_template('calendar.html', calendar = calendar,signedIn= isloggedIn())
        else:
            account = miispaceDB.getInfo(session["user"])
            calendar = account["calendar"]
            return render_template('calendar.html', calendar = calendar,signedIn= isloggedIn())

    else:
        return render_template('signin.html', signedIn= isloggedIn())

@app.route('/removeCalendar')
def deleteC():
    if "user" in session:#checks to see if logged in
        #process distance from user to rallys

        account = miispaceDB.getInfo(session["user"])

        name=account["username"]## testing
        miispaceDB.removeCalendar(name)
        account = miispaceDB.getInfo(session["user"])
        calendar = account["calendar"]

        return render_template('calendar.html',name=name, signedIn= isloggedIn(),calendar=calendar)
    else:
        return render_template('signin.html', signedIn= isloggedIn())
if __name__ == "__main__":
    app.run(debug=True)