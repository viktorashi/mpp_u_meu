import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import ItemList from "./components/ItemList";
import Details from "./components/Details";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ItemList />} />
        <Route path="/details/:number" element={<Details />} />
      </Routes>
    </Router>
  );
}

export default App;
