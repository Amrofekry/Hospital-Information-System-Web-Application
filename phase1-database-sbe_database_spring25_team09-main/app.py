from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))
application = app

# Cloudinary configuration — ✅ FIXED: Removed < > from api_secret
cloudinary.config(
    cloud_name="di8dmhgwv",
    api_key="965592548551826",
    api_secret="MMtvNtgb9TDoDGBVn3VK5a15LP0",  # Corrected: No angle brackets
    secure=True
)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='ep-raspy-bird-abkmjvxm-pooler.eu-west-2.aws.neon.tech',
            database='database_name',
            user='postgres',
            password='npg_j8fnx3zcySom'
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS patient
                    (
                        patient_id BIGSERIAL PRIMARY KEY,
                        medical_record_number VARCHAR(20) UNIQUE NOT NULL,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        date_of_birth DATE NOT NULL,
                        gender VARCHAR(10),
                        phone VARCHAR(15),
                        email VARCHAR(100),
                        password TEXT,
                        address TEXT,
                        bloodtype VARCHAR(3),
                        photo_url TEXT
                    )
                    ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS doctor
                    (
                        doctor_id BIGSERIAL PRIMARY KEY,
                        license_number VARCHAR(20) UNIQUE NOT NULL,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        password TEXT,
                        specialty VARCHAR(100),
                        department VARCHAR(100),
                        phone VARCHAR(15),
                        email VARCHAR(100),
                        hire_date DATE,
                        active BOOLEAN DEFAULT TRUE,
                        salary INTEGER,
                        photo_url TEXT
                    )
                    ''')
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
        raise
    finally:
        cur.close()
        conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            user_type = request.form.get('user_type')

            # Shared fields
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')

            photo_url = None
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    if '.' in photo.filename and photo.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
                        result = cloudinary.uploader.upload(photo)
                        photo_url = result['secure_url']
                    else:
                        flash('Allowed image types are: png, jpg, jpeg, gif')
                        return redirect(url_for('signup'))

            if user_type == 'patient':
                mrn = request.form.get('medical_record_number')
                cur.execute("SELECT * FROM patient WHERE medical_record_number = %s", (mrn,))
                if cur.fetchone():
                    flash('Medical Record Number already exists!')
                    return redirect(url_for('signup'))

                cur.execute('''
                    INSERT INTO patient (
                        medical_record_number, first_name, last_name,
                        date_of_birth, gender, phone, email, password,
                        address, bloodtype, photo_url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    mrn,
                    first_name,
                    last_name,
                    request.form.get('date_of_birth'),
                    request.form.get('gender'),
                    request.form.get('phone'),
                    email,
                    password,
                    request.form.get('address'),
                    request.form.get('bloodtype'),
                    photo_url
                ))

            elif user_type == 'doctor':
                license_number = request.form.get('license_number')
                cur.execute("SELECT * FROM doctor WHERE license_number = %s", (license_number,))
                if cur.fetchone():
                    flash('License number already taken!')
                    return redirect(url_for('signup'))

                cur.execute('''
                    INSERT INTO doctor (
                        license_number, first_name, last_name,
                        password, specialty, department, phone,
                        email, hire_date, salary, photo_url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    license_number,
                    first_name,
                    last_name,
                    password,
                    request.form.get('specialty'),
                    request.form.get('department'),
                    request.form.get('phone'),
                    email,
                    request.form.get('hire_date'),
                    request.form.get('salary'),
                    photo_url
                ))

            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))

        except Exception as e:
            if conn:
                conn.rollback()
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('signup'))
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            if user_type == 'patient':
                mrn = request.form.get('medical_record_number')
                pwd = request.form.get('password')
                print(f"Trying to log in as patient with MRN: {mrn}")  # 🔍 Debug
                cur.execute("SELECT * FROM patient WHERE medical_record_number = %s", (mrn,))
                patient = cur.fetchone()
                if patient:
                    print(f"Found patient: {patient['first_name']}")  # 🔍 Debug
                    print(f"Stored hash: {patient['password']}")      # 🔍 Debug
                    if check_password_hash(patient['password'], pwd):
                        session['user_id'] = patient['patient_id']
                        session['user_type'] = 'patient'
                        return redirect(url_for('patient_profile'))
                    else:
                        print("Password mismatch")  # 🔍 Debug

            elif user_type == 'doctor':
                lic = request.form.get('license_number')
                pwd = request.form.get('password')
                print(f"Trying to log in as doctor with License: {lic}")  # 🔍 Debug
                cur.execute("SELECT * FROM doctor WHERE license_number = %s", (lic,))
                doctor = cur.fetchone()
                if doctor:
                    print(f"Found doctor: Dr. {doctor['first_name']} {doctor['last_name']}")  # 🔍 Debug
                    print(f"Stored hash: {doctor['password']}")  # 🔍 Debug
                    if check_password_hash(doctor['password'], pwd):
                        session['user_id'] = doctor['doctor_id']
                        session['user_type'] = 'doctor'
                        return redirect(url_for('doctor_profile'))
                    else:
                        print("Password mismatch")  # 🔍 Debug

            flash('Invalid credentials!')

        finally:
            cur.close()
            conn.close()
    return render_template('login.html')

@app.route('/patient_profile')
def patient_profile():
    if 'user_id' not in session or session['user_type'] != 'patient':
        flash('Please login first!')
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM patient WHERE patient_id = %s", (session['user_id'],))
        patient = cur.fetchone()
        return render_template('patient_profile.html', patient=patient) if patient else redirect(url_for('login'))
    finally:
        cur.close()
        conn.close()

@app.route('/doctor_profile')
def doctor_profile():
    if 'user_id' not in session or session['user_type'] != 'doctor':
        flash('Please login first!')
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM doctor WHERE doctor_id = %s", (session['user_id'],))
        doctor = cur.fetchone()
        return render_template('doctor_profile.html', doctor=doctor) if doctor else redirect(url_for('login'))
    finally:
        cur.close()
        conn.close()


@app.route('/edit_patient_profile', methods=['GET', 'POST'])
def edit_patient_profile():
    if 'user_id' not in session or session['user_type'] != 'patient':
        flash('Please login first!')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT * FROM patient WHERE patient_id = %s", (session['user_id'],))
        patient = cur.fetchone()

        if not patient:
            flash('Patient not found!')
            return redirect(url_for('login'))

        if request.method == 'POST':
            # Get form data
            medical_record_number = request.form.get('medical_record_number')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            date_of_birth = request.form.get('date_of_birth')
            gender = request.form.get('gender')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            bloodtype = request.form.get('bloodtype')

            # Handle photo upload if provided
            photo_url = patient['photo_url']
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    if '.' in photo.filename and photo.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg',
                                                                                              'gif'}:
                        result = cloudinary.uploader.upload(photo)
                        photo_url = result['secure_url']
                    else:
                        flash('Allowed image types are: png, jpg, jpeg, gif')
                        return render_template('edit_patient_profile.html', patient=patient)

            # Check if another patient already has this MRN (only if changed)
            if medical_record_number != patient['medical_record_number']:
                cur.execute("SELECT * FROM patient WHERE medical_record_number = %s AND patient_id != %s",
                            (medical_record_number, session['user_id']))
                if cur.fetchone():
                    flash('Medical Record Number already exists!')
                    return render_template('edit_patient_profile.html', patient=patient)

            # Update patient record
            cur.execute('''
                UPDATE patient
                SET medical_record_number = %s,
                    first_name = %s, 
                    last_name = %s,
                    date_of_birth = %s,
                    gender = %s,
                    phone = %s,
                    email = %s,
                    address = %s,
                    bloodtype = %s,
                    photo_url = %s
                WHERE patient_id = %s
            ''', (
                medical_record_number,
                first_name,
                last_name,
                date_of_birth,
                gender,
                phone,
                email,
                address,
                bloodtype,
                photo_url,
                session['user_id']
            ))

            conn.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('patient_profile'))

        return render_template('edit_patient_profile.html', patient=patient)

    except Exception as e:
        conn.rollback()
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('patient_profile'))
    finally:
        cur.close()
        conn.close()

@app.route('/edit_doctor_profile', methods=['GET', 'POST'])
def edit_doctor_profile():
    if 'user_id' not in session or session['user_type'] != 'doctor':
        flash('Please log in first!')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT * FROM doctor WHERE doctor_id = %s", (session['user_id'],))
        doctor = cur.fetchone()

        if request.method == 'POST':
            # Handle form submission for updating the doctor profile
            license_number = request.form.get('license_number')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            specialty = request.form.get('specialty')
            department = request.form.get('department')
            phone = request.form.get('phone')
            email = request.form.get('email')
            hire_date = request.form.get('hire_date')
            salary = request.form.get('salary')

            # Handle photo upload
            photo_url = doctor['photo_url']
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    result = cloudinary.uploader.upload(photo)
                    photo_url = result['secure_url']

            # Update the doctor record
            cur.execute('''
                UPDATE doctor
                SET license_number = %s,
                    first_name = %s,
                    last_name = %s,
                    specialty = %s,
                    department = %s,
                    phone = %s,
                    email = %s,
                    hire_date = %s,
                    salary = %s,
                    photo_url = %s
                WHERE doctor_id = %s
            ''', (
                license_number,
                first_name,
                last_name,
                specialty,
                department,
                phone,
                email,
                hire_date,
                salary,
                photo_url,
                session['user_id']
            ))
            conn.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('doctor_profile'))

        return render_template('edit_doctor_profile.html', doctor=doctor)

    except Exception as e:
        conn.rollback()
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('doctor_profile'))
    finally:
        cur.close()
        conn.close()

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    try:
        conn = get_db_connection()
        print("Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")
    app.run(debug=True)