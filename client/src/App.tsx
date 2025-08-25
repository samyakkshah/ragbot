import "./App.css";
import AuthModal from "./components/signInSignUpModal";
import { SessionProvider } from "./context/SessionContext";
import { ChatProvider } from "./context/ChatContext";
import { AuthProvider } from "./context/AuthContext";
import Chat from "./views/Chat";

export default function App() {
  return (
    <AuthProvider>
      <SessionProvider>
        <ChatProvider>
          <Chat />
          <AuthModal />
        </ChatProvider>
      </SessionProvider>
    </AuthProvider>
  );
}
