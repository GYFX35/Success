document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');
    const worldBankDataContainer = document.getElementById('world-bank-data');
    const undpDataContainer = document.getElementById('undp-data');

    // Fetch and display World Bank data on page load
    fetchWorldBankData();
    // Fetch and display UNDP data on page load
    fetchUNDPData();

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

    async function fetchUNDPData() {
        try {
            const response = await fetch('/api/sdg_data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                undpDataContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            if (data.length === 0) {
                undpDataContainer.innerHTML = '<p>No UNDP data available for the selected countries.</p>';
                return;
            }

            let html = '<ul>';
            data.forEach(item => {
                html += `<li><b>${item.country} (Target ${item.target_id}):</b> ${item.description}
                    <ul>
                        <li>Budget: $${item.budget ? item.budget.toFixed(2) : 'N/A'}</li>
                        <li>Expense: $${item.expense ? item.expense.toFixed(2) : 'N/A'}</li>
                    </ul>
                </li>`;
            });
            html += '</ul>';

            undpDataContainer.innerHTML = html;

        } catch (error) {
            undpDataContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }
});
