const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/api/test', (req, res) => {
    res.json({ status: "Success", message: "Cloud Server is responding!" });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});