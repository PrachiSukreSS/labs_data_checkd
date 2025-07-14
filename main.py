from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from typing import List, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="Lab Availability API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic models
class LocationRequest(BaseModel):
    location_name: str
    day: str
    time_slot: str

class CapacityRequest(BaseModel):
    capacity: int

class FacultyRequest(BaseModel):
    faculty_name: str

class LabEntry(BaseModel):
    location: str
    day: str
    time_slot: str
    faculty: str
    batch: Optional[str] = None
    capacity: int

class UpdateLabEntry(BaseModel):
    location: Optional[str] = None
    day: Optional[str] = None
    time_slot: Optional[str] = None
    faculty: Optional[str] = None
    batch: Optional[str] = None
    capacity: Optional[int] = None

@app.get("/")
def greet():
    return {"message": "Hello! Welcome to the Lab/Classroom Availability System v2.0!"}

@app.get("/locations/")
def list_locations():
    try:
        response = supabase.table('lab_schedule').select('location').execute()
        locations = list(set([item['location'] for item in response.data]))
        return {"locations": sorted(locations)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations: {str(e)}")

@app.post("/availability/")
def check_availability(request: LocationRequest):
    try:
        response = supabase.table('lab_schedule').select('*').eq('location', request.location_name).eq('day', request.day).eq('time_slot', request.time_slot).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"No information available for '{request.location_name}' at {request.time_slot} on {request.day}.")
        
        entry = response.data[0]
        if entry['faculty'] == 'Free':
            return {"message": f"{request.location_name} is available at {request.time_slot} on {request.day}."}
        else:
            batch_info = f" (Batch: {entry['batch']})" if entry['batch'] else ""
            return {"message": f"{request.location_name} is occupied by {entry['faculty']}{batch_info} at {request.time_slot} on {request.day}."}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking availability: {str(e)}")

@app.post("/locations/capacity/")
def find_location_by_capacity(request: CapacityRequest):
    try:
        response = supabase.table('lab_schedule').select('location, capacity').gte('capacity', request.capacity).execute()
        
        if not response.data:
            return {"message": "No locations found with the required capacity."}
        
        locations = list(set([item['location'] for item in response.data]))
        return {"locations": sorted(locations)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding locations by capacity: {str(e)}")

@app.get("/timetable/")
def display_full_timetable():
    try:
        response = supabase.table('lab_schedule').select('*').order('location').execute()
        return {"timetable": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching timetable: {str(e)}")

@app.get("/locations/day/")
def check_available_locations_by_day(day: str):
    try:
        response = supabase.table('lab_schedule').select('location').eq('day', day).execute()
        
        if not response.data:
            return {"message": f"No locations available on {day}."}
        
        locations = list(set([item['location'] for item in response.data]))
        return {"locations": sorted(locations)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations by day: {str(e)}")

@app.get("/locations/time/")
def check_available_locations_by_time(time_slot: str):
    try:
        response = supabase.table('lab_schedule').select('location').eq('time_slot', time_slot).execute()
        
        if not response.data:
            return {"message": f"No locations available during {time_slot}."}
        
        locations = list(set([item['location'] for item in response.data]))
        return {"locations": sorted(locations)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations by time: {str(e)}")

@app.post("/locations/faculty/")
def search_by_faculty(request: FacultyRequest):
    try:
        response = supabase.table('lab_schedule').select('*').eq('faculty', request.faculty_name).order('day').execute()
        
        if not response.data:
            return {"message": f"No locations found for Faculty: {request.faculty_name}."}
        
        return {"schedule": response.data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching by faculty: {str(e)}")

# Admin endpoints for CRUD operations
@app.post("/admin/entries/")
def create_entry(entry: LabEntry):
    try:
        response = supabase.table('lab_schedule').insert(entry.dict()).execute()
        return {"message": "Entry created successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating entry: {str(e)}")

@app.put("/admin/entries/{entry_id}")
def update_entry(entry_id: int, entry: UpdateLabEntry):
    try:
        # Remove None values from the update data
        update_data = {k: v for k, v in entry.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        response = supabase.table('lab_schedule').update(update_data).eq('id', entry_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        return {"message": "Entry updated successfully", "data": response.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating entry: {str(e)}")

@app.delete("/admin/entries/{entry_id}")
def delete_entry(entry_id: int):
    try:
        response = supabase.table('lab_schedule').delete().eq('id', entry_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        return {"message": "Entry deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting entry: {str(e)}")

@app.get("/admin/entries/")
def get_all_entries():
    try:
        response = supabase.table('lab_schedule').select('*').order('location').execute()
        return {"entries": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching entries: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)