import React, { createContext, useContext, useMemo, useState } from "react";
import {
  login as userLogin,
  signup as userSignup,
  logout as userLogout,
  setAuthToken,
} from "../utils/api";

type AuthState = {
  token: string | null;
  userId: string | null;
  email: string | null;
};

type AuthContextType = {
  auth: AuthState;
  // modal controls
  isOpen: boolean;
  openAuth: () => void;
  closeAuth: () => void;
  // actions
  login: (email: string, password: string) => Promise<boolean>;
  signup: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);
export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within <AuthProvider>");
  return ctx;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [auth, setAuth] = useState<AuthState>(() => ({
    token: localStorage.getItem("jwt_user_token"),
    userId: localStorage.getItem("user_id"),
    email: localStorage.getItem("email"),
  }));
  const [isOpen, setIsOpen] = useState(false);

  const openAuth = () => setIsOpen(true);
  const closeAuth = () => setIsOpen(false);

  const login = async (email: string, password: string) => {
    const res = await userLogin(email, password);
    if (!res?.jwt_user_token) return false;
    setAuthToken(res.jwt_user_token);
    localStorage.setItem("user_id", res.user_id || "");
    localStorage.setItem("email", email);
    setAuth({ token: res.jwt_user_token, userId: res.user_id || null, email });
    closeAuth();
    return true;
  };

  const signup = async (email: string, password: string) => {
    const res = await userSignup(email, password);
    if (!res) return false;

    if (res.message) {
      alert(res.message);
      closeAuth();
      return true;
    }
    return false;
  };

  const logout = async () => {
    await userLogout();
    setAuthToken(null);
    localStorage.removeItem("user_id");
    localStorage.removeItem("email");
    setAuth({ token: null, userId: null, email: null });
  };

  const value = useMemo(
    () => ({ auth, isOpen, openAuth, closeAuth, login, signup, logout }),
    [auth, isOpen]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
