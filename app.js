const express = require('express')
var path = require('path');
const app = express()
const port = 8000

app.use(express.static(__dirname));
app.get('/', (req, res) =>  {
    res.sendFile(path.join(__dirname, '/views', 'main.html'))
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))


