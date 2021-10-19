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
    User.sync()
    console.log("Connected")
}).catch((error) => {
    console.log("Error:", error)
});

app.get("/api/users/", (req, res) => {
    User.findAll().then(user => res.json(user))
})

app.get("/api/users/:id", (req, res) => {
    User.findByPk(req.params.id).then(user => {
        if (!user)
            res.status(400).send("User not found")
        else
            res.send(user)
    }).catch(error => {
        res.status(400).send(error)
    })
})

app.post("/api/users/", (req, res) => {
    sequelize.transaction().then(transaction => {
        User.create(req.body, {transaction: transaction}).then(user => {
            transaction.commit().then(() => {
                res.send(user.id)
            })
        }).catch(error => {
            transaction.rollback().then(() => {
                res.status(400).send(error)
            })
        })
    })
})

app.put("/api/users/:id", (req, res) => {
    sequelize.transaction().then(transaction => {
        User.update(req.body, {
            where: {
                userID: req.params.id
            }
        }).then(affectedCount => {
            if (affectedCount[0] === 0)
                transaction.rollback().then(() => {
                    res.status(400).send("User not found")
                })
            else
                transaction.commit().then(() => {
                    res.send("User updated")
                })
        }).catch(error => {
            transaction.rollback().then(() => {
                res.status(400).send(error)
            })
        })
    })
})

app.delete("/api/users/:id", (req, res) => {
    sequelize.transaction().then(transaction => {
        User.destroy({
            where: {
                userID: req.params.id
            }
        }).then(affectedCount => {
            if (affectedCount.valueOf() === 0)
                transaction.rollback().then(() => {
                    res.status(400).send("User not found")
                })
            else
                transaction.commit().then(() => {
                    res.send("User deleted")
                })
        }).catch(error => {
            transaction.rollback().then(() => {
                res.status(400).send(error)
            })
        })
    })
})

app.listen(PORT, () => console.log(`User API listening on port ${PORT}`));
