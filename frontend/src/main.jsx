
// import { StrictMode } from "react";
// import { createRoot } from "react-dom/client";
// import App from "./App.jsx";
// import "./style.css";

// createRoot(document.getElementById("root")).render(
//   <StrictMode>
//     <App />
//   </StrictMode>
// );

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  ConversationProvider,
} from "@elevenlabs/react";

import App from "./App.jsx";
import "./style.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ConversationProvider>
      <App />
    </ConversationProvider>
  </StrictMode>
);
