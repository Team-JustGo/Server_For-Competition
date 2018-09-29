const jsonwebtoken = require('jsonwebtoken');
const rp = require('request-promise');
const User = require('../../models/user');
const config = require('../../config');

const login = function loginWithId(req, res) {
  const { userId, name } = req.body;
  rp({
    url: 'http://localhost:7777/api/user/login',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    json: {
      userId,
      name,
    },
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body));
};

const getProfile = function getProfileWithJWT(req, res) {
  const jwt = req.get('X-Access-Token');
  rp({
    url: 'http://localhost:7777/api/user/profile',
    method: 'GET',
    headers: {
      Authorization: `Bearer ${jwt}`,
    },
    json: true,
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body));
};

const modifyProfileImage = function modifyProfileImageWithJWT(req, res) {
  const jwt = req.get('X-Access-Token');
  const image = req.files['profile-image'];
  rp({
    url: 'http://localhost:7777/api/user/profile-image',
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${jwt}`,
    },
    formData: {
      'profile-image': image,
    },
    json: true,
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body));
};

const modifyProfileName = function modifyProfileNameWithJWT(req, res) {
  const jwt = req.get('X-Access-Token');
  const { name } = req.body;
  rp({
    url: 'http://localhost:7777/api/user/login',
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${jwt}`,
    },
    body: {
      name,
    },
    json: true,
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body));
};

const getWentSpot = async function getWentSpotWithJWT(req, res) {
  try {
    const payload = jsonwebtoken.verify(req.get('X-Access-Token'), config.SALT);
    const wentSpot = await User.findOne({ userId: payload.identity }).select('wentspot');
    res.status(200).json(wentSpot.wentspot);
  } catch (e) {
    res.status(403).json({ result: 'failure' });
  }
};

const saveWentSpot = async function saveWentSpotWithJWT(req, res) {
  try {
    const payload = jsonwebtoken.verify(req.get('X-Access-Token'), config.SALT);
    const { placeid } = req.body;
    const placeInfo = (await rp({
      url: 'https://maps.googleapis.com/maps/api/place/details/json',
      method: 'GET',
      qs: {
        key: config.GOOGLE_MAP_KEY,
        placeid,
        language: 'ko',
      },
      json: true,
    })).result;
    User.findOneAndUpdate({ userId: payload.identity },
      { $push: { wentspot: { placeid, name: placeInfo.name, tags: placeInfo.types.toString() } } })
      .then(() => res.status(201).json({ result: 'success' }))
      .catch(() => res.status(500).json({ result: 'failure' }));
  } catch (e) {
    res.status(403).json({ result: 'failure' });
  }
  /* const jwt = req.get('X-Access-Token');
  const { tourId } = req.body;
  rp({
    url: 'http://localhost:7777/api/user/tour-spot',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${jwt}`,
    },
    body: {
      tourId,
    },
    json: true,
    resolveWithFullResponse: true,
    simple: false,
  }).then(data => res.status(data.statusCode).send(data.body)); */
};

module.exports = {
  login,
  getProfile,
  modifyProfileImage,
  modifyProfileName,
  getWentSpot,
  saveWentSpot,
};
