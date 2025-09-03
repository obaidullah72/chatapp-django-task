# ChatApp (Django)

A simple, educational chat application built with **Django**.  
The project is organized as a standard Django project (`chatapp`) with feature apps for **chat** and **users**, plus HTML templates.  
Repo structure includes `chat/`, `users/`, `chatapp/`, `templates/`, `manage.py`, and `requirements.txt`.  
([GitHub][1])

---

## ✨ Features

- User authentication (register, login, logout)
- Create/join chat rooms (basic text chat)
- Server-rendered templates for a straightforward UX
- SQLite by default for quick local setup

> **Note:** The project is meant as a learning scaffold. Extend with pagination, profile pages, file uploads, or real-time websockets (Django Channels) as you iterate.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Templates:** Django templates (HTML)
- **Database:** SQLite (development)
- **Tooling:** pip / venv

GitHub reports the code mix as ~**86% Python** and **14% HTML** for this repo. ([GitHub][1])

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/obaidullah72/chatapp-django-task.git
cd chatapp-django-task
````

### 2. Create & activate a virtual environment

```bash
# Linux / Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

(The repo includes a `requirements.txt` at project root.) ([GitHub][2])

### 4. Set environment variables

Create a `.env` file (or set in shell) with at least:

```bash
# Required
SECRET_KEY=change-me

# Optional
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

> If `.env` loading isn’t wired yet, you can set these directly in `settings.py`.

### 5. Apply migrations & create superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📂 Project Layout

```
chatapp-django-task/
├─ chat/            # Chat app: views, urls, models for rooms/messages
├─ users/           # Users app: auth, profiles (Django auth hooks)
├─ templates/       # base.html, auth and chat templates
├─ chatapp/         # Project settings, urls, wsgi/asgi
├─ manage.py
└─ requirements.txt
```

(Top-level folders visible on GitHub.) ([GitHub][1])

---

## 🔗 Common URLs (conventional)

* `/` – Home / rooms list
* `/chat/<room_slug>/` – Room detail
* `/login/`, `/logout/`, `/register/` – Authentication
* `/admin/` – Django admin panel

Check each app’s `urls.py` to confirm exact patterns.

---

## 💡 Development Tips

* **Styling:** Extend `base.html` and add components in `templates/`.
* **Messages model:** Add indexes on `(room, created_at)` for faster loads.
* **Users:** Hook signals to create a profile on user creation if needed.
* **Settings split:** Consider `settings/base.py`, `settings/dev.py`, `settings/prod.py` as the app grows.

---

## ⚡ Going Real-Time (Optional)

To enable **real-time chat**:

1. Add **Django Channels** and an ASGI server (e.g., Daphne/Uvicorn).
2. Configure `ASGI_APPLICATION` and `CHANNEL_LAYERS` (Redis recommended).
3. Create `consumers.py` and `routing.py` in the `chat` app.
4. Update templates to connect to the websocket room group.

---

## 🧪 Testing

```bash
pytest
# or
python manage.py test
```

Add unit tests under each app (e.g., `chat/tests/`, `users/tests/`).

---

## 📦 Deployment

* Set `DEBUG=False`
* Configure `ALLOWED_HOSTS`
* Use a production DB (PostgreSQL recommended)
* Collect static files:

```bash
python manage.py collectstatic
```

* Run with **Gunicorn/Uvicorn + Nginx** (ASGI required if using Channels)

---

## 📜 License

If you plan to open-source, add a LICENSE file (e.g., MIT).
Otherwise, state proprietary use.

---

## 🙏 Acknowledgements

* Django documentation & tutorial patterns
* (Optional) Django Channels for real-time extensions

---

## 📚 References

* Repository overview and structure ([GitHub][1])
* Dependencies file `requirements.txt` ([GitHub][2])

---

[1]: https://github.com/obaidullah72/chatapp-django-task "GitHub - obaidullah72/chatapp-django-task"
[2]: https://github.com/obaidullah72/chatapp-django-task/blob/main/requirements.txt "chatapp-django-task/requirements.txt"