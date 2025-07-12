document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const rideSections = document.querySelectorAll('.rides-section');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding section
            rideSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === tabId) {
                    section.classList.add('active');
                }
            });
        });
    });
    
    // Filter functionality for past rides
    const pastRidesFilter = document.getElementById('pastRidesFilter');
    const pastRides = document.querySelectorAll('#past .ride-card');
    
    pastRidesFilter.addEventListener('change', function() {
        const filterValue = this.value;
        
        pastRides.forEach(ride => {
            const rideType = ride.classList.contains('driver') ? 'driver' : 'passenger';
            
            if (filterValue === 'all' || filterValue === rideType) {
                ride.style.display = 'block';
            } else {
                ride.style.display = 'none';
            }
        });
    });
    
    // Filter functionality for bookings
    const bookingsFilter = document.getElementById('bookingsFilter');
    const bookings = document.querySelectorAll('.booking-card');
    
    bookingsFilter.addEventListener('change', function() {
        const filterValue = this.value;
        
        bookings.forEach(booking => {
            const bookingStatus = booking.classList.contains(filterValue) ? filterValue : '';
            
            if (filterValue === 'all' || bookingStatus) {
                booking.style.display = 'flex';
                booking.style.flexDirection = 'column';
            } else {
                booking.style.display = 'none';
            }
        });
    });
    
    // Cancel ride functionality
    const cancelButtons = document.querySelectorAll('.ride-actions .btn-outline, .booking-actions .btn-outline');
    
    cancelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const card = this.closest('.ride-card, .booking-card');
            const isBooking = card.classList.contains('booking-card');
            const rideType = card.classList.contains('driver') ? 'drive' : 'ride';
            
            if (confirm(`Are you sure you want to cancel this ${isBooking ? 'booking' : rideType}?`)) {
                // In a real app, this would make an API call
                console.log(`Cancelling ${isBooking ? 'booking' : rideType}`);
                
                // Simulate removal from UI
                card.style.opacity = '0.5';
                card.style.pointerEvents = 'none';
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cancelling...';
                
                setTimeout(() => {
                    // In a real app, we'd update the status rather than remove
                    if (isBooking) {
                        card.querySelector('.status-badge').textContent = 'Cancelled';
                        card.querySelector('.status-badge').className = 'status-badge cancelled';
                        this.textContent = 'Cancelled';
                        this.disabled = true;
                    } else {
                        card.remove();
                    }
                }, 1500);
            }
        });
    });
    
    // User menu dropdown
    const userMenu = document.querySelector('.user-menu');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    
    userMenu.addEventListener('click', function() {
        dropdownMenu.classList.toggle('show');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!userMenu.contains(e.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});