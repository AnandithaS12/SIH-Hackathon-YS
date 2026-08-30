import { useCallback, useRef, useState } from "react";
import type { ChatMessageUi, CitizenProfile } from "@/types";

interface Options {
  language: string;
  citizenProfile?: CitizenProfile | null;
  activeSchemeId?: string | null;
  /** Called right before a message is sent, so voice activity can be stopped. */
  onBeforeSend?: () => void;
}

interface SseEvent {
  type?: string;
  content?: string;
  session_id?: string;
  error?: string;
}

/**
 * Owns the Yojana Sahayak conversation: message list, SSE streaming from
 * POST /api/chat/stream, and per-session continuity.
 */
export function useChat({
  language,
  citizenProfile,
  activeSchemeId,
  onBeforeSend,
}: Options) {
  const [messages, setMessages] = useState<ChatMessageUi[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const sessionIdRef = useRef<string | null>(null);

  const appendToAssistant = useCallback((id: string, chunk: string) => {
    setMessages((prev) =>
      prev.map((m) => (m.id === id ? { ...m, content: m.content + chunk } : m)),
    );
  }, []);

  const replaceAssistant = useCallback((id: string, content: string) => {
    setMessages((prev) => prev.map((m) => (m.id === id ? { ...m, content } : m)));
  }, []);

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || isStreaming) return;

      onBeforeSend?.();

      const assistantId = `a-${Date.now()}`;
      setMessages((prev) => [
        ...prev,
        { id: `u-${Date.now()}`, role: "user", content: trimmed },
        { id: assistantId, role: "assistant", content: "", isStreaming: true },
      ]);
      setIsStreaming(true);

      try {
        const res = await fetch("/api/chat/stream", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: sessionIdRef.current,
            message: trimmed,
            language,
            citizen_profile: citizenProfile ?? null,
            active_scheme_id: activeSchemeId ?? null,
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

          // Keep the trailing partial frame in the buffer for the next read.
          const frames = buffer.split("\n\n");
          buffer = frames.pop() ?? "";

          for (const frame of frames) {
            const line = frame.trim();
            if (!line.startsWith("data:")) continue;
            const payload = line.slice(5).trim();
            if (!payload) continue;

            try {
              const evt = JSON.parse(payload) as SseEvent;
              if (evt.session_id) sessionIdRef.current = evt.session_id;
              if (evt.type === "chunk" && evt.content) {
                appendToAssistant(assistantId, evt.content);
              }
              if (evt.type === "error" && evt.error) {
                replaceAssistant(
                  assistantId,
                  `Sorry, the assistant hit an error: ${evt.error}`,
                );
              }
            } catch (err) {
              console.error("[useChat] Skipped malformed SSE frame:", payload, err);
            }
          }
        }
      } catch (err) {
        const detail = err instanceof Error ? err.message : "Unknown error";
        console.error("[useChat] Chat stream failed:", err);
        replaceAssistant(
          assistantId,
          `Yojana Sahayak could not respond right now (${detail}). Please try again shortly.`,
        );
      } finally {
        setMessages((prev) =>
          prev.map((m) => (m.id === assistantId ? { ...m, isStreaming: false } : m)),
        );
        setIsStreaming(false);
      }
    },
    [
      isStreaming,
      language,
      citizenProfile,
      activeSchemeId,
      onBeforeSend,
      appendToAssistant,
      replaceAssistant,
    ],
  );

  return { messages, isStreaming, sendMessage };
}
