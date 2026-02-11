document.addEventListener('DOMContentLoaded', () => {
    const podcastContainer = document.getElementById('podcast-container');

    // iTunes Search API for environmental podcasts
    const apiUrl = 'https://itunes.apple.com/search?term=environment&entity=podcast&limit=15';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            podcastContainer.innerHTML = ''; // Clear loading message

            if (!data.results || data.results.length === 0) {
                podcastContainer.innerHTML = '<p>No podcasts found.</p>';
                return;
            }

            data.results.forEach(podcast => {
                const podcastCard = document.createElement('div');
                podcastCard.classList.add('podcast-card');

                const img = document.createElement('img');
                img.src = podcast.artworkUrl600 || podcast.artworkUrl100;
                img.alt = podcast.collectionName;

                const h3 = document.createElement('h3');
                h3.textContent = podcast.collectionName;

                const artistP = document.createElement('p');
                artistP.innerHTML = `<strong>Artist:</strong> `;
                const artistSpan = document.createElement('span');
                artistSpan.textContent = podcast.artistName;
                artistP.appendChild(artistSpan);

                const genreP = document.createElement('p');
                genreP.innerHTML = `<strong>Genre:</strong> `;
                const genreSpan = document.createElement('span');
                genreSpan.textContent = podcast.primaryGenreName;
                genreP.appendChild(genreSpan);

                const link = document.createElement('a');
                link.href = podcast.collectionViewUrl;
                link.target = "_blank";
                link.textContent = "View on Apple Podcasts";

                podcastCard.appendChild(img);
                podcastCard.appendChild(h3);
                podcastCard.appendChild(artistP);
                podcastCard.appendChild(genreP);
                podcastCard.appendChild(link);

                podcastContainer.appendChild(podcastCard);
            });
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            podcastContainer.innerHTML = '<p>Could not fetch podcast data. Please try again later.</p>';
        });
});
