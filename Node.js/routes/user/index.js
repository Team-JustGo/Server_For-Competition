const router = require('express').Router();
const rp = require('request-promise');

router.post('/login', (req, res) => {
  const { userId, name, picture } = req.body;
  rp({
    url: 'http://localhost:5000/api/user/login',
    method: 'POST',
    body: {
      userId,
      name,
      picture,
    },
    json: true,
    resolveWithFullResponse: true,
  }).then((data) => {
    res.status(200).send(data);
  });
});

router.put('/:id/profile-image', (req, res) => {
  // TODO: Reqeust 보내기
});

router.put('/:id/profile-name', (req, res) => {
  // TODO: Reqeust 보내기
});

router.post('/:id/tour-spot', (req, res) => {
  // TODO: Reqeust 보내기
});

module.exports = router;
