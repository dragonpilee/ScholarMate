from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, User, Session, Message, groq_client
from werkzeug.security import generate_password_hash

# Available subjects and topics
SUBJECTS = {
    'mathematics': ['Algebra', 'Geometry', 'Calculus', 'Statistics', 'Trigonometry'],
    'science': ['Physics', 'Chemistry', 'Biology', 'Earth Science', 'Astronomy'],
    'english': ['Grammar', 'Literature', 'Writing', 'Vocabulary', 'Comprehension'],
    'history': ['World History', 'US History', 'European History', 'Ancient Civilizations']
}

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
            
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', subjects=SUBJECTS)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.curriculum = request.form.get('curriculum')
        current_user.grade_level = request.form.get('grade_level')
        
        if request.form.get('new_password'):
            if current_user.check_password(request.form.get('current_password')):
                current_user.set_password(request.form.get('new_password'))
            else:
                flash('Current password is incorrect', 'error')
                return redirect(url_for('settings'))
                
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        
    return render_template('settings.html')

@app.route('/chat/<subject>')
@login_required
def chat(subject):
    topic = request.args.get('topic', 'General')
    session = Session(
        user_id=current_user.id,
        subject=subject,
        topic=topic
    )
    db.session.add(session)
    db.session.commit()
    
    return render_template('chat.html', subject=subject, topic=topic, session_id=session.id)

@app.route('/api/chat', methods=['POST'])
@login_required
def process_message():
    data = request.json
    session_id = data.get('session_id')
    user_message = data.get('message')
    
    # Save user message
    message = Message(
        session_id=session_id,
        content=user_message,
        is_ai=False
    )
    db.session.add(message)
    
    # Get session context
    session = Session.query.get(session_id)
    
    # Create AI response using Groq
    system_prompt = f"""You are an expert tutor in {session.subject}, specifically {session.topic}.
    The student is at a {current_user.grade_level} level following {current_user.curriculum} curriculum.
    Provide clear, helpful explanations and guide the student's learning."""
    
    try:
        completion = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",  # or "llama2-70b-4096"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        ai_response = completion.choices[0].message.content
        
        # Save AI response
        ai_message = Message(
            session_id=session_id,
            content=ai_response,
            is_ai=True
        )
        db.session.add(ai_message)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "response": ai_response
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/history')
@login_required
def history():
    sessions = Session.query.filter_by(user_id=current_user.id).order_by(Session.timestamp.desc()).all()
    return render_template('history.html', sessions=sessions) 