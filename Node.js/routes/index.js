const router = require('express').Router();

router.use('/docs', require('./docs'))
  .use('/travel', require('./travel'))
  .use('/user', require('./user'))
  .use('/contact', require('./contact'))
  .get('/', (req, res) => {
    res.status(200).json({
      result: 'success',
    });
  });

module.exports = router;
