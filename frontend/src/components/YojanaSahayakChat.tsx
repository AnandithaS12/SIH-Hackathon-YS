import { useEffect, useRef, useState } from "react";
import {
  MessageCircle,
  Mic,
  MicOff,
  Send,
  Sparkles,
  Volume2,
  VolumeX,
  X,
  Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { useEvaluation, useLanguage } from "@/lib/citizenStore";
import { CHAT_GREETINGS, FALLBACK_LANGUAGES, SUGGESTED_PROMPTS } from "@/lib/languages";
import { useSpeechRecognition, useSpeechSynthesis, localeFor } from "@/lib/speech";
import ChatMarkdown from "@/components/ChatMarkdown";
import type { ChatMessageUi } from "@/types";

interface Props {
  activeSchemeId?: string | null;
}

export default function YojanaSahayakChat({ activeSchemeId = null }: Props) {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessageUi[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const sessionIdRef = useRef<string | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const { language } = useLanguage();
  const evaluation = useEvaluation();

  const speechIn = useSpeechRecognition(language);
  const speechOut = useSpeechSynthesis(language);

  // Stop any in-flight voice activity when the panel closes.
  // Depend on the stable stop callbacks, not the hook objects (which are new each render).
  const stopListening = speechIn.stop;
  const stopSpeaking = speechOut.stop;
  useEffect(() => {
    if (!open) {
      stopListening();
      stopSpeaking();
    }
  }, [open, stopListening, stopSpeaking]);

  function toggleMic() {
    if (speechIn.isListening) {
      speechIn.stop();
      return;
    }
    speechOut.stop();
    speechIn.start((text) => setInput(text));
  }

  const langNative =
    FALLBACK_LANGUAGES.find((l) => l.code === language)?.native ?? "हिन्दी";
  const greeting = CHAT_GREETINGS[language] ?? CHAT_GREETINGS.en;
  const prompts = SUGGESTED_PROMPTS[language] ?? SUGGESTED_PROMPTS.en;

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, open]);

  async function sendMessage(text: string) {
    const trimmed = text.trim();
    if (!trimmed || isStreaming) return;

    // Voice input ends the moment the question is submitted.
    stopListening();
    stopSpeaking();

    const userMsg: ChatMessageUi = {
      id: `u-${Date.now()}`,
      role: "user",
      content: trimmed,
    };
    const assistantId = `a-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      userMsg,
      { id: assistantId, role: "assistant", content: "", isStreaming: true },
    ]);
    setInput("");
    setIsStreaming(true);

    try {
      const res = await fetch("/api/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionIdRef.current,
          message: trimmed,
          language,
          citizen_profile: evaluation?.profile ?? null,
          active_scheme_id: activeSchemeId,
        }),
      });

      if (!res.ok || !res.body) {
        throw new Error(`Assistant unavailable (status ${res.status})`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() ?? "";

        for (const part of parts) {
          const line = part.trim();
          if (!line.startsWith("data:")) continue;
          const payload = line.slice(5).trim();
          if (!payload) continue;
          try {
            const evt = JSON.parse(payload) as {
              type?: string;
              content?: string;
              session_id?: string;
              error?: string;
            };
            if (evt.session_id) sessionIdRef.current = evt.session_id;
            if (evt.type === "chunk" && evt.content) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId ? { ...m, content: m.content + evt.content } : m,
                ),
              );
            }
            if (evt.type === "error" && evt.error) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId
                    ? { ...m, content: `Sorry, the assistant hit an error: ${evt.error}` }
                    : m,
                ),
              );
            }
          } catch {
            /* skip malformed SSE frame */
          }
        }
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Unknown error";
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? {
                ...m,
                content: `Yojana Sahayak could not respond right now (${msg}). Please try again shortly.`,
              }
            : m,
        ),
      );
    } finally {
      setMessages((prev) =>
        prev.map((m) => (m.id === assistantId ? { ...m, isStreaming: false } : m)),
      );
      setIsStreaming(false);
    }
  }

  return (
    <>
      {/* Floating launcher */}
      {!open && (
        <button
          type="button"
          onClick={() => setOpen(true)}
          data-testid="chat-launcher-button"
          className="no-print fixed bottom-5 right-5 z-50 flex items-center gap-2.5 rounded-full bg-[#1E3A8A] py-3.5 pl-4 pr-5 text-white shadow-xl shadow-[#1E3A8A]/25 transition-transform duration-300 hover:-translate-y-1 hover:bg-[#1E40AF] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#EA580C]"
        >
          <span className="relative flex size-6 items-center justify-center">
            <MessageCircle className="size-6" />
            <span className="absolute -right-1 -top-1 size-2.5 animate-pulse rounded-full bg-[#EA580C]" />
          </span>
          <span className="text-left leading-tight">
            <span className="block text-sm font-bold">Yojana Sahayak</span>
            <span className="block text-[11px] opacity-80">{langNative} · speak or type</span>
          </span>
        </button>
      )}

      {/* Chat panel */}
      {open && (
        <div
          className="no-print fixed inset-x-3 bottom-3 z-50 flex max-h-[82vh] flex-col overflow-hidden rounded-2xl border border-border bg-white shadow-2xl sm:inset-x-auto sm:right-5 sm:bottom-5 sm:w-[420px]"
          data-testid="chat-panel"
        >
          <div className="flex items-start justify-between gap-3 border-b border-border bg-[#1E3A8A] px-4 py-3 text-white">
            <div className="flex items-start gap-2.5">
              <span className="mt-0.5 flex size-8 items-center justify-center rounded-full bg-white/15">
                <Sparkles className="size-4" />
              </span>
              <div className="leading-tight">
                <p className="font-heading text-sm font-bold" data-testid="chat-panel-title">
                  Yojana Sahayak · योजना सहायक
                </p>
                <p className="text-[11px] opacity-80">
                  Replying in {langNative} · voice enabled
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setOpen(false)}
              data-testid="chat-close-button"
              className="rounded-full p-1 transition-colors duration-200 hover:bg-white/15"
              aria-label="Close assistant"
            >
              <X className="size-4" />
            </button>
          </div>

          <div
            ref={scrollRef}
            className="flex-1 space-y-3 overflow-y-auto bg-[#F8FAFC] px-4 py-4"
            data-testid="chat-message-list"
          >
            <div className="rounded-xl rounded-tl-sm border border-border bg-white px-3.5 py-3 text-sm leading-relaxed text-foreground shadow-sm">
              {greeting}
            </div>

            {messages.length === 0 && (
              <div className="flex flex-wrap gap-2 pt-1">
                {prompts.map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => sendMessage(p)}
                    data-testid={`chat-suggested-prompt-${prompts.indexOf(p)}`}
                    className="rounded-full border border-[#1E3A8A]/25 bg-white px-3 py-1.5 text-xs font-medium text-[#1E3A8A] transition-colors duration-200 hover:bg-[#1E3A8A]/8"
                  >
                    {p}
                  </button>
                ))}
              </div>
            )}

            {messages.map((m) =>
              m.role === "user" ? (
                <div
                  key={m.id}
                  className="ml-auto max-w-[88%] rounded-xl rounded-br-sm bg-[#1E3A8A] px-3.5 py-2.5 text-sm leading-relaxed text-white shadow-sm"
                  data-testid="chat-message-user"
                >
                  {m.content}
                </div>
              ) : (
                <div
                  key={m.id}
                  className="max-w-[92%] rounded-xl rounded-tl-sm border border-border bg-white px-3.5 py-3 shadow-sm"
                  data-testid="chat-message-assistant"
                >
                  <div className="text-sm leading-relaxed text-foreground">
                    {m.content ? (
                      <ChatMarkdown text={m.content} />
                    ) : m.isStreaming ? (
                      <span className="flex items-center gap-2 text-muted-foreground">
                        <Loader2 className="size-3.5 animate-spin" /> सोच रहा हूँ… thinking
                      </span>
                    ) : (
                      ""
                    )}
                  </div>

                  {/* Read aloud — explicit tap, never auto-plays */}
                  {m.content && !m.isStreaming && speechOut.isSupported && (
                    <button
                      type="button"
                      onClick={() => speechOut.speak(m.id, m.content)}
                      data-testid={`chat-speak-button-${m.id}`}
                      aria-label={
                        speechOut.speakingId === m.id
                          ? "Stop reading this answer aloud"
                          : "Read this answer aloud"
                      }
                      className={`mt-2.5 inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-semibold transition-colors duration-200 ${
                        speechOut.speakingId === m.id
                          ? "border-[#EA580C]/40 bg-[#EA580C]/10 text-[#C2410C]"
                          : "border-border bg-secondary/60 text-muted-foreground hover:bg-secondary"
                      }`}
                    >
                      {speechOut.speakingId === m.id ? (
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
              ),
            )}
          </div>

          <div className="border-t border-border bg-white px-3 py-3">
            {/* Live transcript while speaking */}
            {speechIn.isListening && (
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
                    {speechIn.interimTranscript || input || "…"}
                  </p>
                </div>
              </div>
            )}

            {speechIn.error && (
              <div
                className="mb-2.5 flex items-start justify-between gap-2 rounded-lg border border-destructive/30 bg-destructive/8 px-3 py-2"
                data-testid="chat-voice-error"
              >
                <p className="text-xs leading-relaxed text-destructive">{speechIn.error}</p>
                <button
                  type="button"
                  onClick={speechIn.clearError}
                  aria-label="Dismiss voice error"
                  className="shrink-0 rounded-full p-0.5 transition-colors duration-200 hover:bg-destructive/10"
                >
                  <X className="size-3.5 text-destructive" />
                </button>
              </div>
            )}

            <div className="flex items-end gap-2">
              {speechIn.isSupported && (
                <Button
                  onClick={toggleMic}
                  size="icon"
                  variant={speechIn.isListening ? "default" : "outline"}
                  className={`size-11 shrink-0 rounded-full ${
                    speechIn.isListening
                      ? "bg-[#EA580C] hover:bg-[#C2410C]"
                      : "border-2 border-[#1E3A8A]/25 text-[#1E3A8A]"
                  }`}
                  data-testid="chat-mic-button"
                  aria-label={speechIn.isListening ? "Stop voice input" : "Speak your question"}
                  title={
                    speechIn.isListening
                      ? "Tap to stop listening"
                      : `Speak your question in ${langNative}`
                  }
                >
                  {speechIn.isListening ? (
                    <MicOff className="size-5" />
                  ) : (
                    <Mic className="size-5" />
                  )}
                </Button>
              )}

              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage(input);
                  }
                }}
                placeholder="अपनी भाषा में सवाल लिखें या बोलें… / Type or speak…"
                rows={2}
                className="min-h-[52px] resize-none text-sm"
                data-testid="chat-input-textarea"
              />
              <Button
                onClick={() => sendMessage(input)}
                disabled={isStreaming || !input.trim()}
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
              {speechIn.isSupported
                ? `Speak or type · voice locale ${localeFor(language)} · 22 Indian languages`
                : "Supports all 22 scheduled Indian languages"}
            </Badge>
          </div>
        </div>
      )}
    </>
  );
}
