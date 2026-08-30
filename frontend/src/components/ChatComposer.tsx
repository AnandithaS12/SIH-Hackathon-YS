import { Loader2, Mic, MicOff, Send, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  isStreaming: boolean;
  langNative: string;
  locale: string;
  // Voice input
  micSupported: boolean;
  isListening: boolean;
  interimTranscript: string;
  voiceError: string | null;
  onToggleMic: () => void;
  onDismissVoiceError: () => void;
}

/** Composer row: live transcript, mic, textarea and send button. */
export default function ChatComposer({
  value,
  onChange,
  onSend,
  isStreaming,
  langNative,
  locale,
  micSupported,
  isListening,
  interimTranscript,
  voiceError,
  onToggleMic,
  onDismissVoiceError,
}: Props) {
  return (
    <div className="border-t border-border bg-white px-3 py-3">
      {isListening && (
        <div
          className="mb-2.5 flex items-start gap-2.5 rounded-lg border border-[#EA580C]/30 bg-[#EA580C]/8 px-3 py-2.5"
          data-testid="chat-live-transcript"
        >
          <span className="mt-0.5 flex size-4 shrink-0 items-center justify-center">
            <span className="size-2.5 animate-pulse rounded-full bg-[#EA580C]" />
          </span>
          <div className="min-w-0">
            <p className="text-[11px] font-bold uppercase tracking-wide text-[#C2410C]">
              Listening in {langNative} · बोलिए
            </p>
            <p className="mt-0.5 break-words text-xs leading-relaxed text-foreground">
              {interimTranscript || value || "…"}
            </p>
          </div>
        </div>
      )}

      {voiceError && (
        <div
          className="mb-2.5 flex items-start justify-between gap-2 rounded-lg border border-destructive/30 bg-destructive/8 px-3 py-2"
          data-testid="chat-voice-error"
        >
          <p className="text-xs leading-relaxed text-destructive">{voiceError}</p>
          <button
            type="button"
            onClick={onDismissVoiceError}
            aria-label="Dismiss voice error"
            className="shrink-0 rounded-full p-0.5 transition-colors duration-200 hover:bg-destructive/10"
          >
            <X className="size-3.5 text-destructive" />
          </button>
        </div>
      )}

      <div className="flex items-end gap-2">
        {micSupported && (
          <Button
            onClick={onToggleMic}
            size="icon"
            variant={isListening ? "default" : "outline"}
            className={`size-11 shrink-0 rounded-full ${
              isListening
                ? "bg-[#EA580C] hover:bg-[#C2410C]"
                : "border-2 border-[#1E3A8A]/25 text-[#1E3A8A]"
            }`}
            data-testid="chat-mic-button"
            aria-label={isListening ? "Stop voice input" : "Speak your question"}
            title={
              isListening
                ? "Tap to stop listening"
                : `Speak your question in ${langNative}`
            }
          >
            {isListening ? <MicOff className="size-5" /> : <Mic className="size-5" />}
          </Button>
        )}

        <Textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSend();
            }
          }}
          placeholder="अपनी भाषा में सवाल लिखें या बोलें… / Type or speak…"
          rows={2}
          className="min-h-[52px] resize-none text-sm"
          data-testid="chat-input-textarea"
        />

        <Button
          onClick={onSend}
          disabled={isStreaming || !value.trim()}
          size="icon"
          className="size-11 shrink-0 rounded-full bg-[#EA580C] hover:bg-[#C2410C]"
          data-testid="chat-send-button"
          aria-label="Send message"
        >
          {isStreaming ? (
            <Loader2 className="size-4 animate-spin" />
          ) : (
            <Send className="size-4" />
          )}
        </Button>
      </div>

      <Badge variant="outline" className="mt-2 text-[10px] font-normal">
        {micSupported
          ? `Speak or type · voice locale ${locale} · 22 Indian languages`
          : "Supports all 22 scheduled Indian languages"}
      </Badge>
    </div>
  );
}
