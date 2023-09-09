import { BrowserRouter, Routes, Route } from "react-router-dom";

import Homepage from './pages/Homepage'
import Testpage from './pages/Testpage'

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Homepage/>}/>
        <Route path="/test" element={<Testpage/>}/>

      </Routes>
    </BrowserRouter>
  );
}

export default App
