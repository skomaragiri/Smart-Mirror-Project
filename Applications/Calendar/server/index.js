const express = require('express');
const mongoose = require('mongoose');
const cors = require("cors");
const routes = require('./routes/eventRoute');

require('dotenv').config();

const app = express();
const PORT = process.env.port || 8080;

app.use(express.json())
app.use(cors())
mongoose.connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}, () => console.log('MongoDB connected...'));


app.use(routes);
app.listen(PORT, () => console.log(`listening on: ${PORT}`));