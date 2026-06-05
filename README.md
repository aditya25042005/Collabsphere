# CollabSphere

A student collaboration platform for discovering projects, finding teammates, and managing sprints — built for IIIT Kottayam.

---

## Features

### For Students
- **Discover Projects** — browse all active projects with search and tag filters
- **Apply to Projects** — one-click apply with role selection; track application status (Pending / Accepted)
- **Profile Page** — showcase your tech stack, bio, GitHub, LinkedIn, and project history
- **View Other Profiles** — visit any student's profile without needing to log in

### Project Management
- **Create Projects** — set title, description, tech tags, team size, and timeline
- **Sprint Management** — create sprints, assign tasks, track progress
- **Task Board** — kanban-style task cards with status tracking
- **Project Analytics** — visualise member activity and progress
- **Team Chat** — in-project messaging for collaborators

### Discovery & Networking
- **Users Directory** — search all students by name, role, or skill
- **Skill Filtering** — filter users by tech stack to find the right collaborators
- **Notifications** — real-time alerts for project applications and updates

### Auth & Security
- **Google Sign-In** — Firebase OAuth restricted to `@iiitkottayam.ac.in` emails
- **Email + Password** — alternative login for institute accounts
- **Auto Login** — persistent sessions via httpOnly cookies (uid + device fingerprint)
- **Secure Logout** — server-side cookie deletion so sessions fully expire

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 (App Router), TypeScript, Tailwind CSS |
| UI | shadcn/ui, Material UI Icons, Lucide React, Three.js |
| Backend | Flask (Python) |
| Database | PostgreSQL (Neon) |
| Auth | Firebase Authentication (Google + Email) |
| Session | httpOnly cookies (uid + fingerprint) |

---

## Project Structure

```
CollabSphere/
├── frontend/                        # Next.js 15 app
│   ├── app/                         # App Router pages
│   │   ├── page.tsx                 # Home / landing page
│   │   ├── layout.tsx               # Root layout (Navbar, ripple bg)
│   │   ├── globals.css              # Global styles + animations
│   │   ├── login/                   # Login page
│   │   ├── dashboard/               # Explore projects
│   │   ├── my-projects/             # User's own projects (current + past)
│   │   ├── users/                   # Browse all users
│   │   ├── profile/[id]/            # Dynamic profile page (view/edit)
│   │   ├── project/[id]/            # Project detail + sprint management
│   │   └── create_project/          # Create new project form
│   │
│   ├── components/                  # Reusable components
│   │   ├── navbar.tsx               # Sidebar navigation
│   │   ├── GoogleLogin.tsx          # Firebase Google auth + auto-login
│   │   ├── firebase.tsx             # Firebase config (collabsphere2)
│   │   ├── features.tsx             # Landing page features section
│   │   ├── Footerpage.tsx           # Footer with aurora bg + squiggly text
│   │   ├── hero-3d-scene.tsx        # Three.js 3D hero animation
│   │   ├── feature-3d-scene.tsx     # Three.js features section animation
│   │   ├── page-ripple-bg.tsx       # Full-page interactive ripple grid
│   │   ├── ripple-bg-loader.tsx     # SSR-safe wrapper for ripple bg
│   │   ├── notification.tsx         # Project application notifications
│   │   ├── project-layout.tsx       # Project page shell + top members
│   │   ├── project-details.tsx      # Project info + apply
│   │   ├── project-analytics.tsx    # Project stats charts
│   │   ├── team-members.tsx         # Project team list
│   │   ├── team-member-card.tsx     # User card (users page)
│   │   ├── team-member-modal.tsx    # User profile modal
│   │   ├── sprint-management.tsx    # Sprint CRUD
│   │   ├── sprint-details.tsx       # Sprint detail view
│   │   ├── create-project-form.tsx  # New project form
│   │   ├── create_sprint.tsx        # New sprint form
│   │   ├── task-card.tsx            # Kanban task card
│   │   ├── tasklist.tsx             # Task list view
│   │   ├── analytics.tsx            # Analytics charts
│   │   └── ui/                      # shadcn/ui primitives + custom
│   │       ├── aurora-background.tsx
│   │       ├── background-ripple-effect.tsx
│   │       └── squiggly-text.tsx
│   │
│   ├── lib/
│   │   ├── api.ts                   # API_BASE env var centralisation
│   │   ├── usercontext.tsx          # Global user state (React context)
│   │   ├── types.ts                 # Shared TypeScript types
│   │   └── utils.ts                 # cn() helper
│   │
│   ├── .env.local                   # NEXT_PUBLIC_BACKEND_URL, BACKEND_URL
│   └── next.config.ts               # Rewrite proxy /api/* → Flask
│
└── backend/                         # Flask API
    ├── app.py                       # Routes + CORS + cookie config
    ├── sql.py                       # All SQL query functions
    ├── auth.py                      # firebase_uid_required decorator
    ├── data_valid.py                # Marshmallow request schemas
    ├── smtp.py                      # Email notifications
    ├── sender.py                    # Email sender helper
    ├── key.json                     # Firebase Admin service account key
    ├── requirements.txt             # Python dependencies
    └── .env                         # NEON_DB_URL, FLASK_ENV, ALLOWED_ORIGINS
```

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- A [Neon](https://neon.tech) PostgreSQL database
- A Firebase project with Google Sign-In enabled

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create `backend/.env`:
```
NEON_DB_URL=postgresql://...
FLASK_ENV=development
ALLOWED_ORIGINS=http://localhost:3000
```

Place your Firebase Admin SDK key at `backend/key.json`.

```bash
python app.py
```

### Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:
```
NEXT_PUBLIC_BACKEND_URL=/api
BACKEND_URL=http://127.0.0.1:5000
```

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## Key Concepts

### Authentication Flow
1. User signs in with Google via Firebase (`GoogleLogin.tsx`)
2. Frontend sends `idToken` + `uid` + `fingerprint` to `/verify/google`
3. Backend verifies token with Firebase Admin, sets httpOnly cookies (`uid`, `fingerprint`)
4. On every page load, `/auto_login` checks cookies and redirects to dashboard if valid

### Cross-Origin Cookies
Frontend and backend run on different ports in dev. Next.js rewrites `/api/*` to `http://127.0.0.1:5000/*` so cookies are treated as same-origin.

### Environment Switching
| Setting | Development | Production |
|---------|-------------|------------|
| `FLASK_ENV` | `development` | `production` |
| `COOKIE_SECURE` | `False` | `True` |
| `COOKIE_SAMESITE` | `Lax` | `None` |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | your frontend URL |
| `NEXT_PUBLIC_BACKEND_URL` | `/api` | your backend URL |
