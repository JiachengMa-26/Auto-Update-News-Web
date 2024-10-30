// Set tomorrow's date dynamically in the weather box
window.onload = function() {
    const weatherDate = document.getElementById("weather-date");
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    weatherDate.textContent = `Date: ${tomorrow.toLocaleDateString('en-US', options)}`;
};

async function fetchData() {
    // getting politics data
    try {
        const response = await fetch('/api/politic');
        const data = await response.json();

        // Update the HTML with the new data
        news_list = document.querySelector('#news-list');
        for (const news of data) {
            // Step 1: Create a new <li> element
            const newLi = document.createElement('li');

            // Step 2: Create a new <a> element
            const newA = document.createElement('a');

            // Step 3: Change the text and href of the <a> tag
            newA.textContent = news[0]; // Set the link text
            newA.href = news[1]; // Set the href attribute

            // Step 4: Append the <a> tag to the <li>
            newLi.appendChild(newA);

            // Step 5: Append the <li> to the <ul>
            news_list.appendChild(newLi);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
  
// Fetch data when the page loads
document.addEventListener('DOMContentLoaded', fetchData);

// Optional: Refresh data every 10 seconds (change this to everyday at 12am maybe)
// setInterval(fetchData, 10000);