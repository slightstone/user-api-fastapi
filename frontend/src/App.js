import React from "react";
import "./App.css";
import UserForm from "./UserForm";
import UserList from "./UserList";

function App() {
  return (
    <div className="App">
      <h1 style={{ textAlign: "center", marginTop: "30px" }}>
        User API Demo
      </h1>
      <UserForm />
      <UserList />
    </div>
  );
}

export default App;