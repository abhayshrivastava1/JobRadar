// const express = require("express");
// const path = require("path");
// const { readCSVWithCompany } = require("./csvutils");

// const router = express.Router();

// router.get("/api/filtered", async (req, res) => {
//   const folder = path.join(__dirname, "output");
//   const data = await readCSVWithCompany(folder, "filtered_jobs");

//   if (!data) return res.status(404).json({ error: "No filtered CSV found" });

//   res.json(data);
// });

// router.get("/api/manual", async (req, res) => {
//   const folder = path.join(__dirname, "output");
//   const data = await readCSVWithCompany(folder, "manual_review");

//   if (!data) return res.status(404).json({ error: "No manual CSV found" });

//   res.json(data);
// });

// module.exports = router;


// routes.js
const express = require("express");
const path = require("path");
const { getLatestTableName, getAllRowsFromTable } = require("./sqlutils");
const { extractCompany } = require("./companyextractor"); // adjust path if needed

const router = express.Router();

/**
 * Helper to fetch and attach Company field (keeps behaviour same as csvutils)
 */
function attachCompanyField(rows) {
  return rows.map(row => {
    // If your CSV column name differs (e.g., "Message" vs "message") map accordingly.
    // Here we try to detect common column names.
    const messageField = row.Message ?? row.message ?? row.msg ?? "";
    const company = extractCompany(messageField);
    // return a new object with Company field
    return { ...row, Company: company };
  });
}

router.get("/api/filtered", async (req, res) => {
  try {
    const prefix = "filtered_jobs_";
    const table = await getLatestTableName(prefix);
    if (!table) return res.status(404).json({ error: "No filtered table found" });

    const rows = await getAllRowsFromTable(table);
    const withCompany = attachCompanyField(rows);
    res.json(withCompany);
  } catch (err) {
    console.error("Error /api/filtered:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

router.get("/api/manual", async (req, res) => {
  try {
    const prefix = "manual_review_";
    const table = await getLatestTableName(prefix);
    if (!table) return res.status(404).json({ error: "No manual table found" });

    const rows = await getAllRowsFromTable(table);
    const withCompany = attachCompanyField(rows);
    res.json(withCompany);
  } catch (err) {
    console.error("Error /api/manual:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

module.exports = router;
