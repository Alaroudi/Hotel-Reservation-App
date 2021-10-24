const router = require("express").Router();
const { User } = require("../models");
const Joi = require("joi");
const jwt = require("jsonwebtoken");

router.post("/", async (req, res) => {
  const { error } = validate(req.body);
  if (error) {
    return res.status(400).send(error.message);
  }
  try {
    const user = await User.findOne({ where: { email: req.body.email } });
    if (!user) {
      return res.status(400).send("Invalid email or password");
    }

    if (req.body.password !== user.password) {
      return res.status(400).send("Invalid email or password");
    }

    const token = jwt.sign(
      {
        id: user.user_id,
        isAdmin: user.isAdmin
      },
      process.env.Private_Key
    );

    res.header("x-auth-token", token).send("Successful login.");
  } catch (error) {
    res.status(500).send(error);
  }
});

function validate(req) {
  const schema = Joi.object({
    email: Joi.string().email().min(5).max(100).required(),
    password: Joi.string().min(4).max(50).required()
  });

  return schema.validate(req);
}
module.exports = router;
