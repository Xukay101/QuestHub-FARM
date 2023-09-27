import { Card } from "@material-tailwind/react"
import { ListModules } from "../components/ListModules"
import { NavbarDefault } from "../components/Navbar"
import RecentQuestions from "../components/RecentQuestions"

function Homepage() {
  return (
    <div>
      <header className="">
        <NavbarDefault />
      </header>

      <div className="my-5 w-full flex flex-col space-y-4 md:flex-row md:space-x-4 md:space-y-0">
        <main className="md:w-2/3 lg:w-3/4 px-5 md:px-0 md:pl-5 md:py-5">
          <Card className="w-full overflow-hidden rounded-md">
            <RecentQuestions />
          </Card>
        </main>
        <aside className="md:w-1/3 lg:w-1/4 px-5 md:py-5 md:pl-0">
          <ListModules />
        </aside>
      </div>

    </div>
  )
}

export default Homepage