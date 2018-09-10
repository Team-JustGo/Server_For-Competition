const request = require('request');

const getList = function getTourAttractionListByTheme(req, res) {
  const {
    transport,
    lat,
    lng,
    theme,
    minTime,
    maxTime,
  } = req.query;

  request({
    url: 'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
    method: 'GET',
    qs: {
      key: process.env.GOOGLE_MAP_KEY,
      location: `${lat},${lng}`,
      radius: 50000,
      language: 'ko',
      maxprice: 0,
      type: theme.split(',')[0],
    },
  }, (err, response, body) => {
    if (err) return res.status(500).send({ result: 'failure' });

    return res.status(200).end();
  });
};

exports.getList = getList;
