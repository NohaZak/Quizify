# Quizify
"Interactive Learning Platform - ALX Portfolio Project."
# Quizify: Interactive Learning Platform

## **Project Description**

Quizify is an interactive web application designed to enhance learning through engaging quizzes. The platform provides a user-friendly interface where users can securely log in, attempt quizzes on various topics, receive instant feedback, and track their performance over time. With Quizify, learning becomes gamified, reinforcing knowledge effectively.

---

## **Features**

- **Secure Authentication:** Register, log in, and log out with encrypted credentials.
- **Quizzes on Various Topics:** Dynamic quiz generation across multiple domains.
- **Instant Feedback:** Immediate evaluation of answers with correct explanations.
- **Performance Tracking:** Monitor progress and scores over time.
- **Responsive Design:** Seamless user experience across devices.

---

## **Technologies Used**

### **Backend**

- **Flask/Django**: Python frameworks for server-side functionality.
- **Flask-Login/Django Authentication**: Secure user management.
- **Flask-SQLAlchemy/Django ORM**: Interaction with the database.

### **Frontend**

- **HTML, CSS, JavaScript**: For responsive and interactive user interfaces.
- **Bootstrap**: Enhancing UI responsiveness and design.

### **Database**

- **SQLite**: Local development database.
- **PostgreSQL**: Production-ready database.

### **Version Control**

- **Git and GitHub**: For source code management and collaboration.

---

## **Setup Instructions**

### **Prerequisites**

- Python 3.8+
- Visual Studio
- Git

### **Local Installation**

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/Quizify.git
   cd Quizify
   ```

2. **Set Up a Virtual Environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # For Windows
   source venv/bin/activate  # For macOS/Linux
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   - For Flask:
     ```bash
     python app.py
     ```
   - For Django:
     ```bash
     python manage.py runserver
     ```

5. **Access the Application:**

   - Flask: Open [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - Django: Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

### **Database Setup**

- Default: SQLite for development.
- To use PostgreSQL:
  1. Update database configuration in the settings file.
  2. Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

---

## **Project Structure**

```
Quizify/
├── quizify/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   └── static/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## **Planned Enhancements**

- **Leaderboard:** Introduce global and topic-specific rankings.
- **Quiz Analytics:** Advanced analytics for users and admins.
- **Gamification:** Badges and rewards for milestones.

---

## **Contributors**

- **Noha Zakaria**: Backend and Frontend architecture design.



##

---

## **Contact Information**

For queries or contributions:

- **Email:** [nohazakaria55@gmail.com](mailto\:nohazakaria55@gmail.com)
- **GitHub:** NohaZak

