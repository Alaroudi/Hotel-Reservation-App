const { Sequelize } = require("sequelize");

const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASS,
  {
    host: process.env.DB_HOST,
    dialect: process.env.DB_DIALECT,
    logging: false
  }
);

sequelize
  .authenticate()
  .then(() => {
    console.log(`Connected to ${process.env.DB_NAME} database`);
  })
  .catch(error => {
    console.log("Error:", error);
  });

const db = {};
db.Sequelize = Sequelize;
db.sequelize = sequelize;
db.User = require("./user.model")(sequelize);

module.exports = db;
