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
      <h2>Details for Page {number}</h2>
      <p>{details.description}</p>
      <p>{details.category}</p>
      <p>{details.appearance}</p>
      <p>{details.discovered_by}</p>
      <p>{details.named_by}</p>
      <p>{details.phase}</p>
      <img src={details.bohr_model_image} alt="Bohr Model" />
      <p>{details.summary}</p>
    </div>
  );
}

export default DetailsPage;
