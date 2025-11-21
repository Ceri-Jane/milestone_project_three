# Deployment

QuickFlicks was deployed to **Heroku** using a standard Django production setup with Gunicorn, WhiteNoise and environment variables. Below are the exact steps followed during deployment, along with explanations of *why* each step was necessary.

Return to [README.md](../README.md)

---

## 1. Create the Heroku App
1. Log in to the Heroku Dashboard.  
2. Click **Create New App**.  
3. Enter a unique name and choose the appropriate region (EU for UK users).

This creates the remote environment where the Django project will be hosted.

---

## 2. Configure Heroku Environment Variables
Inside the **Settings → Config Vars**, the following variables were added:

| KEY | VALUE | Purpose |
|-----|--------|---------|
| `SECRET_KEY` | *hidden* | Required for Django security |
| `DEBUG` | `False` | Prevents debug mode on live site |
| `TMDB_API_KEY` | *hidden* | API key for TMDb requests |
| `DISABLE_COLLECTSTATIC` | `1` (initially) | Avoids static collection errors during first build |

`DISABLE_COLLECTSTATIC` is *temporary*. It is removed once static file settings are complete.

---

## 3. Prepare Django for Production

### Install Gunicorn (production WSGI server)
```bash
pip install gunicorn~=20.1
pip freeze > requirements.txt
```

Gunicorn replaces `manage.py runserver` on Heroku.

### Add WhiteNoise for serving static files
In `settings.py`:
```python
MIDDLEWARE = [
    ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

WhiteNoise allows Django to serve static files without needing Nginx.

### Add STATIC_ROOT
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Heroku gathers all static files into this folder during deployment.

---

## 4. Create the Procfile
At the project root:

```
web: gunicorn quickflicks.wsgi
```

This tells Heroku how to run the Django application.

---

## 5. Update `ALLOWED_HOSTS`
In `settings.py`:

```python
ALLOWED_HOSTS = ['.herokuapp.com', '127.0.0.1', 'localhost']
```

Heroku requires its domain to be included.

---

## 6. Disable Django Debug Mode
```python
DEBUG = False
```

Debug MUST be off in production for security.

---

## 7. Push Code to GitHub
```bash
git add .
git commit -m "Prepare project for Heroku deployment"
git push
```

Heroku pulls from GitHub during deployment.

---

## 8. Connect Heroku to GitHub
In **Heroku → Deploy tab**:

1. Click **Connect to GitHub**  
2. Search for the QuickFlicks repository  
3. Click **Connect**  
4. Scroll down and click **Deploy Branch**

You can watch the build log in the Activity tab.

---

## 9. Enable an Eco Dyno
In **Resources → Dynos**, enable:

- **Eco Dyno** (required to run the site)

---

## 10. Remove Temporary Static Setting
Once the build succeeds:

1. Return to **Settings → Config Vars**  
2. Remove:  
   ```
   DISABLE_COLLECTSTATIC
   ```
3. Redeploy the branch.

Heroku runs `collectstatic` and WhiteNoise correctly serves static files.

---

## 11. Verify Deployment
Once deployed, the following checks were performed:

- Home page loads correctly  
- TMDb API requests succeed  
- Static files load (CSS, JS, images)  
- Navigation and shelves work as expected  
- Authentication system fully functional  
- Password reset emails previewed via Mailtrap  
- Admin panel loads without errors  
- Mobile and desktop responsiveness validated  
- Accessibility checks performed with WAVE  
- Lighthouse score tested  

**Live site:**  
https://quickflicks-2de9f6786033.herokuapp.com/

**Repository:**  
https://github.com/Ceri-Jane/milestone_project_three

---
---

Return to [README.md](../README.md)
