
// Import Express — a simple web framework (like Flask in Python)
const express = require('express');

// Create an instance of the Express application
const app = express();

// Port on which the server will listen (e.g., localhost:3000)
const PORT = 3000;

// List of possible lunches to recommend
const lunchOptions = ['Sushi', 'Pizza', 'Burrito', 'Ramen', 'Tacos'];

// GET /recommendation endpoint
app.get('/recommendation', (req, res) => {
    // Select a random element from the array
    const randomLunch = lunchOptions[Math.floor(Math.random() * lunchOptions.length)];
    // Return as JSON
    res.json({ recommendation: randomLunch });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Recommendation service running on http://localhost:${PORT}`);
});

