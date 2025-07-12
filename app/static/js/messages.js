document.addEventListener('DOMContentLoaded', function() {
    // Toggle conversation selection
    const conversations = document.querySelectorAll('.conversation');
    
    conversations.forEach(conversation => {
        conversation.addEventListener('click', function() {
            conversations.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            
            // In a real app, this would load the conversation messages
            console.log('Loading conversation with:', this.querySelector('.user-name').textContent);
        });
    });
    
    // Toggle ride details panel
    const viewDetailsBtn = document.querySelector('.panel-actions .btn-primary');
    const closePanelBtn = document.querySelector('.close-panel');
    const rideDetailsPanel = document.querySelector('.ride-details-panel');
    
    viewDetailsBtn.addEventListener('click', function() {
        rideDetailsPanel.classList.add('active');
    });
    
    closePanelBtn.addEventListener('click', function() {
        rideDetailsPanel.classList.remove('active');
    });
    
    // Send message functionality
    const messageInput = document.querySelector('.message-composer input');
    const sendBtn = document.querySelector('.send-btn');
    
    function sendMessage() {
        const messageText = messageInput.value.trim();
        
        if (messageText) {
            // Create new message element
            const messagesArea = document.querySelector('.messages-area');
            const newMessage = document.createElement('div');
            newMessage.className = 'message sent';
            newMessage.innerHTML = `
                <div class="message-content">
                    <p>${messageText}</p>
                    <span class="message-time">Just now <i class="fas fa-check-double"></i></span>
                </div>
            `;
            
            messagesArea.appendChild(newMessage);
            messageInput.value = '';
            
            // Scroll to bottom
            messagesArea.scrollTop = messagesArea.scrollHeight;
            
            // Simulate reply after 1-3 seconds
            setTimeout(simulateReply, 1000 + Math.random() * 2000);
        }
    }
    
    function simulateReply() {
        const messagesArea = document.querySelector('.messages-area');
        const activeConversation = document.querySelector('.conversation.active');
        const userName = activeConversation.querySelector('.user-name').textContent;
        const userAvatar = activeConversation.querySelector('.user-avatar').src;
        
        const replies = [
            "Thanks, that works for me!",
            "I'll be there on time",
            "Can we change the meeting point?",
            "How much luggage can I bring?",
            "Do you accept mobile money payment?",
            "See you soon!"
        ];
        
        const randomReply = replies[Math.floor(Math.random() * replies.length)];
        
        const newMessage = document.createElement('div');
        newMessage.className = 'message received';
        newMessage.innerHTML = `
            <img src="${userAvatar}" alt="${userName}" class="user-avatar">
            <div class="message-content">
                <p>${randomReply}</p>
                <span class="message-time">Just now</span>
            </div>
        `;
        
        messagesArea.appendChild(newMessage);
        
        // Update last message in conversation list
        activeConversation.querySelector('.last-message').textContent = randomReply;
        
        // Add unread badge if not active
        if (!document.querySelector('.conversation-view').contains(document.activeElement)) {
            const badge = activeConversation.querySelector('.unread-count') || 
                          document.createElement('span');
            if (!activeConversation.querySelector('.unread-count')) {
                badge.className = 'unread-count';
                activeConversation.querySelector('.conversation-badge').prepend(badge);
            }
            const currentCount = parseInt(badge.textContent) || 0;
            badge.textContent = currentCount + 1;
        }
        
        // Scroll to bottom
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }
    
    sendBtn.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
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
    
    // Initialize with first conversation active
    if (conversations.length > 0) {
        conversations[0].click();
    }
});