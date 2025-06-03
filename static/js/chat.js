document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages');
    const sessionId = document.getElementById('session-id').value;

    function appendMessage(content, isAI) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${isAI ? 'justify-start' : 'justify-end'} mb-4`;
        
        const innerDiv = document.createElement('div');
        innerDiv.className = `max-w-3/4 rounded-lg p-3 ${
            isAI ? 'bg-blue-100 dark:bg-blue-900' : 'bg-green-100 dark:bg-green-900'
        }`;
        
        const text = document.createElement('p');
        text.className = `text-sm ${
            isAI ? 'text-blue-900 dark:text-blue-100' : 'text-green-900 dark:text-green-100'
        }`;
        text.textContent = content;
        
        innerDiv.appendChild(text);
        messageDiv.appendChild(innerDiv);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    messageForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Disable input while processing
        messageInput.disabled = true;
        messageForm.querySelector('button').disabled = true;
        
        // Show user message
        appendMessage(message, false);
        messageInput.value = '';
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: message
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                appendMessage(data.response, true);
            } else {
                appendMessage('Sorry, there was an error processing your message. Please try again.', true);
            }
        } catch (error) {
            console.error('Error:', error);
            appendMessage('Sorry, there was an error processing your message. Please try again.', true);
        } finally {
            // Re-enable input
            messageInput.disabled = false;
            messageForm.querySelector('button').disabled = false;
            messageInput.focus();
        }
    });
}); 