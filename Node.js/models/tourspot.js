const mongoose = require('mongoose');

const TourSpot = new mongoose.Schema({
  placeid: String,
  name: String,
  address: String,
  image: String,
  theme: [String],
  lat: Number,
  lng: Number,
  comment: [{
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'user' },
    date: { type: Date, default: Date.now() },
    rate: { type: Number, default: 0 },
    content: String,
  }],
});

module.exports = mongoose.model('tourspot', TourSpot);
