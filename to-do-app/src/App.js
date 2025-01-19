import "./App.css";
import { Route, Routes } from "react-router";
// import { useState } from "react";
import LoginPage from "./components/login";
import SignUpPage from "./components/signup";
import TaskForm from "./components/createTask";
import TaskList from "./components/listTask";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<LoginPage />}></Route>
        <Route path="/signup" element={<SignUpPage />}></Route>
        <Route path="/login" element={<LoginPage />}></Route>
        <Route path="/task/create" element={<TaskForm />}></Route>
        <Route path="/task/list" element={<TaskList />}></Route>
      </Routes>
    </>
  );
}

export default App;
