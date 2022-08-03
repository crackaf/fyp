import React from "react";
import { Button } from "@mui/material";
import "./footer_style.css";

const NavigationData = ["Features", "About Us", "Get Started"];
const FeatureData = [
  "Watermarking",
  "Tampering Detection",
  "Multimedia Recovery",
];

function Footer() {
  return (
    <div className="footer">
      <div className="footer-container">
        <div className="footer-col">
          <div className="footer-title">Navigation</div>
          {NavigationData.map((item) => {
            return (
              <Button
                className="footer-item"
                sx={{
                  color: "white",
                  "&:hover": {
                    color: "black",
                  },
                }}
                key={item}
              >
                {item}
              </Button>
            );
          })}
        </div>
        <div className="footer-col">
          <div className="footer-title">Features</div>
          {FeatureData.map((item) => {
            return (
              <Button
                className="footer-item"
                sx={{
                  color: "white",
                  "&:hover": {
                    color: "black",
                  },
                }}
                key={item}
              >
                {item}
              </Button>
            );
          })}
        </div>
      </div>
      <span className="footer-span">
        <Button
          sx={{
            fontSize: "18px",
            color: "white",
            marginTop: "-5px",
            "&:hover": {
              color: "black",
            },
          }}
        >
          hMark
        </Button>{" "}
        Developed by Team Alpha
      </span>
    </div>
  );
}

export default Footer;
