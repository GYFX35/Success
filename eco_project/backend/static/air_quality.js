document.addEventListener('DOMContentLoaded', () => {
    const dataContainer = document.getElementById('data-container');

    fetch('/api/air_quality')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!data || data.length === 0) {
                dataContainer.innerHTML = '<p>No air quality data found.</p>';
                return;
            }
            data.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('data-item');
                itemElement.innerHTML = `
                    <h3>${item.city}</h3>
                    <p><strong>AQI:</strong> ${item.aqi}</p>
                    <p><strong>Pollutant:</strong> ${item.pollutant}</p>
                `;
                dataContainer.appendChild(itemElement);
            });
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            dataContainer.innerHTML = '<p>Could not fetch air quality data. Please try again later.</p>';
        });
});
