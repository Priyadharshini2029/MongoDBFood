// models/customer.js
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const customerSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  age:{ type: Number, required: true },
  mobilenumber:{ type: Number, required: true },
  approved:{type:Boolean,default:false},
  rolehotel:{type:String,default:"Customer"}
});

customerSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  const salt = await bcrypt.genSalt(10);  
  this.password = await bcrypt.hash(this.password, salt);
  next();
});

module.exports = mongoose.model('Customer', customerSchema);