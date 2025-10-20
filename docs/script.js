document.addEventListener('DOMContentLoaded', () => {
    // The dynamic data fetching has been removed as it is not supported by GitHub Pages.
});

fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        const ipAddressElement = document.getElementById('ip-address');
        if (ipAddressElement) {
            ipAddressElement.textContent = data.ip;
        }
    })
    .catch(error => {
        console.error('Error fetching IP address:', error);
        const ipAddressElement = document.getElementById('ip-address');
        if (ipAddressElement) {
            ipAddressElement.textContent = 'Could not fetch IP address.';
        }
    });