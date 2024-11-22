const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({
   items: [{itemName: String, category: String, price: Number, quantity: Number}],
   totalprice: Number,
   mobilenumber: Number,
   name: String,
  });
   
 
 module.exports  = mongoose.model("Order", orderSchema);
  