import { NavbarDefault } from "../components/Navbar"
import { RegisterCard } from "../components/RegisterCard"

function Registerpage() {

  return (
    <div>
      <header className="">
        <NavbarDefault />
      </header>

      <main className="flex justify-center items-center mt-20 m-5">
        <RegisterCard />
      </main>

    </div>
  )
}

export default Registerpage