import "./App.css";
import { SessionProvider } from "./context/SessionContext";
import Chat from "./views/Chat";

export default function App() {
  return (
    <SessionProvider>
      <Chat />
    </SessionProvider>
  );
}
