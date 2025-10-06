document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');
    const worldBankDataContainer = document.getElementById('world-bank-data');
    const eurostatDataContainer = document.getElementById('eurostat-data');
    const agriculturalLandDataContainer = document.getElementById('agricultural-land-data');

    // Fetch and display data on page load
    if (worldBankDataContainer) {
        fetchWorldBankData();
    }
    if (eurostatDataContainer) {
        fetchEurostatData();
    }
    if (agriculturalLandDataContainer) {
        fetchAgriculturalLandData();
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', async () => {
            const userInput = chatInput.value;
            if (userInput) {
                appendMessage('You: ' + userInput);
                chatInput.value = '';

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message: userInput })
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();
                    appendMessage('AI: ' + data.response);

                } catch (error) {
                    appendMessage('AI: Sorry, something went wrong. Please try again later.');
                    console.error('Fetch error:', error);
                }
            }
        });
    }

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

    async function fetchAgriculturalLandData() {
        try {
            const response = await fetch('/api/agricultural_land');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                agriculturalLandDataContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            let html = '<ul>';
            data.forEach(item => {
                html += `<li>${item.country}: ${item.value ? item.value.toFixed(2) : 'N/A'}% (${item.year})</li>`;
            });
            html += '</ul>';

            agriculturalLandDataContainer.innerHTML = html;

        } catch (error) {
            agriculturalLandDataContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }
});
