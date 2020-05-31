const express = require("express");
const cors = require("cors");
const logger = require("morgan");
const bodyParser = require("body-parser");
const router = express.Router();

const app = express();
const port = 5000;

app.use(cors());

// Parse incoming requests data (https://github.com/expressjs/body-parser)
app.use(bodyParser.json({ limit: "50mb" }));
app.use(bodyParser.urlencoded({ extended: false, limit: "50mb" }));

// Log requests to the console.
app.use(logger("dev"));

// Route
const route_root = require("./Router/root");

app.use("/", route_root);

app.listen(port, () =>
    console.log(`Example app listening at http://localhost:${port}`)
);
