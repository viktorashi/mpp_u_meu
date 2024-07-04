//configure this file to be a simple navbar
import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';

const Navbar = () => {
    return (
        <AppBar position="static">
            <Toolbar>
                <Button color="inherit" component={Link} to="/molecules">
                    Molecules
                </Button>
                <Button color="inherit" component={Link} to="/elements">
                    Elements
                </Button>
                <Typography variant="h6" component="span" sx={{ flexGrow: 3 }}>
                    Periodic Table
                </Typography>
            </Toolbar>
        </AppBar>
    );
}

export default Navbar;
