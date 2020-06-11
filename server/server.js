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

app.get('/', (req, res) => res.send('Hello World!'))

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

app.get('/post', function (req, res){
  con.query("SELECT * FROM danger", function (err, result) {
    con.end();
    if (err) throw err;
    data = JSON.stringify(result);
    res.send(data);
  }); 
});

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
