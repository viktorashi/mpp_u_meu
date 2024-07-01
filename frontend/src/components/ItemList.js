import React, { useState, useEffect } from "react";
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
  const [description, setDescription] = useState("");
  const [editId, setEditId] = useState(0);
  const [category, setCategory] = useState("");
  const [appearance, setAppearance] = useState("");
  const [discovered_by, setDiscovered_by] = useState("");
  const [named_by, setNamed_by] = useState("");
  const [phase, setPhase] = useState("");
  const [bohr_model_image, setbohr_model_image] = useState("");
  const [summary, setSummary] = useState("");

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    const response = await axios.get("http://127.0.0.1:5000/items");
    console.log(response.data);
    setItems(response.data);
  };

  const resetFields = () => {
    setEditId(0);
    setName("");
    setDescription("");
    setCategory("");
    setAppearance("");
    setDiscovered_by("");
    setNamed_by("");
    setPhase("");
    setbohr_model_image("");
    setSummary("");
  };

  const addItem = async () => {
    const response = await axios.post("http://127.0.0.1:5000/items", {
      name,
      description,
      category,
      appearance,
      discovered_by,
      named_by,
      phase,
      bohr_model_image,
      summary,
    });
    setItems([...items, response.data]);
    resetFields();
  };

  const updateItem = async (id) => {
    const response = await axios.put(`http://127.0.0.1:5000/items/${id}`, {
      name,
      description,
      category,
      appearance,
      discovered_by,
      named_by,
      phase,
      bohr_model_image,
      summary,
    });
    console.log(response.data);
    setItems(items.map((item) => (item.number === id ? response.data : item)));
    resetFields();
  };

  const deleteItem = async (id) => {
    await axios.delete(`http://127.0.0.1:5000/items/${id}`);
    setItems(items.filter((item) => item.number !== id));
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
    setEditId(item.number);
    setName(item.name || "");
    setDescription(item.description || "");
    setCategory(item.category || "");
    setAppearance(item.appearance || "");
    setDiscovered_by(item.discovered_by || "");
    setNamed_by(item.named_by || "");
    setPhase(item.phase || "");
    setbohr_model_image(item.bohr_model_image || "");
    setSummary(item.summary || "");
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
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
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
        {items.map((item) => (
          <Paper
            key={item.number}
            elevation={2}
            style={{ marginBottom: "10px" }}
          >
            <ListItem>
              <ListItemText primary={item.name} secondary={item.description} />
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
                onClick={() => deleteItem(item.number)}
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
