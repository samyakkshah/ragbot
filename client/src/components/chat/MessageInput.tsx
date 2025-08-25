import React, { useRef, useEffect } from "react";
import { useChat } from "../../context/ChatContext";
import { Button } from "../ui/Button";
import { SendHorizonal } from "lucide-react";
import { Textarea } from "../ui/Textarea";
import { motion } from "framer-motion";

const MessageInput: React.FC = () => {
  const { input, setInput, send, streaming } = useChat();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Smooth autosize textarea
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <motion.div
      key="input-box"
      initial={{ y: 48, opacity: 0, x: "-50%" }}
      animate={{ y: 0, opacity: 1, x: "-50%" }}
      transition={{
        delay: 0.1,
        duration: 0.4,
        type: "spring",
        stiffness: 120,
      }}
      className="fixed bottom-6 left-1/2 w-[90%] sm:w-[70%] md:w-[60%] lg:w-[40%]"
    >
      <div className="w-full bg-white/70 dark:bg-zinc-900/60 backdrop-blur-lg border border-zinc-200 dark:border-zinc-700 shadow-lg p-2 rounded-2xl space-y-2 transition-all duration-300 ease focus-within:ring-1 focus-within:ring-primary-400/70">
        <div className="flex items-end justify-center gap-2">
          <Textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Ask your question..."
            rows={1}
            className="flex-1 resize-none overflow-x-hidden overflow-y-auto text-sm bg-transparent dark:bg-transparent border-none shadow-none h-auto min-h-[1dvh] max-h-40 px-2 py-2 transition-[height] duration-200 ease-in-out"
            style={{ lineHeight: "1.5" }}
          />

          <Button
            onClick={send}
            disabled={streaming || !input.trim()}
            className="rounded-full w-8 h-8 cursor-pointer flex items-center justify-center"
          >
            <SendHorizonal className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </motion.div>
  );
};

export default MessageInput;
