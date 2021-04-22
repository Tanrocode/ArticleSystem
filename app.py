import secrets
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length

app = Flask(__name__, static_folder="YOUR STATIC FOLDER DIRECTORY HERE")

#MySQLdb Database Config
app.config["MYSQL_HOST"] = '{0}'.format(secrets.dbhost)
app.config["MYSQL_USER"] = '{0}'.format(secrets.dbuser)
app.config["MYSQL_PASSWORD"] = '{0}'.format(secrets.dbpass)
app.config["MYSQL_DB"] = '{0}'.format(secrets.dbname)
app.config['MySQL_CURSORCLASS'] = 'DictCursor'

#SQLAlchemy Database Config
conn = 'mysql://{0}:{1}@{2}/{3}'.format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
app.config['SECRET_KEY'] = '{0}'.format(secrets.dbsecretkey)
app.config['SQLALCHEMY_DATABASE_URI'] = conn 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mysql = MySQL(app)

class AdminLogin(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])

#Creating Array Called Articles to Store Our Info
class articles(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    author = db.Column(db.String(500))
    content = db.Column(db.String(8000))

#Creating Form to Input Our Data Into
class articleinput(FlaskForm):
    name = StringField('Name:', validators=[InputRequired()])
    content = StringField('Content:', validators=[InputRequired()])
    
@app.route("/createarticle", methods=['GET', 'POST'])
def articlecreate():
    form = articleinput()
    name = articleinput.name
    content = articleinput.content
    cur = mysql.connection.cursor()

    return render_template("articlecreator.html", form=form)

    if request.method == 'POST' and form.validate_on_submit():
        cur.execute("INSERT INTO articles(author, content) VALUES(%s, %s)",(name, content))
        mysql.connection.commit()
        cur.close()  

    else:
        return "invalid" 

    if form.validate_on_submit():
        return redirect("/")
        flash("Congrats {}, your article has been submitted").format(articleinput.name.data)    
        
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
