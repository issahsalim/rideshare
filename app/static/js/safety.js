document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality for safety tips
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabId) {
                    content.classList.add('active');
                }
            });
        });
    });
    
    // FAQ accordion functionality
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const faqCard = this.parentElement;
            faqCard.classList.toggle('active');
            
            // Close other FAQs when opening one
            if (faqCard.classList.contains('active')) {
                document.querySelectorAll('.faq-card').forEach(card => {
                    if (card !== faqCard && card.classList.contains('active')) {
                        card.classList.remove('active');
                    }
                });
            }
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Make emergency contacts more accessible
    const emergencyContacts = document.querySelectorAll('.contact-list li');
    emergencyContacts.forEach(contact => {
        contact.addEventListener('click', function() {
            const text = this.textContent;
            const phoneNumber = text.split(':')[1].trim();
            
            if (confirm(`Call ${phoneNumber}?`)) {
                // In a real app, this would initiate a phone call
                console.log(`Calling ${phoneNumber}`);
            }
        });
    });
});