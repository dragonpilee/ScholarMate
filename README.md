# ScholarMate - AI-Powered Learning Companion

ScholarMate is an intelligent tutoring platform that leverages advanced AI technology to provide personalized learning experiences across various subjects and educational levels. Powered by the DeepSeek-R1-Distill-LLaMA-70B model, it delivers high-quality, contextual responses optimized for educational purposes.

## Features

### Core Functionality
- **Advanced AI Model**: Utilizes DeepSeek-R1-Distill-LLaMA-70B with optimized parameters (temperature=0.5, max_tokens=1536, top_p=0.9)
- **Multi-Subject Support**: Covers Mathematics, Physics, Chemistry, and Computer Science
- **Curriculum Alignment**: Supports multiple curricula (General, IB, AP, Cambridge)
- **Grade Level Adaptation**: From Pre-School to Post-Doctoral levels

### Learning Tools
- **Interactive Sessions**: Real-time Q&A with detailed explanations
- **Progress Tracking**: Visual analytics of learning progress
- **Session History**: Comprehensive record of past learning interactions
- **Personalized Learning**: Adapts to individual learning styles and pace

### User Experience
- **Modern UI**: Clean, responsive dark-mode interface
- **Accessibility**: ARIA-compliant navigation
- **Mobile-Friendly**: Optimized for all screen sizes
- **File Upload Support**: Easy attachment sharing for questions

## Tech Stack

### Backend
- **Framework**: Flask 3.0.2 (Python web framework)
- **Database**: SQLAlchemy 2.0.41 with SQLite
- **Authentication**: Flask-Login 0.6.3
- **Database Migrations**: Flask-Migrate 4.0.5 with Alembic
- **Form Handling**: WTForms 3.2.1
- **Security**: Bcrypt 4.1.2 for password hashing
- **Environment Management**: Python-dotenv 1.0.1

### Frontend
- **Framework**: Jinja2 3.1.6 (Template engine)
- **CSS Framework**: TailwindCSS 2.2.19
- **Icons**: FontAwesome 6.0.0
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Responsive Design**: Mobile-first approach
- **Dark Mode**: Built-in dark theme

### AI Integration
- **Model**: DeepSeek-R1-Distill-LLaMA-70B
- **API Client**: Groq API (v0.26.0)
- **Response Format**: Markdown with LaTeX support
- **Optimization**: Custom parameter tuning for educational context

### Development & Deployment
- **Server**: Gunicorn 21.2.0 (WSGI HTTP Server)
- **Version Control**: Git
- **Python Version**: 3.8+
- **Code Style**: PEP 8 compliant
- **Documentation**: Markdown
- **Environment**: Virtual environment (venv)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/scholarmate.git
cd scholarmate
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```env
SECRET_KEY=your_secret_key_here
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite:///scholarmate.db
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Migrate
- Groq API
- Python-dotenv
- Werkzeug
- Other dependencies listed in requirements.txt

## Project Structure

```
scholarmate/
├── app.py              # Main application file
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── about.html     # About page
│   ├── contact.html   # Contact form
│   ├── dashboard.html # User dashboard
│   └── ...           # Other templates
├── static/            # Static files
│   └── css/          # CSS files
├── migrations/        # Database migrations
└── requirements.txt   # Project dependencies
```

## Features in Detail

### AI Tutoring
- **Model**: DeepSeek-R1-Distill-LLaMA-70B
- **Parameters**:
  * Temperature: 0.5 (for consistent, focused responses)
  * Max Tokens: 1536 (optimal length for educational content)
  * Top P: 0.9 (balanced creativity and accuracy)
  * Frequency Penalty: 0.3 (reduces repetition)
  * Presence Penalty: 0.3 (maintains topic relevance)
- Step-by-step explanations with LaTeX support
- Real-time response generation

### User Management
- Secure authentication system
- Profile customization
- Grade level and curriculum selection
- Progress tracking and analytics

### Support System
- Comprehensive help center
- Feedback submission with file attachments
- Priority-based support tickets
- Contact form with response tracking

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Support Email: support@scholarmate.com

## Acknowledgments

- Groq API for AI model access
- TailwindCSS for styling
- FontAwesome for icons
- All contributors and users of ScholarMate 
