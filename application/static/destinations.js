document.addEventListener('DOMContentLoaded', function() {

    const destinations = ['destination1', 'destination2', 'destination3', 'destination4', 'destination5'];

    // Function to populate the dropdown with destinations
    function populateDestinations() {
        const selectElement1 = document.getElementById('county');
        const selectElement2 = document.getElementById('destination');

        // Clear existing options
        selectElement1.innerHTML = '<option selected>Choose...</option>';
        selectElement2.innerHTML = '<option selected>Choose...</option>';

        // Populate options from the destinations array
        destinations.forEach(destination => {
            const option1 = document.createElement('option');
            const option2 = document.createElement('option');
            option1.value = destination;
            option1.text = destination;
            option2.value = destination;
            option2.text = destination;
            selectElement1.appendChild(option1);
            selectElement2.appendChild(option2);
        });
    }

    populateDestinations();
});
