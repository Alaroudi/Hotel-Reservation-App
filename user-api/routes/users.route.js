const router = require("express").Router();
const {User, sequelize} = require("../models");

router.get("/", (req, res) => {
  User.findAll().then(user => res.json(user));
});

router.get("/:id", (req, res) => {
  User.findByPk(req.params.id)
    .then(user => {
      if (user === null) res.status(404).send("User not found");
      else res.send(user);
    })
    .catch(error => res.status(400).send(error));
});

router.post("/", (req, res) => {
  sequelize.transaction().then(transaction => {
    User.create(req.body, {transaction: transaction})
      .then(() => {
        res.send("User created");
        transaction.commit();
      })
      .catch(error => {
        res.status(400).send(error);
        transaction.rollback();
      });
  });
});

router.put("/:id", (req, res) => {
  sequelize.transaction().then(transaction => {
    User.update(req.body, {
      where: {
        user_id: req.params.id
      },
      transaction: transaction
    })
      .then(affected => {
        if (affected[0] !== 1) {
          res.status(400).send("Could not update user");
          transaction.rollback();
        } else {
          res.send("User updated");
          transaction.commit();
        }
      })
      .catch(error => {
        res.status(400).send(error);
        transaction.rollback();
      });
  });
});

router.delete("/:id", (req, res) => {
  sequelize.transaction().then(transaction => {
    User.destroy({
      where: {
        user_id: req.params.id
      },
      transaction: transaction
    })
      .then(affected => {
        if (affected !== 1) {
          res.status(400).send("Could not delete user");
          transaction.rollback();
        } else {
          res.send("User deleted");
          transaction.commit();
        }
      })
      .catch(error => {
        res.status(400).send(error);
        transaction.rollback();
      });
  });
});

module.exports = router;
