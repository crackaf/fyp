import React, { useState } from "react";
import styled from "styled-components";
import Navbar from "../../components/Navbar";
import HeaderBreadcrumb from "../../components/HeaderBreadcrumb";
import SubmitComponent from "./components/SubmitComponent";
import DownloadComponent from "components/DownloadComponent";
import Footer from "../../components/Footer";

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

const A = styled.a`
  color: blue;
  font-weight: bold;
  text-decoration: none;
  :hover {
    text-decoration: underline;
    cursor: pointer;
  }
`;

function Recover_Image() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const breadcrumb = [
    { name: "Home", href: "/" },
    { name: "Recover Image", href: "/recover-image" },
  ];
  return (
    <>
      <Navbar />
      <HeaderBreadcrumb breadcrumbItems={breadcrumb} />
      <BodyDiv>
        <Title>Upload Your Watermarked Image</Title>
        <P>Most image types are supported.</P>
        <P>
          <A href="/recover-video">Click Here</A> to Recover video
        </P>

        <div className="container">
          <div className="row justify-content-between">
            <div
              className="col-md-6 col-sm-12 mb-4 mb-md-0"
              style={{
                padding: 0,
              }}
            >
              <SubmitComponent setLoading={setLoading} setResult={setResult} />
            </div>
            <div
              className="col-md-6 col-sm-12 mb-4 mb-md-0"
              style={{
                padding: 0,
              }}
            >
              <DownloadComponent loading={loading} result={result} />
            </div>
          </div>
        </div>
        <P>...or drag & drop files files in the upload box.</P>
      </BodyDiv>
      <Footer />
    </>
  );
}

export default Recover_Image;
