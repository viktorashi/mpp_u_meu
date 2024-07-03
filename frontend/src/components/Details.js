// DetailsPage.js

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function DetailsPage() {
  const { number } = useParams();
  const [details, setDetails] = useState(null);

  useEffect(() => {
    // Define a function to fetch details based on the number
    const fetchDetails = async () => {
      try {
        // Example URL to fetch data from (replace with your actual API endpoint)
        const response = await fetch(`http://127.0.0.1:5000/details/${number}`);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setDetails(data); // Update state with fetched data
        console.log(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
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
    </div>
  );
}

export default DetailsPage;
