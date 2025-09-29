**JobRadar** is a personal project demonstrating **automation, data processing, and full-stack integration** skills. It focuses on structured extraction and categorization of messages from chat sources.

> ⚠️ **Note:** This project is for **portfolio / technical demonstration only**. It is **not intended for public use**.

---

## Key Highlights

* **Automated Data Collection:** Gathers messages from chat sources programmatically.
* **Categorization & Filtering:** Separates messages into **filtered** (keyword-matched) and **manual review** categories.
* **Structured Storage:**

  * **CSV exports** for quick access and offline inspection.
  * **SQLite database** for scalable storage and querying.
* **Batching & Run Management:** Each run is timestamped, keeping datasets distinct.
* **Company Extraction:** Automatically extracts company names from messages for structured insights.
* **API-Ready Backend:** Node.js endpoints fetch latest datasets, ready for frontend integration.
* **Frontend-Ready:** React-compatible APIs for dashboard visualization.

---

## Technical Stack

* **Backend:** Python (scraping, filtering, CSV & SQLite storage)
* **Database:** SQLite for local structured storage
* **API Layer:** Node.js + Express
* **Frontend:** React (ready to consume structured data)
* **Utilities:** Pandas, CSV, regex-based company extraction

