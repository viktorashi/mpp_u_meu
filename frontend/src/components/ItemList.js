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

const ItemList = () => {
  const [items, setItems] = useState([]);
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
    fetchItems();
  }, []);

  const fetchItems = async () => {
    const response = await axios.get("http://127.0.0.1:5000/elements");
    console.log(response.data);
    setItems(response.data);
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

  const addItem = async () => {
    await axios
      .post("http://127.0.0.1:5000/elements", {
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
        setItems([...items, response.data]);
        resetFields();
      })
      .catch((error) => {
        console.error(error.response.data.message);
      });
  };

  const updateItem = async (id) => {
    await axios
      .put(`http://127.0.0.1:5000/elements/${id}`, {
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
        setItems(
          items.map((item) =>
            item.atomic_number === id ? response.data : item
          )
        );
        resetFields();
      })
      .catch((error) => {
        console.error(error.response.data.message);
      });
  };

  const deleteItem = async (id) => {
    await axios
      .delete(`http://127.0.0.1:5000/elements/${id}`)
      .then((response) => {
        setItems(items.filter((item) => item.atomic_number !== id));
      })
      .catch((error) => {
        console.error(error.response.data.message);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(editId);
    if (editId !== 0 && editId !== undefined) {
      updateItem(editId);
    } else {
      addItem();
    }
  };

  const handleEdit = (item) => {
    setEditId(item.atomic_number);
    setAtomic_number(item.atomic_number);
    setName(item.name || "");
    setCategory(item.category || "");
    setAppearance(item.appearance || "");
    setDiscovered_by(item.discovered_by || "");
    setNamed_by(item.named_by || "");
    setPhase(item.phase || "");
    setbohr_model_image(item.bohr_model_image || "");
    setSummary(item.summary || "");
    setSymbol(item.symbol || "");
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" component="h1" gutterBottom>
        Item List
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
        {items
          .sort((a, b) => a.atomic_number - b.atomic_number)
          .map((item) => (
            <Paper
              key={item.atomic_number}
              elevation={2}
              style={{ marginBottom: "10px" }}
            >
              <ListItem>
                <Link to={`/details/${item.atomic_number}`}>
                  <ListItemText
                    primary={item.name}
                    secondary={item.appearance}
                  />
                </Link>
                <IconButton
                  edge="end"
                  aria-label="edit"
                  onClick={() => handleEdit(item)}
                >
                  <EditIcon />
                </IconButton>
                <IconButton
                  edge="end"
                  aria-label="delete"
                  onClick={() => deleteItem(item.atomic_number)}
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

export default ItemList;
