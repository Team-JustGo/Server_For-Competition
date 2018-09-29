const mongoose = require('mongoose');

const User = new mongoose.Schema({
  userId: String,
  profileName: String,
  profileImage: String,
  wentspot: [{
    placeid: String,
    name: String,
    tags: String,
    date: { type: Date, default: Date.now() },
  }],
});

module.exports = mongoose.model('user', User, 'user');
