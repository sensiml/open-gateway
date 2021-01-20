import React from "react";
import { lightBlue, deepOrange, red, blueGrey } from "@material-ui/core/colors";
import {
  useTheme,
  createMuiTheme,
  MuiThemeProvider
} from "@material-ui/core/styles";

const LightTheme = props => {
  const theme = useTheme();

  const currentTheme = createMuiTheme({
    palette: {
      primary: {
        light: lightBlue[600],
        main: lightBlue[800],
        dark: lightBlue[800],
        contrastText: theme.palette.getContrastText(lightBlue[800])
      },
      accent: {
        light: deepOrange[200],
        main: deepOrange[500],
        dark: deepOrange[800],
        contrastText: theme.palette.getContrastText(deepOrange[500])
      },
      secondary: {
        light: lightBlue[600],
        main: lightBlue[700],
        dark: lightBlue[800],
        contrastText: theme.palette.getContrastText(lightBlue[600])
      },
      notSelected: {
        light: blueGrey[500],
        main: blueGrey[700],
        dark: blueGrey[800],
        contrastText: theme.palette.getContrastText(blueGrey[600])
      },
      error: {
        light: red[200],
        main: red[500],
        dark: red[800],
        contrastText: theme.palette.getContrastText(red[500])
      }
    }
  });

  return (
    <MuiThemeProvider theme={currentTheme}>{props.children}</MuiThemeProvider>
  );
};

export default LightTheme;
