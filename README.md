# Flask Notes App

A simple Flask web application where users can register, log in, and manage their personal notes.
Each user can create, edit, delete, and view only their own notes.
The app uses SQLite as the database and Bootstrap 5 for a clean modern UI.

---

##  Features
- User Registration
- User Login & Logout
- Create Notes
- Edit Notes
- Delete Notes
- Private notes per user
- SQLite Database
- Modern Bootstrap UI
- Secure password hashing

---

##  Project Structure
flask-notes-app
│
├─ app.py
├─ requirements.txt
├─ notes.db  (generated automatically)
│
├─ templates
│    ├─ base.html
│    ├─ index.html
│    ├─ add.html
│    ├─ edit.html
│    ├─ login.html
│    └─ register.html
│
└─ static
     └─ style.css  (optional)


---

##  Installation
Install required packages:

pip install flask werkzeug

or:

pip install -r requirements.txt

---

##  Run the App
python app.py

Then open in your browser:

http://127.0.0.1:5000

The database (notes.db) and tables will be created automatically on first run.

---

##  Authentication
### Register
Users create an account with username + password.

### Login
Login to access your notes.

### Logout
Clears session and redirects to login page.

### Protected Routes
All note-related pages require login.

---

## Notes Feature
Each logged-in user can:
- Add notes
- Edit notes
- Delete notes
- View only their own notes

Each note is linked to a user via `user_id`.

---

##  Requirements
Flask
Werkzeug

---

##  Common Issue
If you get an error like "no such column: user_id",
delete the file `notes.db` and run the app again.

---

##  Future Improvements
- Dark mode
- Search notes
- Password reset
- Tags/categories for notes
- Deploy online (Render, Railway)

---

##  Show Support
If you like this project, give it a star on GitHub!
