from flask import Flask, render_template, url_for, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:root@localhost:5432/train_db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///train.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable = False)
    Surname = db.Column(db.String(50), nullable = False)
    Bith_date = db.Column(db.DateTime, default = datetime.utcnow)
    Phone = db.Column(db.String(12), nullable = False)
    Sex = db.Column(db.String(3))
    Short_info = db.Column(db.Text, default = 'Коротко обо мне')
    Position = db.Column(db.String(20))
    __tablename__ = 'User'

    def __repr__(self):
        return '<User %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users')
def users():
    users = User.query.order_by(User.Surname).all()
    return render_template('users.html', users=users)


@app.route('/users/<int:id>', methods=['GET','POST'])
def user_info(id):
    user = User.query.get(id)
    if request.method == 'POST':
        command = request.form['action']
        if command=='Delete':
            try:
                db.session.delete(user)
                db.session.commit()
                return redirect('/confirmation_page')
            except:
                return redirect('/error_page')
    else:
        return render_template('user_info.html', user_info=user)


@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        # name = request.form['name']
        # surname = request.form['surname']
        # phone = request.form['phone']
        # bith_date = request.form['bith_date']
        # short_info = request.form['short_info']
        # sex = request.form['sex']
        # position = request.form['position']
        USER_ATR = [
            ('Name','name'),
            ('Surname','surname'),
            ('Phone','phone'),
            ('Bith_date','bith_date'),
            ('Sex','sex'),
            ('Position','position'),
            ('Short_info','short_info')
        ]
        user_atr = {
            key: request.form[val]
            for key, val in USER_ATR 
        }
        
        user = User(**user_atr)
        # user = User(Name=name, Surname=surname, Phone=phone, Bith_date=bith_date, Sex=sex, Position=position, Short_info=short_info)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/confirmation_page')
        except:
            return redirect('/error_page')
    return render_template('create_user.html')


@app.route('/confirmation_page')
def confirm():
    return render_template('confirmation_page.html')


@app.route('/error_page')
def error_write():
    return render_template('error_page.html')
        

if __name__ == "__main__":
    app.run(debug = True)
