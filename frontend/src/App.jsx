import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState('');
  const [result, setResult] = useState('');
  const [receive, setReceive] = useState(false);

  const handleChange = (event) => {
    setFormData(event.target.value);
    setReceive(false);
    setResult('');
  };

  const handlePredictClick = () => {
    const url = "http://localhost:5000/predict";
    const jsonData = JSON.stringify({ text: formData }); // wrap formData in an object

    fetch(url, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: jsonData,
    })
    .then((response) => response.json())
    .then((response) => {
      setReceive(true);
      setResult(response.prediction);
    })
    .catch(() => {
      setReceive(true);
      setResult('Error fetching prediction');
    });
  };

  const getBackgroundColor = () => {
    if (!receive || !formData) return 'white';
    return result === "The news is Fake" ? 'red' : 'lightgreen';
  };

  return (
    <div className="app-container-outer">
      <div className="app-container-inside">
        <h1 className="app-header">Fake News Detection</h1>
        <textarea
          placeholder="Enter the news text"
          value={formData}
          onChange={handleChange}
          className="app-textarea"
        />
        <button
          onClick={handlePredictClick}
          className="app-button"
        >
          Predict
        </button>
        <div className="app-result">
          PREDICTED RESULT{" : "}
          <span style={{ backgroundColor: getBackgroundColor() }}>
            {receive && formData ? result : " "}
          </span>
        </div>
      </div>
    </div>
  );
}

export default App;
