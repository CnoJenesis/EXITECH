// Global variables
let displayTimeout;
let socket;
let socketConnected = false;

// Make processRfid globally available immediately - CRITICAL
// Process RFID input - Define this first to ensure it's available globally
function processRfid(rfid) {
    console.log("\n=== Processing RFID ===");
    console.log("RFID value:", rfid);

    // Validate RFID format
    if (!rfid || rfid.length < 8) {
        console.error("❌ Invalid RFID format:", rfid);
        return;
    }

    // Send request to server
    console.log("📤 Sending request to server...");
    fetch('/api/process-exit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rfid_uid: rfid.trim() })
    })
    .then(response => {
        console.log("📥 Server response status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("Server response data:", data);
        
        if (data.status === 'success' && data.student) {
            console.log("\n✅ Success! Student info received:");
            console.log("  Name:", formatName(data.student.first_name, data.student.middle_initial, data.student.last_name));
            console.log("  ID:", data.student.id_number);
            console.log("  Section:", `${data.student.strand_code || ''} ${data.student.grade_level || ''} - ${data.student.section || 'Unknown Section'}`);
            console.log("  Status:", data.student.exit_status);
            console.log("  Reason:", data.student.reason || 'No reason provided');
            
            // Only call displayStudentInfo when we're sure jQuery is ready
            if (typeof $ === 'function') {
                displayStudentInfo(data.student);
            } else {
                // If jQuery isn't available yet, wait for document ready
                document.addEventListener('DOMContentLoaded', () => {
                    displayStudentInfo(data.student);
                });
            }
        } else {
            console.error("❌ Error:", data.message || 'Unknown error occurred');
            if (typeof $ === 'function') {
                handleAccessDenied(data.message);
            } else {
                document.addEventListener('DOMContentLoaded', () => {
                    handleAccessDenied(data.message);
                });
            }
        }
    })
    .catch(error => {
        console.error("❌ Network error:", error);
        if (typeof $ === 'function') {
            displayError("Network error occurred");
        } else {
            document.addEventListener('DOMContentLoaded', () => {
                displayError("Network error occurred");
            });
        }
    });
}

// IMMEDIATELY expose to global scope
window.processRfid = processRfid;
console.log("processRfid function is now available globally");

// Format date for display
function formatDateTime(timestamp) {
    if (!timestamp) return new Date().toLocaleString('en-US');
    
    try {
        // Handle different timestamp formats
        if (typeof timestamp === 'string') {
            // Try to parse the timestamp string
            const date = new Date(timestamp);
            if (!isNaN(date.getTime())) {
                return date.toLocaleString('en-US', {
                    hour: 'numeric',
                    minute: 'numeric',
                    hour12: true,
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
            }
            return timestamp; // Return original if parsing fails
        }
        
        if (timestamp instanceof Date) {
            return timestamp.toLocaleString('en-US', {
                hour: 'numeric',
                minute: 'numeric',
                hour12: true,
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
        }
        
        return new Date().toLocaleString('en-US');
    } catch (error) {
        console.error('Date formatting error:', error);
        return new Date().toLocaleString('en-US');
    }
}

// Format student name
function formatName(firstName, middleInitial, lastName) {
    let name = firstName || '';
    if (middleInitial) {
        name += ` ${middleInitial}.`;
    }
    if (lastName) {
        name += ` ${lastName}`;
    }
    return name.trim();
}

// Format profile picture URL
function formatProfilePicture(profilePicture) {
    if (!profilePicture) {
        return '/static/img/default-profile.png';
    }
    return profilePicture;
}

// Display student information
function displayStudentInfo(studentData) {
    console.log('\n=== Displaying Student Info ===');
    
    // Make sure jQuery is available
    if (typeof $ !== 'function') {
        console.error("jQuery not available for displayStudentInfo");
        return;
    }
    
    try {
        // Show the ID card and hide the scan prompt
        $('#scan-prompt').hide();
        $('.id-card').show();
        
        console.log('Updating display elements...');
        
        // Update student photo
        const photoUrl = formatProfilePicture(studentData.profile_picture);
        console.log('Photo URL:', photoUrl);
        $('#student-photo').attr('src', photoUrl);
        
        // Update student information
        const formattedName = formatName(studentData.first_name, studentData.middle_initial, studentData.last_name);
        console.log('Formatted Name:', formattedName);
        $('.student-name').text(formattedName);
        
        const idNumber = studentData.id_number || 'Unknown';
        console.log('ID Number:', idNumber);
        $('.student-id').text(idNumber);
        
        const section = `${studentData.strand_code || ''} ${studentData.grade_level || ''} - ${studentData.section || 'Unknown Section'}`.trim();
        console.log('Section:', section);
        $('.student-section').text(section);
        
        const exitTime = formatDateTime(new Date());
        console.log('Exit Time:', exitTime);
        $('.exit-time').text(exitTime);
        
        // Update status and reason
        const status = studentData.exit_status || 'UNKNOWN';
        const reason = studentData.reason || '';
        console.log('Status:', status);
        console.log('Reason:', reason);
        
        $('.exit-status-container').removeClass('allowed denied');
        $('.exit-status').hide();
        
        if (status.toUpperCase() === 'ALLOWED') {
            console.log('✅ Exit Allowed');
            $('.exit-status-container').addClass('allowed');
            $('.exit-status.allowed').show();
            $('.status-text').text('ALLOWED');
            $('.status-reason').text(reason || 'No active classes');
        } else {
            console.log('❌ Exit Denied');
            $('.exit-status-container').addClass('denied');
            $('.exit-status.denied').show();
            $('.status-text').text('DENIED');
            $('.status-reason').text(reason || 'Access denied');
        }
        
        // Reset display after 5 seconds
        if (displayTimeout) {
            clearTimeout(displayTimeout);
        }
        console.log('Setting display timeout: 5 seconds');
        displayTimeout = setTimeout(resetDisplay, 5000);
    } catch (error) {
        console.error('Error displaying student info:', error);
    }
}

// Reset display to initial state
function resetDisplay() {
    if (typeof $ === 'function') {
        $('.id-card').hide();
        $('#scan-prompt').show();
        $('.status-reason').text('');
    }
}

// Show loading state
function showLoadingState() {
    if (typeof $ === 'function') {
        $('#scan-prompt').hide();
        $('.id-card').show();
        $('.student-id').text('Loading...');
        $('.student-name').text('Please wait...');
        $('.student-section').text('');
        $('.exit-time').text('');
        $('.exit-status-container').removeClass('allowed denied');
        $('.exit-status').hide();
        $('.status-reason').text('Processing your request...');
    }
}

// Handle RFID response
function handleRfidResponse(response) {
    if (response.status === 'success' && response.student) {
        displayStudentInfo(response.student);
    } else {
        handleAccessDenied(response.message);
    }
}

// Handle RFID error
function handleRfidError(error) {
    console.error('Error processing RFID:', error);
    displayError('Error processing your request. Please try again.');
}

// Handle access denied
function handleAccessDenied(message) {
    if (typeof $ !== 'function') {
        console.error("jQuery not available for handleAccessDenied");
        return;
    }
    
    displayStudentInfo({
        first_name: 'Access',
        last_name: 'Denied',
        id_number: 'N/A',
        grade_level: '',
        section: '',
        exit_status: 'DENIED',
        reason: message || 'Access denied'
    });
}

// Display error message
function displayError(message) {
    console.error(message);
    if (typeof $ === 'function') {
        $('.status-reason').text(message);
    }
}

// Ensure these are available globally immediately
window.formatName = formatName;
window.formatDateTime = formatDateTime;
window.formatProfilePicture = formatProfilePicture;

// Add a document ready handler for additional setup
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setupDisplayFunctions();
} else {
    document.addEventListener('DOMContentLoaded', setupDisplayFunctions);
}

// Setup function to initialize the display
function setupDisplayFunctions() {
    console.log("Exit display functions are ready");
    // Verify jQuery is available
    if (typeof $ === 'function') {
        resetDisplay();
    } else {
        console.error("jQuery not available on document ready!");
    }
}