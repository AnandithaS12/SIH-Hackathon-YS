import { Link } from "react-router-dom";

const LOGO_URL =
  "https://customer-assets-eiarnc6j.emergentagent.net/job_e43c439c-0a56-49ac-ad23-99fa1ca30ab5/artifacts/2fvf23e5_image.png";

export default function Logo({ compact = false }: { compact?: boolean }) {
  return (
    <Link
      to="/"
      className="flex items-center gap-3 group"
      data-testid="app-logo-link"
      aria-label="Yojana Setu home"
    >
      <span className="relative flex size-11 shrink-0 items-center justify-center overflow-hidden rounded-full border border-border bg-white shadow-sm transition-transform duration-300 group-hover:scale-105">
        <img
          src={LOGO_URL}
          alt="Yojana Setu logo"
          className="size-full scale-[1.55] object-contain"
          data-testid="app-logo-image"
        />
      </span>
      {!compact && (
        <span className="flex flex-col leading-none">
          <span className="font-heading text-lg font-extrabold tracking-tight text-[#1E3A8A]">
            Yojana<span className="text-[#EA580C]"> Setu</span>
          </span>
          <span className="mt-0.5 text-[11px] font-medium text-muted-foreground">
            Bridging Schemes to Citizens
          </span>
        </span>
      )}
    </Link>
  );
}
