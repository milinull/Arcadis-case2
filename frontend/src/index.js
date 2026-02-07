import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";

import "assets/plugins/nucleo/css/nucleo.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/scss/arcadis-case.scss";

import Case2Layout from "layouts/Case2.js";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/page/*" element={<Case2Layout />} />
      <Route path="*" element={<Navigate to="/page/index" replace />} />
    </Routes>
  </BrowserRouter>,
);
