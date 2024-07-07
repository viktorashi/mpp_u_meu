import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import {
  Container,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Typography,
  Paper,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

const ElementList = () => {
  const [elements, setelements] = useState([]);
  const [name, setName] = useState("");
  const [editId, setEditId] = useState(0);
  const [category, setCategory] = useState("");
  const [appearance, setAppearance] = useState("");
  const [discovered_by, setDiscovered_by] = useState("");
  const [named_by, setNamed_by] = useState("");
  const [phase, setPhase] = useState("");
  const [bohr_model_image, setbohr_model_image] = useState("");
  const [summary, setSummary] = useState("");
  const [symbol, setSymbol] = useState("");
  const [atomic_number, setAtomic_number] = useState(0);

  useEffect(() => {
    fetchelements();
  }, []);

  const fetchelements = async () => {
    const response = await axios.get("/elements");
    console.log(response.data);
    setelements(response.data);
  };

  const resetFields = () => {
    setEditId(0);
    setName("");
    setCategory("");
    setAppearance("");
    setDiscovered_by("");
    setNamed_by("");
    setPhase("");
    setbohr_model_image("");
    setSummary("");
    setAtomic_number(0);
    setSymbol("");
  };

  const addelement = async () => {
    await axios
      .post("/elements", {
        name,
        category,
        appearance,
        discovered_by,
        named_by,
        phase,
        bohr_model_image,
        summary,
        atomic_number,
        symbol,
      })
      .then((response) => {
        setelements([...elements, response.data]);
        resetFields();
      })
      .catch((error) => {
        console.error(error.response.data.message);
      });
  };

  const updateelement = async (id) => {
    await axios
      .put(`/elements/${id}`, {
        name,
        category,
        appearance,
        discovered_by,
        named_by,
        phase,
        bohr_model_image,
        summary,
        atomic_number,
        symbol,
      })
      .then((response) => {
        console.log(response.data);
        setelements(
          elements.map((element) =>
            element.atomic_number === id ? response.data : element
          )
        );
        resetFields();
      })
      .catch((error) => {
        console.error(error.response.data.message);
      });
  };

  const deleteelement = async (id) => {
    await axios
      .delete(`/elements/${id}`)
      .then(() => {
        setelements(elements.filter((element) => element.atomic_number !== id));
      })
      .catch((error) => {
        console.error(error.response.data.message);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(editId);
    if (editId !== 0 && editId !== undefined) {
      updateelement(editId);
    } else {
      addelement();
    }
  };

  const handleEdit = (element) => {
    setEditId(element.atomic_number);
    setAtomic_number(element.atomic_number);
    setName(element.name || "");
    setCategory(element.category || "");
    setAppearance(element.appearance || "");
    setDiscovered_by(element.discovered_by || "");
    setNamed_by(element.named_by || "");
    setPhase(element.phase || "");
    setbohr_model_image(element.bohr_model_image || "");
    setSummary(element.summary || "");
    setSymbol(element.symbol || "");
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" component="h1" gutterBottom>
        Elements List
      </Typography>
      <Paper elevation={3} style={{ padding: "20px", marginBottom: "20px" }}>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            margin="normal"
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Symbol"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Atomic Number"
            value={atomic_number}
            onChange={(e) => setAtomic_number(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Appearance"
            value={appearance}
            onChange={(e) => setAppearance(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Discovered by"
            value={discovered_by}
            onChange={(e) => setDiscovered_by(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Named by"
            value={named_by}
            onChange={(e) => setNamed_by(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Phase"
            value={phase}
            onChange={(e) => setPhase(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Bohr model"
            value={bohr_model_image}
            onChange={(e) => setbohr_model_image(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Summary"
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            style={{ marginTop: "20px" }}
          >
            {editId ? "Update" : "Add"}
          </Button>
        </form>
        <Button onClick={resetFields}>Reset selection</Button>
      </Paper>
      <List>
        {elements
          .sort((a, b) => a.atomic_number - b.atomic_number)
          .map((element) => (
            <Paper
              key={element.atomic_number}
              elevation={2}
              style={{ marginBottom: "10px" }}
            >
              <ListItem>
                <Link to={`/elements/${element.atomic_number}`}>
                  <ListItemText
                    primary={element.name}
                    secondary={element.appearance}
                  />
                </Link>
                <IconButton
                  edge="end"
                  aria-label="edit"
                  onClick={() => handleEdit(element)}
                >
                  <EditIcon />
                </IconButton>
                <IconButton
                  edge="end"
                  aria-label="delete"
                  onClick={() => deleteelement(element.atomic_number)}
                >
                  <DeleteIcon />
                </IconButton>
              </ListItem>
            </Paper>
          ))}
      </List>
    </Container>
  );
};

export default ElementList;
