# Lab & Classroom Availability System

A full-stack web application for checking and managing lab and classroom schedules. The system helps students, faculty, and administrators find available locations, search schedules by capacity or faculty, view the complete timetable, and manage schedule data.

## Features

- Check whether a lab or classroom is available for a specific day and time slot
- Find locations that meet a minimum capacity requirement
- Search faculty schedules
- Filter locations by day or time slot
- View the complete timetable
- Add, update, and delete schedule entries through the management interface
- Display schedule statistics, including free and occupied slots
- Store schedule data in Supabase
- Responsive browser-based interface

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript (ES modules)
- Vite
- Font Awesome

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- Supabase Python client
- python-dotenv

### Database

- Supabase
- `lab_schedule` table

## Project Structure

```text
.
├── index.html                 # Frontend entry point
├── src/
│   ├── js/main.js             # Frontend behavior and API requests
│   └── styles/main.css        # Application styles
├── main.py                    # FastAPI backend using Supabase
├── main2.py                   # Alternative backend using a local Excel file
├── requirements.txt           # Python dependencies
├── package.json               # Frontend scripts and dependencies
├── package-lock.json
├── supabase/                  # Supabase-related project files
└── Newlabdata/                # Local data files, if used
```

## Prerequisites

Install the following before running the project:

- Python 3.9 or newer
- Node.js 18 or newer
- npm
- A Supabase project and database table

## Supabase Configuration

Create a `.env` file in the project root:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
```

The backend expects a Supabase table named `lab_schedule` with columns similar to:

| Column | Suggested type | Description |
|---|---|---|
| `id` | UUID or text | Unique schedule entry identifier |
| `location` | text | Lab or classroom name |
| `day` | text | Day of the week |
| `time_slot` | text | `Slot 1`, `Slot 2`, or `Slot 3` |
| `faculty` | text | Faculty name or `Free` |
| `batch` | text, nullable | Assigned batch or class |
| `capacity` | integer | Room capacity |

Do not commit `.env` files or Supabase secret keys to version control.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/PrachiSukreSS/labs_data_checkd.git
cd labs_data_checkd
```

### 2. Install frontend dependencies

```bash
npm install
```

### 3. Create and activate a Python virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create the `.env` file described in the [Supabase Configuration](#supabase-configuration) section.

## Running the Application

Start the FastAPI backend from the project root:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

In a separate terminal, start the Vite frontend:

```bash
npm run dev
```

Open the local URL printed by Vite, usually:

```text
http://localhost:5173
```

To create a production frontend build:

```bash
npm run build
```

To preview the production build locally:

```bash
npm run preview
```

## API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns API information and supported features |
| `GET` | `/stats/` | Returns schedule statistics |

### Schedule Queries

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/locations/` | Lists all locations |
| `POST` | `/availability/` | Checks availability for a location, day, and time slot |
| `POST` | `/locations/capacity/` | Finds locations matching a minimum capacity |
| `GET` | `/timetable/` | Returns the complete timetable |
| `GET` | `/locations/day/?day=Monday` | Lists locations scheduled on a day |
| `GET` | `/locations/time/?time_slot=Slot%201` | Lists locations scheduled in a time slot |
| `POST` | `/locations/faculty/` | Returns a faculty member's schedule |

### Administration

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/admin/entries/` | Lists all schedule entries |
| `POST` | `/admin/entries/` | Creates a schedule entry |
| `PUT` | `/admin/entries/{entry_id}` | Updates a schedule entry |
| `DELETE` | `/admin/entries/{entry_id}` | Deletes a schedule entry |

Example request for checking availability:

```json
{
  "location_name": "Computer Lab",
  "day": "Monday",
  "time_slot": "Slot 1"
}
```

Example request for creating a schedule entry:

```json
{
  "location": "Computer Lab",
  "day": "Monday",
  "time_slot": "Slot 1",
  "faculty": "Free",
  "batch": null,
  "capacity":  treinta
}
```

Replace `treinta` with a numeric capacity value, for example `30`.

## Alternative Local Excel Backend

`main2.py` contains an alternative FastAPI implementation that reads schedule data from an Excel file using pandas. To use it, set the file location in `.env`:

```env
FILE_PATH=/path/to/your/schedule.xlsx
```

Then start it with:

```bash
uvicorn main2:app --reload --host 127.0.0.1 --port 8000
```

The Excel file should contain columns such as:

```text
location, day, time_slot, faculty, batch, capacity
```

## Usage

1. Open the frontend in a browser.
2. Select a location, day, and time slot to check availability.
3. Search for rooms by minimum capacity.
4. Search for a faculty member's schedule.
5. Use the day and time filters to explore scheduled locations.
6. Load the complete timetable when a full view is needed.
7. Use **Manage Data** to add, edit, or delete schedule entries.

A slot is treated as available when its `faculty` value is `Free`.

## Security Notes

- Restrict CORS origins before deploying to production.
- Use environment variables for Supabase credentials.
- Avoid exposing service-role keys in the frontend.
- Add authentication and authorization before enabling administrative operations publicly.
- Validate and sanitize all user-provided schedule data.

## Troubleshooting

### The backend does not start

- Confirm that Python dependencies are installed.
- Verify that `SUPABASE_URL` and `SUPABASE_ANON_KEY` exist in `.env`.
- Ensure the Supabase project is reachable.

### The frontend cannot reach the API

- Confirm that the FastAPI server is running on port `8000`.
- Check the API base URL in `src/js/main.js`.
- Check browser developer tools for CORS or network errors.

### No schedule data is returned

- Confirm that the `lab_schedule` table exists.
- Verify the table column names and data types.
- Check that the selected day and time slot match the stored values exactly.

## License

No license has been specified yet. Add a license file if you plan to distribute or reuse this project.
