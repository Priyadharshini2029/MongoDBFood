const express = require('express');
const router = express.Router();
 const Order = require('../model/order');
 const Menu = require('../model/menu')

 router.post("/", async (req, res) => {
  try {
    const { items, totalprice, mobilenumber, name } = req.body;

    const order = new Order({ items, totalprice, mobilenumber, name });
    await order.save();

    res.status(201).json({ message: "Order placed successfully!" , order});
  } catch (error) {
    res.status(500).json({ message: "Failed to place order", error });
  }
});


// Get all orders
router.get('/', async (req, res) => {
    try {
      const menu = await Menu.find();
      res.status(200).json(menu);
    } catch (error) {
      res.status(500).json({ message: 'Error fetching items', error });
    }
  });

module.exports = router;