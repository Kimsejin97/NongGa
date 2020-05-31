const express = require("express");
const router = express.Router();
const Sequelize = require("sequelize");
const dotenv = require("dotenv");

dotenv.config();

const sequelize = new Sequelize(
    process.env.database,
    process.env.username,
    process.env.password,
    {
        host: process.env.host,
        dialect: "mysql",
    }
);

sequelize
    .authenticate()
    .then(() => {
        console.log("Connection has been established successfully.");
    })
    .catch((err) => {
        console.error("Unable to connect to the database:", err);
    });

router.get("/", (req, res) => {
    sequelize
        .query("SELECT * FROM A", { type: sequelize.QueryTypes.SELECT })
        .then((results) => res.send(results));
});

router.get("/insert", (req, res) => {
    sequelize
        .query(`INSERT INTO A VALUES ("486")`, {
            type: sequelize.QueryTypes.INSERT,
        })
        .then((results) => res.send(results));
});

module.exports = router;
