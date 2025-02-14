from flask import Flask, request, jsonify, render_template, redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user,current_user
import webbrowser
from threading import Timer
from utils.config import Config
from utils.rate_limiter import RateLimiter
from utils.gemini_client import GeminiClient
from utils.file_service import FileService

gemini_client=None
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'group2'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite for simplicity
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# Initialize services
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(int(user_id))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

config = Config()
rate_limiter = RateLimiter(config.MAX_RPM, config.MAX_TPM, config.MAX_RPD)
file_service = FileService(config.UPLOAD_FOLDER, config.ALLOWED_EXTENSIONS)


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        print("data:",data)
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
            
        # Get recent conversation history
        # Send message to Gemini
        response = gemini_client.send_message(message,current_user.name)
        
        # Save to memory
        
        return jsonify({
            "message": response
        })
        
    except Exception as e:
        print("error:",e)
        return jsonify({"error": str(e)}), 500
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validation
        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return redirect(url_for('register'))
        
        if User.query.filter_by(contact=contact).first():
            flash('Contact number already registered!')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Create new user
        user = User(email=email, contact=contact, name=name)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration.')
            return redirect(url_for('register'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            # New user registration
            flash("user not found !! please register")
            return redirect(url_for("register"))
        else:
            # Existing user login
            if not user.check_password(password):
                flash('Invalid password!')
                return redirect(url_for('login'))
            
        login_user(user)
        return redirect(url_for('input'))
    
    return render_template('login.html')

@app.route("/input")
@login_required
def input():
    global gemini_client
    gemini_client = GeminiClient(config.GOOGLE_API_KEY, rate_limiter,user_name=current_user.name)
    return render_template("input.html",user_name=current_user.name)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
def check_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                if 'GOOGLE_API_KEY' in line:
                    google_key_found = True
            if google_key_found:
                return True
        return False
    except FileNotFoundError:
        return False
@app.route('/check_keys', methods=['GET'])
def check_keys():
    keys_present = check_env_file()
    return jsonify({'keys_present': keys_present})

@app.route('/save_keys', methods=['POST'])
def save_keys():
    data=request.get_json()
    google_api_key = data.get('google_api_key','')

    with open('.env', 'w') as f:
        f.write(f"""GOOGLE_API_KEY="{google_api_key}"\n""")
        f.write(f"""TF_ENABLE_ONEDNN_OPTS=0\n""")

    return jsonify({'success': True})
@app.route('/documentation')
def documentation():
    return render_template('documentation.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/resources')
def resources():
    return render_template('references.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
            
        file = request.files['file']
        filepath = file_service.save_file(file)
        
        message = f"summarize the {file.filename} file"
        response = gemini_client.send_message(message)
        
        return jsonify({"message": response})
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == "__main__":
    Timer(1, open_browser).start()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",debug=True, port="5000")