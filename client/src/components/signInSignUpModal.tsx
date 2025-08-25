import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Button } from "./ui/Button";

const AuthModal: React.FC = () => {
  const { isOpen, closeAuth, login, signup } = useAuth();
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  if (!isOpen) return null;

  const submit = async () => {
    const ok =
      mode === "login"
        ? await login(email, password)
        : await signup(email, password);
    if (!ok) alert(`${mode} failed`);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-xl bg-bg-base p-6 shadow-lg">
        <h2 className="mb-4 text-xl font-semibold">
          {mode === "login" ? "Log in" : "Sign up"}
        </h2>

        <input
          type="email"
          className="mb-2 w-full rounded-md border border-border-base p-2 bg-bg-base"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="mb-4 w-full rounded-md border border-border-base p-2 bg-bg-base"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <Button onClick={submit} className="w-full p-2 rounded-sm">
          {mode === "login" ? "Log in" : "Create account"}
        </Button>

        <button
          onClick={() => setMode(mode === "login" ? "signup" : "login")}
          className="w-full text-sm text-text-muted"
        >
          {mode === "login"
            ? "Need an account? Sign up"
            : "Have an account? Log in"}
        </button>

        <button
          onClick={closeAuth}
          className="mt-4 w-full text-sm text-red-500"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default AuthModal;
