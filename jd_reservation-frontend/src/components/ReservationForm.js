import React, { useState } from 'react';
import { createReservation } from '../services/api';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';

const ReservationForm = ({ roomId }) => {
  const [formData, setFormData] = useState({
    check_in: '',
    check_out: '',
    total_price: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const reservationData = {
      ...formData,
      room: roomId,
    };
    await createReservation(reservationData);
    alert('Reservation created successfully!');
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <TextField
        label="Check-in Date"
        type="date"
        value={formData.check_in}
        onChange={(e) => setFormData({ ...formData, check_in: e.target.value })}
        fullWidth
        margin="normal"
        InputLabelProps={{ shrink: true }}
      />
      <TextField
        label="Check-out Date"
        type="date"
        value={formData.check_out}
        onChange={(e) => setFormData({ ...formData, check_out: e.target.value })}
        fullWidth
        margin="normal"
        InputLabelProps={{ shrink: true }}
      />
      <TextField
        label="Total Price"
        type="number"
        value={formData.total_price}
        onChange={(e) => setFormData({ ...formData, total_price: e.target.value })}
        fullWidth
        margin="normal"
      />
      <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
        Book Now
      </Button>
    </Box>
  );
};

export default ReservationForm;