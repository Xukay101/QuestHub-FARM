import { useState, useEffect } from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Input,
  Checkbox,
  Button,
} from "@material-tailwind/react";
import { useNavigate } from "react-router-dom";
import { isTokenExpired } from "../utils/tokenUtils";

export function LoginCard() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();

  // Login verify
  useEffect(() => {
    const userDataString = localStorage.getItem('userData') || sessionStorage.getItem('userData');
    if (userDataString) {
      const userData = JSON.parse(userDataString);
      const token = userData.access_token;
      
      if (token && !isTokenExpired(token)) {
        navigate('/');
      }
    }
  }, [navigate]);

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        body: formData,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      if (response.ok) {
        const data = await response.json();

        if (data && data.access_token && data.refresh_token) {
          const userData = {
            access_token: data.access_token,
            refresh_token: data.access_token,
          };

          if (rememberMe) {
            localStorage.setItem('userData', JSON.stringify(userData));
            localStorage.setItem('rememberMe', 'true');
          } else {
            sessionStorage.setItem('userData', JSON.stringify(userData));
            localStorage.removeItem('rememberMe');
          }

          navigate('/');

        } else {
          console.error("Datos de tokens no válidos en la respuesta.");
        }
      } else {
        console.error("Inicio de sesión fallido");
      }
    } catch (error) {
      console.error("Error al realizar la solicitud:", error);
    }
  };

  return (
    <Card className="w-96">
      <CardHeader
        variant="filling"
        className="mb-4 grid h-28 place-items-center bg-color3"
      >
        <Typography variant="h3" color="white">
          Sign In
        </Typography>
      </CardHeader>
      <CardBody className="flex flex-col gap-4">
        <Input label="Username" size="lg" onChange={(e) => setUsername(e.target.value)} value={username} />
        <Input type="password" label="Password" size="lg" className="border-gray-200" onChange={(e) => setPassword(e.target.value)} value={password} />
        <div className="-ml-2.5">
          <Checkbox label="Remember Me" onChange={() => setRememberMe(!rememberMe)} checked={rememberMe} />
        </div>
      </CardBody>
      <CardFooter className="pt-0">
        <Button variant="gradient" fullWidth onClick={handleLogin}>
          Sign In
        </Button>
        <Typography variant="small" className="mt-6 flex justify-center">
          Don&apos;t have an account?
          <Typography
            as="a"
            href="#signup"
            variant="small"
            color="blue-gray"
            className="ml-1 font-bold"
          >
            Sign up
          </Typography>
        </Typography>
      </CardFooter>
    </Card>
  );
}