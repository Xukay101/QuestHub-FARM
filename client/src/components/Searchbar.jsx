import React from "react";
import { Input, Button } from "@material-tailwind/react";
 
export function Searchbar() {
  const [keywords, setKeywords] = React.useState("");
  const onChange = ({ target }) => setKeywords(target.value);
 
  return (
    <div className="relative flex w-full">
      <Input
        type="text"
        label="Search..."
        value={keywords}
        onChange={onChange}
        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 "
        containerProps={{
          className: "min-w-[350px]",
        }}
      />
      <Button
        size="sm"
        variant={keywords? "filled" : "outlined"}
        disabled={!keywords}
        className="!absolute right-1 top-1 rounded"
      >
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
</svg>

      </Button>
    </div>
  );
}