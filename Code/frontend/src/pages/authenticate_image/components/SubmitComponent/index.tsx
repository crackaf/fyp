import React, { useState } from "react";
import axios from "axios";
import UploadFile from "components/Upload";
import { Button } from "@mui/material";
import "../ComponentStyles/style.css";

function SubmitComponent({
  setLoading,
  setResult,
}: {
  setLoading: (loading: boolean) => void;
  setResult: (result: string) => void;
}) {
  const [images, setImages] = useState<any[]>([]);

  const handleSubmit = () => {
    if (images.length > 0) {
      console.log("BEFORE REQUEST");
      setLoading(true);
      // console.log(images[0]);
      const dataURI = images[0].dataURL;
      const imageData = dataURI.split(",")[1];
      axios
        .post("http://127.0.0.1:8000/image/authenticate/", {
          image: imageData,
        })
        .then((res) => {
          console.log("AFTER REQUEST");
          setLoading(false);
          console.log(res);
          setResult(res.data);
        })
        .catch((err) => {
          console.log(err);
          setLoading(false);
        });
    }
  };

  return (
    <>
      <UploadFile images={images} setImages={setImages} setResult={setResult} />
      <div className="input-container">
        <Button
          variant="contained"
          onClick={handleSubmit}
          className="action-btn mt-2"
        >
          Submit
        </Button>
      </div>
    </>
  );
}

export default SubmitComponent;
