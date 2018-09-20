const express = require('express');

const router = express.Router();
const ctrl = require('./travel.ctrl');

router.get('/tour-list', ctrl.getList)
  .get('/direction', ctrl.getDirection)
  .get('/:id/tour-info', ctrl.getInfo)
  .post('/:id/tour-info', ctrl.postComment);

module.exports = router;
