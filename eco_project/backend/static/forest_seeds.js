document.addEventListener('DOMContentLoaded', () => {
    const videoContainer = document.querySelector('.video-container');
    const videoForm = document.getElementById('video-form');

    async function fetchVideos() {
        try {
            const response = await fetch('/api/forest_seeds_videos');
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
            const embedUrl = video.url.includes('youtube.com/watch?v=')
                ? video.url.replace('watch?v=', 'embed/')
                : video.url;

            html += `
                <div class="video-item">
                    <iframe src="${embedUrl}" frameborder="0" allowfullscreen></iframe>
                    <div class="video-item-title">${video.title}</div>
                </div>
            `;
        });
        videoContainer.innerHTML = html;
    }

    videoForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const titleInput = document.getElementById('video-title');
        const urlInput = document.getElementById('video-url');
        const errorMessage = document.getElementById('error-message');

        errorMessage.textContent = '';

        let videoUrl = urlInput.value;
        if (videoUrl.includes('youtube.com/watch?v=')) {
            videoUrl = videoUrl.replace('watch?v=', 'embed/');
        }

        const newVideo = {
            title: titleInput.value,
            url: videoUrl,
        };

        try {
            const response = await fetch('/api/forest_seeds_videos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newVideo),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            titleInput.value = '';
            urlInput.value = '';

            fetchVideos(); // Refresh the list of videos
        } catch (error) {
            console.error('Failed to submit video:', error);
            errorMessage.textContent = `Error: ${error.message}`;
        }
    });

    fetchVideos();
});
