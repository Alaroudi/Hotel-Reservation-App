const {Model, DataTypes} = require("sequelize");

module.exports = (sequelize) => {
    class User extends Model {
    }

    User.init({
        userID: {type: DataTypes.INTEGER, allowNull: false, primaryKey: true, field: "user_id", autoIncrement: true},
        firstName: {type: DataTypes.STRING(50), allowNull: false, field: "first_name"},
        lastName: {type: DataTypes.STRING(50), allowNull: false, field: "last_name"},
        email: {type: DataTypes.STRING(50), allowNull: false, unique: true},
        password: {type: DataTypes.STRING(50), allowNull: false},
        isAdmin: {type: DataTypes.BOOLEAN, defaultValue: false},
        phoneNumber: {type: DataTypes.STRING(15), defaultValue: null, field: "phone_number"},
        dateOfBirth: {type: DataTypes.DATE, allowNull: false, field: "date_of_birth"}
    }, {sequelize, modelName: "user", freezeTableName: true, timestamps: false})
    return User
}
