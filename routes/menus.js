const express = require('express');
const router = express.Router();
const Menu = require('../model/menu');

// Create a new item
router.post('/', async (req, res) => {
  try {
    const newMenu = new Menu({
      itemName: req.body.itemName,
      price: req.body.price || 0,
      category: req.body.category,
    });
    const savedMenu = await newMenu.save();
    res.status(201).json(savedMenu);
  } catch (error) {
    res.status(400).json({ message: 'Error creating item', error });
  }
});

// Get all items
router.get('/', async (req, res) => {
  try {
    const menu = await Menu.find();
    res.status(200).json(menu);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching items', error });
  }
});

// Update an item by ID
router.put('/:id', async (req, res) => {
  try {
    const updatedMenu = await Menu.findByIdAndUpdate(
      req.params.id,
      {
        itemName: req.body.itemName,
        price: req.body.price,
        category: req.body.category,
      },
      { new: true, runValidators: true }
    );
    if (updatedMenu) {
      res.status(200).json(updatedMenu);
    } else {
      res.status(404).json({ message: 'Item not found' });
    }
  } catch (error) {
    res.status(400).json({ message: 'Error updating item', error });
  }
});

// Delete an item by ID
router.delete('/:id', async (req, res) => {
  try {
    const deletedMenu = await Menu.findByIdAndDelete(req.params.id);
    if (deletedMenu) {
      res.status(200).json({ message: 'Item deleted successfully' });
    } else {
      res.status(404).json({ message: 'Item not found' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Error deleting item', error });
  }
});

module.exports = router;
