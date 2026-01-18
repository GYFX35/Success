document.addEventListener('DOMContentLoaded', () => {
    const videoContainer = document.querySelector('.video-container');

    async function fetchVideos() {
        try {
            const response = await fetch('/api/youtube_videos');
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
        if (videos.length === 0) {
            videoContainer.innerHTML = '<p>No videos to display.</p>';
            return;
        }
        let html = '';
        videos.forEach(video => {
            const embedUrl = `https://www.youtube.com/embed/${video.video_id}`;
            html += `
                <div class="video-item">
                    <iframe src="${embedUrl}" frameborder="0" allowfullscreen></iframe>
                    <div class="video-item-title">${video.title}</div>
                </div>
            `;
        });
        videoContainer.innerHTML = html;
    }

    fetchVideos();
});
