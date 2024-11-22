const express = require('express');
const router = express.Router();
const Customer = require('../model/customer');



router.get('/', async (req, res) => {
    try {
      const customer = await Customer.find();
      res.status(200).json(customer);
    } catch (error) {
      res.status(500).json({ message: 'Error fetching items', error });
    }
  });

// PUT route to update employee status and role
router.put('/:id', async (req, res) => {  
  const { approved, rolehotel } = req.body;  

  try {
    // Find the employee by ID and update
    const updatedCustomer = await Customer.findByIdAndUpdate(
      req.params.id,  
      { approved, rolehotel },  
      { new: true }  
    );
    
    // If no employee was found with the given ID, return a 404 error
    if (!updatedCustomer) {
      return res.status(404).json({ error: "Employee not found" });
    }
    
    // Return a success message with the updated employee details
    res.status(200).json({message: 'Updated Successfully',updatedCustomer, });
  } catch (error) {
    console.error("Error updating employee:", error);  // Log the error for debugging
    res.status(500).json({ error: "Failed to update employee" }); // Return a 500 error if something goes wrong
  }
});

  

  // DELETE route to delete employee
  router.delete('/:id', async (req, res) => {
    try {
      const deletedCustomer = await Customer.findByIdAndDelete(req.params.id);
      if (deletedCustomer) {
        res.status(200).json({ message: 'Deleted successfully' });
      } else {
        res.status(404).json({ message: 'User not found' });
      }
    } catch (error) {
      res.status(500).json({ message: 'Error deleting user', error });
    }
  });
  
module.exports = router;