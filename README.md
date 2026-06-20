# FitTrack 🚀

FitTrack is a personal fitness-tracking web app built as a learning-by-building project. The repository is intentionally developed in public to demonstrate practical full-stack patterns using FastAPI (backend) and a Vite + React + TypeScript frontend.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quickstart](#quickstart)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Development Notes](#development-notes)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Log fitness data (workouts, measurements, metrics)
- View progress over time with simple visualizations
- Authentication (including Google sign-in)
- Lightweight, learnable architecture designed for incremental enhancements

---

## Tech Stack

- **Backend:** FastAPI (see [Backend/requirements.txt](Backend/requirements.txt))
- **Frontend:** React + TypeScript + Vite (see [Frontend/package.json](Frontend/package.json))
- **Database:** PostgreSQL (local or hosted)
- **Other:** Git, REST APIs, environment-based configuration

---

## Project Structure

```text
FitTrack/
├── Backend/        # FastAPI backend (Python)
│   └── app/
├── Frontend/       # Vite + React + TypeScript
├── assets/         # screenshots and other static assets used in README
└── README.md
```

---

## Quickstart

Below are minimal steps to run the app locally for development. They assume you have Python 3.10+ and Node.js/npm installed.

### Backend

1. Open a terminal and change to the backend folder:

```powershell
cd Backend
```

2. Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the FastAPI development server:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend app entry is `app.main:app` (see `Backend/app/main.py`).

### Frontend

1. Open a new terminal and change to the frontend folder:

```bash
cd Frontend
```

2. Install dependencies and start the dev server:

```bash
npm install
npm run dev
```

The default Vite dev server runs on `http://localhost:5173` and CORS is already allowed from that origin in the backend config.

---

## Development Notes

- The FastAPI app is in `Backend/app/main.py` and exposes routers declared under `Backend/app/routers/`.
- The frontend entry is `Frontend/src/main.tsx` and uses Vite for HMR during development.
- Environment-specific settings and secrets should be provided via environment variables or a .env file; avoid committing secrets.

---

## Screenshots

<p align="center">
	<img src="assets/thumbnail.jpg" alt="Thumbnail" width="320" />
</p>

Gallery:

<p align="center">
	<img src="assets/pic1.png" alt="Screenshot 1" width="520" />
	<img src="assets/pic2.png" alt="Screenshot 2" width="520" />
	<img src="assets/pic3.png" alt="Screenshot 3" width="520" />
</p>

---

## Contributing

- Contributions, issues, and feature requests are welcome. Please open an issue first to discuss larger changes.
- Keep commits focused and add tests where applicable.
