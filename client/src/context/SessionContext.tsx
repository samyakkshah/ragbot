import React, { createContext, useContext, useEffect, useState } from "react";
import { useAuth } from "./AuthContext";
import { SessionOut } from "../utils/types";
import { initSession } from "../utils/api";

interface SessionContextType {
  session: SessionOut | null;
  loading: boolean;
  error: string | null;
}

const SessionContext = createContext<SessionContextType>({
  session: null,
  loading: true,
  error: null,
});

export const useSession = () => useContext(SessionContext);

export const SessionProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [session, setSession] = useState<SessionOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { auth } = useAuth();

  useEffect(() => {
    let cancelled = false;
    if (session) return;
    async function init() {
      try {
        const s = await initSession();
        if (!cancelled) setSession(s);
      } catch (err) {
        console.error("[Session Init Error]", err);
        if (!cancelled) setError("Failed to initialize session");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    init();
    return () => {
      cancelled = true;
    };
  }, [auth?.token]);

  return (
    <SessionContext.Provider value={{ session, loading, error }}>
      {children}
    </SessionContext.Provider>
  );
};
