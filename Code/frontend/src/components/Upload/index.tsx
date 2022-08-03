import React, { useState } from "react";
import styled from "styled-components";
import ImageUploading, { ImageListType } from "react-images-uploading";
import { IconButton, Tooltip } from "@mui/material";
import { DeleteOutline } from "@mui/icons-material";
import SVG_File from "components/SVG_Component";

const UploadDiv = styled.div<{ isDragging: boolean; images: any }>`
  height: 300px;
  max-width: 65%;
  border: ${({ isDragging }) =>
    isDragging ? "1px dashed red" : "1px solid black"};
  margin: 0 auto;
  padding-bottom: 10px;
  display: ${({ images }) => (images.length > 0 ? "none" : "flex")};
  justify-content: center;
  align-items: center;
  background-color: white;
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

const ImageUpload = styled.div`
  display: none;
  position: absolute;
  top: 42%;
  left: 45%;
  border-radius: 50%;
  height: 50px;
  width: 50px;
  background-color: #00000070;
  z-index: 100;
`;

const ImageDiv = styled.img`
  height: 300px;
  max-width: 100%;
  z-index: 50;
`;

const Container = styled.div`
  position: relative;
  height: 300px;
  max-width: 100%;
  &:hover ${ImageDiv} {
    opacity: 0.5;
  }
  &:hover ${ImageUpload} {
    display: block;
  }
`;

function UploadImage({
  images,
  setImages,
  setResult,
}: {
  images: any;
  setImages: any;
  setResult?: (result: string) => void;
}) {
  // const [images, setImages] = useState([]);

  const onChange = (
    imageList: ImageListType,
    addUpdateIndex: number[] | undefined
  ) => {
    // data for submit
    // console.log(imageList, addUpdateIndex);
    setImages(imageList as never[]);
  };
  return (
    <div className="App">
      <ImageUploading multiple value={images} onChange={onChange}>
        {({
          imageList,
          onImageUpload,
          onImageRemove,
          isDragging,
          dragProps,
        }) => (
          // write your building UI
          <div className="upload__image-wrapper">
            {imageList.map((image, index) => (
              <Container key={index}>
                <ImageDiv
                  src={image.dataURL}
                  alt="image"
                  className="image-item"
                />
                <ImageUpload>
                  <IconButton
                    onClick={() => {
                      onImageRemove(index);
                      if (!!setResult) setResult("");
                    }}
                  >
                    <Tooltip title="Remove">
                      <DeleteOutline
                        sx={{
                          color: "white",
                        }}
                        fontSize="large"
                      />
                    </Tooltip>
                  </IconButton>
                </ImageUpload>
              </Container>
            ))}
            <UploadDiv
              isDragging={isDragging}
              images={images}
              onClick={() => {
                onImageUpload();
              }}
              {...dragProps}
            >
              <SVG_File filename="import" />
              Click or Drop here
            </UploadDiv>
          </div>
        )}
      </ImageUploading>
    </div>
  );
}

export default UploadImage;
