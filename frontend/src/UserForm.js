import React, { useState } from "react";

function UserForm() {
  const [name, setName] = useState("");
  const [zipCode, setZipCode] = useState("");

  const isValidZip = (zip) => /^\d{5}(-\d{4})?$/.test(zip);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isValidZip(zipCode)) {
      alert("Invalid ZIP code format. Please enter a 5-digit or 9-digit US ZIP code.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, zip_code: zipCode }),
      });

      if (response.ok) {
        const result = await response.json();
        alert("User created successfully!");
        setName("");
        setZipCode("");
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (err) {
      console.error("Request failed:", err);
      alert("An unexpected error occurred. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add a New User</h2>
      <div>
        <label>Name: </label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div>
        <label>ZIP Code: </label>
        <input
          value={zipCode}
          onChange={(e) => setZipCode(e.target.value)}
          required
        />
      </div>
      <button type="submit">Create User</button>
    </form>
  );
}

export default UserForm;