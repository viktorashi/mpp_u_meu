//this is the page with all the molecules
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { IconButton, TextField, Paper, List, ListItem, ListItemText, Container, Typography, Button } from '@mui/material';
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

const Molecules = () => {
    const [molecules, setMolecules] = useState([]);
    const [id, setid] = useState(0);
    const [formula, setFormula] = useState("");
    const [logp, setLogp] = useState(0);
    const [primary_element_symbol, setPrimary_element_symbol] = useState("");
    const [primary_element, setprimary_element] = useState(0);

    const fetchMolecules = async () => {
        const response = await axios.get('/molecules');
        console.log(response.data);
        setMolecules(response.data);
    }

    useEffect(() => {
        fetchMolecules()
    }, []);

    const resetFields = () => {
        setid(0);
        setFormula("");
        setLogp(0);
        setPrimary_element_symbol("");
        setprimary_element(0);
    };

    const addMolecule = async () => {
        await axios.post(`/molecules`, {
            id,
            formula,
            logp,
            primary_element_symbol,
            primary_element
        }).then((response) => {
            setMolecules([...molecules, response.data]);
            resetFields();
        }).catch((error) => console.error(error.response.data.message));
    }

    const updateMolecule = async () => {
        await axios.put(`/molecules/${id}`, {
            formula,
            logp,
            primary_element_symbol,
            primary_element
        }).then((response) => {
            setMolecules(molecules.map((molecule) => molecule.id === id ? response.data : molecule));
            console.log(response.data)
            resetFields();
        }).catch((error) => console.error(error.response.data.message));
    }

    const deleteMolecule = async (id) => {
        await axios.delete(`/molecules/${id}`).then(() => {
            setMolecules(molecules.filter((molecule) => molecule.id !== id));
        }).catch((error) => console.error(error.response.data.message));
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        if (id) {
            updateMolecule();
        } else {
            addMolecule();
        }
    }

    const handleEdit = (molecule) => {
        setid(molecule.id || 0);
        setFormula(molecule.formula || "");
        setLogp(molecule.logp || 0);
        setPrimary_element_symbol(molecule.primary_element_symbol || "");
        setprimary_element(molecule.primary_element || 0);
    }

    return (
        <Container>
            <Typography variant="h2" gutterBottom>
                Molecules
            </Typography>
            <Paper elevation={3} style={{ padding: "20px", marginBottom: "20px" }}>
                <form onSubmit={handleSubmit}>
                    <TextField
                        fullWidth
                        margin="normal"
                        label="Formula"
                        value={formula}
                        onChange={(e) => setFormula(e.target.value)}
                    />
                    <TextField
                        fullWidth
                        margin="normal"
                        label="logp"
                        value={logp}
                        onChange={(e) => setLogp(e.target.value)}
                    />
                    <TextField
                        fullWidth
                        margin="normal"
                        label="Primary Element Symbol"
                        value={primary_element_symbol}
                        onChange={(e) => setPrimary_element_symbol(e.target.value)}
                    />
                    <TextField
                        fullWidth
                        margin="normal"
                        label="Primary Atomic Number"
                        value={primary_element}
                        onChange={(e) => setprimary_element(e.target.value)}
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        style={{ marginTop: "20px" }}
                    >
                        {id ? "Update" : "Add"}
                    </Button>
                </form>
                <Button onClick={resetFields}>Reset selection</Button>
            </Paper>
            <List>
                {molecules.map((molecule) => (
                    <ListItem key={molecule.id}>
                        <ListItemText primary={molecule.formula} />
                        <Typography variant="h5" gutterBottom>{molecule.logp}</Typography>
                        {/* button towards the details page for the molecule*/}
                        <Link to={`/molecules/${molecule.id}`}>
                            <Button>Details</Button>
                        </Link>
                        <IconButton
                            edge="end"
                            aria-label="edit"
                            onClick={() => handleEdit(molecule)}
                        >
                            <EditIcon />
                        </IconButton>
                        <IconButton
                            edge="end"
                            aria-label="delete"
                            onClick={() => deleteMolecule(molecule.id)}
                        >
                            <DeleteIcon />
                        </IconButton>
                    </ListItem>
                ))}
            </List>
        </Container>
    );
}
export default Molecules;