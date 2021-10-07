const express = require("express");
const app = express();

const PORT = process.env.PORT || 8080;

app.get("/", (req, res) => {
  res.send("Welcome to User API");
});

app.listen(PORT, console.log(`User API listening on port ${PORT}`));
