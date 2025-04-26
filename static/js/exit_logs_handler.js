// Exit Logs Handler
// This script handles the persistence and real-time updates of exit logs

/**
 * Exit Logs Handler
 * 
 * This module provides functions for managing exit logs in both the exit display
 * and admin dashboard. It handles:
 * - Caching exit logs to localStorage
 * - Loading cached exit logs
 * - Socket.IO connection and event handling
 * - Displaying exit logs in the UI
 */

// Configuration
const EXIT_DISPLAY_CACHE_KEY = 'recentExits';
const ADMIN_CACHE_KEY = 'adminRecentExits';
const MAX_DISPLAY_EXITS = 20;
const MAX_ADMIN_EXITS = 50;

// Socket.IO connection instance
let socket;

/**
 * Initialize the exit logs handler
 * @param {string} mode - Either 'display' or 'admin'
 */
function initExitLogsHandler(mode) {
    console.log(`Initializing exit logs handler in ${mode} mode`);
    
    // Load cached exits immediately for a better user experience
    loadCachedExits(mode);
    
    // Set up Socket.IO connection
    setupSocketConnection(mode);
    
    // Load recent exits from server
    loadRecentExits(mode);
    
    // Set up periodic refresh as fallback
    const refreshInterval = mode === 'admin' ? 60000 : 30000; // 1 minute for admin, 30 seconds for display
    setInterval(() => loadRecentExits(mode), refreshInterval);
}

/**
 * Set up Socket.IO connection and event handlers
 * @param {string} mode - Either 'display' or 'admin'
 */
function setupSocketConnection(mode) {
    try {
        console.log(`Setting up Socket.IO connection for ${mode}`);
        
        // Create socket connection with robust settings
        socket = io({
            reconnectionDelayMax: 10000,
            reconnectionAttempts: 10,
            timeout: 20000,
            transports: ['websocket', 'polling']
        });
        
        // Connection events
        socket.on('connect', function() {
            console.log(`Socket.IO connected successfully in ${mode} mode`);
            socket.emit('test_connection');
        });
        
        socket.on('disconnect', function() {
            console.log('Socket.IO disconnected - will try to reconnect');
        });
        
        socket.on('reconnect', function(attemptNumber) {
            console.log(`Socket.IO reconnected after ${attemptNumber} attempts`);
            loadRecentExits(mode); // Refresh data on reconnection
        });
        
        socket.on('connect_error', function(error) {
            console.error('Socket.IO connection error:', error);
            setTimeout(function() {
                socket.connect();
            }, 5000);
        });
        
        // Initial exits event
        socket.on('initial_exits', function(exits) {
            console.log(`Received ${exits.length} initial exits via Socket.IO`);
            if (exits && exits.length > 0) {
                // Cache the exits
                cacheExits(exits, mode);
                
                // Display the exits
                if (mode === 'display') {
                    displayExitLogs(exits, true);
                } else {
                    // For admin dashboard, update the table
                    updateAdminExitTable(exits);
                }
            }
        });
        
        // New exit event
        socket.on('new_exit_log', function(exitData) {
            console.log(`New exit received via Socket.IO in ${mode} mode:`, exitData);
            
            if (exitData) {
                // Cache the new exit
                cacheExits(exitData, mode);
                
                // Display the new exit
                if (mode === 'display') {
                    addNewExitToDisplay(exitData);
                } else {
                    // For admin dashboard
                    addNewExitRow(exitData);
                }
                
                // Play notification sound if available
                if (typeof playNotificationSound === 'function') {
                    playNotificationSound();
                }
            }
        });
        
        // Error handling
        socket.on('error', function(error) {
            console.error('Socket.IO error:', error);
        });
        
        return true;
    } catch (error) {
        console.error('Error setting up Socket.IO:', error);
        return false;
    }
}

/**
 * Load cached exits from localStorage
 * @param {string} mode - Either 'display' or 'admin'
 */
function loadCachedExits(mode) {
    try {
        const cacheKey = mode === 'display' ? EXIT_DISPLAY_CACHE_KEY : ADMIN_CACHE_KEY;
        console.log(`Loading cached exits from localStorage using key: ${cacheKey}`);
        
        const cachedExits = JSON.parse(localStorage.getItem(cacheKey) || '[]');
        
        if (cachedExits && cachedExits.length > 0) {
            console.log(`Found ${cachedExits.length} cached exits in localStorage`);
            
            if (mode === 'display') {
                displayExitLogs(cachedExits, false); // Don't clear existing data
            } else {
                // For admin dashboard, format timestamps before displaying
                cachedExits.forEach(exit => {
                    if (exit.exit_time && typeof formatTimestamp === 'function') {
                        exit.formatted_time = formatTimestamp(exit.exit_time);
                    }
                });
                
                // Update the admin dashboard
                updateAdminExitTable(cachedExits);
            }
            
            return true;
        } else {
            console.log("No cached exits found in localStorage");
            return false;
        }
    } catch (error) {
        console.error("Error loading cached exits:", error);
        return false;
    }
}

/**
 * Cache exits to localStorage
 * @param {Object|Array} exits - Exit log(s) to cache
 * @param {string} mode - Either 'display' or 'admin'
 */
function cacheExits(exits, mode) {
    try {
        // If single exit, convert to array
        const exitsArray = Array.isArray(exits) ? exits : [exits];
        
        // Get the appropriate cache key and max items
        const cacheKey = mode === 'display' ? EXIT_DISPLAY_CACHE_KEY : ADMIN_CACHE_KEY;
        const maxItems = mode === 'display' ? MAX_DISPLAY_EXITS : MAX_ADMIN_EXITS;
        
        // Get existing exits from localStorage
        const existingExits = JSON.parse(localStorage.getItem(cacheKey) || '[]');
        
        // Check for duplicates and add new exits
        const updatedExits = [...existingExits];
        let newExitsAdded = 0;
        
        exitsArray.forEach(newExit => {
            // Check if this exit is already cached
            const isDuplicate = existingExits.some(existingExit => {
                // Check by log_id if available
                if (newExit.log_id && existingExit.log_id) {
                    return newExit.log_id === existingExit.log_id;
                }
                
                // Otherwise check by student name and timestamp
                const nameMatch = (
                    (newExit.student_name && existingExit.student_name && 
                     newExit.student_name === existingExit.student_name) ||
                    (newExit.id_number && existingExit.id_number && 
                     newExit.id_number === existingExit.id_number)
                );
                
                const timeMatch = (
                    (newExit.exit_time && existingExit.exit_time && 
                     newExit.exit_time === existingExit.exit_time) ||
                    (newExit.timestamp && existingExit.timestamp && 
                     newExit.timestamp === existingExit.timestamp)
                );
                
                return nameMatch && timeMatch;
            });
            
            if (!isDuplicate) {
                // Add to the beginning of the array
                updatedExits.unshift(newExit);
                newExitsAdded++;
            }
        });
        
        // Keep only the most recent exits up to maxItems
        const limitedExits = updatedExits.slice(0, maxItems);
        
        // Save back to localStorage
        localStorage.setItem(cacheKey, JSON.stringify(limitedExits));
        
        console.log(`Cached ${newExitsAdded} new exits to localStorage. Total cached: ${limitedExits.length}`);
        return true;
    } catch (error) {
        console.error("Error caching exits:", error);
        return false;
    }
}

/**
 * Load recent exits from the server
 * @param {string} mode - Either 'display' or 'admin'
 */
function loadRecentExits(mode) {
    console.log(`Loading recent exits from server in ${mode} mode`);
    
    // Force bypass cache with timestamp + random
    const params = `nocache=${Date.now()}-${Math.random()}`;
    const endpoint = mode === 'display' ? '/api/recent-exits' : '/api/recent-exits';
    
    // Request with no-cache headers
    fetch(`${endpoint}?${params}`, {
        headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(`Received ${data.length} exit logs from server`);
        
        if (data && data.length > 0) {
            // Cache the exits
            cacheExits(data, mode);
            
            // Display the exits
            if (mode === 'display') {
                displayExitLogs(data, true);
            } else {
                // For admin dashboard
                updateAdminExitTable(data);
            }
        }
    })
    .catch(error => {
        console.error('Error loading exits:', error);
    });
}

// Export functions for global use
window.exitLogsHandler = {
    init: initExitLogsHandler,
    loadCachedExits: loadCachedExits,
    cacheExits: cacheExits,
    loadRecentExits: loadRecentExits
};