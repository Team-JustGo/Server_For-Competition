const express = require('express');

const router = express.Router();
const ctrl = require('./travel.ctrl');

router.get('/tour-list', ctrl.getList);

module.exports = router;
