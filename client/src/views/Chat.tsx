import React from "react";
import { ChatProvider } from "../context/ChatContext";
import ChatWindow from "../components/chat/ChatWindow";
import MessageInput from "../components/chat/MessageInput";
import Header from "../components/Header";

const Chat: React.FC = () => {
  return (
    <ChatProvider>
      <div className="relative flex flex-col h-screen bg-bg-base text-text-primary font-sans">
        <Header />
        <ChatWindow />
        <MessageInput />
      </div>
    </ChatProvider>
  );
};

export default Chat;
