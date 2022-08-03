import * as React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import WatermarkImage from "./pages/watermark_image";
import WatermarkVideo from "./pages/watermark_video";
import Authenticate_Image from "pages/authenticate_image";
import Authenticate_Video from "pages/authenticate_video";
import Recover_Image from "pages/recover_image";
import Recover_Video from "pages/recover_video";

// markup
const App = () => {
  return (
    <div style={{ backgroundColor: "#ecf3fc" }}>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/watermark-image" element={<WatermarkImage />} />
          <Route path="/watermark-video" element={<WatermarkVideo />} />
          <Route path="/authenticate-image" element={<Authenticate_Image />} />
          <Route path="/authenticate-video" element={<Authenticate_Video />} />
          <Route path="/recover-image" element={<Recover_Image />} />
          <Route path="/recover-video" element={<Recover_Video />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
