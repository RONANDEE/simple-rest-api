const users = require('./db')
const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

// - เวอร์ชั่น Express 4.16.0+ ขึ้นไป
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// - เวอร์ชั่นต่ำกว่า Express 4.16.0+
// const bodyParser = require('body-parser')
// app.use(bodyParser.json())
// app.use(bodyParser.urlencoded({ extended: true }))

app.get("/", (req, res) => {
  res.send("Hello! Node.js");
});

app.get('/users', (req, res) => {
  res.json(users)
})

app.get('/users/:id', (req, res) => {
  res.json(users.find(user => user.id === Number(req.params.id)))
})

app.post('/users', (req, res) => {
  users.push(req.body)
  let json = req.body
  res.send(`Add new user '${json.username}' completed.`)
})

app.put('/users/:id', (req, res) => {
  const updateIndex = users.findIndex(user => user.id === Number(req.params.id))
  res.send(`Update user id: '${users[updateIndex].id}' completed.`)
})

app.delete('/users/:id', (req, res) => {
  const deletedIndex = users.findIndex(user => user.id === Number(req.params.id))
  res.send(`Delete user '${users[deletedIndex].username}' completed.`)
})

app.listen(port, () => {
  console.log(`Starting node.js at port ${port}`);
});