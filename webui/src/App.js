import "./App.css";

import React from "react";
import { LightTheme } from "./components/Themes";
import { Main } from "./components/Main";
import { Provider } from "react-redux";
import { SnackbarProvider } from "notistack";

import store from "./redux/store";
import { initStreamSensorReader } from "./redux/repositories/StreamSensorReader";

import ApiService from "./services/api";
import { apiHosts } from "./configs";

ApiService.init(apiHosts.baseHost);

// initialize StreamSensorReader for handle as entrypoint
initStreamSensorReader();

const App = () => {
  return (
    <LightTheme>
      <Provider store={store}>
        <SnackbarProvider
          anchorOrigin={{
            horizontal: "right",
            vertical: "top",
          }}
          autoHideDuration={2000}
        >
          <Main />
        </SnackbarProvider>
      </Provider>
    </LightTheme>
  );
};

export default App;
