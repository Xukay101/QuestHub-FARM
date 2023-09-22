import { NavbarDefault } from "../components/Navbar"
import { LoginCard } from "../components/LoginCard"

function Loginpage() {


  return (
    <div>
      <header className="">
        <NavbarDefault />
      </header>

      <main className="flex justify-center items-center mt-20 m-5">
        <LoginCard />
      </main>
      
    </div>
  )
}

export default Loginpage