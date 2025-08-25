import React from "react";
import { MessageResponse } from "../../utils/types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const MessageBubble: React.FC<{ msg: MessageResponse }> = ({ msg }) => {
  const isUser = msg.role === "user";
  return (
    <div
      className={`p-3 rounded-lg shadow-sm transition-base ${
        isUser
          ? "bg-primary-500 max-w-[70%] text-text-inverted self-end"
          : "bg-bg-subtle max-w-[90%] text-text-primary self-start"
      }`}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
    </div>
  );
};

export default MessageBubble;
