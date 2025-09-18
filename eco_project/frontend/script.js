document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');

    sendBtn.addEventListener('click', () => {
        const userInput = chatInput.value;
        if (userInput) {
            appendMessage('You: ' + userInput);
            chatInput.value = '';

            // Placeholder for AI response
            setTimeout(() => {
                appendMessage('AI: You said "' + userInput + '"');
            }, 500);
        }
    });

    function appendMessage(message) {
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
