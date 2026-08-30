import { useCallback, useEffect, useRef, useState } from "react";

// ---------------------------------------------------------------------------
// Minimal Web Speech API typings. TypeScript's DOM lib does not ship
// SpeechRecognition (it is still a draft spec, prefixed in Chromium), so the
// pieces we actually use are declared here rather than cast to `any`.
// ---------------------------------------------------------------------------
interface SpeechRecognitionAlternative {
  transcript: string;
  confidence: number;
}

interface SpeechRecognitionResultLike {
  readonly length: number;
  readonly isFinal: boolean;
  item: (index: number) => SpeechRecognitionAlternative;
  [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionResultListLike {
  readonly length: number;
  item: (index: number) => SpeechRecognitionResultLike;
  [index: number]: SpeechRecognitionResultLike;
}

interface SpeechRecognitionEventLike extends Event {
  readonly resultIndex: number;
  readonly results: SpeechRecognitionResultListLike;
}

interface SpeechRecognitionErrorEventLike extends Event {
  readonly error: string;
}

interface SpeechRecognitionLike {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  maxAlternatives: number;
  start: () => void;
  stop: () => void;
  abort: () => void;
  onresult: ((e: SpeechRecognitionEventLike) => void) | null;
  onerror: ((e: SpeechRecognitionErrorEventLike) => void) | null;
  onend: (() => void) | null;
  onstart: (() => void) | null;
}

type SpeechRecognitionCtor = new () => SpeechRecognitionLike;

interface SpeechWindow {
  SpeechRecognition?: SpeechRecognitionCtor;
  webkitSpeechRecognition?: SpeechRecognitionCtor;
}

function getRecognitionCtor(): SpeechRecognitionCtor | null {
  if (typeof window === "undefined") return null;
  const w = window as unknown as SpeechWindow;
  return w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null;
}

// ---------------------------------------------------------------------------
// BCP-47 locale per app language code — what the browser's recognizer and the
// speech synthesiser both expect. Covers the 22 scheduled languages; families
// without a dedicated voice fall back to the closest Indian locale.
// ---------------------------------------------------------------------------
export const SPEECH_LOCALES: Record<string, string> = {
  hi: "hi-IN",
  en: "en-IN",
  bn: "bn-IN",
  te: "te-IN",
  mr: "mr-IN",
  ta: "ta-IN",
  gu: "gu-IN",
  ur: "ur-IN",
  kn: "kn-IN",
  or: "or-IN",
  ml: "ml-IN",
  pa: "pa-IN",
  as: "as-IN",
  mai: "hi-IN",
  sat: "hi-IN",
  ks: "ur-IN",
  ne: "ne-NP",
  kok: "mr-IN",
  doi: "hi-IN",
  sd: "hi-IN",
  brx: "hi-IN",
  sa: "hi-IN",
  mni: "bn-IN",
};

export function localeFor(languageCode: string): string {
  return SPEECH_LOCALES[languageCode] ?? "hi-IN";
}

/**
 * Speech-to-text with a live interim transcript. The citizen sees words appear
 * as they speak and can edit the text before sending.
 */
export function useSpeechRecognition(languageCode: string) {
  const [isListening, setIsListening] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState("");
  const [error, setError] = useState<string | null>(null);
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);
  const finalRef = useRef("");
  const onFinalRef = useRef<((text: string) => void) | null>(null);

  const isSupported = getRecognitionCtor() !== null;

  const stop = useCallback(() => {
    recognitionRef.current?.stop();
    setIsListening(false);
  }, []);

  const start = useCallback(
    (onTranscript: (text: string) => void) => {
      const Ctor = getRecognitionCtor();
      if (!Ctor) {
        setError("Your browser does not support voice input. Try Chrome or Edge.");
        return;
      }

      // Tear down any previous session before starting a new one.
      recognitionRef.current?.abort();
      finalRef.current = "";
      onFinalRef.current = onTranscript;
      setInterimTranscript("");
      setError(null);

      const recognition = new Ctor();
      recognition.lang = localeFor(languageCode);
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => setIsListening(true);

      recognition.onresult = (event) => {
        let interim = "";
        for (let i = event.resultIndex; i < event.results.length; i += 1) {
          const result = event.results[i];
          const text = result[0]?.transcript ?? "";
          if (result.isFinal) {
            finalRef.current = `${finalRef.current} ${text}`.trim();
          } else {
            interim += text;
          }
        }
        setInterimTranscript(interim);
        const combined = `${finalRef.current} ${interim}`.trim();
        if (combined) onFinalRef.current?.(combined);
      };

      recognition.onerror = (event) => {
        if (event.error === "not-allowed" || event.error === "service-not-allowed") {
          setError("Microphone permission was blocked. Allow mic access and try again.");
        } else if (event.error === "no-speech") {
          setError("No speech detected. Please try speaking again.");
        } else if (event.error !== "aborted") {
          setError(`Voice input error: ${event.error}`);
        }
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
        setInterimTranscript("");
      };

      recognitionRef.current = recognition;
      try {
        recognition.start();
      } catch {
        setError("Could not start voice input. Please try again.");
        setIsListening(false);
      }
    },
    [languageCode],
  );

  useEffect(() => () => recognitionRef.current?.abort(), []);

  return { isSupported, isListening, interimTranscript, error, start, stop, clearError: () => setError(null) };
}

/**
 * Text-to-speech for assistant replies. Playback is explicit — the citizen taps
 * the speaker icon on a reply; nothing is ever spoken automatically.
 */
export function useSpeechSynthesis(languageCode: string) {
  const [speakingId, setSpeakingId] = useState<string | null>(null);
  const [voicesReady, setVoicesReady] = useState(false);

  const isSupported = typeof window !== "undefined" && "speechSynthesis" in window;

  // Voices load asynchronously in Chrome; re-render once they arrive.
  useEffect(() => {
    if (!isSupported) return;
    const sync = () => setVoicesReady(window.speechSynthesis.getVoices().length > 0);
    sync();
    window.speechSynthesis.onvoiceschanged = sync;
    return () => {
      window.speechSynthesis.onvoiceschanged = null;
    };
  }, [isSupported]);

  const stop = useCallback(() => {
    if (!isSupported) return;
    window.speechSynthesis.cancel();
    setSpeakingId(null);
  }, [isSupported]);

  const speak = useCallback(
    (id: string, text: string) => {
      if (!isSupported || !text.trim()) return;

      // Tapping the speaker on the currently playing reply stops it.
      window.speechSynthesis.cancel();
      if (speakingId === id) {
        setSpeakingId(null);
        return;
      }

      const locale = localeFor(languageCode);
      // Strip markdown emphasis/bullets so the voice does not read "asterisk".
      const clean = text
        .replace(/\*\*/g, "")
        .replace(/[*_`#]/g, "")
        .replace(/\s+/g, " ")
        .trim();

      const utterance = new SpeechSynthesisUtterance(clean);
      utterance.lang = locale;
      utterance.rate = 0.92;
      utterance.pitch = 1;

      const voices = window.speechSynthesis.getVoices();
      const exact = voices.find((v) => v.lang === locale);
      const sameLanguage = voices.find(
        (v) => v.lang.split("-")[0] === locale.split("-")[0],
      );
      const indian = voices.find((v) => v.lang.endsWith("-IN"));
      const chosen = exact ?? sameLanguage ?? indian;
      if (chosen) utterance.voice = chosen;

      utterance.onend = () => setSpeakingId(null);
      utterance.onerror = () => setSpeakingId(null);

      setSpeakingId(id);
      window.speechSynthesis.speak(utterance);
    },
    [isSupported, languageCode, speakingId],
  );

  useEffect(() => {
    return () => {
      if (isSupported) window.speechSynthesis.cancel();
    };
  }, [isSupported]);

  return { isSupported, voicesReady, speakingId, speak, stop };
}
