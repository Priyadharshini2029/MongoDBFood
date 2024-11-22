const Customer = require('../model/customer');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

exports.register = async (req, res) => {
  try {
    const { name, email, password, approved, rolehotel, age, mobilenumber } = req.body;
    let customer = await Customer.findOne({ email });
    if (customer) return res.status(400).json({ msg: 'Customer already exists' });

    customer= new Customer({ name, email, password, approved, rolehotel, age, mobilenumber });
    await customer.save();

    const payload = { customerId: customer._id };
    const token = jwt.sign(payload, process.env.JWT_SECRET);
    

    res.status(201).json({ token, customer});
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;
    const customer = await Customer.findOne({ email });
    if (!customer) return res.status(400).json({ msg: 'Invalid credentials' });

    const isMatch = await bcrypt.compare(password, customer.password);
    if (!isMatch) return res.status(400).json({ msg: 'Invalid credentials' });

    const payload = {customerId: customer._id };
    const token = jwt.sign(payload, process.env.JWT_SECRET);
  
    res.json({ token,customer  });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};