const express = require('express')
const app = express()
const port = 3000

var mysql = require('mysql');

var con = mysql.createConnection({
  host: "앤드포인트",
  user: "admin",
  database: "test",
  password: "비번",
  port: 3306
});

con.connect();

app.get('/', (req, res) => res.send('Hello World!'))

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
