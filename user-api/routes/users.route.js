const router = require("express").Router();
const { User, sequelize } = require("../models");

router.get("/", (req, res) => {
  User.findAll().then(user => res.json(user));
});

router.get("/:id", (req, res) => {
  User.findByPk(req.params.id)
    .then(user => {
      if (user === null) return res.status(404).send("User not found");
      return res.send(user);
    })
    .catch(error => res.status(500).send(error));
});

router.post("/", (req, res) => {
  sequelize.transaction().then(transaction => {
    User.create(req.body, { transaction: transaction })
      .then(user => {
        transaction.commit();
        res.send(user.id);
      })
      .catch(error => {
        transaction.rollback();
        res.status(400).send(error);
      });
  });
});

router.put("/:id", (req, res) => {
  sequelize.transaction().then(transaction => {
    User.update(req.body, {
      where: {
        userID: req.params.id
      }
    })
      .then(() => {
        transaction.commit();
      })
      .catch(error => {
        transaction.rollback();
        res.status(400).send(error);
      });
  });
  res.send(req.params.id);
});

router.delete("/:id", (req, res) => {
  sequelize.transaction().then(transaction => {
    User.destroy({
      where: {
        userID: req.params.id
      }
    })
      .then(() => {
        transaction.commit();
        res.send();
      })
      .catch(error => {
        transaction.rollback();
        res.send(error, 400);
      });
  });
});

module.exports = router;
