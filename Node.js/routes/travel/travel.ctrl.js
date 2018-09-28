const rp = require('request-promise');
const jwt = require('jsonwebtoken');
const config = require('../../config');
const TourSpot = require('../../models/tourspot');

/* https://www.movable-type.co.uk/scripts/latlong.html */
const degToRad = deg => deg * (Math.PI / 180);

const getDistance = function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
  const R = 6371; // Radius of the earth in km
  const dLat = degToRad(lat2 - lat1); // deg2rad above
  const dLon = degToRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2)
    + Math.cos(degToRad(lat1)) * Math.cos(degToRad(lat2))
    * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

// TODO: Polyline 인코딩 오류 고치기
// https://developers.google.com/maps/documentation/utilities/polylinealgorithm
const encoding = function encodingToPolyLineAlgorithm(coordinates) {
  let polyline = '';
  coordinates.forEach((e, index, originArr) => {
    // 1, 2, 3, 4
    let n;
    if (index <= 1) n = (e * 10 ** 5).toFixed(0) << 1;
    else n = ((e - originArr[index - 2]) * 10 ** 5).toFixed(0) << 1;
    // 5
    n = n < 0 ? ~n + 1 : n;
    // 6, 7
    const arr = [];
    while (n > 0) {
      arr.push(n % 32);
      n = parseInt(n / 32, 10);
    }
    // 8, 9, 10, 11
    polyline += arr.map((char, i) => String.fromCharCode(i === arr.length - 1 ? char + 63 : (char | 0x20) + 63)).toString().replace(/,/gi, '');
  });

  return polyline;
};

const tmapParse = function tmapParseWithResult(result) {
  const coordinates = [];
  const pointArr = [];
  result.features.forEach((e) => {
    if (e.geometry.type === 'LineString') {
      e.geometry.coordinates.forEach((coor) => {
        coordinates.push(coor[1]);
        coordinates.push(coor[0]);
      });
    } else if (e.geometry.type === 'Point') {
      pointArr.push({
        instruction: e.properties.description,
        lat: e.geometry.coordinates[1],
        lng: e.geometry.coordinates[0],
      });
    }
  });
  return {
    points: pointArr,
    polyline: encoding(coordinates),
  };
};

// TODO: 무조건 리팩토링 하기, ZERO_RESULT 처리하기, TourSpot/Comment 처리하기, Response 속도좀 높이기
const getList = function getTourAttractionListByTheme(req, res) {
  const {
    lat, lng, theme, minDistance, maxDistance,
  } = req.query;
  const themeArr = theme.split(',').filter(e => e[0] !== '!');
  const avoidThemeArr = theme.split(',').filter(e => e[0] === '!').map(at => at.slice(1));
  const requestOption = {
    url: 'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
    method: 'GET',
    qs: {
      key: config.GOOGLE_MAP_KEY,
      location: `${lat},${lng}`,
      radius: maxDistance,
      language: 'ko',
      type: undefined,
    },
    json: true,
  };

  let tourList = [];
  let thingsToRequest = themeArr.length;

  themeArr.forEach((t) => {
    requestOption.qs.type = t;
    rp(requestOption)
      .then(async (result) => {
        const data = result.results;
        data.forEach((e) => {
          if (e.types.every(pt => !avoidThemeArr.includes(pt))) {
            const place = {
              placeid: e.place_id,
              lat: e.geometry.location.lat,
              lng: e.geometry.location.lng,
              rate: e.rating,
              theme: e.types.toString(),
            };
            tourList.push(place);
          }
        });
        thingsToRequest -= 1;
        if (thingsToRequest !== 0) return;
        // Get Distance
        tourList.forEach((e, index) => {
          const distance = getDistance(lat, lng, e.lat, e.lng) * 1000;
          if (distance <= minDistance) tourList.splice(index, 1);
          else e.distance = distance;
        });
        // Get Comments
        const comments = await TourSpot.find({ placeid: { $in: tourList.map(e => e.placeid) } });
        comments.forEach((c) => {
          tourList[tourList.findIndex(e => e.placeid === c.placeid)].comment = c.comment[0].content;
        });
        res.status(200).json({
          result: 'success',
          list: tourList,
        });
      });
  });
};

const getDirection = function getDirectionForEachTransport(req, res) {
  const {
    transport, depLat, depLng, desLat, desLng,
  } = req.query;
  let requestOption = {};

  switch (parseInt(transport, 10)) {
    case 0: // 자동차
      requestOption = {
        url: 'https://api2.sktelecom.com/tmap/routes?version=1',
        method: 'POST',
        headers: {
          Accept: 'application/json',
          appKey: config.TMAP_KEY,
        },
        form: {
          endX: desLng,
          endY: desLat,
          startX: depLng,
          startY: depLat,
        },
      };
      rp(requestOption)
        .then(data => res.status(200).json(tmapParse(JSON.parse(data))));
      break;
    case 1: // 대중교통
      requestOption = {
        url: 'https://maps.googleapis.com/maps/api/directions/json',
        method: 'GET',
        qs: {
          origin: `${depLat},${depLng}`,
          destination: `${desLat},${desLng}`,
          key: config.GOOGLE_MAP_KEY,
          language: 'ko',
          mode: 'transit',
        },
      };
      rp(requestOption)
        .then((data) => {
          const result = JSON.parse(data).routes[0];
          const pointArr = [];
          result.legs[0].steps.forEach(e => pointArr.push({
            lat: e.start_location.lat,
            lng: e.start_location.lng,
            instruction: e.html_instructions,
          }));
          res.status(200).json({
            points: pointArr,
            polyline: result.overview_polyline.points,
          });
        });
      break;
    case 2: // 도보
      requestOption = {
        url: 'https://api2.sktelecom.com/tmap/routes/pedestrian?version=1',
        method: 'POST',
        headers: {
          Accept: 'application/json',
          appKey: config.TMAP_KEY,
        },
        form: {
          startName: '출발지',
          endName: '목적지',
          endX: desLng,
          endY: desLat,
          startX: depLng,
          startY: depLat,
        },
      };
      rp(requestOption)
        .then(data => res.status(200).json(tmapParse(JSON.parse(data))));
      break;
    default:
      res.status(405).json({ result: 'failure' });
      break;
  }
};

const getInfo = async function getInfoWithId(req, res) {
  const { id } = req.params;
  const place = await TourSpot.findOne({ placeid: id });
  let requestOption = {
    url: 'https://maps.googleapis.com/maps/api/place/details/json',
    method: 'GET',
    qs: {
      key: config.GOOGLE_MAP_KEY,
      placeid: id,
      language: 'ko',
    },
    json: true,
  };
  const placeInfo = (await rp(requestOption)).result;
  requestOption = {
    url: `http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?MobileOS=ETC&MobileApp=Justgo&ServiceKey=${config.TOUR_API_KEY}&mapX=${placeInfo.geometry.location.lng}&mapY=${placeInfo.geometry.location.lat}&radius=1000&_type=json`,
    method: 'GET',
    json: true,
  };
  const nearTourSpot = (await rp(requestOption)).response.body.items.item;
  const nearSpot = [];
  // TODO: API-Docs에서 nearSpot response 수정하기, 안드로이드 모델 봐주기
  nearTourSpot.forEach(e => nearSpot.push({
    title: e.title,
    image: e.firstimage,
    address: e.addr1,
    lat: e.mapy,
    lng: e.mapx,
  }));
  requestOption = {
    url: 'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
    method: 'GET',
    headers: {
      Accept: 'application/json',
      appKey: config.TMAP_KEY,
    },
    qs: {
      key: config.GOOGLE_MAP_KEY,
      location: `${placeInfo.geometry.location.lat},${placeInfo.geometry.location.lng}`,
      radius: 1000,
      language: 'ko',
      type: 'restaurant',
    },
    json: true,
  };
  const nearByRestaurant = (await rp(requestOption)).results;
  const nearRestaurant = [];
  nearByRestaurant.forEach(e => nearRestaurant.push({
    title: e.name,
    image: e.icon,
    address: e.vicinity,
    lat: e.geometry.location.lat,
    lng: e.geometry.location.lng,
  }));

  res.status(200).json({
    result: 'success',
    name: placeInfo.name,
    address: placeInfo.formatted_address,
    image: placeInfo.icon, // TODO: 이미지로 변환하기
    theme: placeInfo.types.toString(),
    nearSpot,
    nearRestaurant,
    comment: place.comment,
  });
};

const postComment = function postCommentAtPlace(req, res) {
  try {
    const { id } = req.params;
    const { rate, content } = req.body;
    const payload = jwt.verify(req.get('X-Access-Token'), config.SALT);
    TourSpot.findOneAndUpdate(
      { placeid: id },
      { $push: { comment: { userId: payload.id, rate, content } } },
      { upsert: true },
    )
      .then(() => res.status(201).json({ result: 'success' }))
      .catch(() => res.status(500).json({ result: 'failure' }));
  } catch (e) {
    res.status(403).send({ result: 'failure', e });
  }
};

exports.getList = getList;
exports.getDirection = getDirection;
exports.getInfo = getInfo;
exports.postComment = postComment;
