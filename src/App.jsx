import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Recommendations from "./pages/Recommendations";

function App() {
  return (
    <main className="main-content">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recommendations" element={<Recommendations />} />
      </Routes>
    </main>
  );
}

export default App;
