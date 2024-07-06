import { React } from "react";
import {
  Navigate,
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import "./App.css";
import ElementList from "./components/ElementList";
import Details from "./components/Details";
import Navbar from "./components/Navbar";
import Molecules from "./components/Molecules";
import Molecule from "./components/Molecule";

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Navigate replace to="/elements" />} />
          <Route path="/elements/:number" element={<Details />} />
          <Route path="/elements" element={<ElementList />} />
          <Route path="/molecules" element={<Molecules />} />
          <Route path="/molecules/:id" element={<Molecule />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
