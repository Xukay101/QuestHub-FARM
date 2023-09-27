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
 
export function RegisterCard() {
  return (
    <Card className="w-96">
      <CardHeader
        variant="filling"
        className="mb-4 grid h-28 place-items-center bg-color2"
      >
        <Typography variant="h3" color="white">
          Sign Up
        </Typography>
      </CardHeader>
      <CardBody className="flex flex-col gap-4">
        <Input label="Username" size="lg" />
        <Input label="Email" size="lg" />
        <Input type="password" label="Password" size="lg" className="border-gray-200" />
      </CardBody>
      <CardFooter className="pt-0">
        <Button variant="gradient" fullWidth>
          Sign up 
        </Button>
        <Typography variant="small" className="mt-6 flex justify-center">
          Do you already have an account?
          <Typography
            as="a"
            href="#signup"
            variant="small"
            color="blue-gray"
            className="ml-1 font-bold"
          >
            Sign in 
          </Typography>
        </Typography>
      </CardFooter>
    </Card>
  );
}