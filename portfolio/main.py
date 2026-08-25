
from flask import Flask, render_template, flash, url_for,request
from flask_mail import Mail,Message
import os
from dotenv import load_dotenv
from werkzeug.utils import redirect
from datetime import datetime             # <-- timestamp each message
from portfolio.database import messages_collection
from portfolio.forms import Contact_form

load_dotenv()


app=Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)



@app.route('/')

def home():
    return render_template("index.html")




# --------------TO send your message---------------------------------------
@app.route('/contact2', methods=["GET", "POST"])
def contact():
    form = Contact_form()

    if form.validate_on_submit():
        name = form.Name.data
        email = form.Email.data
        message = form.Message.data

        # Save message to MongoDB
        messages_collection.insert_one({
            "name": name,
            "email": email,
            "message": message,
            "timestamp": datetime.utcnow()
        })

        # Send email notification
        try:
            msg = Message(
                subject=f"New Portfolio Message from {name}",
                recipients=[app.config['MAIL_USERNAME']],
                reply_to=email,
                body=f"""You received a new message through your portfolio contact form.

                Name: {name}
                Email: {email}

                Message:
                {message}
                """
            )

            mail.send(msg)

        except Exception as e:
            print("EMAIL ERROR:", e)

        flash("Message sent successfully!", "success")
        return redirect(url_for("submission", name=name))

    return render_template("contact2.html", form=form)


# -----------------successful submission--------------
@app.route('/submission')
def submission():
    name = request.args.get("name", "")
    name = name.strip().title()

    return render_template("submission.html",name=name)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/projects')
def project():
    return render_template("projects.html")


@app.route('/cv')
def cv():
    return render_template("cv.html")



if __name__ == "__main__":
    app.run(debug=True)


