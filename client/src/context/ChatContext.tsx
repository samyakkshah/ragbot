import React, { createContext, useContext, useState, useEffect } from "react";
import { useSession } from "./SessionContext";
import { getIntro, getChatHistory, sendMessage } from "../utils/api";
import { IntroMessage, MessageResponse, RAGQuery } from "../utils/types";

interface ChatContextType {
  messages: MessageResponse[];
  input: string;
  setInput: (val: string) => void;
  streaming: boolean;
  send: () => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const useChat = () => {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error("useChat must be used within ChatProvider");
  return ctx;
};

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { session } = useSession();
  const [messages, setMessages] = useState<MessageResponse[]>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);

  // Load intro + history
  useEffect(() => {
    if (!session) return;
    (async () => {
      try {
        const history = await getChatHistory(session.id);
        if (history.length > 0) {
          setMessages(history);
        } else {
          const intro: IntroMessage = await getIntro(session.id);
          setMessages([
            {
              id: "intro",
              session_id: session.id,
              role: intro.role,
              content: intro.content,
              created_at: new Date().toISOString(),
            },
          ]);
        }
      } catch (err) {
        console.error("[Chat Init Error]", err);
      }
    })();
  }, [session]);

  const send = async () => {
    if (!session || !input.trim()) return;
    const userMsg: MessageResponse = {
      id: crypto.randomUUID(),
      session_id: session.id,
      role: "user",
      content: input,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    setStreaming(true);
    let assistantMsg = "";
    const assistantId = crypto.randomUUID();

    try {
      await sendMessage(
        { session_id: session.id, message: userMsg.content } as RAGQuery,
        (chunk: string) => {
          assistantMsg += chunk;
          setMessages((prev) => [
            ...prev.filter((m) => m.id !== assistantId),
            {
              id: assistantId,
              session_id: session.id,
              role: "finbot",
              content: assistantMsg,
              created_at: new Date().toISOString(),
            },
          ]);
        }
      );
    } catch (err) {
      console.error("[Message Send Error]", err);
      setMessages((prev) => [
        ...prev,
        {
          id: assistantId,
          session_id: session.id,
          role: "finbot",
          content: "⚠️ Something went wrong. Please try again.",
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setStreaming(false);
    }
  };

  return (
    <ChatContext.Provider
      value={{ messages, input, setInput, streaming, send }}
    >
      {children}
    </ChatContext.Provider>
  );
};
