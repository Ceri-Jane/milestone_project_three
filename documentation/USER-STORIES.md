# User Story 1
## Must-have
- **Title:** User Registration
- **User Story:** As a new user I want to create an account so that I can save and manage my movie shelves.

- **Acceptance Criteria:**
  - A sign-up form exists
  - Errors are shown for invalid input

- **Tasks:**
  - Create registration view
  - Build template
  - Add URL route
  - Add success redirect
  - Validate form

Return to [README.md](../README.md)

---
---

# User Story 2
## Must-have
- **Title:** User Login
- **User Story:** As a returning user I want to log in so that I can access my saved movies.

- **Acceptance Criteria:**
  - Login page exists
  - Incorrect credentials show an error
  - Successful login signs the user in and redirects to the authenticated homepage
  - Navbar updates to show logged-in options (Profile, My Shelf, Logout)

- **Tasks:**
  - Use Django login view
  - Add template
  - Add URL
  - Configure redirect URL
  - Add accessible error messages

Return to [README.md](../README.md)

---
---

# User Story 3
## Must-have
- **Title:** User Logout
- **User Story:** As a logged-in user I want to log out so that no one else can access my account

- **Acceptance Criteria:**
  - Log out button available
  - Logs out and redirects to home

- **Tasks:**
  - Add logout view
  - Add link in navbar
  - Add redirect

Return to [README.md](../README.md)

---
---

# User Story 4
## Must-have
- **Title:** View Shelves
- **User Story:** As a user I want to view my movie shelves so that I can see what I’ve watched and what to watch

- **Acceptance Criteria:**
•	Shelves page shows: To Watch, Watched, To Put Away
•	Sections are displayed using accordions
•	Only the logged-in user’s movies show
•	Each section lists its movies correctly based on the stored status

- **Tasks:**
  - Create shelves view
  - Add template
  - Query only the logged-in user’s movies
  - Split movies into three lists based on their status
  - Add URL

Return to [README.md](../README.md)

---
---

# User Story 5
## Must-have
- **Title:** Add Movie to Shelf
- **User Story:** As a user I want to add a movie to a shelf so that I can track what I plan to watch

- **Acceptance Criteria:**
  - When a movie is added, it is automatically placed in the To Put Away shelf
  - The “Add to Shelf” button disappears and becomes ‘Already in Your Shelf’
  - Duplicate movies are prevented from being added
  - Movie details (title, poster, tmdb_id) are saved correctly to the database

- **Tasks:**
  - Create add_to_shelf view
  - Add button + form submission logic
  - Add database logic for creating the Movie entry
  - Block duplicates using tmdb_id + user check
  - Return user to search results with feedback state

Return to [README.md](../README.md)

---
---

# User Story 6
## Must-have
- **Title:** Update Movie Status
- **User Story:** As a user I want to move movies between shelves so that I can update their status based on viewing

- **Acceptance Criteria:**
  - Buttons exist to move movies between shelves:
    - To Put Away → To Watch
    - To Put Away → Watched
    - To Watch → Watched
    - Watched → To Watch
  - Page updates with preserved UI state
  - Status updates correctly in the database

- **Tasks:**
  - Add URL/action endpoints
  - Update view logic to modify status field
  - Ensure UI state is saved and restored via shelf.js
  - Style buttons

Return to [README.md](../README.md)

---
---

# User Story 7
## Should-have
- **Title:** Remove Movie
- **User Story:** As a user I want to remove movies from my shelves so that I can clean up my lists

- **Acceptance Criteria:**
  - Delete button exists
  - Movie removed from DB

- **Tasks:**
  - Add delete view
  - Add button

Return to [README.md](../README.md)

---
---

# User Story 8
## Must-have
- **Title:** Search Movies
- **User Story:** As a user I want to search for movies using an external API so that I can find titles easily

- **Acceptance Criteria:**
  - Search bar exists
  - Queries TMDb
  - Displays results with posters and info
  - Each result has “Add to Shelf” options

- **Tasks:**
  - TMDb API view
  - Search form
  - Results template
  - Add API key in environment

Return to [README.md](../README.md)

---
---

# User Story 9
## Must-have
- **Title:** Responsive Navbar
- **User Story:** As a user I want a responsive navbar so that I can navigate the site easily on any device

- **Acceptance Criteria:**
  - Navbar easily accessible on all screen sizes
  - Navbar shows correct links depending on login/logout
  - Uses partial template

- **Tasks:**
  - Add conditional logic for logged-in vs logged-out users
  - Include navbar partial in base.html
  - Test on mobile and desktop sizes
  - Fix any alignment, spacing, or accessibility issues

Return to [README.md](../README.md)

---
---

# User Story 10
## Should-have
- **Title:** Consistent Layout
- **User Story:** As a user I want consistent pages so the site feels professional

- **Acceptance Criteria:**
  - All pages use the same layout
  - Navbar & footer appear everywhere
  - No duplicated HTML structures
  - All pages extend base.html

- **Tasks:**
  - Create templates/base.html
  - Move navbar + footer into partial templates
  - Include those partials inside base.html
  - Update all pages to use {% extends "base.html" %}
  - Move static CSS/JS into proper static directories
  - Test all views for layout consistency

Return to [README.md](../README.md)

---
---

# User Story 11
## Should-have
- **Title:** Admin Movie List
- **User Story:** As an admin I want to manage movies so that I can monitor site usage

- **Acceptance Criteria:**
  - Movies appear in Django admin with:
    - Poster thumbnails
    - Title, User, Status, Rating, TMDb ID
    - Created date
  - Admin can filter by:
    - Status
    - Rating
    - User
    - Created date
  - Admin can search by:
    - Movie title
    - TMDb ID
    - Username
  - Sorting (ordering) works correctly
  - Clicking the movie count on the User admin goes to a filtered list
  - No broken reverse URLs or permission issues
  - Group admin includes:
    - GroupProfile inline
    - Member count
    - Permission count
    - Group description

- **Tasks:**
  - Register Movie model in movies/admin.py
  - Add list_display, list_filter, search_fields, ordering
  - Add thumbnail method using format_html
  - Add user → movie count column with clickable filter
  - Unregister default User admin and create CustomUserAdmin
  - Remove first/last name from UserAdmin
  - Add GroupProfile model + GroupProfileInline
  - Create CustomGroupAdmin (member count, permissions count, description)
  - Fix/avoid reverse URL issues
  - Test admin pages on desktop/mobile
  - Confirm no broken queries or lookup errors

Return to [README.md](../README.md)

---
---

# User Story 12
## Must-have
- **Title:** Heroku Deployment
- **User Story:** As a developer I want the site deployed so users can access it online

- **Acceptance Criteria:**
•	App deploys without errors
•	Static files load correctly
•	Environment variables work
•	DEBUG is off in production
•	Secret key is hidden

- **Tasks:**
  - Backend / Settings
    - Add STATIC_ROOT
    - Add WhiteNoise to middleware
    - Add whitenoise.storage.CompressedManifestStaticFilesStorage
    - Add allowed hosts
    - Add environment variable for SECRET_KEY
    - Add environment variable for DEBUG
    - Update settings to use os.environ
  - Heroku Setup
    - Create Heroku app
    - Add Heroku Postgres (if needed)
    - Add Heroku config vars
      - SECRET_KEY
      - DEBUG=False
      - DISABLE_COLLECTSTATIC=1 initially
    - Create Procfile with gunicorn
    - Install dependences: gunicorn, whitenoise
    - Push to Heroku
    - Fix static file paths
    - Remove DISABLE_COLLECTSTATIC when ready
  - Final Deployment Checks
    - Load site & test all pages
    - Confirm templates render
    - Check all links
    - Check admin page
    - Check API key loads
    - Test on desktop + mobile
    - Validate HTML & CSS

Return to [README.md](../README.md)

---
---

# User Story 13
## Could-have
- **Title:** Dark Mode Toggle
- **User Story:** As a user I want to switch the site between light mode and dark mode so that I can view the app in whichever theme feels more comfortable

- **Acceptance Criteria:**
  - A toggle button appears in the navbar.
  - Clicking the toggle switches between two pre-defined themes.
  - The user’s choice is saved in local storage (optional).
  - Default theme remains light if the feature is not implemented.
  - If the toggle isn’t available, the site continues to function normally.

- **Tasks:**
  - Create a dark theme CSS class.
  - Add a toggle button (icon/button) to the navbar.
  - Add JavaScript to apply the theme on toggle.
  - Store theme preference (optional).

Return to [README.md](../README.md)

---
---

# User Story 14
## Could-have
- **Title:** User Avatar Upload
- **User Story:** As a user I want to upload a profile picture so that I can personalise my account

- **Acceptance Criteria:**
  - A user can optionally upload an image.
  - The image would display in their profile area.
  - A default avatar is used if no upload is made.
  - If the feature is missing, the site still works fully.

- **Tasks:**
  - Add an avatar field to the user model.
  - Create an upload form.
  - Add validation for file type and size.
  - Display the uploaded avatar on profile pages.
  - Add fallback default avatar.

Return to [README.md](../README.md)

---
---

# User Story 15
## Could-have
- **Title:** Add Pagination to Search Results
- **User Story:** As a user I want the search results to show a limited number of movies per page so that the page is easier to navigate without endless scrolling

- **Acceptance Criteria:**
  - Results are limited to a fixed number per page.
  - Pagination buttons (Next, Previous, page numbers) appear when needed.
  - Search query stays visible when switching pages.
  - No empty/broken pages appear.

- **Tasks:**
  - Add pagination logic to the home/search view.
  - Update template to show paginated results only.
  - Add and style pagination controls.
  - Ensure search query persists across pages.

Return to [README.md](../README.md)

---
---

