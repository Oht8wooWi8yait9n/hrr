#!/usr/bin/env python3
"""
NASA Human Research Roadmap (HRR) Sitemap Generator
===================================================
Crawls https://humanresearchroadmap.nasa.gov/ to extract:
  1. All Human Research Program (HRP) Evidence Reports, Evidence Books, and Strategy Documents (PDFs).
  2. All Human Spaceflight Risk pages (/Risks/?i=...).
  3. All Research Gap pages (/Gaps/?i=...).
  4. All Research Task pages (/Tasks/?i=...).
  5. Architecture, Acronyms, Reviews, and Governance pages.

Generates:
  - hrr_sitemap.xml          (Full consolidated sitemap: PDFs + HTML pages)
  - hrr_evidence_sitemap.xml (PDF Evidence Reports & Evidence Books only)
  - hrr_risks_sitemap.xml    (Risks & Evidence only)
  - hrr_urls.txt             (Plain text newline-delimited list of all URLs)
"""

import sys
import re
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse, urlunparse, quote, unquote
import xml.etree.ElementTree as ET
import requests

BASE_URL = "https://humanresearchroadmap.nasa.gov"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

CORE_INDEX_PAGES = [
    f"{BASE_URL}/",
    f"{BASE_URL}/Evidence/",
    f"{BASE_URL}/Risks/",
    f"{BASE_URL}/Gaps/",
    f"{BASE_URL}/Tasks/",
    f"{BASE_URL}/Explore/",
    f"{BASE_URL}/MDRPs/",
    f"{BASE_URL}/Reports/",
    f"{BASE_URL}/architecture/",
    f"{BASE_URL}/acronyms/",
    f"{BASE_URL}/intro/",
    f"{BASE_URL}/orgchart/",
    f"{BASE_URL}/reviews/",
    f"{BASE_URL}/help/",
]


def normalize_url(url: str) -> str:
    """Normalize URL by stripping fragments and ensuring clean single percent-encoding."""
    clean = url.split("#")[0].strip()
    parsed = urlparse(clean)
    # Unquote first to prevent double-encoding (%2520 -> %20)
    clean_path = quote(unquote(parsed.path), safe="/:")
    return urlunparse((parsed.scheme, parsed.netloc, clean_path, parsed.params, parsed.query, ""))


def crawl_hrr():
    print("=" * 70)
    print(" NASA Human Research Roadmap (HRR) Crawler")
    print("=" * 70)

    session = requests.Session()
    session.headers.update(HEADERS)

    discovered_pdfs = set()
    discovered_risks = set()
    discovered_gaps = set()
    discovered_tasks = set()
    discovered_pages = set()

    # Always include the core IRP document
    discovered_pdfs.add(f"{BASE_URL}/Documents/IRP_Rev-Current.pdf")

    for page_url in CORE_INDEX_PAGES:
        print(f"[*] Crawling section: {page_url}...", flush=True)
        try:
            r = session.get(page_url, timeout=15)
            if r.status_code != 200:
                print(f"    [!] HTTP {r.status_code} for {page_url}")
                continue
            discovered_pages.add(normalize_url(page_url))

            for m in re.finditer(r'href=[\"\']([^\"\'#\s]+)[\"\']', r.text):
                href = m.group(1)
                full = urljoin(page_url, href)
                parsed = urlparse(full)

                if parsed.netloc != "humanresearchroadmap.nasa.gov":
                    continue

                # Skip web resources, icons, styles
                if any(ext in parsed.path.lower() for ext in [".css", ".js", ".png", ".jpg", ".ico", ".axd", ".json"]):
                    continue

                clean_url = normalize_url(full)

                if clean_url.lower().endswith(".pdf"):
                    discovered_pdfs.add(clean_url)
                elif "/risks/" in clean_url.lower() and "?i=" in clean_url:
                    discovered_risks.add(clean_url)
                elif "/gaps/" in clean_url.lower() and "?i=" in clean_url:
                    discovered_gaps.add(clean_url)
                elif "/tasks/" in clean_url.lower() and "?i=" in clean_url:
                    discovered_tasks.add(clean_url)
                else:
                    path_clean = parsed.path.rstrip("/")
                    if path_clean in ("", "/evidence", "/risks", "/gaps", "/tasks", "/explore", "/mdrps", "/reports", "/architecture", "/acronyms", "/intro", "/orgchart", "/reviews", "/help"):
                        discovered_pages.add(clean_url)

        except Exception as e:
            print(f"    [!] Error crawling {page_url}: {e}")

    print("\n" + "=" * 70)
    print(" HRR Content Discovery Summary:")
    print("=" * 70)
    print(f"  Evidence Reports & Books (PDFs): {len(discovered_pdfs)}")
    print(f"  Risk Overview Pages:            {len(discovered_risks)}")
    print(f"  Research Gap Pages:             {len(discovered_gaps)}")
    print(f"  Research Task Pages:            {len(discovered_tasks)}")
    print(f"  Core Architecture & Info Pages: {len(discovered_pages)}")
    total = len(discovered_pdfs) + len(discovered_risks) + len(discovered_gaps) + len(discovered_tasks) + len(discovered_pages)
    print(f"  Total Indexed Items:            {total}")
    print("=" * 70)

    return (
        sorted(discovered_pdfs),
        sorted(discovered_risks),
        sorted(discovered_gaps),
        sorted(discovered_tasks),
        sorted(discovered_pages),
    )


def build_sitemap_xml(urls: list[str], output_path: str):
    """Build a sitemaps.org compliant XML sitemap."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for url in urls:
        url_elem = ET.SubElement(root, "url")
        loc_elem = ET.SubElement(url_elem, "loc")
        loc_elem.text = url
        lastmod_elem = ET.SubElement(url_elem, "lastmod")
        lastmod_elem.text = today

    xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with open(output_path, "wb") as f:
        f.write(xml_bytes)
        f.write(b"\n")
    print(f"[+] Written {len(urls)} URLs to {output_path}")


def main():
    pdfs, risks, gaps, tasks, pages = crawl_hrr()

    # 1. Full Consolidated Sitemap (All URLs)
    all_urls = sorted(set(pdfs + risks + gaps + tasks + pages))
    build_sitemap_xml(all_urls, "hrr_sitemap.xml")

    # 2. Evidence Reports & Strategy Documents Only (PDFs)
    build_sitemap_xml(pdfs, "hrr_evidence_sitemap.xml")

    # 3. Risks & Evidence Sitemap (Focused on Program Risks + Reports)
    risks_and_evidence = sorted(set(pdfs + risks + pages))
    build_sitemap_xml(risks_and_evidence, "hrr_risks_sitemap.xml")

    # 4. Plain Text URL List
    with open("hrr_urls.txt", "w", encoding="utf-8") as f:
        for u in all_urls:
            f.write(f"{u}\n")
    print(f"[+] Written full URL list to hrr_urls.txt")


if __name__ == "__main__":
    main()
