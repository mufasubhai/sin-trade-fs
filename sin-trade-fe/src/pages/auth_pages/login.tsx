import { useState } from "react";
import Input from "../../components/Input";
import Button from "../../components/AsyncButton";
import { login } from "../../api/Auth";




export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const handleLogin = () => {
    void login(email, password, setIsLoading, setIsError);
  }

  

  return (
    <div className="flex flex-col h-screen justify-center items-center">
        <div className="flex flex-col gap-4 items-center justify-center self-center">

      <Input
        label="Email"
        placeholder={email}
        type="email"
        name="email"
        id="email"
        onChange={(e) => {
            setEmail(e.target.value);
        }}
        />
      <Input
        label="Password"
        placeholder={password}
        type="password"
        name="password"
        id="email"
        onChange={(e) => {
            setPassword(e.target.value);
        }}
        />
        <Button text="Login" onClick={handleLogin} disabled={false} isLoading={isLoading} isError={isError} />
        </div>
    </div>
  );
}
