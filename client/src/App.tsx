import AppLayout from "./components/layout/AppLayout";
import { MessageBubble } from "./components/ui/chat/MessageBubble";
import { TextArea } from "./components/ui/Textarea";

export default function App() {
  return (
    <AppLayout>
      <div>
        <div className="rounded-xl p-4 shadow-md bg-surface-base border border-border-subtle">
          <p className="mb-2">Try the theme toggle in the header.</p>
          <TextArea
            // ref={textareaRef}
            // value={input}
            // onChange={handleInputChange}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                // handleSubmit();
              }
            }}
            placeholder="Ask whatever you want..."
            rows={1}
            className="flex-1 resize-none overflow-hidden text-sm bg-transparent dark:bg-transparent border-none shadow-none focus-visible:ring-0 h-auto min-h-[36px] max-h-40 px-2 py-2 transition-all duration-200 ease-in-out"
            style={{ lineHeight: "1.5", willChange: "height" }}
          />
          <MessageBubble role="assistant">Nice</MessageBubble>
        </div>
      </div>
    </AppLayout>
  );
}
