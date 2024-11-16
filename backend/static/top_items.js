function highlightSelectedButton(button) {
    if (!button) return;
    const buttons = document.querySelectorAll('.buttons button');
    buttons.forEach(btn => btn.classList.remove('active')); 
    button.classList.add('active'); 
}
// button highlight function that has yet to be fully implememnted

function fetchTopItems(itemType, timeRange, button) {
    highlightSelectedButton(button);
    console.log(`Fetching top items for ${itemType} with time range ${timeRange}`);
    fetch(`/top/${itemType}/${timeRange}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.error) {
                console.error("Error fetching data:", data.error);
            } else {
                displayTopItems(data.items);
            }
        })
        .catch(error => console.error("Error fetching data:", error));
}
// fetches top items (like tracks or artists) based on the selected itemType and timeRange, highlights the clicked button, and displays the data. If an error occurs, it logs the error to the console


function displayTopItems(items) {
    const container = document.getElementById('top-items');
    container.innerHTML = ''; // Clear previous items

    items.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'top-item';
        itemDiv.innerHTML = `
            <h3>${item.name}</h3>
            <p>${item.artists ? item.artists.map(a => a.name).join(', ') : ''}</p>
        `;
        container.appendChild(itemDiv);
    });
}
// clears the previous items from the container, then creates and appends a new div for each item, displaying its name and artist
