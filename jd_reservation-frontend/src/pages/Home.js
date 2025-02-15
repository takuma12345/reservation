import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import Typography from '@mui/material/Typography';

const Home = () => {
  return (
    <div>
      <Navbar />
      <Typography variant="h3" align="center" sx={{ mt: 4 }}>
        Welcome to JD Reservation
      </Typography>
      <Footer />
    </div>
  );
};

export default Home;