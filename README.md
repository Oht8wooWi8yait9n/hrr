# NASA Human Research Roadmap (HRR) Sitemaps

Automated crawler and sitemap repository indexing NASA's **Human Research Roadmap** ([`https://humanresearchroadmap.nasa.gov/`](https://humanresearchroadmap.nasa.gov/)), including all Human Research Program (**HRP**) Evidence Reports, Evidence Books, Spaceflight Risks, Research Gaps, and Research Tasks.

- **Primary Entry Point**: [`https://humanresearchroadmap.nasa.gov/`](https://humanresearchroadmap.nasa.gov/)
- **Repository**: [`https://github.com/Oht8wooWi8yait9n/hrr`](https://github.com/Oht8wooWi8yait9n/hrr)

---

## What is Indexed

The crawler systematically catalogs the complete HRP evidence and research architecture:

| Category | Count | Description & Key Contents |
| :--- | :--- | :--- |
| **Evidence Reports & Books (PDFs)** | **36 PDFs** | All formal HRP Evidence Books, Evidence Reports, ConOps appendices, and the current Integrated Research Plan (`IRP_Rev-Current.pdf`). Covers Cardiovascular, SANS, Immune, Bone Fracture, Renal, Pharm, Food/Nutrition, Behavioral Health/Team, Hypoxia/DCS, EVA Injury, and Dynamic Loads. |
| **Spaceflight Risk Pages** | **44 Pages** | Comprehensive risk overview dossiers (`/Risks/?i=...`), including mitigation strategies, risk postures across DRM classes, and links to relevant gaps. |
| **Research Gap Pages** | **193 Pages** | Individual gap descriptions (`/Gaps/?i=...`), detailing unresolved scientific questions and required knowledge deliverables. |
| **Research Task Pages** | **1,059 Pages** | Specific funded research investigations (`/Tasks/?i=...`) with principal investigators, experiment designs, and deliverable schedules. |
| **Architecture & Governance** | **18 Pages** | Program architecture, acronyms, reviews, MDRPs, and organization charts. |
| **Total Indexed Resources** | **1,350 Items** | **36 Canonical PDFs + 1,314 Web Documentation Pages** |

---

## Available Sitemaps & Feeds

All sitemaps conform to the standard [sitemaps.org 0.9 XML schema](http://www.sitemaps.org/schemas/sitemap/0.9).

1. **Full Consolidated Sitemap (PDFs + Risks + Gaps + Tasks + Overview)**:
   ```text
   https://raw.githubusercontent.com/Oht8wooWi8yait9n/hrr/main/hrr_sitemap.xml
   ```
   *(1,350 indexed URLs — Recommended for complete HRP research knowledge base coverage in Onyx)*

2. **Evidence Reports & Evidence Books Only (PDFs)**:
   ```text
   https://raw.githubusercontent.com/Oht8wooWi8yait9n/hrr/main/hrr_evidence_sitemap.xml
   ```
   *(36 formal PDF reports and books — Ideal if you only wish to index the authoritative synthesis documents)*

3. **Risks & Evidence Sitemap (Focused Risk Portfolio)**:
   ```text
   https://raw.githubusercontent.com/Oht8wooWi8yait9n/hrr/main/hrr_risks_sitemap.xml
   ```
   *(98 URLs — Focused on the 44 Spaceflight Risks and the 36 Evidence Reports without individual research tasks)*

4. **Plain Text URL List**:
   ```text
   https://raw.githubusercontent.com/Oht8wooWi8yait9n/hrr/main/hrr_urls.txt
   ```

---

## Onyx Web Connector Configuration

To index this entire collection into Onyx:

1. Navigate to **Onyx Admin** $\rightarrow$ **Connectors** $\rightarrow$ **Web**.
2. Click **Create Connector** and configure:
   - **Connector Name**: `NASA-Human-Research-Roadmap`
   - **Base URL**:
     ```text
     https://raw.githubusercontent.com/Oht8wooWi8yait9n/hrr/main/hrr_sitemap.xml
     ```
   - **Scrape Method**: Select **`sitemap`**
   - **Refresh Frequency**: `Weekly` (matches crawler schedule)
3. Save and trigger the initial crawl.

---

## Automated Weekly Updates

A GitHub Actions workflow ([`.github/workflows/update-sitemap.yml`](.github/workflows/update-sitemap.yml)) runs every **Sunday at 00:00 UTC** and can be triggered manually via `workflow_dispatch`.

It scans `humanresearchroadmap.nasa.gov`, detects newly released Evidence Reports, added risks, or updated tasks, regenerates all sitemaps, and automatically commits updates with `github-actions[bot] [skip ci]`.
