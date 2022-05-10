import React, { useState } from "react";
import { Box, Button, Typography } from "@material-ui/core";
import axios from "axios";

const UploadClassImagesJson = (props) => {
  const [errorMessage, setErrorMessage] = useState("");

  const handleFile = (event) => {
    const uploadedFile = event.target.files[0];
    const reader = new FileReader();

    reader.readAsText(uploadedFile);
    debugger;

    reader.onload = function () {
      console.log(reader.result);
      let json_data = {};
      try {
        json_data = JSON.parse(reader.result);
        axios
          .post(
            `${process.env.REACT_APP_API_URL}config-class-map-images-json`,
            json_data
          )
          .then((response) => {
            console.log(response.data);
            setErrorMessage("");
          })
          .catch((error) => {
            setErrorMessage("upload failed");
            console.log(error);
          });
      } catch {}
    };

    reader.onerror = function () {
      console.log(reader.error);
    };
  };
  return (
    <Box>
      <Button variant="contained" component="label">
        Upload Class Images JSON
        <input type="file" hidden onChange={handleFile} />
      </Button>
      <Typography> {errorMessage}</Typography>
    </Box>
  );
};

export default UploadClassImagesJson;
