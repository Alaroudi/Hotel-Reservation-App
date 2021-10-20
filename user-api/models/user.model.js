const { Model, DataTypes } = require("sequelize");

module.exports = sequelize => {
  class User extends Model {}

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
        allowNull: false
      },
      last_name: {
        type: DataTypes.CHAR(50),
        allowNull: false
      },
      email: {
        type: DataTypes.STRING(50),
        allowNull: false
      },
      password: {
        type: DataTypes.STRING(50),
        allowNull: false
      },
      isAdmin: {
        type: DataTypes.BOOLEAN,
        allowNull: true,
        defaultValue: 0
      },
      phone_number: {
        type: DataTypes.CHAR(15),
        allowNull: true
      },
      date_of_birth: {
        type: DataTypes.DATEONLY,
        allowNull: false
      }
    },
    { sequelize, modelName: "user", freezeTableName: true, timestamps: false }
  );
  return User;
};
