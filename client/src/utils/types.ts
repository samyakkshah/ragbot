export type Role = "user" | "finbot";

// Session
export interface SessionOut {
  id: string;
  created_at: string;
}

// Intro message
export interface IntroMessage {
  role: "finbot";
  content: string;
}

// Chat messages
export interface MessageResponse {
  id: string;
  session_id: string;
  role: Role;
  content: string;
  created_at: string;
}

// RAG query
export interface RAGQuery {
  session_id: string;
  message: string;
}
