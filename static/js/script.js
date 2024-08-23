document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('promptForm');
    const promptInput = document.getElementById('prompt');
    const imagesContainer = document.getElementById('imagesContainer');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const loadingOverlay = document.getElementById('loadingOverlay');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const prompt = promptInput.value.trim();

        // Display loading indicator and overlay
        loadingIndicator.classList.add('active');
        loadingOverlay.classList.add('active');

        // Clear any existing images
        imagesContainer.innerHTML = '';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ 'prompt': prompt })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            if (data.images && Array.isArray(data.images)) {
                // Loop through each image and display it
                data.images.forEach(base64Img => {
                    const img = document.createElement('img');
                    img.src = `data:image/png;base64,${base64Img}`;
                    imagesContainer.appendChild(img);
                });
            } else {
                throw new Error('Failed to generate images');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating the images.');
        } finally {
            // Hide loading indicator and overlay
            loadingIndicator.classList.remove('active');
            loadingOverlay.classList.remove('active');
        }
    });
});
