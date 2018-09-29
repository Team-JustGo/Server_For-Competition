const router = require('express').Router();
const multer = require('multer');
const ctrl = require('./user.ctrl');

const upload = multer();

router.post('/login', ctrl.login)
  .get('/profile', ctrl.getProfile)
  .put('/:id/profile-image', upload.array('picture'), ctrl.modifyProfileImage)
  .put('/:id/profile-name', ctrl.modifyProfileName)
  .get('/tour-spot', ctrl.getWentSpot)
  .post('/tour-spot', ctrl.saveWentSpot);

module.exports = router;
