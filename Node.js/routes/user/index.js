const router = require('express').Router();
const rp = require('request-promise');
const multer = require('multer');

const upload = multer();

router.post('/login', (req, res) => {
  const { userId, name } = req.body;
  rp({
    url: 'http://ec2-52-79-240-33.ap-northeast-2.compute.amazonaws.com:7777/api/user/login',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    json: {
      userId,
      name,
    },
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body));
});

router.put('/:id/profile-image', upload.array('picture'), (req, res) => {
  const jwt = req.get('X-Access-Token');
  const image = req.files['profile-image'];
  rp({
    url: 'http://ec2-52-79-240-33.ap-northeast-2.compute.amazonaws.com:7777/api/user/profile-image',
    method: 'PUT',
    headers: {
      Authentication: `bearer ${jwt}`,
    },
    formData: {
      'profile-image': image,
    },
    json: true,
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body));
});

router.put('/:id/profile-name', (req, res) => {
  const jwt = req.get('X-Access-Token');
  const { name } = req.body;
  rp({
    url: 'http://ec2-52-79-240-33.ap-northeast-2.compute.amazonaws.com:7777/api/user/login',
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authentication: `bearer ${jwt}`,
    },
    body: {
      name,
    },
    json: true,
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body));
});

router.post('/tour-spot', (req, res) => {
  const jwt = req.get('X-Access-Token');
  const { tourId } = req.body;
  rp({
    url: 'http://ec2-52-79-240-33.ap-northeast-2.compute.amazonaws.com:7777/api/user/login',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authentication: `bearer ${jwt}`,
    },
    body: {
      tourId,
    },
    json: true,
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body));
});

module.exports = router;
