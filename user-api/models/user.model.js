const {Model, DataTypes} = require("sequelize");

module.exports = sequelize => {
  class User extends Model {
  }

  User.init(
    {
      user_id: {
        autoIncrement: true,
        type: DataTypes.INTEGER,
        allowNull: false,
        primaryKey: true
      },
      first_name: {
        type: DataTypes.CHAR(50),
        allowNull: false,
        validate: {
          isAlphanumeric: true,
          notEmpty: true
        }
      },
      last_name: {
        type: DataTypes.CHAR(50),
        allowNull: false,
        validate: {
          isAlphanumeric: true,
          notEmpty: true
        }
      },
      email: {
        type: DataTypes.STRING(50),
        allowNull: false,
        validate: {
          isEmail: true,
          notEmpty: true
        }
      },
      password: {
        type: DataTypes.STRING(50),
        allowNull: false,
        validate: {
          notEmpty: true,
          min: 4
        }
      },
      isAdmin: {
        type: DataTypes.BOOLEAN,
        allowNull: true,
        defaultValue: false
      },
      phone_number: {
        type: DataTypes.CHAR(15),
        allowNull: true,
        validate: {
          notEmpty: true
        }
      },
      date_of_birth: {
        type: DataTypes.DATEONLY,
        allowNull: false,
        validate: {
          isDate: true
        }
      }
    },
    {sequelize, modelName: "user", freezeTableName: true, timestamps: false}
  );
  return User;
};
