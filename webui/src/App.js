import "./App.css";

import React from "react";
import { LightTheme } from "./components/Themes";
import { Main } from "./components/Main";
import { Provider } from "react-redux";
import { SnackbarProvider } from "notistack";

import store from "./redux/store";
import ApiService from "./services/api";
import { initStreamSensorReader } from "./redux/repositories/StreamSensorReader";
import { apiHosts } from "./configs";

// set base host to the axios instance
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
          autoHideDuration={ 2000 }
        >
          <Main />
        </SnackbarProvider>
      </Provider>
    </LightTheme>
  );
};

export default App;
