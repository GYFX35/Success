document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');
    const worldBankDataContainer = document.getElementById('world-bank-data');
    const eurostatDataContainer = document.getElementById('eurostat-data');

    // Fetch and display World Bank data on page load
    fetchWorldBankData();
    fetchEurostatData();

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

    async function fetchWorldBankData() {
        try {
            const response = await fetch('/api/forest_area');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                worldBankDataContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            let html = '<ul>';
            data.forEach(item => {
                html += `<li>${item.country}: ${item.value ? item.value.toFixed(2) : 'N/A'}% (${item.year})</li>`;
            });
            html += '</ul>';

            worldBankDataContainer.innerHTML = html;

        } catch (error) {
            worldBankDataContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }

    async function fetchEurostatData() {
        try {
            const response = await fetch('/api/eu_forest_area');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                eurostatDataContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            let html = '<ul>';
            data.forEach(item => {
                html += `<li>${item.country}: ${item.value ? item.value.toFixed(2) : 'N/A'}% (${item.year})</li>`;
            });
            html += '</ul>';

            eurostatDataContainer.innerHTML = html;

        } catch (error) {
            eurostatDataContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }
});
