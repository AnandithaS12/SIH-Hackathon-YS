import { Link, useLocation } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Globe, LayoutGrid, RotateCcw } from "lucide-react";
import { apiGet } from "@/lib/api";
import { Button, buttonVariants } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Logo from "@/components/Logo";
import { clearEvaluation, useEvaluation, useLanguage } from "@/lib/citizenStore";
import type { VernacularLanguage } from "@/types";
import { FALLBACK_LANGUAGES } from "@/lib/languages";

export default function AppHeader() {
  const { language, setLanguage } = useLanguage();
  const evaluation = useEvaluation();
  const location = useLocation();

  const { data: languages } = useQuery({
    queryKey: ["languages"],
    queryFn: () => apiGet<VernacularLanguage[]>("/chat/languages"),
  });

  const languageList = languages && languages.length > 0 ? languages : FALLBACK_LANGUAGES;
  const labelMap: Record<string, string> = {};
  languageList.forEach((l) => {
    labelMap[l.code] = l.native;
  });

  return (
    <header
      className="sticky top-0 z-40 w-full border-b-2 border-border bg-white/95 backdrop-blur-sm"
      data-testid="app-header"
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <Logo />

        <div className="flex items-center gap-2 sm:gap-3">
          {evaluation && location.pathname !== "/results" && (
            <Link
              to="/results"
              className={buttonVariants({ variant: "outline", size: "sm" })}
              data-testid="header-my-schemes-link"
            >
              <LayoutGrid className="size-4" />
              <span className="hidden sm:inline">My Schemes</span>
            </Link>
          )}

          {evaluation && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => clearEvaluation()}
              data-testid="header-reset-button"
              title="Start a new eligibility check"
            >
              <RotateCcw className="size-4" />
              <span className="hidden md:inline">Restart</span>
            </Button>
          )}

          <div className="flex items-center gap-1.5 rounded-full border border-border bg-secondary/60 py-1 pl-3 pr-1">
            <Globe className="size-4 shrink-0 text-[#1E3A8A]" />
            <Select value={language} onValueChange={(value: string) => setLanguage(value)}>
              <SelectTrigger
                size="sm"
                className="h-8 w-[112px] border-0 bg-transparent shadow-none sm:w-[140px]"
                data-testid="language-switcher-trigger"
              >
                <SelectValue>{(v) => labelMap[v as string] ?? "हिन्दी"}</SelectValue>
              </SelectTrigger>
              <SelectContent className="max-h-[320px]">
                {languageList.map((l) => (
                  <SelectItem
                    key={l.code}
                    value={l.code}
                    data-testid={`language-option-${l.code}`}
                  >
                    {l.native} · {l.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>
    </header>
  );
}
