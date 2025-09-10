const express = require("express");
const path = require("path");
const { readCSVWithCompany } = require("./csvutils");

const router = express.Router();

router.get("/api/filtered", async (req, res) => {
  const folder = path.join(__dirname, "output");
  const data = await readCSVWithCompany(folder, "filtered_jobs");

  if (!data) return res.status(404).json({ error: "No filtered CSV found" });

  res.json(data);
});

router.get("/api/manual", async (req, res) => {
  const folder = path.join(__dirname, "output");
  const data = await readCSVWithCompany(folder, "manual_review");

  if (!data) return res.status(404).json({ error: "No manual CSV found" });

  res.json(data);
});

module.exports = router;
