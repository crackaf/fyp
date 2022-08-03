import React from "react";
import { ArrowRightOutlined } from "@mui/icons-material";
import { Button } from "@mui/material";
import { navbarDropdownButtons } from "constants/navbarDropdown";
import DropdownButton from "./components/Dropdown";
import "./nav_style.css";

function Navbar({ navBtnText }: { navBtnText?: string }) {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark navbar-style">
      <div className="container-fluid">
        <a className="navbar-brand sm-mx-auto" href="/">
          <div className="logo" />
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div
          className="collapse navbar-collapse fw-bold"
          id="navbarSupportedContent"
          style={{
            backgroundColor: "#06628a",
            width: "100%",
            padding: "10px",
            height: "80px",
          }}
        >
          <ul className="ms-auto navbar-nav">
            {navbarDropdownButtons.map((item, index) => (
              <li key={index} className="nav-item">
                <DropdownButton {...item} />
              </li>
            ))}
          </ul>
          {navBtnText && (
            <Button
              variant="contained"
              className="nav-btn"
              size="medium"
              sx={{
                margin: "10px",
                background: "rgba(255, 255, 255, 0.3)",
                fontWeight: "600",
                fontSize: "18px",
                border: "1px solid rgba(255, 255, 255, 0.3)",
                "&:hover": {
                  color: "white",
                },
              }}
              href="/watermark-image"
            >
              {navBtnText}
              <ArrowRightOutlined fontSize="medium" />
            </Button>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
