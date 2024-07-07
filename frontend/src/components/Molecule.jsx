import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';
import { ListItemText, Container, Typography, } from '@mui/material';

const Molecule = () => {
    const [molecule, setMolecule] = useState({});
    const [primaryElement, setPrimaryElement] = useState({});
    const { id } = useParams();


    useEffect(() => {
        const fetchMoleculeDetails = async () => {
            const response = await axios.get(`/molecules/${id}`);
            setMolecule(response.data);
            const primaryElementResponse = await axios.get(`/elements/${response.data.primary_element}`);
            setPrimaryElement(primaryElementResponse.data);
        }
        fetchMoleculeDetails()

    }, [id]);

    return (
        <Container>
            <Typography variant="h2" gutterBottom>
                Molecule Details
            </Typography>
            <ListItemText primary={molecule.formula} />
            <Typography variant="h5" gutterBottom>LogP</Typography>
            <ListItemText primary={molecule.logp} />
            <Typography variant="h5" gutterBottom>primary:   </Typography>
            <ListItemText primary={molecule.primary_element_symbol} />

            <Typography variant="h5" gutterBottom>Primary Element Details</Typography>
            <ListItemText primary={primaryElement.name} />
            <ListItemText primary={primaryElement.summary} />
            <ListItemText primary={primaryElement.symbol} />
            <ListItemText primary={primaryElement.atomic_number} />
            <ListItemText primary={primaryElement.category} />
            <ListItemText primary={primaryElement.appearance} />

            {primaryElement.discovered_by && (
                <div>
                    <Typography variant="h6" gutterBottom>
                        Discovered By
                    </Typography>
                    <ListItemText primary={primaryElement.discovered_by} />
                </div>
            )}

            {/* only display if namned by is not empty string */}
            {primaryElement.named_by && (
                <div>
                    <Typography variant="h6" gutterBottom>
                        Named By
                    </Typography>
                    <ListItemText primary={primaryElement.named_by} />
                </div>
            )}

            <Typography variant="h6" gutterBottom>
                Phase
            </Typography>
            <ListItemText primary={primaryElement.phase} />
            <Link to={`/elements/${primaryElement.atomic_number}`}>
                <img src={primaryElement.bohr_model_image} alt="Bohr Model" />
            </Link>

        </Container>
    );
}
export default Molecule;    