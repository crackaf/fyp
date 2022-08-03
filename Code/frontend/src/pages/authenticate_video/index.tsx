import React, { useState } from "react";
import styled from "styled-components";
import Navbar from "components/Navbar";
import HeaderBreadcrumb from "components/HeaderBreadcrumb";
import SubmitComponent from "./components/SubmitComponent";
import VideoDownloadComponent from "components/VideoDownloadComponent";
import Footer from "components/Footer";

const BodyDiv = styled.div<{ height?: string }>`
  background-color: "#ecf3fc";
  width: 100%;
  height: fit-content;
  text-align: center;
  padding: 2% 10% 10% 10%;
  color: #4a5568;
`;

const Title = styled.div`
  font-weight: 600;
  font-size: 34px;
`;

const P = styled.p<{ fontWeight?: string; fontSize?: string }>`
  font-weight: ${({ fontWeight }) => fontWeight ?? "normal"};
  font-size: ${({ fontWeight }) => fontWeight ?? "18px"}; ;
`;

function Authenticate_Video() {
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const breadcrumb = [
    { name: "Home", href: "/" },
    { name: "Watermark Video", href: "/watermark-video" },
  ];
  return (
    <>
      <Navbar />
      <HeaderBreadcrumb breadcrumbItems={breadcrumb} />
      <BodyDiv>
        <Title>Upload Your Video</Title>
        <P>Most video types are supported.</P>

        <div className="container">
          <div className="row">
            <div
              className="col-md-6 col-sm-12 mb-4 mb-md-0"
              style={{
                padding: "0",
              }}
            >
              <SubmitComponent />
            </div>
            <div
              className="col-md-6 col-sm-12 mb-4 mb-md-0"
              style={{
                padding: "0",
              }}
            >
              <VideoDownloadComponent loading={loading} result={result} />
            </div>
          </div>
        </div>
        <P>...or drag & drop files files in the upload box.</P>
      </BodyDiv>
      <Footer />
    </>
  );
}

export default Authenticate_Video;
