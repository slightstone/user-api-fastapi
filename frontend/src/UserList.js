import React, { useEffect, useState } from "react";

function UserList() {
  const [users, setUsers] = useState({});

  useEffect(() => {
    fetch("http://localhost:8000/users/")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch users");
        }
        return res.json();
      })
      .then((data) => setUsers(data))
      .catch((err) => console.error("Error fetching users:", err));
  }, []);

  return (
    <div>
      <h2>Registered Users</h2>
      {Object.keys(users).length === 0 ? (
        <p>No users found.</p>
      ) : (
        <ul>
          {Object.entries(users).map(([id, user]) => (
            <li key={id}>
              <strong>{user.name}</strong> — ZIP: {user.zip_code}, Timezone:{" "}
              {user.timezone}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default UserList;