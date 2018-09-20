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

  const tourList = [];
  let thingsToRequest = themeArr.length;

  themeArr.forEach((t) => {
    requestOption.qs.type = t;
    rp(requestOption)
      .then((result) => {
        const data = result.results;
        for(const e in data) {
          if (data[e].types.every(pt => !avoidThemeArr.includes(pt))) {
            /* const placeInfo = await TourSpot.findOne({ placeid: data[e].place_id });
            if (placeInfo === null) {
              const newSpot = new TourSpot({
                placeid: data[e].place_id,
                name: data[e].name,
                address: data[e].vicinity,
                image: data[e].icon, // TODO: 이미지로 변경하기
                theme: data[e].types.toString(),
                lat: data[e].geometry.location.lat,
                lng: data[e].geometry.location.lng,
                comment: [],
              });
              newSpot.save();
            } */
            const place = {
              placeid: data[e].place_id,
              lat: data[e].geometry.location.lat,
              lng: data[e].geometry.location.lng,
              rate: data[e].rating,
              theme: data[e].types.toString(),
            };
            tourList.push(place);
          }
        }
        // TODO: 코멘트 $or 로 찾고 place에 넣고 response 전송
        //const comments = TourSpot.find()
        thingsToRequest -= 1;
        if (thingsToRequest !== 0) return;
        tourList.forEach((e, index) => {
          const distance = getDistance(lat, lng, e.lat, e.lng) * 1000;
          if (distance <= minDistance) tourList.splice(index, 1);
          else e.distance = distance;
        });
        res.status(200).json({
          result: 'success',
          iist: tourList,
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
    url: `http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?MobileOS=ETC&MobileApp=Justgo&ServiceKey=${config.TOUR_API_KEY}&mapX=${place.lng}&mapY=${place.lat}&radius=1000&_type=json`,
    method: 'GET',
    json: true,
  }
  const nearTourSpot = (await rp(requestOption)).response.body.items.item;;
  const nearSpot = [];
  // TODO: API-Docs에서 nearSpot response 수정하기
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
      location: `${place.lat},${place.lng}`,
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
    image: placeInfo.icon, // TODO: 고치기
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
      { $push: { comment: { userId: payload.id, rate, content } } }
    )
      .then(() => res.status(201).json({ result: 'success' }))
      .catch(() => res.status(500).json({ result: 'failure' }));
  } catch (e) {
    res.status(403).send({ result: 'failure' });
  }
};

exports.getList = getList;
exports.getDirection = getDirection;
exports.getInfo = getInfo;
exports.postComment = postComment;
