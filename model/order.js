const mongoose = require('mongoose');

const OrderItemSchema = new mongoose.Schema({
  category: String,
  itemName: String,
  price: Number,
  quantity: Number,
});

const OrderSchema = new mongoose.Schema({
  items: [OrderItemSchema],
  orderId: String,
  orderedAt: { type: Date, default: Date.now },
  status: {type: String, default: "ordered"},
  name: {type: String, required: true},
  mobile: {type: Number, required: true},
  table: {type: Number},
  totalPrice: Number,
});

module.exports = mongoose.model('Order', OrderSchema);
