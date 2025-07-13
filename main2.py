from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd # type: ignore
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Global variable to hold the data
data = None

def load_data():
    global data
    # File path from environment variable
    FILE_PATH = os.getenv('FILE_PATH', r'C:/Users/prach/Desktop/Automation Project/Newlabdata/Newlabdata.xlsx')
    try:
        data = pd.read_excel(FILE_PATH)
        if data.empty:
            raise ValueError("Data file is empty.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading the file: {str(e)}")

# Load the data when the application starts
@app.on_event("startup")
def startup_event():
    load_data()

# Define request models
class LocationRequest(BaseModel):
    location_name: str
    day: str
    time_slot: str

class CapacityRequest(BaseModel):
    capacity: int

class FacultyRequest(BaseModel):
    faculty_name: str

@app.get("/")
def greet():
    return {"message": "Hello! Welcome to the Lab/Classroom Availability System!"}

@app.get("/locations/")
def list_locations():
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded.")
    location_names = data['location'].unique()
    return {"locations": list(location_names)}

@app.post("/availability/")
def check_availability(request: LocationRequest):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded.")
    location_info = data[(data['location'] == request.location_name) &
                         (data['day'] == request.day) &
                         (data['time_slot'] == request.time_slot)]
    
    if not location_info.empty:
        for index, row in location_info.iterrows():
            if row['faculty'] == 'Free':
                return {"message": f"{request.location_name} is available at {request.time_slot} on {request.day}."}
            else:
                return {"message": f"{request.location_name} is occupied by Batch: {row['batch']} at {request.time_slot} on {request.day}."}
    else:
        raise HTTPException(status_code=404, detail=f"No information available for '{request.location_name}' at {request.time_slot} on {request.day}.")

@app.post("/locations/capacity/")
def find_location_by_capacity(request: CapacityRequest):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded.")
    available_locations = data[data['capacity'] >= request.capacity]
    if available_locations.empty:
        return {"message": "No locations found with the required capacity."}
    else:
        locations = available_locations['location'].unique()
        return {"locations": list(locations)}

@app.get("/timetable/")
def display_full_timetable():
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded.")
    return data.to_dict(orient='records')

@app.get("/locations/day/")
def check_available_locations_by_day(day: str):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded.")
    available_locations = data[data['day'] == day]
    if available_locations.empty:
        return {"message": f"No locations available on {day}."}
    else:
        locations = available_locations['location'].unique()
        return {"locations": list(locations)}

@app.get("/locations/time/")
def check_available_locations_by_time(time_slot: str):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded.")
    available_locations = data[data['time_slot'] == time_slot]
    if available_locations.empty:
        return {"message": f"No locations available during {time_slot}."}
    else:
        locations = available_locations['location'].unique()
        return {"locations": list(locations)}

@app.post("/locations/faculty/")
def search_by_faculty(request: FacultyRequest):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded.")
    locations_by_faculty = data[data['faculty'] == request.faculty_name]
    if locations_by_faculty.empty:
        return {"message": f"No locations found for Faculty: {request.faculty_name}."}
    else:
        return locations_by_faculty.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)