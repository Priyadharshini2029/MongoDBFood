 const express = require('express');
 const router = express.Router();
 const Order = require('../model/order');
 const Menu = require('../model/menu')
 
 // Fetch all orders
 router.get('/', async (req, res) => {
  try {
    const orders = await Order.find();
    res.status(200).json(orders);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching orders' });
  }
});

// PUT API to update an order's status
router.put('/', async (req, res) => {
  try {
    const { _id, status } = req.body; // Retrieve the order ID and status from the request body

    if (!_id || !status) {
      return res.status(400).json({ error: 'Order ID and status are required' });
    }

    // Find and update the order
    const updatedOrder = await Order.findByIdAndUpdate(
      _id, 
      { status },
      { new: true } // Return the updated document
    );

    if (!updatedOrder) {
      return res.status(404).json({ error: 'Order not found' });
    }

    res.status(200).json({ message: 'Order updated successfully', order: updatedOrder });
  } catch (error) {
    console.error('Error updating order:', error);
    res.status(500).json({ error: 'Error updating order' });
  }
});
// Add a new order
router.post('/', async (req, res) => {
  try {
    const { items, totalPrice, name, mobile, table } = req.body;

    const newOrder = new Order({
      items,
      totalPrice,name, mobile, table
    });

    const savedOrder = await newOrder.save();
    res.status(201).json(savedOrder);
  } catch (error) {
    res.status(500).json({ error: 'Error adding new order' });
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