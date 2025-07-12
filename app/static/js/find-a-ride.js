document.addEventListener('DOMContentLoaded', function() {
    // Toggle filters panel
    const filterToggle = document.querySelector('.filter-toggle');
    const filtersPanel = document.querySelector('.filters-panel');
    const filtersOverlay = document.querySelector('.filters-overlay');
    const closeFilters = document.querySelector('.close-filters');
    
    filterToggle.addEventListener('click', function() {
        filtersPanel.classList.add('active');
        filtersOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
    
    closeFilters.addEventListener('click', function() {
        filtersPanel.classList.remove('active');
        filtersOverlay.classList.remove('active');
        document.body.style.overflow = '';
    });
    
    filtersOverlay.addEventListener('click', function() {
        filtersPanel.classList.remove('active');
        this.classList.remove('active');
        document.body.style.overflow = '';
    });
    
    // Price range slider
    const priceRange = document.getElementById('price-range');
    const selectedPrice = document.getElementById('selected-price');
    
    priceRange.addEventListener('input', function() {
        selectedPrice.textContent = this.value;
    });
    
    // View toggle
    const viewToggleButtons = document.querySelectorAll('.map-view-toggle .btn');
    
    viewToggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            viewToggleButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Here you would toggle between list and map view
            // For now we'll just log it
            if (this.querySelector('.fa-list')) {
                console.log('Switched to list view');
            } else {
                console.log('Switched to map view');
            }
        });
    });
    
    // Ride card hover effect
    const rideCards = document.querySelectorAll('.ride-card');
    
    rideCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
    
    // Book now buttons
    const bookButtons = document.querySelectorAll('.ride-actions .btn-primary');
    
    bookButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // In a real app, this would redirect to booking page
            const rideCard = this.closest('.ride-card');
            const driverName = rideCard.querySelector('.driver-info h3').textContent;
            const price = rideCard.querySelector('.ride-price .price').textContent;
            
            console.log(`Booking ride with ${driverName} for ${price}`);
            alert(`You're about to book a ride with ${driverName} for ${price}. In a real app, this would take you to the booking page.`);
        });
    });
    
    // Quick search route tags
    const routeTags = document.querySelectorAll('.route-tag');
    
    routeTags.forEach(tag => {
        tag.addEventListener('click', function(e) {
            e.preventDefault();
            const route = this.textContent.split('→').map(item => item.trim());
            document.getElementById('from').value = route[0];
            document.getElementById('to').value = route[1];
            
            // Trigger search (in a real app)
            console.log(`Searching for rides from ${route[0]} to ${route[1]}`);
        });
    });
    
    // Sort options
    const sortSelect = document.getElementById('sort-by');
    
    sortSelect.addEventListener('change', function() {
        console.log(`Sorting by: ${this.value}`);
        // In a real app, this would re-sort the results
    });
    
    // Set min date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').setAttribute('min', today);
});