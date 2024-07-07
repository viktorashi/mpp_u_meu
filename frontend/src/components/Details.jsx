// DetailsPage.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function DetailsPage() {
  const { number } = useParams();
  const [details, setDetails] = useState(null);
  const [primaryMolecules, setPrimaryMolecules] = useState([]);
  const [statusCode, setStatusCode] = useState(0);


  useEffect(() => {

    const fetchDetails = async () => {
      await axios.get(`/elements/${number}`).then((response) => setDetails(response.data)).catch((error) => console.error("Error fetching data:", error));

      // Fetch molecules that have the current element as their primary element
      await axios.get(`/molecules/primary/${number}`).then((response) => {
        console.log(response.data)
        setPrimaryMolecules(response.data)
      }).catch((error) => {
        setStatusCode(error.response.status);
        console.error("Error fetching data:", error.response.data.message)
      });
    };

    fetchDetails(); // Call the fetchDetails function when component mounts
  }, [number]); // Re-run effect whenever the 'number' parameter changes

  if (!details) {
    return <p>Loading...</p>;
  }
  //display them
  return (
    <div>
      <h2>Details for {details.name}</h2>
      <p>{details.summary}</p>
      <h2>Symbol</h2>
      <p>{details.symbol}</p>
      <h2>Atomic number</h2>
      <p>{details.atomic_number}</p>
      <h2>Category</h2>
      <p>{details.category}</p>
      <h2>Appearance</h2>
      <p>{details.appearance}</p>
      <h2>Discovered by</h2>
      <p>{details.discovered_by}</p>
      <h2>Named by</h2>
      <p>{details.named_by}</p>
      <h2>Phase</h2>
      <p>{details.phase}</p>
      <h2>Bohr model image</h2>
      <img src={details.bohr_model_image} alt="Bohr Model" />

      {/* primary molecules details if they're not empty list */}
      {primaryMolecules.length > 0 && (
        <div>
          <h2>Primary Molecules</h2>
          <ul>
            {primaryMolecules.map((molecule) => (
              <li key={molecule.id}>
                <h3>{molecule.formula}</h3>
                <p>LogP: {molecule.logp}</p>
                <p>Primary Element: {molecule.primary_element_symbol}</p>
              </li>
            ))}
          </ul>
        </div>)
      }
      {statusCode === 404 && <p>No primary molecules found</p>}
    </div>


  );
}

export default DetailsPage;
