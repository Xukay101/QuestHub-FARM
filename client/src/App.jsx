import { BrowserRouter, Routes, Route } from "react-router-dom";

import Homepage from './pages/Home'
import Testpage from './pages/Test'
import Loginpage from "./pages/Login";
import Registerpage from "./pages/Register";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Homepage/>}/>
        <Route path="/test" element={<Testpage/>}/>

        <Route path="/auth">
          <Route path="login" element={<Loginpage />} />
          <Route path="register" element={<Registerpage />} />
        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App
