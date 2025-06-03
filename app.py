from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ff18e9b506ff42a1922312c08094f705eb20a46d4a306ba523b495d335e26614')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///scholarmate.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Subject configurations
SUBJECTS = {
    'mathematics': {
        'topics': ['Algebra', 'Geometry', 'Calculus', 'Statistics', 'Trigonometry', 'Number Theory'],
        'description': 'Master mathematical concepts from basic arithmetic to advanced calculus'
    },
    'physics': {
        'topics': ['Mechanics', 'Thermodynamics', 'Electromagnetism', 'Quantum Physics', 'Optics', 'Waves'],
        'description': 'Understand the fundamental laws that govern our universe'
    },
    'chemistry': {
        'topics': ['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry', 'Biochemistry', 'Analytical Chemistry'],
        'description': 'Explore the composition, structure, and properties of matter'
    },
    'computer_science': {
        'topics': ['Programming', 'Data Structures', 'Algorithms', 'Web Development', 'Database Systems', 'Computer Architecture'],
        'description': 'Learn the principles of computing and software development'
    }
}

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    curriculum = db.Column(db.String(50), default='General')
    grade_level = db.Column(db.String(20), default='High School')
    sessions = db.relationship('Session', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    question = db.Column(db.Text)
    response = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# Context processor to make subjects available to all templates
@app.context_processor
def inject_subjects():
    return dict(subjects=SUBJECTS)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        flash('Invalid username or password.', 'error')
        return render_template('login.html')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all fields.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Tutoring routes
@app.route('/tutor/<subject>', methods=['GET'])
@app.route('/tutor', methods=['GET', 'POST'])
@login_required
def tutor(subject=None):
    if request.method == 'GET' and subject:
        return render_template('tutor.html', 
                            subjects=SUBJECTS,
                            subject=subject,
                            topics=SUBJECTS[subject]['topics'] if subject in SUBJECTS else [])
    
    if request.method == 'POST':
        subject = request.form.get('subject', '')
        topic = request.form.get('topic', '')
        question = request.form.get('question', '')
        
        if not subject or not topic or not question:
            flash('Please select a subject, topic, and provide a question.', 'error')
            return render_template('tutor.html', subjects=SUBJECTS)
        
        try:
            groq_api_key = os.getenv('GROQ_API_KEY')
            if not groq_api_key:
                flash('AI Tutor is not properly configured. Please contact support.', 'error')
                return render_template('tutor.html', subjects=SUBJECTS)

            client = Groq(api_key=groq_api_key)
            
            chat_prompt = f"""You are an expert {subject} tutor specializing in {topic} for {current_user.grade_level} students.
            Please explain the following concept/question in a clear, step-by-step manner:

            {question}

            Structure your response with:
            1. Basic concept explanation in simple terms
            2. Key formulas, rules, or principles (if applicable)
            3. Step-by-step solution or explanation
            4. Real-world applications and examples
            5. A practice problem for the student to try
            6. Additional resources or related topics to explore
            
            Format your response in markdown for better readability.
            Use LaTeX notation for mathematical formulas where appropriate."""

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are Sapiens Tutor, a highly knowledgeable and patient {subject} tutor. You excel at explaining complex concepts in simple terms while maintaining academic rigor. You follow {current_user.curriculum} curriculum standards."
                    },
                    {
                        "role": "user",
                        "content": chat_prompt
                    }
                ],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.5,
                max_tokens=1536,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.3,
            )

            response = chat_completion.choices[0].message.content

            # Save the tutoring session
            new_session = Session(
                user_id=current_user.id,
                subject=subject,
                topic=topic,
                question=question,
                response=response
            )
            db.session.add(new_session)
            db.session.commit()

            return render_template('tutor.html', 
                                subjects=SUBJECTS,
                                response=response, 
                                subject=subject, 
                                topic=topic,
                                question=question)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return render_template('tutor.html', subjects=SUBJECTS)

    return render_template('tutor.html', subjects=SUBJECTS)

@app.route('/dashboard')
@login_required
def dashboard():
    sessions = Session.query.filter_by(user_id=current_user.id).order_by(Session.timestamp.desc()).all()
    return render_template('dashboard.html', sessions=sessions, subjects=SUBJECTS)

# Profile and Settings Routes
@app.route('/profile')
@login_required
def profile():
    sessions = Session.query.filter_by(user_id=current_user.id).order_by(Session.timestamp.desc()).all()
    return render_template('profile.html', sessions=sessions, subjects=SUBJECTS)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        try:
            # Update email if provided and different
            new_email = request.form.get('email')
            if new_email and new_email != current_user.email:
                if User.query.filter_by(email=new_email).first():
                    flash('Email already exists.', 'error')
                    return redirect(url_for('settings'))
                current_user.email = new_email

            # Update curriculum if provided
            if 'curriculum' in request.form:
                current_user.curriculum = request.form['curriculum']
            
            # Update grade level if provided
            if 'grade_level' in request.form:
                current_user.grade_level = request.form['grade_level']
            
            # Handle password change
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if current_password and new_password:
                if not current_user.check_password(current_password):
                    flash('Current password is incorrect.', 'error')
                    return redirect(url_for('settings'))
                
                if new_password != confirm_password:
                    flash('New passwords do not match.', 'error')
                    return redirect(url_for('settings'))
                
                current_user.set_password(new_password)
            
            db.session.commit()
            flash('Settings updated successfully!', 'success')
            return redirect(url_for('settings'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating settings: {str(e)}', 'error')
            
    return render_template('settings.html')

@app.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    try:
        # Delete all user sessions
        Session.query.filter_by(user_id=current_user.id).delete()
        
        # Delete the user
        user = User.query.get(current_user.id)
        db.session.delete(user)
        db.session.commit()
        
        # Log out the user
        logout_user()
        flash('Your account has been successfully deleted.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        db.session.rollback()
        flash('Error deleting account. Please try again.', 'error')
        return redirect(url_for('settings'))

# Learning Progress Routes
@app.route('/progress')
@login_required
def progress():
    # Get user's learning progress statistics
    total_sessions = Session.query.filter_by(user_id=current_user.id).count()
    
    # Get subject statistics with proper counting
    subject_stats = db.session.query(
        Session.subject,
        db.func.count(Session.id).label('count')
    ).filter_by(user_id=current_user.id)\
     .group_by(Session.subject)\
     .order_by(db.func.count(Session.id).desc())\
     .all()
    
    # Get recent sessions
    recent_sessions = Session.query.filter_by(user_id=current_user.id)\
        .order_by(Session.timestamp.desc())\
        .limit(5).all()
    
    # Calculate subject percentages
    subject_percentages = []
    if total_sessions > 0:
        for subject, count in subject_stats:
            percentage = (count / total_sessions) * 100
            subject_percentages.append((subject, count, percentage))
    
    return render_template('progress.html', 
                         total_sessions=total_sessions,
                         subject_stats=subject_stats,
                         sessions=recent_sessions,
                         subject_percentages=subject_percentages)

@app.route('/history')
@login_required
def history():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # Get paginated sessions
        sessions = Session.query.filter_by(user_id=current_user.id)\
            .order_by(Session.timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        if not sessions.items and page > 1:
            return redirect(url_for('history', page=1))
            
        return render_template('history.html', 
                             sessions=sessions,
                             current_page=page,
                             total_pages=sessions.pages)
    except Exception as e:
        flash(f'Error loading session history: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/curriculum', methods=['GET', 'POST'])
@login_required
def curriculum():
    try:
        if request.method == 'POST':
            new_curriculum = request.form.get('curriculum')
            if new_curriculum:
                current_user.curriculum = new_curriculum
                db.session.commit()
                flash('Curriculum updated successfully!', 'success')
            else:
                flash('Please select a curriculum.', 'error')
            return redirect(url_for('curriculum'))
        
        return render_template('curriculum.html')
    except Exception as e:
        flash(f'Error updating curriculum: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/grade-level', methods=['GET', 'POST'])
@login_required
def grade_level():
    try:
        if request.method == 'POST':
            new_grade = request.form.get('grade_level')
            if new_grade:
                current_user.grade_level = new_grade
                db.session.commit()
                flash('Grade level updated successfully!', 'success')
            else:
                flash('Please select a grade level.', 'error')
            return redirect(url_for('grade_level'))
        
        return render_template('grade_level.html')
    except Exception as e:
        flash(f'Error updating grade level: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

# Help and Support Routes
@app.route('/help')
def help_center():
    return render_template('help.html')

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    try:
        if request.method == 'POST':
            feedback_type = request.form.get('feedback_type')
            subject = request.form.get('subject')
            message = request.form.get('message')
            priority = request.form.get('priority')
            
            if not all([feedback_type, subject, message, priority]):
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('feedback'))
            
            # Here you would typically save the feedback to a database
            # For now, we'll just show a success message
            flash('Thank you for your feedback! We will review it shortly.', 'success')
            return redirect(url_for('dashboard'))
            
        return render_template('feedback.html')
    except Exception as e:
        flash(f'Error submitting feedback: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

# Additional Routes
@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        flash(f'Error loading about page: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/privacy')
def privacy():
    try:
        return render_template('privacy.html')
    except Exception as e:
        flash(f'Error loading privacy policy: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/terms')
def terms():
    try:
        return render_template('terms.html')
    except Exception as e:
        flash(f'Error loading terms of service: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')
            priority = request.form.get('priority')
            
            if not all([name, email, subject, message, priority]):
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('contact'))
            
            # Here you would typically save the contact message to a database
            # and/or send an email notification to support@scholarmate.com
            flash('Thank you for your message. We will get back to you soon!', 'success')
            return redirect(url_for('contact'))
            
        return render_template('contact.html')
    except Exception as e:
        flash(f'Error processing contact form: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True) 