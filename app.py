from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '4876bb9c1ba52bd8615cad70161c975e2e2f12e01e8c88c040e06e3ad108bd9f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'  # Set a default database URI
# Database configurations
app.config['SQLALCHEMY_BINDS'] = {
    'doctors': 'sqlite:///doctors_bangalore.db',
    'patients': 'sqlite:///patients_bangalore.db'
}

db = SQLAlchemy(app)

class Doctor(db.Model):
    __bind_key__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    specialization = db.Column(db.String(120), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)

class Patient(db.Model):
    __bind_key__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    dob = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    medical_history = db.Column(db.Text, nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)

@app.route('/')
def home():
    return 'Welcome to the Telemedicine Chatbot!'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user_type = request.form['user_type']  # 'doctor' or 'patient'
        
        if user_type == 'doctor':
            existing_user = Doctor.query.filter_by(email=email).first()
            if existing_user:
                return 'Doctor already exists!', 400
            new_user = Doctor(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            session['user_type'] = 'doctor'
            return redirect(url_for('dashboard'))

        elif user_type == 'patient':
            existing_user = Patient.query.filter_by(email=email).first()
            if existing_user:
                return 'Patient already exists!', 400
            new_user = Patient(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            session['user_type'] = 'patient'
            return redirect(url_for('dashboard'))

        else:
            return 'Invalid user type!', 400
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']  # 'doctor' or 'patient'

        if user_type == 'doctor':
            user = Doctor.query.filter_by(email=email).first()
        elif user_type == 'patient':
            user = Patient.query.filter_by(email=email).first()
        else:
            return 'Invalid user type!', 400

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user_type
            return redirect("http://localhost:8501")
        else:
            return 'Invalid credentials!', 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['user_type'] == 'doctor':
        doctor = Doctor.query.get(session['user_id'])
        return render_template('dashboard.html', user=doctor)
    elif session['user_type'] == 'patient':
        patient = Patient.query.get(session['user_id'])
        return render_template('dashboard.html', user=patient)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
