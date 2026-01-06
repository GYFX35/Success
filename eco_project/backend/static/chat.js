document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });

    socket.on('chat_message', (msg) => {
        appendMessage(msg);
    });

    if (sendBtn) {
        sendBtn.addEventListener('click', () => {
            const userInput = chatInput.value;
            if (userInput) {
                socket.emit('chat_message', userInput);
                chatInput.value = '';
            }
        });
    }

    function appendMessage(message) {
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});