document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.getElementById('password');
    
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Toggle eye icon
        this.innerHTML = type === 'password' 
            ? '<i class="far fa-eye"></i>' 
            : '<i class="far fa-eye-slash"></i>';
    });
    
    // Form submission
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const rememberMe = document.querySelector('input[name="remember"]').checked;
        
        // Simple validation
        if (!email || !password) {
            alert('Please fill in all fields');
            return;
        }
        
        // Show loading state
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
        submitBtn.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
            // In a real app, this would be an actual API call
            console.log('Login attempt with:', { email, password, rememberMe });
            
            // Reset button state
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            
            // Show success message (in real app, redirect on success)
            alert('Login successful! Redirecting to dashboard...');
            // window.location.href = 'dashboard.html';
        }, 1500);
    });
    
    // Social login buttons
    const socialButtons = document.querySelectorAll('.social-btn');
    
    socialButtons.forEach(button => {
        button.addEventListener('click', function() {
            const provider = this.classList.contains('google') ? 'Google' : 'Facebook';
            
            // Show loading state
            const originalBtnText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Redirecting...';
            this.disabled = true;
            
            // Simulate social login redirect
            setTimeout(() => {
                console.log(`Redirecting to ${provider} login`);
                this.innerHTML = originalBtnText;
                this.disabled = false;
                
                // In a real app, this would redirect to OAuth provider
                alert(`In a real app, this would redirect to ${provider} login`);
            }, 1000);
        });
    });
    
    // Set focus on email field when page loads
    document.getElementById('email').focus();
});


// Add these to your existing auth.js

// Password strength indicator
const passwordInput = document.getElementById('password');
const strengthBars = document.querySelectorAll('.strength-bar');
const strengthLabel = document.getElementById('strengthLabel');

passwordInput.addEventListener('input', function() {
    const password = this.value;
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    
    // Complexity checks
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    // Cap at 4 for our 4 bars
    strength = Math.min(strength, 4);
    
    // Update UI
    strengthBars.forEach((bar, index) => {
        if (index < strength) {
            bar.style.backgroundColor = getStrengthColor(strength);
        } else {
            bar.style.backgroundColor = 'var(--light-gray)';
        }
    });
    
    strengthLabel.textContent = getStrengthText(strength);
    strengthLabel.style.color = getStrengthColor(strength);
});

function getStrengthColor(strength) {
    switch(strength) {
        case 1: return '#FF4D4D'; // Red
        case 2: return '#FFA500'; // Orange
        case 3: return '#FFD700'; // Gold
        case 4: return '#2ECC71'; // Green
        default: return 'var(--gray-color)';
    }
}

function getStrengthText(strength) {
    switch(strength) {
        case 1: return 'Very Weak';
        case 2: return 'Weak';
        case 3: return 'Good';
        case 4: return 'Strong';
        default: return '';
    }
}

// Form validation
const signupForm = document.getElementById('signupForm');

signupForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const userType = document.querySelector('input[name="userType"]:checked').value;
    const termsAccepted = document.querySelector('input[name="terms"]').checked;
    
    // Validation
    if (!firstName || !lastName || !email || !phone || !password || !confirmPassword) {
        alert('Please fill in all required fields');
        return;
    }
    
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }
    
    if (password.length < 8) {
        alert('Password must be at least 8 characters');
        return;
    }
    
    if (!termsAccepted) {
        alert('You must accept the terms and conditions');
        return;
    }
    
    // Validate Ghana phone number format
    if (!/^0[2345][0-9]{8}$/.test(phone)) {
        alert('Please enter a valid Ghanaian phone number (e.g., 0241234567)');
        return;
    }
    
    // Show loading state
    const submitBtn = signupForm.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating account...';
    submitBtn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        console.log('Signup data:', {
            firstName,
            lastName,
            email,
            phone: '+233' + phone.substring(1),
            password, // In real app, this would be hashed
            userType,
            termsAccepted
        });
        
        // Reset button state
        submitBtn.innerHTML = originalBtnText;
        submitBtn.disabled = false;
        
        // Show success message (in real app, redirect to verification page)
        alert('Account created successfully! Please check your email for verification.');
        // window.location.href = 'verify-email.html';
    }, 2000);
});