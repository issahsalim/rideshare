document.addEventListener('DOMContentLoaded', function() {
    // Initialize map (Leaflet.js)
    let map;
    const mapPreview = document.getElementById('mapPreview');
    
    function initMap() {
        // Default to Accra coordinates
        map = L.map('mapPreview').setView([5.6037, -0.1870], 12);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        // Add marker for Accra
        L.marker([5.6037, -0.1870]).addTo(map)
            .bindPopup('Accra, Ghana')
            .openPopup();
    }
    
    // Initialize map if container exists
    if (mapPreview) {
        initMap();
    }
    
    // File upload display
    const fileInput = document.getElementById('carPhoto');
    const fileNameDisplay = document.querySelector('.file-name');
    
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            fileNameDisplay.textContent = this.files[0].name;
        } else {
            fileNameDisplay.textContent = 'No file chosen';
        }
    });
    
    // Form validation
    const rideForm = document.getElementById('rideForm');
    
    rideForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const departure = document.getElementById('departure').value;
        const destination = document.getElementById('destination').value;
        const departureDate = document.getElementById('departureDate').value;
        const departureTime = document.getElementById('departureTime').value;
        const seats = document.getElementById('seats').value;
        const price = document.getElementById('price').value;
        const carMake = document.getElementById('carMake').value;
        const carModel = document.getElementById('carModel').value;
        const licensePlate = document.getElementById('licensePlate').value;
        
        // Validate required fields
        if (!departure || !destination || !departureDate || !departureTime || !seats || !price || !carMake || !carModel || !licensePlate) {
            alert('Please fill in all required fields');
            return;
        }
        
        // Validate price
        if (price < 20) {
            alert('Price per seat must be at least GH₵20');
            return;
        }
        
        // Show loading state
        const submitBtn = rideForm.querySelector('.submit-btn');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Publishing...';
        submitBtn.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
            console.log('Ride offer submitted:', {
                departure,
                destination,
                departureDate,
                departureTime,
                seats,
                price,
                carMake,
                carModel,
                licensePlate
            });
            
            // Reset button state
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            
            // Show success message (in real app, redirect to ride management page)
            alert('Your ride has been published successfully!');
            // window.location.href = 'my-rides.html';
        }, 2000);
    });
    
    // Preview button
    const previewBtn = document.querySelector('.preview-btn');
    
    previewBtn.addEventListener('click', function() {
        // In a real app, this would show a preview modal
        alert('In a complete implementation, this would show a preview of your ride listing');
    });
    
    // Set min date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('departureDate').setAttribute('min', today);
    
    // Set default time to next hour
    const now = new Date();
    const nextHour = new Date(now.getTime() + 60 * 60 * 1000);
    const hours = nextHour.getHours().toString().padStart(2, '0');
    const minutes = nextHour.getMinutes().toString().padStart(2, '0');
    document.getElementById('departureTime').value = `${hours}:${minutes}`;
});