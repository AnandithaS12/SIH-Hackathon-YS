import { useCallback, useEffect, useState } from "react";
import type { CitizenEvaluationResponse } from "@/types";

const EVAL_KEY = "yojana-setu:evaluation";
const LANG_KEY = "yojana-setu:language";
const DOCS_KEY = "yojana-setu:owned-documents";
const STORE_EVENT = "yojana-setu:store-change";

function readJson<T>(key: string): T | null {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : null;
  } catch {
    return null;
  }
}

function writeJson(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* storage unavailable — non-fatal */
  }
  window.dispatchEvent(new Event(STORE_EVENT));
}

export function saveEvaluation(evaluation: CitizenEvaluationResponse) {
  writeJson(EVAL_KEY, evaluation);
}

export function clearEvaluation() {
  localStorage.removeItem(EVAL_KEY);
  window.dispatchEvent(new Event(STORE_EVENT));
}

export function getEvaluation(): CitizenEvaluationResponse | null {
  return readJson<CitizenEvaluationResponse>(EVAL_KEY);
}

export function useEvaluation() {
  const [evaluation, setEvaluation] = useState<CitizenEvaluationResponse | null>(() =>
    readJson<CitizenEvaluationResponse>(EVAL_KEY),
  );

  useEffect(() => {
    const sync = () => setEvaluation(readJson<CitizenEvaluationResponse>(EVAL_KEY));
    window.addEventListener(STORE_EVENT, sync);
    window.addEventListener("storage", sync);
    return () => {
      window.removeEventListener(STORE_EVENT, sync);
      window.removeEventListener("storage", sync);
    };
  }, []);

  return evaluation;
}

export function useLanguage() {
  const [language, setLanguageState] = useState<string>(
    () => localStorage.getItem(LANG_KEY) ?? "hi",
  );

  useEffect(() => {
    const sync = () => setLanguageState(localStorage.getItem(LANG_KEY) ?? "hi");
    window.addEventListener(STORE_EVENT, sync);
    return () => window.removeEventListener(STORE_EVENT, sync);
  }, []);

  const setLanguage = useCallback((code: string) => {
    localStorage.setItem(LANG_KEY, code);
    window.dispatchEvent(new Event(STORE_EVENT));
  }, []);

  return { language, setLanguage };
}

export function useOwnedDocuments() {
  const [ownedDocuments, setOwned] = useState<string[]>(
    () => readJson<string[]>(DOCS_KEY) ?? [],
  );

  useEffect(() => {
    const sync = () => setOwned(readJson<string[]>(DOCS_KEY) ?? []);
    window.addEventListener(STORE_EVENT, sync);
    return () => window.removeEventListener(STORE_EVENT, sync);
  }, []);

  const toggleDocument = useCallback((docName: string) => {
    const current = readJson<string[]>(DOCS_KEY) ?? [];
    const next = current.includes(docName)
      ? current.filter((d) => d !== docName)
      : [...current, docName];
    writeJson(DOCS_KEY, next);
  }, []);

  return { ownedDocuments, toggleDocument };
}
