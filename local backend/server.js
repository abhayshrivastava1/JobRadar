
const express = require("express");
const fs = require("fs");
const path = require("path");
const cors = require("cors");
const csv = require("csv-parser");

const app = express();
app.use(cors());

// -----------------------
// Company extraction logic in JS
// -----------------------
function preprocess(text) {
  return text
    .replace(/\|/g, " ")
    .replace(/-/g, " ")
    .replace(/—/g, " ")
    .replace(/\n/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractCompany(text) {
  text = preprocess(text);

  // 1. "X is hiring" → first two words
  let match = text.match(/\b([\w&.\-]+(?:\s+[\w&.\-]+)?)(?=\s+is hiring)/i);
  if (match) return match[1].trim();

  // 2. "at X" → first two words after "at"
  match = text.match(/\bat\s+([A-Za-z&.\-]+(?:\s+[A-Za-z&.\-]+)?)/i);
  if (match) return match[1].trim();

  return "Unknown";
}

// -----------------------
// CSV API endpoints
// -----------------------
app.get("/api/filtered", async (req, res) => {
  const results = [];
  const stream = fs
    .createReadStream(path.join(__dirname, "output/filtered_jobs.csv"))
    .pipe(csv());

  for await (const data of stream) {
    data.Company = extractCompany(data["Message"]);
    results.push(data);
  }

  res.json(results);
});

app.get("/api/manual", async (req, res) => {
  const results = [];
  const stream = fs
    .createReadStream(path.join(__dirname, "output/manual_review.csv"))
    .pipe(csv());

  for await (const data of stream) {
    data.Company = extractCompany(data["Message"]);
    results.push(data);
  }

  res.json(results);
});

app.listen(5000, () =>
  console.log(" Server running on http://localhost:5000")
);
