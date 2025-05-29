import React, { useEffect, useState } from "react";

const cellStyle = {
  padding: "10px",
  border: "1px solid #ddd",
  textAlign: "left",
};

function UserList() {
  const [users, setUsers] = useState({});
  const [editUserId, setEditUserId] = useState(null);
  const [editData, setEditData] = useState({ name: "", zip_code: "" });
  const [getUserId, setGetUserId] = useState("");
  const [fetchedUser, setFetchedUser] = useState(null);
  const [fetchError, setFetchError] = useState("");

  const fetchUsers = async () => {
    const res = await fetch("http://127.0.0.1:8000/users/");
    if (res.ok) {
      const data = await res.json();
      setUsers(data);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleDelete = async (id) => {
    await fetch(`http://127.0.0.1:8000/users/${id}`, {
      method: "DELETE",
    });
    fetchUsers();
  };

  const handleEdit = (id) => {
    setEditUserId(id);
    setEditData({
      name: users[id].name,
      zip_code: users[id].zip_code,
    });
  };

  const handleCancel = () => {
    setEditUserId(null);
    setEditData({ name: "", zip_code: "" });
  };

  const handleChange = (field, value) => {
    setEditData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (
      editData.zip_code &&
      !/^\d{5}(-\d{4})?$/.test(editData.zip_code)
    ) {
      alert("Invalid ZIP code format.");
      return;
    }

    await fetch(`http://127.0.0.1:8000/users/${editUserId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(editData),
    });

    setEditUserId(null);
    fetchUsers();
  };

  const handleGetUser = async () => {
    setFetchedUser(null);
    setFetchError("");
    const res = await fetch(`http://127.0.0.1:8000/users/${getUserId}`);
    if (res.ok) {
      const data = await res.json();
      setFetchedUser(data);
    } else {
      const err = await res.json();
      setFetchError(err.detail || "Error fetching user.");
    }
  };

  const userEntries = Object.entries(users);

  return (
    <div>
      <h2 style={{ textAlign: "center" }}>User List</h2>

      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter User ID"
          value={getUserId}
          onChange={(e) => setGetUserId(e.target.value)}
          style={{ marginRight: "10px", padding: "5px" }}
        />
        <button onClick={handleGetUser}>Get User by ID</button>
        {fetchError && (
          <p style={{ color: "red", marginTop: "5px" }}>{fetchError}</p>
        )}
        {fetchedUser && (
          <div
            style={{
              marginTop: "10px",
              padding: "10px",
              border: "1px solid #ccc",
              width: "fit-content",
              marginInline: "auto",
              textAlign: "left",
            }}
          >
            <strong>Name:</strong> {fetchedUser.name} <br />
            <strong>ZIP Code:</strong> {fetchedUser.zip_code} <br />
            <strong>Latitude:</strong> {fetchedUser.latitude} <br />
            <strong>Longitude:</strong> {fetchedUser.longitude} <br />
            <strong>Timezone Offset (sec):</strong> {fetchedUser.timezone_offset_seconds} <br />
            <strong>Timezone:</strong> {fetchedUser.timezone} <br />
            <strong>Timezone Error:</strong> {fetchedUser.timezone_error ? "Yes" : "No"} <br />
          </div>
        )}
      </div>

      {userEntries.length === 0 ? (
        <p style={{ textAlign: "center" }}>No users found.</p>
      ) : (
        <table
          style={{
            margin: "0 auto",
            borderCollapse: "collapse",
            width: "80%",
            boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
            fontFamily: "Arial, sans-serif",
          }}
        >
          <thead style={{ backgroundColor: "#f4f4f4" }}>
            <tr>
              <th style={cellStyle}>ID</th>
              <th style={cellStyle}>Name</th>
              <th style={cellStyle}>ZIP Code</th>
              <th style={cellStyle}>Timezone</th>
              <th style={cellStyle}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {userEntries.map(([id, user]) => (
              <tr key={id}>
                <td style={cellStyle}>{id}</td>
                {editUserId === id ? (
                  <>
                    <td style={cellStyle}>
                      <input
                        value={editData.name}
                        onChange={(e) =>
                          handleChange("name", e.target.value)
                        }
                      />
                    </td>
                    <td style={cellStyle}>
                      <input
                        value={editData.zip_code}
                        onChange={(e) =>
                          handleChange("zip_code", e.target.value)
                        }
                      />
                    </td>
                    <td style={cellStyle}>{user.timezone}</td>
                    <td style={cellStyle}>
                      <button onClick={handleSave}>Save</button>{" "}
                      <button onClick={handleCancel}>Cancel</button>
                    </td>
                  </>
                ) : (
                  <>
                    <td style={cellStyle}>{user.name}</td>
                    <td style={cellStyle}>{user.zip_code}</td>
                    <td style={cellStyle}>{user.timezone}</td>
                    <td style={cellStyle}>
                      <button onClick={() => handleEdit(id)}>Edit</button>{" "}
                      <button onClick={() => handleDelete(id)}>Delete</button>
                    </td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default UserList;