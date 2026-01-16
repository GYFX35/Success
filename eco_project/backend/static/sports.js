document.addEventListener('DOMContentLoaded', () => {
    const channelContainer = document.getElementById('channel-container');

    fetch('https://www.thesportsdb.com/api/v1/json/123/all_leagues.php')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!data.leagues || data.leagues.length === 0) {
                channelContainer.innerHTML = '<p>No leagues found.</p>';
                return;
            }
            data.leagues.forEach(league => {
                const leagueElement = document.createElement('div');
                leagueElement.classList.add('channel');
                leagueElement.innerHTML = `
                    <h3>${league.strLeague}</h3>
                    <p><strong>Sport:</strong> ${league.strSport}</p>
                `;
                channelContainer.appendChild(leagueElement);
            });
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            channelContainer.innerHTML = '<p>Could not fetch league data. Please try again later.</p>';
        });
});
