import { useState } from 'react';
import { Routes, Route,BrowserRouter} from 'react-router-dom';
import Login from './Login.jsx';
import Process from './Process.jsx';
import Signup from './Signup.jsx';

export default function App() {
  return(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />}></Route>
      <Route path="/signup" element={<Signup />}></Route>
      <Route path="/process" element={<Process />}></Route>

    </Routes>
  </BrowserRouter>
  );
}