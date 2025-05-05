// this is going to be a flexible input component that can be used in the login page and the register page
import { useState } from "react";

export default function Input({
  label,
  placeholder,
  type,
  name,
  id,
  onChange,
  onValidation = () => {
    return true;
  },
}: {
  label: string;
  placeholder: string;
  type: string;
  name: string;
  id: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onValidation?: (value: string) => boolean;
  //   className: string;
}) {
  const [valid, setIsValid] = useState(true);

  if (onValidation === undefined) {
    onValidation = () => {
      return true;
    };
  }

  return (
    <div className="flex flex-col ">
      <label htmlFor={id} className="block text-sm/6 font-medium text-gray-900">
        {label}
      </label>
      <div className="mt-2">
        <input
          id={id}
          name={name}
          type={type}
          placeholder={placeholder}
          className={
            !valid
              ? "col-start-1 row-start-1 block w-full rounded-md bg-white py-1.5 pl-3 pr-10 text-base text-red-900 outline outline-1 -outline-offset-1 outline-red-300 placeholder:text-red-300 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-red-600 sm:pr-9 sm:text-sm/6"
              : "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
          }
          onChange={(e) => {
            onChange(e);
            setIsValid(onValidation(e.target.value));
          }}
          aria-invalid={!valid ? "true" : "false"}
          aria-describedby={!valid ? `${id}-error` : ""}
        />
      </div>
    </div>
  );
}
