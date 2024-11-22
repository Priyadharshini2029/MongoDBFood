const mongoose = require('mongoose');

const MenuSchema = new mongoose.Schema({
  itemName: { 
    type: String,
    required: true,
  },
  category: {
    type: String,
    required: true,
  },
  price: {
    type: Number,
    default: 0,
  },
});

module.exports = mongoose.model('Menu', MenuSchema);
