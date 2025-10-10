document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');
    const worldBankDataContainer = document.getElementById('world-bank-data');
    const eurostatDataContainer = document.getElementById('eurostat-data');
    const agriculturalLandDataContainer = document.getElementById('agricultural-land-data');
    const drinkingWaterDataContainer = document.getElementById('drinking-water-data');
    const energyAccessDataContainer = document.getElementById('energy-access-data');
    const lifeExpectancyDataContainer = document.getElementById('life-expectancy-chart-container');
    const childMortalityDataContainer = document.getElementById('child-mortality-chart-container');
    const livestockChartContainer = document.getElementById('livestockChart');

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
    if (drinkingWaterDataContainer) {
        fetchDrinkingWaterData();
    }
    if (energyAccessDataContainer) {
        fetchEnergyAccessData();
    }
    if (lifeExpectancyDataContainer) {
        fetchLifeExpectancyData();
    }
    if (childMortalityDataContainer) {
        fetchChildMortalityData();
    }
    if (livestockChartContainer) {
        fetchLivestockData();
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

    async function fetchDrinkingWaterData() {
        try {
            const response = await fetch('/api/drinking_water');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                drinkingWaterDataContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            const canvas = document.createElement('canvas');
            drinkingWaterDataContainer.appendChild(canvas);

            const chart = new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.country),
                    datasets: [{
                        label: 'Access to Safely Managed Drinking Water (%)',
                        data: data.map(item => item.value),
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        } catch (error) {
            drinkingWaterDataContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }

    async function fetchEnergyAccessData() {
        try {
            const response = await fetch('/api/energy_access');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                energyAccessDataContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            const canvas = document.createElement('canvas');
            energyAccessDataContainer.appendChild(canvas);

            const chart = new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.country),
                    datasets: [{
                        label: 'Access to Electricity (%)',
                        data: data.map(item => item.value),
                        backgroundColor: 'rgba(255, 206, 86, 0.6)',
                        borderColor: 'rgba(255, 206, 86, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        } catch (error) {
            energyAccessDataContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }

    async function fetchLifeExpectancyData() {
        try {
            const response = await fetch('/api/life_expectancy');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                lifeExpectancyDataContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            // For now, just display the raw data to inspect the structure
            let html = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            lifeExpectancyDataContainer.innerHTML = html;

        } catch (error) {
            lifeExpectancyDataContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }

    async function fetchChildMortalityData() {
        try {
            const response = await fetch('/api/child_mortality');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                childMortalityDataContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            if (data.length === 0) {
                childMortalityDataContainer.innerHTML = `<p>No child mortality data available for the selected criteria.</p>`;
                return;
            }

            const canvas = document.createElement('canvas');
            canvas.id = 'childMortalityChart';
            childMortalityDataContainer.appendChild(canvas);

            const chart = new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: data.map(item => `${item.country} (${item.year})`),
                    datasets: [{
                        label: 'Child Mortality Rate (per 1,000 live births)',
                        data: data.map(item => item.value),
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        } catch (error) {
            childMortalityDataContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }

    async function fetchLivestockData() {
        try {
            const response = await fetch('/api/livestock');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.error) {
                livestockChartContainer.innerHTML = `<p>Error fetching data: ${data.error}</p>`;
                return;
            }

            const chart = new Chart(livestockChartContainer, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.country),
                    datasets: [{
                        label: 'Livestock Population (in millions)',
                        data: data.map(item => item.value),
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        } catch (error) {
            livestockChartContainer.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
        }
    }
});
