import React, { useEffect, useState } from 'react';
import { getRooms } from '../services/api';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';

const RoomList = () => {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    const fetchRooms = async () => {
      const data = await getRooms();
      setRooms(data);
    };
    fetchRooms();
  }, []);

  return (
    <Grid container spacing={3}>
      {rooms.map((room) => (
        <Grid item key={room.id} xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h5">{room.type}</Typography>
              <Typography variant="body2">{room.description}</Typography>
              <Typography variant="body1">Price: ${room.price}</Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export function RoomList();{
    return <div>Room List</div>;
}