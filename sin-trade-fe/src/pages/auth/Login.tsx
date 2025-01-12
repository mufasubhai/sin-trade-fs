import { useEffect, useState } from "react";
import Input from "../../components/Input";
import Button from "../../components/AsyncButton";
import { login } from "../../api/Auth";
import { useAuth } from "../../context/useAuth";
import { useNavigate } from "react-router";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  // here we're pulling
  const { loginUser, logoutUser } = useAuth();
  const navigate = useNavigate();




  const handleLogin = () => {
    console.log("handleLogin");
    console.log(email, password, setIsLoading, loginUser, logoutUser, setIsError, setIsSuccess);
    void login({
      email: email,
      password: password,
      setIsLoading: setIsLoading,
      loginUser: loginUser,
      logoutUser: logoutUser,
      setIsError: setIsError,
      setIsSuccess: setIsSuccess,
    });
  };

  useEffect(() => {
    if (isSuccess) {
      void navigate("/dashboard");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSuccess]);

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
        <Button
          text="Login"
          onClick={handleLogin}
          disabled={false}
          isLoading={isLoading}
          isError={isError}
        />
      </div>
    </div>
  );
}
