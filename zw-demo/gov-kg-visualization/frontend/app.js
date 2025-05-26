// This file contains the main logic for the frontend application.
// It handles user interactions, makes API calls to the backend, and processes the data for visualization.

document.addEventListener('DOMContentLoaded', function() {
    const fetchDataButton = document.getElementById('fetch-data');
    const visualizationContainer = document.getElementById('visualization');

    fetchDataButton.addEventListener('click', function() {
        fetch('/api/neo4j/data')
            .then(response => response.json())
            .then(data => {
                renderVisualization(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });

    function renderVisualization(data) {
        // Clear previous visualization
        visualizationContainer.innerHTML = '';

        // Call the D3 visualization function
        createD3Visualization(data);
    }
});