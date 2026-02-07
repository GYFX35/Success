fetchRecyclingData();
fetchProtectedAreasData();

function fetchRecyclingData() {
    fetch('/api/unep_recycling')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching recycling data:', data.error);
                return;
            }
            renderChart('recyclingChart', data, 'Recycling Rate (%)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 1)');
        })
        .catch(error => console.error('Error:', error));
}

function fetchProtectedAreasData() {
    fetch('/api/unep_protected_areas')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching protected areas data:', data.error);
                return;
            }
            renderChart('protectedAreasChart', data, 'Protected Area Coverage (%)', 'rgba(153, 102, 255, 0.2)', 'rgba(153, 102, 255, 1)');
        })
        .catch(error => console.error('Error:', error));
}

function renderChart(canvasId, data, label, bgColor, borderColor) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const labels = data.map(item => item.country);
    const values = data.map(item => item.value);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
                backgroundColor: bgColor,
                borderColor: borderColor,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}
