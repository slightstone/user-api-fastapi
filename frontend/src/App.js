import React from "react";
import "./App.css";
import UserList from "./UserList";
import UserForm from "./UserForm"; // ✅ Add this

function App() {
  return (
    <div className="App">
      <h1>User API Demo</h1>
      <UserForm /> {/* ✅ Add this */}
      <UserList />
    </div>
  );
}

export default App;