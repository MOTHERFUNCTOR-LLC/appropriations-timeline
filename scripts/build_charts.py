#!/usr/bin/env python3
"""Build both SVG charts from the canonical CSV; Python standard library only."""
import csv
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'data/appropriations.csv').open(newline='') as f:
    ALL_ROWS=list(csv.DictReader(f))
for row in ALL_ROWS:
    for field in ('fiscal_year','days_after_october_1','days_late'):
        row[field]=int(row[field])
    elapsed=(date.fromisoformat(row['enactment_date'])-date.fromisoformat(row['fiscal_year_start'])).days
    if row['days_after_october_1'] != elapsed or row['days_late'] != max(0,elapsed):
        raise ValueError(f"Incorrect day count for fiscal year {row['fiscal_year']}")
if [r['fiscal_year'] for r in ALL_ROWS] != list(range(1997,2027)):
    raise ValueError('Expected one chronological row per fiscal year, 1997–2026')
def draw(start_year):
    rows=[r for r in ALL_ROWS if r['fiscal_year']>=start_year]
    G='#4cbb17';FG='#404040';BG='#fafafa';M='#737373'
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="800" viewBox="0 0 1600 800" role="img" aria-labelledby="title desc">', '<title id="title">Last on time? 1996.</title>','<desc id="desc">Bar chart of days late for fiscal years 1997 through 2026. Fiscal year 1997 was completed September 30, 1996, one day before its start, shown as zero days late. Every subsequent fiscal year finished late. Fiscal year 2026 uses April 30; separate immigration-enforcement funding followed June 10.</desc>',f'<rect width="1600" height="800" rx="22" fill="{BG}"/>',f'<g font-family="Menlo,DejaVu Sans Mono,monospace" fill="{FG}">',f'<rect x="55" y="40" width="14" height="20" rx="3" fill="{G}"/>','<text x="81" y="56" font-size="17" font-weight="bold" letter-spacing="2">MOTHERFUNCTOR</text>','<text x="55" y="112" font-size="38" font-weight="bold" letter-spacing="-1.4">Last on time? 1996.</text>',f'<text x="55" y="150" font-size="19" fill="{M}">29 straight fiscal years finished late · fiscal years 1998–2026</text>',f'<rect x="55" y="174" width="380" height="40" rx="20" fill="{G}"/>','<text x="245" y="200" text-anchor="middle" font-size="17" font-weight="bold">FY1997: signed Sept. 30, 1996</text>']
    x0=90;step=1440/len(rows);w=min(42,step*.61);base=605;scale=1.38
    for n in [0,60,120,180,240]:
     y=base-n*scale
     s.append(f'<path d="M75 {y} H1530" stroke="#d4d4d8" stroke-width="1"/>')
     s.append(f'<text x="62" y="{y+5}" text-anchor="end" font-size="14" fill="{M}">{n}</text>')
    for i,r in enumerate(rows):
     x=x0+i*step;d=r['days_late'];y=base-d*scale
     
     if d==0:s.append(f'<circle cx="{x+w/2}" cy="{base}" r="7" fill="{BG}" stroke="{G}" stroke-width="4"/>')
     s.extend([f'<rect x="{x}" y="{y:.2f}" width="{w}" height="{base-y:.2f}" rx="5" fill="{G}"/>',f'<text x="{x+w/2}" y="{y-12:.2f}" text-anchor="middle" font-size="15" font-weight="bold">{d}</text>',f'<text x="{x+w/2}" y="633" text-anchor="middle" font-size="11">{r["fiscal_year"]}{"*" if r["fiscal_year"]==2026 else ""}</text>'])
    s.extend(['<text x="800" y="665" text-anchor="middle" font-size="15">Fiscal year · measured from its October 1 start</text>',f'<text x="55" y="706" font-size="14" fill="{M}">Last regular appropriations measure or full-year continuing resolution. These are not shutdown days.</text>',f'<text x="55" y="731" font-size="14" fill="{M}">*2026: April 30 enactment; separate immigration-enforcement funding followed June 10 (252 days late).</text>','<a href="https://www.congress.gov/crs-product/R47235"><text x="55" y="765" font-size="13" fill="#525252">Sources: Congressional Research Service; enacted public laws, U.S. Government Publishing Office.</text></a>','</g></svg>'])
    svg='\n'.join(s)
    if start_year == 2007:
        svg=svg.replace('Last on time? 1996.','Twenty years. Zero on-time finishes.').replace('29 straight fiscal years finished late · fiscal years 1998–2026','Days late for final annual appropriations · fiscal years 2007–2026').replace('FY1997: signed Sept. 30, 1996','138 days late, on average')
        svg=svg.replace('Bar chart of days late for fiscal years 1997 through 2026. Fiscal year 1997 was completed September 30, 1996, one day before its start, shown as zero days late. Every subsequent fiscal year finished late.','Bar chart of days late for fiscal years 2007 through 2026. Every year finished late. Average 138 days.')
    output=ROOT/'charts'/f'motherfunctor-days-late-{start_year}-2026.svg'
    output.parent.mkdir(exist_ok=True)
    output.write_text(svg)
    print(output)

if __name__=='__main__':
    for start in (1997,2007):
        draw(start)
