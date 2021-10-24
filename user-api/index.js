require("dotenv").config();
const express = require("express");
const app = express();

app.use(express.json());

const db = require("./models");
db.sequelize.sync();

app.use("/api/auth", require("./routes/auth.route"));
app.use("/api/users", require("./routes/users.route"));

app.get("/", (req, res) => {
  res.send("Welcome to User API");
});

const PORT = process.env.PORT || 8080;

app.listen(PORT, () => console.log(`User API listening on port ${PORT}`));
