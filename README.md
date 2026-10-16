# Lab & Classroom Availability System

A beginner-friendly project to check lab/classroom availability by **location, day, and time slot**. It also supports searching by capacity, checking faculty schedules, and managing timetable entries.

## Tech stack
- Frontend: HTML, CSS, JavaScript (Vite)
- Backend API: FastAPI (Python)
- Database: Supabase (`lab_schedule` table)

## Main features
- Check whether a location is free or occupied
- Find locations by minimum capacity
- Search timetable entries by faculty
- Filter locations by day or time slot
- Admin-style add/update/delete schedule entries

## Repository structure
- `index.html`, `src/js`, `src/styles` - web UI
- `main.py` - current FastAPI API (Supabase-backed)
- `main2.py` - older FastAPI variant (Excel-file based)
- `supabase/migrations/` - SQL migration/data seed
- `requirements.txt` - Python dependencies
- `package.json` - frontend scripts/dependencies

## Setup
### 1) Frontend
```bash
npm install
```

Create a `.env` file for Vite frontend variables:
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 2) Backend
```bash
pip install -r requirements.txt
```

Set backend environment variables (for `main.py`):
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Run
### Start frontend (Vite)
```bash
npm run dev
```

### Start backend (FastAPI)
```bash
uvicorn main:app --reload
```

## Notes
- Frontend scripts are defined in `package.json`: `dev`, `build`, `preview`.
- If you use the older Excel-based API (`main2.py`), it expects a `FILE_PATH` to an `.xlsx` file.
