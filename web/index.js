const express = require('express');
const path = require('path')

const app = express();
const api_port = 5555;

app.use(express.static(path.join(__dirname, 'public')));

// home page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Endpoint to fetch data from Python backend for politics
app.get('/api/politic', async (req, res) => {
  try {
    const response = await fetch(`http://localhost:${api_port}/api/politic`);
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('Error fetching data from Python backend:', error);
    res.status(500).send('Error fetching data');
  }
});

const port = 4444;
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});