const express = require('express')
const app = express()
const port = 3000

var db_config = require('./config/config.json')
var mysql = require('mysql');

var con = mysql.createConnection({
  host: db_config.host,
  user: db_config.user,
  database: db_config.database,
  password: db_config.password,
  port: 3306
});

var data = [];

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
  con.query("SELECT * FROM danger", function (err, result) {
    if (err) throw err;
    data = JSON.stringify(result);
    console.log(data);
  });
});