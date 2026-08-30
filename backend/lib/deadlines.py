"""Application cut-off computation.

Every date here is anchored to the server clock via lib.dates.today_iso() (IST — the timezone every
Indian government portal publishes its cut-offs in). Never compute "days remaining" in the browser:
a citizen with a wrong device clock would otherwise be told a scheme is still open.
"""

from datetime import date, timedelta
from typing import Optional

from lib.dates import today_iso
from models.scheme import DeadlineStatus, Scheme, SchemeDeadline

# "Closing soon" thresholds agreed with the product owner.
CRITICAL_DAYS = 7
SOON_DAYS = 30

IST = "Asia/Kolkata"


def _today() -> date:
    return date.fromisoformat(today_iso(IST))


def _next_occurrence(month: int, day: int, today: date) -> date:
    """The next time this recurring MM-DD falls due, today included."""
    for year in (today.year, today.year + 1):
        try:
            candidate = date(year, month, day)
        except ValueError:
            # 29 Feb in a non-leap year — fall back to the 28th.
            candidate = date(year, month, day - 1)
        if candidate >= today:
            return candidate
    return date(today.year + 1, month, day)


def _human_date(d: date) -> str:
    return d.strftime("%d %b %Y")


def compute_deadline_status(deadline: SchemeDeadline, today: Optional[date] = None) -> DeadlineStatus:
    today = today or _today()
    window = (deadline.window_type or "ROLLING").upper()

    if window == "ROLLING" or not deadline.cutoff_dates:
        if window == "EVENT_BASED":
            return DeadlineStatus(
                window_type="EVENT_BASED",
                urgency="EVENT_BASED",
                headline="Time-limited after event",
                detail=deadline.note
                or "The application window starts from a personal event — apply as early as possible.",
                is_urgent=False,
            )
        return DeadlineStatus(
            window_type="ROLLING",
            urgency="ROLLING",
            headline="Open all year",
            detail=deadline.note
            or "Applications are accepted throughout the year — there is no annual cut-off date.",
            is_urgent=False,
        )

    # ANNUAL / SEASONAL — find the soonest upcoming cut-off.
    upcoming = sorted(
        (
            (_next_occurrence(c.month, c.day, today), c.label)
            for c in deadline.cutoff_dates
        ),
        key=lambda pair: pair[0],
    )
    next_date, next_label = upcoming[0]
    days = (next_date - today).days

    if days <= CRITICAL_DAYS:
        urgency = "CLOSING_CRITICAL"
        headline = "Closes in 1 day" if days == 1 else (
            "Closes today" if days == 0 else f"Closes in {days} days"
        )
    elif days <= SOON_DAYS:
        urgency = "CLOSING_SOON"
        headline = f"Closes in {days} days"
    else:
        urgency = "OPEN"
        headline = f"Next cut-off {_human_date(next_date)}"

    detail = (
        f"{next_label} closes on {_human_date(next_date)}"
        f" — {days} day{'' if days == 1 else 's'} left."
    )
    if days == 0:
        detail = f"{next_label} closes today ({_human_date(next_date)}). Apply before the portal shuts."
    if len(deadline.cutoff_dates) > 1:
        others = ", ".join(
            f"{lbl} on {_human_date(dt)}" for dt, lbl in upcoming[1:]
        )
        detail = f"{detail} Later window: {others}."
    if deadline.source_note:
        detail = f"{detail} {deadline.source_note}"

    return DeadlineStatus(
        window_type=window,
        urgency=urgency,
        headline=headline,
        detail=detail,
        next_cutoff_date=next_date.isoformat(),
        next_cutoff_label=next_label,
        days_remaining=days,
        is_urgent=urgency in ("CLOSING_SOON", "CLOSING_CRITICAL"),
    )


def attach_deadline_status(scheme: Scheme, today: Optional[date] = None) -> Scheme:
    """Return the scheme with its freshly computed deadline_status filled in."""
    scheme.deadline_status = compute_deadline_status(scheme.deadline, today)
    return scheme
