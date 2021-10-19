require("dotenv").config()
const express = require("express");
const {Sequelize} = require("sequelize")
const sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USER, process.env.DB_PASS, {
    host: process.env.DB_HOST,
    dialect: process.env.DB_DIALECT
})
const User = require("./models/User")(sequelize);
const PORT = process.env.PORT || 8080;
const app = express();

app.use(express.json())
sequelize.authenticate().then(() => {
    console.log("Connected")
    User.sync()
}).catch((error) => {
    console.log("Error:", error)
});

app.get("/api/users/", (req, res) => {
    User.findAll().then(user => res.json(user))
})

app.get("/api/users/:id", (req, res) => {
    User.findByPk(req.params.id).then(user => {
        if (user === null)
            return res.status(400)
        return res.send(user)
    })
})

app.post("/api/users/", (req, res) => {
    sequelize.transaction().then(transaction => {
        User.create(req.body, {transaction: transaction}).then(user => {
            transaction.commit()
            res.send(user.id)
        }).catch(error => {
            transaction.rollback()
            res.status(400).send(error)
        })
    })
})

app.put("/api/users/:id", (req, res) => {
    sequelize.transaction().then(transaction => {
        User.update(req.body, {
            where: {
                userID: req.params.id
            }
        }).then(() => {
            transaction.commit()
        }).catch(error => {
            transaction.rollback()
            res.status(400).send(error)
        })
    })
    res.send(req.params.id)
})

app.delete("/api/users/:id", (req, res) => {
    sequelize.transaction().then(transaction => {
        User.destroy({
            where: {
                userID: req.params.id
            }
        }).then(() => {
            transaction.commit()
        }).catch(error => {
            transaction.rollback()
            res.send(error, 400)
        })

    })
})

app.listen(PORT, () => console.log(`User API listening on port ${PORT}`));
