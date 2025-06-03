# ScholarMate - AI-Powered Learning Companion

![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask)
![Python](https://img.shields.io/badge/Language-Python-blue)
![TailwindCSS](https://img.shields.io/badge/Styling-TailwindCSS-38bdf8)
![DeepSeek-R1](https://img.shields.io/badge/AI-DeepSeek--R1-yellow)
![MIT License](https://img.shields.io/badge/License-MIT-green)

> If you find this project helpful, please consider ⭐ [starring the repository](https://github.com/yourusername/scholarmate)!

---

**ScholarMate** is a fully stack AI project and intelligent tutoring platform that leverages advanced AI technology to provide personalized learning experiences across various subjects and educational levels. Powered by the DeepSeek-R1 model, it delivers high-quality, contextual responses optimized for educational purposes.

---

## 📸 Screenshots

<img src="./Screenshot 2025-06-04 032902.png" alt="Screenshot 1" width="400"/>
<img src="./Screenshot 2025-06-04 032938.png" alt="Screenshot 2" width="400"/>
<img src="./Screenshot 2025-06-04 033008.png" alt="Screenshot 3" width="400"/>
<img src="./Screenshot 2025-06-04 033025.png" alt="Screenshot 4" width="400"/>

---

## ✨ Features

- **Advanced AI Model:** Utilizes DeepSeek-R1 with optimized parameters (temperature=0.5, max_tokens=1536, top_p=0.9)
- **Multi-Subject Support:** Mathematics, Physics, Chemistry, Computer Science
- **Curriculum Alignment:** Supports General, IB, AP, Cambridge
- **Grade Level Adaptation:** From Pre-School to Post-Doctoral
- **Interactive Sessions:** Real-time Q&A with detailed explanations
- **Progress Tracking:** Visual analytics of learning progress
- **Session History:** Comprehensive record of past learning interactions
- **Personalized Learning:** Adapts to individual learning styles and pace
- **Modern UI:** Clean, responsive dark-mode interface
- **Accessibility:** ARIA-compliant navigation
- **Mobile-Friendly:** Optimized for all screen sizes
- **File Upload Support:** Easy attachment sharing for questions

---

## 🛠️ Tech Stack

- **Backend:** Flask 3.0.2, SQLAlchemy 2.0.41 (SQLite), Flask-Login, Flask-Migrate, WTForms, Bcrypt, Python-dotenv
- **Frontend:** Jinja2, TailwindCSS, FontAwesome, Vanilla JS (ES6+), Responsive Design, Dark Mode
- **AI Integration:** DeepSeek-R1, Markdown with LaTeX support, custom parameter tuning
- **Development & Deployment:** Gunicorn, Git, Python 3.8+, PEP 8, Markdown docs, venv

---

## 🚀 Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/scholarmate.git
    cd scholarmate
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Unix/MacOS
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory with:
    ```
    SECRET_KEY=your_secret_key_here
    DATABASE_URL=sqlite:///scholarmate.db
    ```

5. **Initialize the database:**
    ```bash
    flask db upgrade
    ```

6. **Run the application:**
    ```bash
    python app.py
    ```
    The application will be available at [http://localhost:5000](http://localhost:5000)

---

## 📂 Project Structure

```
scholarmate/
├── app.py              # Main application file
├── templates/          # HTML templates
│   ├── base.html
│   ├── about.html
│   ├── contact.html
│   ├── dashboard.html
│   └── ... (other templates)
├── static/             # Static files
│   └── css/
├── migrations/         # Database migrations
└── requirements.txt    # Project dependencies
```

---

## 🧠 Features in Detail

### AI Tutoring
- **Model:** DeepSeek-R1
- **Parameters:**
  - Temperature: 0.5 (for consistent, focused responses)
  - Max Tokens: 1536 (optimal length for educational content)
  - Top P: 0.9 (balanced creativity and accuracy)
  - Frequency Penalty: 0.3 (reduces repetition)
  - Presence Penalty: 0.3 (maintains topic relevance)
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

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📬 Contact

Support Email: support@scholarmate.com

---

