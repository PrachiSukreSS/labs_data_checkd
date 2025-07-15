from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from typing import List, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="Lab Availability API", version="3.0.0")

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
    time_slot: str  # Now accepts "Slot 1", "Slot 2", "Slot 3"
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
    return {
        "message": "Welcome to the Lab/Classroom Availability System v3.0!",
        "features": [
            "Check lab availability by location, day, and time slot",
            "Search by capacity requirements",
            "Find faculty schedules",
            "Filter by day or time slot",
            "Admin data management"
        ],
        "time_slots": ["Slot 1", "Slot 2", "Slot 3"],
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    }

@app.get("/locations/")
def list_locations():
    """Get all unique locations from the database"""
    try:
        response = supabase.table('lab_schedule').select('location').execute()
        locations = list(set([item['location'] for item in response.data]))
        return {"locations": sorted(locations)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations: {str(e)}")

@app.post("/availability/")
def check_availability(request: LocationRequest):
    """Check if a specific location is available at given day and time slot"""
    try:
        response = supabase.table('lab_schedule').select('*').eq('location', request.location_name).eq('day', request.day).eq('time_slot', request.time_slot).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"No schedule information found for '{request.location_name}' on {request.day} during {request.time_slot}")
        
        entry = response.data[0]
        if entry['faculty'] == 'Free':
            return {
                "available": True,
                "message": f"{request.location_name} is available on {request.day} during {request.time_slot}",
                "capacity": entry['capacity']
            }
        else:
            batch_info = f" (Batch: {entry['batch']})" if entry['batch'] else ""
            return {
                "available": False,
                "message": f"{request.location_name} is occupied by {entry['faculty']}{batch_info} on {request.day} during {request.time_slot}",
                "faculty": entry['faculty'],
                "batch": entry['batch'],
                "capacity": entry['capacity']
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking availability: {str(e)}")

@app.post("/locations/capacity/")
def find_location_by_capacity(request: CapacityRequest):
    """Find all locations with capacity greater than or equal to specified value"""
    try:
        response = supabase.table('lab_schedule').select('location, capacity').gte('capacity', request.capacity).execute()
        
        if not response.data:
            return {"message": "No locations found with the required capacity.", "locations": []}
        
        locations = list(set([item['location'] for item in response.data]))
        return {
            "locations": sorted(locations),
            "count": len(locations),
            "message": f"Found {len(locations)} location(s) with capacity ≥ {request.capacity}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding locations by capacity: {str(e)}")

@app.get("/timetable/")
def display_full_timetable():
    """Get complete timetable for all locations"""
    try:
        response = supabase.table('lab_schedule').select('*').order('location').order('day').order('time_slot').execute()
        return {
            "timetable": response.data,
            "total_entries": len(response.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching timetable: {str(e)}")

@app.get("/locations/day/")
def check_available_locations_by_day(day: str):
    """Get all locations that have schedules on a specific day"""
    try:
        response = supabase.table('lab_schedule').select('location').eq('day', day).execute()
        
        if not response.data:
            return {"message": f"No locations scheduled on {day}.", "locations": []}
        
        locations = list(set([item['location'] for item in response.data]))
        return {
            "locations": sorted(locations),
            "day": day,
            "count": len(locations)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations by day: {str(e)}")

@app.get("/locations/time/")
def check_available_locations_by_time(time_slot: str):
    """Get all locations that have schedules during a specific time slot"""
    try:
        response = supabase.table('lab_schedule').select('location').eq('time_slot', time_slot).execute()
        
        if not response.data:
            return {"message": f"No locations scheduled during {time_slot}.", "locations": []}
        
        locations = list(set([item['location'] for item in response.data]))
        return {
            "locations": sorted(locations),
            "time_slot": time_slot,
            "count": len(locations)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations by time: {str(e)}")

@app.post("/locations/faculty/")
def search_by_faculty(request: FacultyRequest):
    """Search for all schedules assigned to a specific faculty"""
    try:
        response = supabase.table('lab_schedule').select('*').eq('faculty', request.faculty_name).order('day').order('time_slot').execute()
        
        if not response.data:
            return {
                "message": f"No schedule found for faculty: {request.faculty_name}",
                "schedule": []
            }
        
        return {
            "faculty": request.faculty_name,
            "schedule": response.data,
            "total_classes": len(response.data)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching by faculty: {str(e)}")

# Admin endpoints for data management
@app.post("/admin/entries/")
def create_entry(entry: LabEntry):
    """Create a new lab schedule entry"""
    try:
        # Validate time slot format
        valid_slots = ["Slot 1", "Slot 2", "Slot 3"]
        if entry.time_slot not in valid_slots:
            raise HTTPException(status_code=400, detail=f"Invalid time slot. Must be one of: {valid_slots}")
        
        # Check if entry already exists
        existing = supabase.table('lab_schedule').select('*').eq('location', entry.location).eq('day', entry.day).eq('time_slot', entry.time_slot).execute()
        
        if existing.data:
            raise HTTPException(status_code=400, detail=f"Schedule entry already exists for {entry.location} on {entry.day} during {entry.time_slot}")
        
        response = supabase.table('lab_schedule').insert(entry.dict()).execute()
        return {
            "message": "Schedule entry created successfully",
            "data": response.data[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating entry: {str(e)}")

@app.put("/admin/entries/{entry_id}")
def update_entry(entry_id: str, entry: UpdateLabEntry):
    """Update an existing lab schedule entry"""
    try:
        # Remove None values from the update data
        update_data = {k: v for k, v in entry.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        # Validate time slot if provided
        if 'time_slot' in update_data:
            valid_slots = ["Slot 1", "Slot 2", "Slot 3"]
            if update_data['time_slot'] not in valid_slots:
                raise HTTPException(status_code=400, detail=f"Invalid time slot. Must be one of: {valid_slots}")
        
        response = supabase.table('lab_schedule').update(update_data).eq('id', entry_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Schedule entry not found")
        
        return {
            "message": "Schedule entry updated successfully",
            "data": response.data[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating entry: {str(e)}")

@app.delete("/admin/entries/{entry_id}")
def delete_entry(entry_id: str):
    """Delete a lab schedule entry"""
    try:
        response = supabase.table('lab_schedule').delete().eq('id', entry_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Schedule entry not found")
        
        return {"message": "Schedule entry deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting entry: {str(e)}")

@app.get("/admin/entries/")
def get_all_entries():
    """Get all lab schedule entries for admin management"""
    try:
        response = supabase.table('lab_schedule').select('*').order('location').order('day').order('time_slot').execute()
        return {
            "entries": response.data,
            "total_count": len(response.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching entries: {str(e)}")

@app.get("/stats/")
def get_statistics():
    """Get system statistics"""
    try:
        all_data = supabase.table('lab_schedule').select('*').execute().data
        
        total_entries = len(all_data)
        total_locations = len(set([item['location'] for item in all_data]))
        free_slots = len([item for item in all_data if item['faculty'] == 'Free'])
        occupied_slots = total_entries - free_slots
        
        return {
            "total_entries": total_entries,
            "total_locations": total_locations,
            "free_slots": free_slots,
            "occupied_slots": occupied_slots,
            "utilization_rate": round((occupied_slots / total_entries) * 100, 2) if total_entries > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)