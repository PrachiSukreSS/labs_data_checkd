import { createClient } from '@supabase/supabase-js';

// Initialize Supabase client
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseKey);

// Database operations
export const dbOperations = {
    // Get all lab data
    async getAllData() {
        const { data, error } = await supabase
            .from('lab_schedule')
            .select('*')
            .order('location', { ascending: true });
        
        if (error) throw error;
        return data;
    },

    // Get unique locations
    async getLocations() {
        const { data, error } = await supabase
            .from('lab_schedule')
            .select('location')
            .order('location', { ascending: true });
        
        if (error) throw error;
        return [...new Set(data.map(item => item.location))];
    },

    // Check availability for specific location, day, and time
    async checkAvailability(location, day, timeSlot) {
        const { data, error } = await supabase
            .from('lab_schedule')
            .select('*')
            .eq('location', location)
            .eq('day', day)
            .eq('time_slot', timeSlot);
        
        if (error) throw error;
        return data;
    },

    // Find locations by capacity
    async findByCapacity(minCapacity) {
        const { data, error } = await supabase
            .from('lab_schedule')
            .select('location, capacity')
            .gte('capacity', minCapacity)
            .order('location', { ascending: true });
        
        if (error) throw error;
        return [...new Set(data.map(item => item.location))];
    },

    // Search by faculty
    async searchByFaculty(facultyName) {
        const { data, error } = await supabase
            .from('lab_schedule')
            .select('*')
            .eq('faculty', facultyName)
            .order('day', { ascending: true });
        
        if (error) throw error;
        return data;
    },

    // Filter by day
    async filterByDay(day) {
        const { data, error } = await supabase
            .from('lab_schedule')
            .select('location')
            .eq('day', day)
            .order('location', { ascending: true });
        
        if (error) throw error;
        return [...new Set(data.map(item => item.location))];
    },

    // Filter by time slot
    async filterByTime(timeSlot) {
        const { data, error } = await supabase
            .from('lab_schedule')
            .select('location')
            .eq('time_slot', timeSlot)
            .order('location', { ascending: true });
        
        if (error) throw error;
        return [...new Set(data.map(item => item.location))];
    },

    // Admin operations
    async addEntry(entry) {
        const { data, error } = await supabase
            .from('lab_schedule')
            .insert([entry])
            .select();
        
        if (error) throw error;
        return data;
    },

    async updateEntry(id, updates) {
        const { data, error } = await supabase
            .from('lab_schedule')
            .update(updates)
            .eq('id', id)
            .select();
        
        if (error) throw error;
        return data;
    },

    async deleteEntry(id) {
        const { error } = await supabase
            .from('lab_schedule')
            .delete()
            .eq('id', id);
        
        if (error) throw error;
        return true;
    }
};