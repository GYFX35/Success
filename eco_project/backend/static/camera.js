document.addEventListener('DOMContentLoaded', () => {
    const cameraStream = document.getElementById('camera-stream');
    const capturePhotoButton = document.getElementById('capture-photo');
    const startVideoButton = document.getElementById('start-video');
    const stopVideoButton = document.getElementById('stop-video');
    const galleryContainer = document.getElementById('gallery-container');

    let mediaRecorder;
    let recordedChunks = [];

    // Access camera
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            cameraStream.srcObject = stream;
        })
        .catch(err => {
            console.error("Error accessing camera: ", err);
            galleryContainer.innerHTML = '<p>Could not access the camera. Please check permissions.</p>';
        });

    // Capture photo
    capturePhotoButton.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        canvas.width = cameraStream.videoWidth;
        canvas.height = cameraStream.videoHeight;
        canvas.getContext('2d').drawImage(cameraStream, 0, 0);
        canvas.toBlob(blob => {
            const timestamp = new Date().toISOString();
            uploadFile(blob, `photo_${timestamp}.png`);
        }, 'image/png');
    });

    // Start recording
    startVideoButton.addEventListener('click', () => {
        recordedChunks = [];
        const stream = cameraStream.srcObject;
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm;codecs=vp9' });

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            const timestamp = new Date().toISOString();
            uploadFile(blob, `video_${timestamp}.webm`);
        };

        mediaRecorder.start();
        startVideoButton.disabled = true;
        stopVideoButton.disabled = false;
    });

    // Stop recording
    stopVideoButton.addEventListener('click', () => {
        mediaRecorder.stop();
        startVideoButton.disabled = false;
        stopVideoButton.disabled = true;
    });

    // Upload file
    function uploadFile(blob, filename) {
        const formData = new FormData();
        formData.append('media', blob, filename);

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            fetchGallery();
        })
        .catch(error => {
            console.error('Error uploading file:', error);
        });
    }

    // Fetch and display gallery
    function fetchGallery() {
        fetch('/api/gallery')
            .then(response => response.json())
            .then(files => {
                displayMedia(files);
            })
            .catch(error => console.error('Error fetching gallery:', error));
    }

    function displayMedia(files) {
        galleryContainer.innerHTML = '';
        if (files.length === 0) {
            galleryContainer.innerHTML = '<p>No media in the gallery yet.</p>';
            return;
        }
        files.forEach(file => {
            const mediaElement = file.endsWith('.png') || file.endsWith('.jpg') ?
                `<img src="/uploads/${file}" alt="${file}">` :
                `<video src="/uploads/${file}" controls></video>`;

            galleryContainer.innerHTML += `<div class="gallery-item">${mediaElement}</div>`;
        });
    }

    // Initial load
    fetchGallery();
});
