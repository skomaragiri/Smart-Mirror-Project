import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/tauri";
import "./App.css";
import Clock from "./Clock";

function App() {
  return (
      <div className="font-digital">
        <Clock /> 
      </div>

  );
}

export default App;
