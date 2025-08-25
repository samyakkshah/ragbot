import { useAuth } from "../context/AuthContext";
import { useThemeMode } from "../hooks/useThemeMode";
import { Button } from "./ui/Button";

const Header: React.FC = () => {
  const { theme, setTheme } = useThemeMode();
  const { auth, openAuth, logout } = useAuth();

  return (
    <div className="fixed md:top-3 rounded-md bg-bg-tinted backdrop-blur-lg shadow-sm left-1/2 -translate-x-1/2 h-14 sm:max-w-lg md:max-w-4xl w-full p-4 mx-auto flex flex-row justify-between items-center z-[999]">
      <p className="font-semibold">Eloquent AI</p>
      <div className="flex gap-2">
        {auth.token ? (
          <Button className="p-2 rounded-sm" onClick={logout}>
            Logout
          </Button>
        ) : (
          <Button className="p-2 rounded-sm" onClick={openAuth}>
            Login / Sign Up
          </Button>
        )}
        <Button
          className="p-2 rounded-sm"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          {theme === "dark" ? "Light" : "Dark"}
        </Button>
      </div>
    </div>
  );
};

export default Header;
