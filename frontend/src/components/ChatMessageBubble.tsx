import { Loader2, Volume2, VolumeX } from "lucide-react";
import ChatMarkdown from "@/components/ChatMarkdown";
import type { ChatMessageUi } from "@/types";

interface Props {
  message: ChatMessageUi;
  /** Native-script name of the active language, e.g. "हिन्दी". */
  langNative: string;
  canSpeak: boolean;
  isSpeaking: boolean;
  onToggleSpeak: (id: string, text: string) => void;
}

/** A single chat bubble — user on the right, Yojana Sahayak on the left with read-aloud. */
export default function ChatMessageBubble({
  message,
  langNative,
  canSpeak,
  isSpeaking,
  onToggleSpeak,
}: Props) {
  if (message.role === "user") {
    return (
      <div
        className="ml-auto max-w-[88%] rounded-xl rounded-br-sm bg-[#1E3A8A] px-3.5 py-2.5 text-sm leading-relaxed text-white shadow-sm"
        data-testid="chat-message-user"
      >
        {message.content}
      </div>
    );
  }

  const showSpeakControl = Boolean(message.content) && !message.isStreaming && canSpeak;

  return (
    <div
      className="max-w-[92%] rounded-xl rounded-tl-sm border border-border bg-white px-3.5 py-3 shadow-sm"
      data-testid="chat-message-assistant"
    >
      <div className="text-sm leading-relaxed text-foreground">
        {message.content ? (
          <ChatMarkdown text={message.content} />
        ) : message.isStreaming ? (
          <span className="flex items-center gap-2 text-muted-foreground">
            <Loader2 className="size-3.5 animate-spin" /> सोच रहा हूँ… thinking
          </span>
        ) : (
          ""
        )}
      </div>

      {showSpeakControl && (
        <button
          type="button"
          onClick={() => onToggleSpeak(message.id, message.content)}
          data-testid={`chat-speak-button-${message.id}`}
          aria-label={
            isSpeaking ? "Stop reading this answer aloud" : "Read this answer aloud"
          }
          className={`mt-2.5 inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-semibold transition-colors duration-200 ${
            isSpeaking
              ? "border-[#EA580C]/40 bg-[#EA580C]/10 text-[#C2410C]"
              : "border-border bg-secondary/60 text-muted-foreground hover:bg-secondary"
          }`}
        >
          {isSpeaking ? (
            <>
              <VolumeX className="size-3.5" />
              Stop
            </>
          ) : (
            <>
              <Volume2 className="size-3.5" />
              Listen · {langNative}
            </>
          )}
        </button>
      )}
    </div>
  );
}
