import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./components/Home";
import History from "./components/History";

function App() {
  return (
    <Router>
      <nav className="bg-gray-900 text-white px-6 py-4 flex gap-6">
        <Link to="/" className="hover:text-purple-400 font-bold">Home</Link>
        <Link to="/history" className="hover:text-purple-400 font-bold">History</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </Router>
  );
}

export default App;