import { SessionOut, IntroMessage, MessageResponse, RAGQuery } from "./types";

const BASE_URL = process.env.REACT_APP_API_URL;

let AUTH_TOKEN: string | null = null;

export const setAuthToken = (token: string | null, persist = true) => {
  AUTH_TOKEN = token;
  if (persist) {
    if (token) localStorage.setItem("jwt_user_token", token);
    else localStorage.removeItem("jwt_user_token");
  }
};

const getAuthToken = () => {
  return AUTH_TOKEN;
};

(() => {
  const t = localStorage.getItem("jwt_user_token");
  if (t) AUTH_TOKEN = t;
})();

const authHeaders = (): HeadersInit => {
  const tkn = getAuthToken();
  return tkn ? { Authorization: `Bearer ${tkn}` } : {};
};

async function safeFetch<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const res = await fetch(url, {
      ...options,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
        ...(options?.headers || {}),
      },
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`HTTP ${res.status} - ${errorText}`);
    }

    return (await res.json()) as T;
  } catch (err) {
    console.error(`[API ERROR] ${url}`, err);
    throw err instanceof Error ? err : new Error("Unknown API error");
  }
}

export async function initSession(): Promise<SessionOut> {
  return safeFetch<SessionOut>(`${BASE_URL}/session/`, { method: "POST" });
}

export async function getChatHistory(
  sessionId: string
): Promise<MessageResponse[]> {
  return safeFetch<MessageResponse[]>(`${BASE_URL}/chat/${sessionId}`);
}

export async function getIntro(sessionId: string): Promise<IntroMessage> {
  return safeFetch<IntroMessage>(`${BASE_URL}/session/${sessionId}/intro`);
}

export async function deleteChat(sessionId: string): Promise<void> {
  await safeFetch<void>(`${BASE_URL}/chat/${sessionId}`, { method: "DELETE" });
}

export async function sendMessage(
  query: RAGQuery,
  onChunk: (text: string) => void
): Promise<void> {
  try {
    const res = await fetch(`${BASE_URL}/rag/query`, {
      method: "POST",
      body: JSON.stringify(query),
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });

    if (!res.ok || !res.body) {
      const errorText = await res.text();
      throw new Error(`Streaming failed: ${res.status} - ${errorText}`);
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      onChunk(decoder.decode(value, { stream: true }));
    }
  } catch (err) {
    console.error("[API STREAM ERROR]", err);
    throw err instanceof Error ? err : new Error("Streaming API error");
  }
}

export async function signup(email: string, password: string) {
  try {
    const res = await fetch(`${BASE_URL}/auth/signup`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw new Error("Signup failed");
    return await res.json();
  } catch (err) {
    console.error("Signup error:", err);
    return null;
  }
}

export async function login(email: string, password: string) {
  try {
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw new Error("Login failed");
    return await res.json();
  } catch (err) {
    console.error("Login error:", err);
    return null;
  }
}

export async function logout() {
  try {
    await fetch(`${BASE_URL}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
    return true;
  } catch (err) {
    console.error("Logout error:", err);
    return false;
  }
}
