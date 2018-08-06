const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const logger = require('morgan');

const app = express();

app.use(logger('common', { stream: fs.createWriteStream('justgo_server.log', {'flags': 'w'}) }))
    .use(bodyParser.json())
    .use(bodyParser.urlencoded({
        extended: true
    }))
    .use('/api', require('./routes'));

app.listen(process.env.PORT || 5000, () => {
    console.log('server running at', process.env.PORT || 5000);
});