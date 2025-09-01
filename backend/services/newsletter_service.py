# backend/services/newsletter_service.py
from textwrap import dedent

SECTION_LABELS = {
    "US": "🌎🔋⚡UNITED STATES",
    "EUROPE": "🌍🔋⚡EUROPE",
    "GLOBAL": "🌐🔋⚡AROUND THE GLOBE & ANALYSES",
}

def _bulletize(items):
    lines = []
    for it in items:
        title = (it.get("title") or "").strip()
        url = (it.get("url") or "").strip()
        if not title:
            continue
        lines.append(f"{title}. Read more" if url else f"{title}")
    return "\n\n".join(lines) if lines else "—"

def build_newsletter(news, events):
    buckets = {"US": [], "EUROPE": [], "GLOBAL": []}
    for n in news:
        cat = (n.get("category") or "GLOBAL").upper()
        buckets.get(cat if cat in buckets else "GLOBAL").append(n)

    us = _bulletize(buckets["US"])
    eu = _bulletize(buckets["EUROPE"])
    gl = _bulletize(buckets["GLOBAL"])

    events_block = "\n".join(
        [
            f"🔸{e.get('title','').strip()}"
            + (f", {e['date']}" if e.get("date") else "")
            + (f", {e['location']}" if e.get("location") else "")
            + "."
            for e in events
            if e.get("title")
        ]
    ) or "—"

    header = dedent(
        """\
        Hi <<First name>>

        🔋✨ New issue of the NewStorage! 🚀 Discover the latest in energy storage and stay up to date with the trends of 2025. ⚡

        Forward this email to your colleagues in the sector and tell me what you think by replying directly. I'll read you! 😃
        """
    ).strip()

    body = dedent(
        f"""\
        {SECTION_LABELS['US']}:

        {us}

        {SECTION_LABELS['EUROPE']}:

        {eu}

        {SECTION_LABELS['GLOBAL']}:

        {gl}

        🤝FACE-TO-FACE EVENTS:

        {events_block}

        That concludes the updates for this month! 🙌

        We will be back next month with more insightful information about energy storage!

        Ian Casares | ATA Insights

        P.S. Follow us on LinkedIn
        """
    ).strip()

    return header + "\n\n" + body
