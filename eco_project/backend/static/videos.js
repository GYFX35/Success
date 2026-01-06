document.addEventListener('DOMContentLoaded', () => {
    const videoContainer = document.querySelector('.video-container');

    async function fetchVideos() {
        try {
            const response = await fetch('/api/videos');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const videos = await response.json();
            displayVideos(videos);
        } catch (error) {
            videoContainer.innerHTML = `<p>Error fetching videos: ${error.message}</p>`;
        }
    }

    function displayVideos(videos) {
        let html = '';
        videos.forEach(video => {
            html += `
                <div class="video-item">
                    <iframe src="${video.url}" frameborder="0" allowfullscreen></iframe>
                    <div class="video-item-title">${video.title}</div>
                </div>
            `;
        });
        videoContainer.innerHTML = html;
    }

    fetchVideos();
});