import "./App.css";

import React from "react";
import { LightTheme } from "./components/Themes";
import { Main } from "./components/Main";
const App = () => {
  return (
    <LightTheme>
      <Main />
    </LightTheme>
  );
};

export default App;
