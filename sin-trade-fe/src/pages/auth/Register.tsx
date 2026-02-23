import { useEffect, useState } from "react";
import Input from "../../components/Input";
import Button from "../../components/AsyncButton";
import GenericModal from "../../components/GenericModal";
import { signup } from "../../api/Auth";
import { useAuth } from "../../context/useAuth";
import { useUI } from "../../context/useUI";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [avatarUrl, setAvatarUrl] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  const { loginUser, logoutUser } = useAuth();
  const {
    isLoading,
    isError,
    setIsLoading,
    setIsError,
    isSuccess,
    setIsSuccess,
    navigate,
  } = useUI();

  const isFormValid = email.trim() !== "" && 
    firstName.trim() !== "" && 
    lastName.trim() !== "" && 
    password.trim() !== "" && 
    confirmPassword.trim() !== "";

  const handleRegister = () => {
    if (password !== confirmPassword) {
      setPasswordError("Passwords do not match");
      return;
    }
    setPasswordError("");

    void signup({
      email,
      password,
      firstName,
      lastName,
      username,
      avatarUrl: avatarUrl || undefined,
      setIsLoading,
      loginUser,
      
      logoutUser,
      setIsError,
      setIsSuccess,
    });
  };

  useEffect(() => {
    if (isSuccess) {
      setShowSuccessModal(true);
    }
  }, [isSuccess]);

  const handleModalClose = () => {
    setShowSuccessModal(false);
    setIsError(false);
    setIsSuccess(false);
    void navigate("/login");
  };

  return (
    <div className="flex flex-col h-screen justify-center items-center">
      <div className="flex flex-col gap-4 items-center justify-center self-center">
        <Input
          label="Email"
          placeholder={email}
          type="email"
          name="email"
          id="email"
          onChange={(e) => setEmail(e.target.value)}
        />
        <Input
          label="First Name"
          placeholder={firstName}
          type="text"
          name="firstName"
          id="firstName"
          onChange={(e) => setFirstName(e.target.value)}
        />
        <Input
          label="Last Name"
          placeholder={lastName}
          type="text"
          name="lastName"
          id="lastName"
          onChange={(e) => setLastName(e.target.value)}
        />
        <Input
          label="Username"
          placeholder={username}
          type="text"
          name="username"
          id="username"
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          label="Avatar URL (optional)"
          placeholder="https://example.com/avatar.jpg"
          type="text"
          name="avatarUrl"
          id="avatarUrl"
          onChange={(e) => setAvatarUrl(e.target.value)}
        />
        <Input
          label="Password"
          placeholder="Enter password"
          type="password"
          name="password"
          id="password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <Input
          label="Confirm Password"
          placeholder="Confirm password"
          type="password"
          name="confirmPassword"
          id="confirmPassword"
          onChange={(e) => setConfirmPassword(e.target.value)}
        />

        {passwordError && (
          <div className="text-red-500 text-sm">{passwordError}</div>
        )}

        <Button
          text="Register"
          onClick={handleRegister}
          disabled={!isFormValid}
          isLoading={isLoading}
          isError={isError}
        />
        <Button
          text="Back to Login"
          onClick={() => void navigate("/login")}
          disabled={false}
          isLoading={false}
          isError={false}
        />

        {isError ? (
          <div>Registration failed. Please try again.</div>
        ) : (
          <></>
        )}
      </div>

      <GenericModal   
        open={showSuccessModal}
        setOpen={setShowSuccessModal}
        title="Registration Successful!"
        confirmFunction={() => {
          handleModalClose();
        }}
        confirmText="Login"
        confirmDisabled={false}
        isLoading={false}
        isError={false}
        icon={
          <div className="text-green-500 text-2xl">✓</div>
        }
        child={
          <div className="text-center py-4">
            <p className="text-gray-600">
              Please check your email for the verification link, and then login.
            </p>
          </div>
        }
      />
    </div>
  );
}
