import React, { useEffect, useRef } from "react";
import { useChat } from "../../context/ChatContext";
import MessageBubble from "./MessageBubble";
import { splitIntoBubbles } from "../../utils/split_bubbles";

const ChatWindow: React.FC = () => {
  const { messages, streaming } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streaming]);
  return (
    <div className="relative flex-1 overflow-y-auto px-4 pb-20 bg-bg-base">
      <div className="max-w-3xl mx-auto pt-[9dvh] flex flex-col gap-8">
        {messages.flatMap((msg) => {
          if (msg.role === "finbot") {
            const parts = splitIntoBubbles(msg.content);
            // render each part as its own bubble
            return parts.map((part, i) => (
              <MessageBubble
                key={`${msg.id}-${i}`}
                msg={{ ...msg, content: part }}
              />
            ));
          }
          // user messages render as a single bubble
          return <MessageBubble key={msg.id} msg={msg} />;
        })}
        {streaming && (
          <div className="text-text-muted italic animate-pulse">
            <div className="bg-bg-subtle animate-pulse rounded-md px-3 py-1 rounded-xl w-[fit-content] flex items-center gap-1">
              <span className="animate-bounce">.</span>
              <span className="animate-bounce animate-delay-150">.</span>
              <span className="animate-bounce animate-delay-300">.</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};

export default ChatWindow;
