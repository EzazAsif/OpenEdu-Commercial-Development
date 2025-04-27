# 📚 Django LMS - Hierarchical Learning Management System

A powerful, modern **Learning Management System (LMS)** built with **Django**, featuring:

- 🏛️ **Hierarchical user and role management**
- 💬 **Real-time chatting and notifications**
- 📹 **Multimedia content management** (images, videos, documents)
- ✅ **Approval system based on hierarchy levels**

---

## 🚀 Features

### Hierarchical User Roles
- Organized roles (e.g., Admin > Manager > Instructor > Student) with different permissions and access levels.

### Real-Time Communication
- Private and group chats with instant delivery
- In-app real-time notifications for updates, approvals, and messages

### Content Management
- Upload and organize multimedia (PDFs, videos, images, SCORM packages)
- Rich content editor for courses and lessons

### Approval System
- Multi-level approval flows for course creation, user actions, or resource requests
- Dynamic decision routing based on hierarchy

### Scalable and Modular
- Built using Django best practices
- Ready to extend with REST APIs, external services, or frontend frameworks

---

## 🛠️ Tech Stack

- **Backend**: Django 4.x, Django Channels (WebSocket support)
- **Database**: PostgreSQL (recommended), SQLite (for development)
- **Real-time**: Django Channels + Redis
- **Frontend**: HTML5, CSS3, JavaScript (Django templates) *(optionally replaceable by React/Vue)*
- **Others**: Django Storages (for media management), Celery (for async tasks), Redis

---

## 📂 Project Structure

```text
GitLms/
│   adminpass.txt
│   db.sqlite3
│   manage.py
│   requirements.txt
│   run_command.txt
│
├───accounts/
│   ├── accountfuncs.py
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── facade.py
│   ├── factory.py
│   ├── models.py
│   ├── observers.py
│   ├── singleton.py
│   ├── strategies.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── __init__.py
│   ├── static/
│   │   ├── css/
│   │   │   welcome.css
│   │   └── js/
│   │       welcome.js
│   └── templates/
│       ├── editprofile.html
│       ├── login.html
│       ├── loginsessions.html
│       ├── Registration.html
│       ├── settings.html
│       ├── viewprofile.html
│       └── welcome.html
│
├───commChat/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── __init__.py
│   ├── static/
│   │   ├── css/
│   │   │   commChat.css
│   │   └── js/
│   │       commChat.js
│   └── templates/
│       ├── commChat.html
│       └── commChatComponents/
│           ├── chatHeader.html
│           ├── inboxForm.html
│           ├── recieverText.html
│           └── senderText.html
│
├───errors/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── __init__.py
│   └── templates/
│       ├── illegalactivity.html
│       └── unauthorizedaccess.html
│
├───gitlms/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
│
├───home/
│   ├── admin.py
│   ├── appoint.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── __init__.py
│   ├── static/
│   │   ├── css/
│   │   │   dashboard.css
│   │   └── js/
│   │       appointDropDown.js
│   │       modal.js
│   │       popup.js
│   │       sidebar.js
│   │       update_modal.js
│   └── templates/
│       ├── courses.html
│       ├── dashboard.html
│       ├── appoint_modals/
│       │   └── appointModal.html
│       ├── content_modals/
│       │   ├── courseModal.html
│       │   ├── deptModal.html
│       │   ├── facultyModal.html
│       │   ├── noteModal.html
│       │   ├── slideModal.html
│       │   └── videoModal.html
│       ├── inc/
│       │   ├── footer.html
│       │   ├── header.html
│       │   ├── navbar.html
│       │   ├── popup.html
│       │   └── profileDropdown.html
│       ├── pages/
│       │   ├── appoint.html
│       │   └── students.html
│       └── update_content_modals/
│           ├── update_courseModal.html
│           ├── update_deptModal.html
│           ├── update_facultyModal.html
│           ├── update_noteModal.html
│           ├── update_slideModal.html
│           └── update_videoModal.html
│
├───lms/
│   ├── add_funcs.py
│   ├── admin.py
│   ├── apps.py
│   ├── contentFactory.py
│   ├── contentUploadAdapter.py
│   ├── contentUploadStratagy.py
│   ├── contentViewers.py
│   ├── delete_funcs.py
│   ├── models.py
│   ├── Observer.py
│   ├── queryProxy.py
│   ├── signals.py
│   ├── tests.py
│   ├── update_funcs.py
│   ├── urls.py
│   ├── views.py
│   ├── __init__.py
│   ├── static/
│   │   └── js/
│   │       ├── cardDropDown.js
│   │       ├── contentFullScreen.js
│   │       └── resourse_card.js
│   └── templates/
│       ├── contentViewers/
│       │   ├── noteViewer.html
│       │   ├── pdfViewer.html
│       │   └── videoViewer.html
│       └── lms/
│           ├── departments.html
│           ├── deptcourses.html
│           ├── faculty.html
│           ├── lectures.html
│           ├── notes.html
│           ├── slides.html
│           └── videos.html
│
├───media/
│   ├── contents/
│   └── images/
│
└───notifications/
    ├── admin.py
    ├── apps.py
    ├── consumers.py
    ├── models.py
    ├── routing.py
    ├── signals.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── __init__.py
    └── templates/
        ├── notification-2.html
        ├── notifications.html
        ├── viewNotificationDetailsSlide.html
        └── viewNotificationDetailsVideo.html
