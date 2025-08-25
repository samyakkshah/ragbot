import { SessionOut, IntroMessage, MessageResponse, RAGQuery } from "./types";

const BASE_URL = process.env.REACT_APP_API_URL;

async function safeFetch<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const res = await fetch(url, {
      ...options,
      credentials: "include",
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

export async function createOrResumeSession(): Promise<SessionOut> {
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
