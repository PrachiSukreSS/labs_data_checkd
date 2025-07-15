import { dbOperations } from './supabase.js';

// DOM Elements
const navButtons = document.querySelectorAll('.nav-btn');
const pages = document.querySelectorAll('.page');

// Navigation
navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetPage = btn.dataset.page;
        
        // Update active nav button
        navButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Show target page
        pages.forEach(page => page.classList.remove('active'));
        document.getElementById(targetPage + 'Page').classList.add('active');
    });
});

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    await loadLocations();
    setupEventListeners();
});

// Load locations for dropdown
async function loadLocations() {
    try {
        const locations = await dbOperations.getLocations();
        const locationSelect = document.getElementById('locationSelect');
        
        locationSelect.innerHTML = '<option value="">Select Location</option>';
        locations.forEach(location => {
            const option = document.createElement('option');
            option.value = location;
            option.textContent = location;
            locationSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading locations:', error);
        showResult('availabilityResult', 'Error loading locations. Please check your connection.', 'error');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Availability check form
    document.getElementById('availabilityForm').addEventListener('submit', handleAvailabilityCheck);
    
    // Capacity search form
    document.getElementById('capacityForm').addEventListener('submit', handleCapacitySearch);
    
    // Faculty search form
    document.getElementById('facultyForm').addEventListener('submit', handleFacultySearch);
    
    // Day/Time filters
    document.getElementById('dayFilter').addEventListener('change', handleDayFilter);
    document.getElementById('timeFilter').addEventListener('change', handleTimeFilter);
    
    // Load timetable button
    document.getElementById('loadTimetable').addEventListener('click', loadFullTimetable);
    
    // Admin functionality
    setupAdminListeners();
}

// Handle availability check
async function handleAvailabilityCheck(e) {
    e.preventDefault();
    
    const location = document.getElementById('locationSelect').value;
    const day = document.getElementById('daySelect').value;
    const timeSlot = document.getElementById('timeSlotSelect').value;
    
    if (!location || !day || !timeSlot) {
        showResult('availabilityResult', 'Please fill all fields to check availability', 'error');
        return;
    }
    
    try {
        showLoading('availabilityResult');
        const result = await dbOperations.checkAvailability(location, day, timeSlot);
        
        if (result.length === 0) {
            showResult('availabilityResult', `No schedule information found for ${location} on ${day} during ${timeSlot}`, 'error');
        } else {
            const entry = result[0];
            if (entry.faculty === 'Free') {
                showResult('availabilityResult', 
                    `✅ ${location} is AVAILABLE on ${day} during ${timeSlot}<br>
                    <strong>Capacity:</strong> ${entry.capacity} students`, 'success');
            } else {
                const batchInfo = entry.batch ? ` (Batch: ${entry.batch})` : '';
                showResult('availabilityResult', 
                    `❌ ${location} is OCCUPIED on ${day} during ${timeSlot}<br>
                    <strong>Faculty:</strong> ${entry.faculty}${batchInfo}<br>
                    <strong>Capacity:</strong> ${entry.capacity} students`, 'error');
            }
        }
    } catch (error) {
        console.error('Error checking availability:', error);
        showResult('availabilityResult', 'Error checking availability. Please try again.', 'error');
    }
}

// Handle capacity search
async function handleCapacitySearch(e) {
    e.preventDefault();
    
    const capacity = parseInt(document.getElementById('capacityInput').value);
    
    if (!capacity || capacity < 1) {
        showResult('capacityResult', 'Please enter a valid capacity number', 'error');
        return;
    }
    
    try {
        showLoading('capacityResult');
        const locations = await dbOperations.findByCapacity(capacity);
        
        if (locations.length === 0) {
            showResult('capacityResult', `No locations found with capacity ≥ ${capacity} students`, 'error');
        } else {
            showResult('capacityResult', 
                `<strong>Locations with capacity ≥ ${capacity} students:</strong><br>
                ${locations.map(loc => `• ${loc}`).join('<br>')}`, 'success');
        }
    } catch (error) {
        console.error('Error searching by capacity:', error);
        showResult('capacityResult', 'Error searching by capacity. Please try again.', 'error');
    }
}

// Handle faculty search
async function handleFacultySearch(e) {
    e.preventDefault();
    
    const faculty = document.getElementById('facultyInput').value.trim();
    
    if (!faculty) {
        showResult('facultyResult', 'Please enter a faculty name', 'error');
        return;
    }
    
    try {
        showLoading('facultyResult');
        const results = await dbOperations.searchByFaculty(faculty);
        
        if (results.length === 0) {
            showResult('facultyResult', `No schedule found for faculty: ${faculty}`, 'error');
        } else {
            let resultText = `<strong>Schedule for ${faculty}:</strong><br><br>`;
            results.forEach(entry => {
                const batchInfo = entry.batch ? ` (${entry.batch})` : '';
                resultText += `📍 ${entry.location} - ${entry.day}, ${entry.time_slot}${batchInfo}<br>`;
            });
            showResult('facultyResult', resultText, 'success');
        }
    } catch (error) {
        console.error('Error searching by faculty:', error);
        showResult('facultyResult', 'Error searching by faculty. Please try again.', 'error');
    }
}

// Handle day filter
async function handleDayFilter(e) {
    const day = e.target.value;
    
    if (!day) {
        document.getElementById('filterResult').innerHTML = '';
        return;
    }
    
    try {
        showLoading('filterResult');
        const locations = await dbOperations.filterByDay(day);
        
        if (locations.length === 0) {
            showResult('filterResult', `No locations scheduled on ${day}`, 'error');
        } else {
            showResult('filterResult', 
                `<strong>Locations scheduled on ${day}:</strong><br>
                ${locations.map(loc => `• ${loc}`).join('<br>')}`, 'success');
        }
    } catch (error) {
        console.error('Error filtering by day:', error);
        showResult('filterResult', 'Error filtering by day. Please try again.', 'error');
    }
}

// Handle time filter
async function handleTimeFilter(e) {
    const timeSlot = e.target.value;
    
    if (!timeSlot) {
        document.getElementById('filterResult').innerHTML = '';
        return;
    }
    
    try {
        showLoading('filterResult');
        const locations = await dbOperations.filterByTime(timeSlot);
        
        if (locations.length === 0) {
            showResult('filterResult', `No locations scheduled during ${timeSlot}`, 'error');
        } else {
            showResult('filterResult', 
                `<strong>Locations scheduled during ${timeSlot}:</strong><br>
                ${locations.map(loc => `• ${loc}`).join('<br>')}`, 'success');
        }
    } catch (error) {
        console.error('Error filtering by time:', error);
        showResult('filterResult', 'Error filtering by time. Please try again.', 'error');
    }
}

// Load full timetable
async function loadFullTimetable() {
    try {
        const button = document.getElementById('loadTimetable');
        button.innerHTML = '<span class="loading"></span> Loading...';
        button.disabled = true;
        
        const data = await dbOperations.getAllData();
        displayTimetable(data);
        
        button.innerHTML = 'Load Full Timetable';
        button.disabled = false;
    } catch (error) {
        console.error('Error loading timetable:', error);
        document.getElementById('timetableContainer').innerHTML = '<p class="error">Error loading timetable. Please try again.</p>';
        
        const button = document.getElementById('loadTimetable');
        button.innerHTML = 'Load Full Timetable';
        button.disabled = false;
    }
}

// Display timetable
function displayTimetable(data) {
    const container = document.getElementById('timetableContainer');
    
    if (data.length === 0) {
        container.innerHTML = '<p>No schedule data available</p>';
        return;
    }
    
    let html = `
        <div class="table-responsive">
            <table class="timetable-table">
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>Day</th>
                        <th>Time Slot</th>
                        <th>Faculty</th>
                        <th>Batch</th>
                        <th>Capacity</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    data.forEach(entry => {
        const status = entry.faculty === 'Free' ? 'Available' : 'Occupied';
        const statusClass = entry.faculty === 'Free' ? 'status-free' : 'status-occupied';
        
        html += `
            <tr>
                <td><strong>${entry.location}</strong></td>
                <td>${entry.day}</td>
                <td>${entry.time_slot}</td>
                <td>${entry.faculty}</td>
                <td>${entry.batch || '-'}</td>
                <td>${entry.capacity}</td>
                <td class="${statusClass}">${status}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

// Utility functions
function showResult(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.innerHTML = message;
    element.className = `result ${type}`;
}

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = '<span class="loading"></span> Loading...';
    element.className = 'result info';
}

// Admin functionality
function setupAdminListeners() {
    document.getElementById('addEntryForm').addEventListener('submit', handleAddEntry);
    document.getElementById('loadDataBtn').addEventListener('click', loadAdminData);
}

// Handle add entry
async function handleAddEntry(e) {
    e.preventDefault();
    
    const entry = {
        location: document.getElementById('addLocation').value.trim(),
        day: document.getElementById('addDay').value,
        time_slot: document.getElementById('addTimeSlot').value,
        faculty: document.getElementById('addFaculty').value.trim(),
        batch: document.getElementById('addBatch').value.trim() || null,
        capacity: parseInt(document.getElementById('addCapacity').value)
    };
    
    // Validation
    if (!entry.location || !entry.day || !entry.time_slot || !entry.faculty || !entry.capacity) {
        alert('Please fill all required fields');
        return;
    }
    
    try {
        await dbOperations.addEntry(entry);
        alert('Schedule entry added successfully!');
        document.getElementById('addEntryForm').reset();
        await loadLocations(); // Refresh locations dropdown
        await loadAdminData(); // Refresh admin data table
    } catch (error) {
        console.error('Error adding entry:', error);
        alert('Error adding entry. Please try again.');
    }
}

// Load admin data
async function loadAdminData() {
    try {
        const button = document.getElementById('loadDataBtn');
        button.innerHTML = '<span class="loading"></span> Loading...';
        button.disabled = true;
        
        const data = await dbOperations.getAllData();
        displayAdminData(data);
        
        button.innerHTML = 'Load All Data';
        button.disabled = false;
    } catch (error) {
        console.error('Error loading admin data:', error);
        document.getElementById('dataTable').innerHTML = '<p class="error">Error loading data. Please try again.</p>';
        
        const button = document.getElementById('loadDataBtn');
        button.innerHTML = 'Load All Data';
        button.disabled = false;
    }
}

// Display admin data
function displayAdminData(data) {
    const container = document.getElementById('dataTable');
    
    if (data.length === 0) {
        container.innerHTML = '<p>No schedule data available</p>';
        return;
    }
    
    let html = `
        <div class="table-responsive">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>Day</th>
                        <th>Time Slot</th>
                        <th>Faculty</th>
                        <th>Batch</th>
                        <th>Capacity</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    data.forEach(entry => {
        html += `
            <tr>
                <td><strong>${entry.location}</strong></td>
                <td>${entry.day}</td>
                <td>${entry.time_slot}</td>
                <td>${entry.faculty}</td>
                <td>${entry.batch || '-'}</td>
                <td>${entry.capacity}</td>
                <td class="action-buttons">
                    <button class="edit-btn" onclick="editEntry('${entry.id}', '${entry.faculty}', '${entry.batch || ''}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="delete-btn" onclick="deleteEntry('${entry.id}', '${entry.location}', '${entry.day}', '${entry.time_slot}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

// Global functions for admin actions
window.editEntry = async function(id, currentFaculty, currentBatch) {
    const newFaculty = prompt('Enter new faculty name:', currentFaculty);
    if (newFaculty !== null && newFaculty.trim() !== '') {
        const newBatch = prompt('Enter batch (optional):', currentBatch);
        try {
            const updateData = { 
                faculty: newFaculty.trim(),
                batch: newBatch && newBatch.trim() ? newBatch.trim() : null
            };
            await dbOperations.updateEntry(id, updateData);
            alert('Entry updated successfully!');
            await loadAdminData();
            await loadLocations();
        } catch (error) {
            console.error('Error updating entry:', error);
            alert('Error updating entry. Please try again.');
        }
    }
};

window.deleteEntry = async function(id, location, day, timeSlot) {
    if (confirm(`Are you sure you want to delete this entry?\n\nLocation: ${location}\nDay: ${day}\nTime: ${timeSlot}`)) {
        try {
            await dbOperations.deleteEntry(id);
            alert('Entry deleted successfully!');
            await loadAdminData();
            await loadLocations();
        } catch (error) {
            console.error('Error deleting entry:', error);
            alert('Error deleting entry. Please try again.');
        }
    }
};