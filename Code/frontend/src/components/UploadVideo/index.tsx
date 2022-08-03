import React, { useState, useRef } from "react";
import styled from "styled-components";
import { IconButton, Tooltip } from "@mui/material";
import { Close } from "@mui/icons-material";
import SVG_File from "components/SVG_Component";

const UploadDiv = styled.div<{ source: any }>`
  height: 300px;
  max-width: 65%;
  border: 1px solid black;
  background-color: white;
  margin: 0 auto;
  padding-bottom: 10px;
  display: ${({ source }) => (source.length > 0 ? "none" : "flex")};
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-weight: bold;
  &:hover {
    cursor: pointer;
  }

  @media screen and (max-width: 1280px) {
    max-width: 75%;
  }

  @media screen and (max-width: 1050px) {
    max-width: 85%;
  }

  @media screen and (max-width: 940px) {
    max-width: 100%;
  }
`;

const Container = styled.div`
  height: 300px;
  max-width: 100%;
`;

function UploadVideo({ setVideo }: { setVideo: any }) {
  const inputRef = useRef() as any;

  const [source, setSource] = useState("");
  const handleFileChange = (event: any) => {
    setVideo(event.target.files[0]);
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    setSource(url);
  };

  const handleChoose = (event: any) => {
    inputRef.current.click();
  };

  return (
    <div>
      <UploadDiv source={source} onClick={handleChoose}>
        <div
          style={{
            display: "none",
          }}
        >
          <input
            ref={inputRef}
            className="VideoInput_input"
            type="file"
            id="file"
            name="file"
            onChange={handleFileChange}
            accept=".mov,.mp4"
          />
        </div>
        <SVG_File filename="import" />
        Click here to upload
      </UploadDiv>
      {source && (
        <Container>
          <IconButton
            sx={{
              float: "right",
            }}
            onClick={() => {
              setSource("");
            }}
          >
            <Tooltip title="Remove">
              <Close
                sx={{
                  color: "black",
                }}
                fontSize="small"
              />
            </Tooltip>
          </IconButton>
          <video width="100%" height="88%" controls src={source} />
        </Container>
      )}
    </div>
  );
}

export default UploadVideo;
