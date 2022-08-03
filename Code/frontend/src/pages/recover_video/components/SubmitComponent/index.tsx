import React, { useState } from "react";
import axios from "axios";
import UploadVideo from "components/UploadVideo";

import {
  Button,
  TextField,
  InputAdornment,
  IconButton,
  Tooltip,
} from "@mui/material";

import {
  VisibilityOutlined,
  VisibilityOffOutlined,
  InfoOutlined,
} from "@mui/icons-material";

import "../ComponentStyles/style.css";

function SubmitComponent() {
  const [video, setVideo] = useState<any>(null);
  // const [showPassword, setShowPassword] = useState(false);
  // const handleClickShowPassword = () => setShowPassword(!showPassword);
  // const handleMouseDownPassword = () => setShowPassword(!showPassword);

  const handleSubmit = (event: any) => {
    if (!!video) {
      event.preventDefault();
      console.log("BEFORE REQUEST");
      // setLoading(true);
      console.log(video);
      const formData = new FormData();
      formData.append("file", video);
      axios({
        method: "post",
        url: "http://127.0.0.1:8000/video/watermark/",
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      })
        .then((res) => {
          console.log("AFTER REQUEST");
          // setLoading(false);
          console.log(res);
          // setResult(res.data);
        })
        .catch((err) => {
          console.log(err);
          // setLoading(false);
        });
    }
  };

  // const infoString =
  //   "This key will be used to authenticate your file. Please make sure you choose a strong key.";

  return (
    <>
      <form encType="multipart/form-data" method="post">
        <UploadVideo setVideo={setVideo} />
        <div className="input-container">
          {/* <TextField
          label="Key"
          variant="outlined"
          type={showPassword ? "text" : "password"}
          sx={{
            width: "300px",
          }}
          // onChange={someChangeHandler}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                >
                  {showPassword ? (
                    <VisibilityOutlined />
                  ) : (
                    <VisibilityOffOutlined />
                  )}
                </IconButton>
              </InputAdornment>
            ),
          }}
        /> */}
          <Button
            type="submit"
            variant="contained"
            onClick={handleSubmit}
            className="action-btn mt-2"
          >
            Submit
          </Button>

          {/* <Tooltip title={infoString} className="mt-2 ms-2">
          <InfoOutlined style={{ color: "rgba(0,0,0,.45)" }} />
        </Tooltip> */}
        </div>
      </form>
    </>
  );
}

export default SubmitComponent;
