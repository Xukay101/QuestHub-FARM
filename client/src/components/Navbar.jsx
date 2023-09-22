import React from "react";
import {
  Navbar,
  MobileNav,
  Typography,
  Button,
  IconButton,
} from "@material-tailwind/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { Searchbar } from "./Searchbar";
import { isAuthenticated } from "../utils/tokenUtils";
import ProfileMenu from "./ProfileMenu";

export function NavbarDefault() {
  const isLoggedIn = isAuthenticated()

  const [openNav, setOpenNav] = React.useState(false);

  React.useEffect(() => {
    window.addEventListener(
      "resize",
      () => window.innerWidth >= 960 && setOpenNav(false)
    );
  }, []);

  const navList = (
    <ul className="mb-4 mt-2 flex flex-col gap-2 lg:mb-0 lg:mt-0 lg:flex-row lg:items-center lg:gap-6">
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="/" className="flex items-center transition-transform hover:text-blue-500">
          Home
        </a>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center transition-transform hover:text-blue-500">
          About Us
        </a>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center transition-transform hover:text-blue-500">
          Blog
        </a>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center transition-transform hover:text-blue-500">
          Contact Us
        </a>
      </Typography>
    </ul>
  );

  return (
    <Navbar className="bg-cream shadow-none border-0 border-b-4 border-blue-800 text-black rounded-none py-2 px-4 lg:px-8 lg:py-4">
      <div className="flex items-center justify-between">

        <div className="flex items-center gap-4">
          <Typography
            as="a"
            href="/"
            className="mr-4 cursor-pointer py-1.5 font-bold"
          >
            Questhub
          </Typography>
          <div className="mr-4 hidden lg:block">{navList}</div>

        </div>

        <div className="hidden lg:inline-block">
          <Searchbar />
        </div>

        <IconButton
          variant="text"
          className="ml-auto mr-3 h-6 w-6 text-inherit hover:bg-transparent focus:bg-transparent active:bg-transparent lg:hidden"
          ripple={false}
          onClick={() => setOpenNav(!openNav)}
        >
          {openNav ? (
            <XMarkIcon className="h-6 w-6" strokeWidth={2} />
          ) : (
            <Bars3Icon className="h-6 w-6" strokeWidth={2} />
          )}
        </IconButton>

        <div className="flex items-center gap-4">

          {isLoggedIn ? (

            <>
              <div className="w-full flex items-end">
                <ProfileMenu />
              </div>
            </>

          ) : (

            <>
              <a href="/auth/login">
                <Button
                  variant="outlined"
                  size="sm"
                  ripple={true}
                  className="hidden lg:inline-block"
                  color="black"
                >
                  <span>LOG IN</span>
                </Button>
              </a><a href="/auth/register">
                <Button
                  variant="filled"
                  size="sm"
                  ripple={true}
                  className="hidden lg:inline-block"
                  color="black"
                >
                  <span>SIGN UP</span>
                </Button>
              </a>
            </>

          )}

        </div>

      </div>
      <MobileNav open={openNav}>

        {navList}

        <div className="w-full lg:hidden my-3">
          <Searchbar fullWidth />
        </div>

        {!isLoggedIn && (

          <>
            <div className="flex w-full flex-nowrap items-center gap-2 lg:hidden">
              <a href="/auth/login">
                <Button
                  fullWidth
                  variant="outlined"
                  size="sm"
                  ripple={true}
                  className="mb-2"
                  color="black"
                >
                  <span>LOG IN</span>
                </Button>
              </a>

              <a href="/auth/register">
                <Button
                  fullWidth
                  variant="filled"
                  size="sm"
                  ripple={true}
                  className="mb-2"
                  color="black"
                >
                  <span>SIGN UP</span>
                </Button>
              </a>
            </div>
          </>

        )}

      </MobileNav>
    </Navbar>
  );
}