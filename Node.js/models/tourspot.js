const mongoose = require('mongoose');

const TourSpot = new mongoose.Schema({
  placeid: String,
  comment: [{
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'user' },
    date: { type: Date, default: Date.now() },
    rate: { type: Number, default: 0 },
    content: String,
  }],
});

module.exports = mongoose.model('tourspot', TourSpot);
