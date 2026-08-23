
from flask import Flask, render_template, flash, url_for
from flask_mail import Mail,Message
from werkzeug.utils import redirect
from datetime import datetime             # <-- timestamp each message
from portfolio.database import messages_collection

from portfolio.forms import Contact_form

app=Flask(__name__)
app.config['SECRET_KEY']='great'



@app.route('/')

def home():
    return render_template("index.html")

@app.route('/contact2',methods=["GET","POST"])
def contact():
    form=Contact_form()
    if form.validate_on_submit():  #if valid and POSTED
        name=form.Name.data
        email=form.Email.data
        message=form.Message.data

        # --------------to save messages to database---------------------
        messages_collection.insert_one({
            "name": name,
            "email": email,
            "message": message,
            "timestamp": datetime.utcnow()
        })

        flash("Message sent successfully!","success")
        return redirect(url_for("contact"))

    return render_template("contact2.html",form=form)




@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/projects')
def project():
    return render_template("projects.html")


if __name__ == "__main__":
    app.run(debug=True)


