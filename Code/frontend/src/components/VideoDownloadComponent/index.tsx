import * as React from "react";
import styled from "styled-components";
import { Button } from "@mui/material";
import loadingGif from "../../assets/loading.gif";

const DownloadDiv = styled.div<{ res: string }>`
  display: ${({ res }) => (res.length > 0 ? "none" : "block")};
  margin: 0 auto;
  height: 300px;
  min-width: 65%;
  border: 1px solid black;
  background-color: white;
  margin: 0 auto;

  @media screen and (max-width: 1280px) {
    min-width: 75%;
  }

  @media screen and (max-width: 1050px) {
    min-width: 85%;
  }

  @media screen and (max-width: 940px) {
    min-width: 100%;
    margin-left: 20px;
  }

  @media screen and (max-width: 768px) {
    min-width: 100%;
    margin-left: 0px;
  }
`;

function VideoDownloadComponent({
  loading,
  result,
}: {
  loading: boolean;
  result: string;
}) {
  const download = (e: any) => {
    fetch(result, {
      method: "GET",
      headers: {},
    })
      .then((response) => {
        response.arrayBuffer().then(function (buffer) {
          const url = window.URL.createObjectURL(new Blob([buffer]));
          const link = document.createElement("a");
          link.href = url;
          link.download = "image.png";
          link.click();
        });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div className="d-flex flex-column justify-content-center">
      <DownloadDiv res={result}>
        {loading && (
          <img
            src={loadingGif}
            height="298px"
            width="300px"
            alt="Computer man"
          />
        )}
      </DownloadDiv>
      {result.length > 0 && (
        <video width="100%" height="88%" controls src={result} />
      )}
      <div style={{ width: "300px", margin: "0 auto" }}>
        <Button
          variant="contained"
          className="mt-2 action-btn"
          onClick={download}
        >
          Download
        </Button>
      </div>
    </div>
  );
}

export default VideoDownloadComponent;
