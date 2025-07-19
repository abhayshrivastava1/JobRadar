// // backend/server.js
// const express = require("express");
// const fs = require("fs");
// const path = require("path");
// const cors = require("cors");

// const app = express();
// const PORT = 5000;

// app.use(cors()); // Enable CORS for frontend

// const CSV_DIR = path.join(__dirname, "csv");

// // Utility: Get latest file of a given prefix
// function getLatestCsv(prefix) {
//   const files = fs
//     .readdirSync(CSV_DIR)
//     .filter((file) => file.startsWith(prefix) && file.endsWith(".csv"))
//     .map((file) => ({
//       name: file,
//       time: fs.statSync(path.join(CSV_DIR, file)).mtime.getTime(),
//     }))
//     .sort((a, b) => b.time - a.time);

//   return files.length > 0 ? files[0].name : null;
// }

// // Endpoint: Serve latest CSV file by type (filtered/manual)
// app.get("/api/latest-csv", (req, res) => {
//   const type = req.query.type;
//   if (!["filtered", "manual"].includes(type)) {
//     return res.status(400).send("Invalid type");
//   }

//   const latestFile = getLatestCsv(`${type}_`);
//   if (!latestFile) {
//     return res.status(404).send("No CSV found");
//   }

//   const filePath = path.join(CSV_DIR, latestFile);
//   res.sendFile(filePath);
// });

// app.listen(PORT, () => {
//   console.log(`✅ Server running on http://localhost:${PORT}`);
// });

// local backend/server.js
const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");

const app = express();
const PORT = 5000;

app.use(cors());

const OUTPUT_DIR = path.join(__dirname, "csv"); // ✅ Corrected path

function getLatestCSVData(type) {
  const files = fs.readdirSync(OUTPUT_DIR)
    .filter(f => f.includes(type) && f.endsWith(".csv")) // ✅ both types filtered separately
    .map(f => ({
      name: f,
      time: fs.statSync(path.join(OUTPUT_DIR, f)).mtime.getTime()
    }))
    .sort((a, b) => b.time - a.time);

  if (files.length === 0) return null;

  const latestFile = files[0].name;
  const data = [];

  return new Promise((resolve, reject) => {
    fs.createReadStream(path.join(OUTPUT_DIR, latestFile))
      .pipe(csv())
      .on("data", (row) => data.push(row))
      .on("end", () => {
        resolve({ filename: latestFile, data });
      })
      .on("error", reject);
  });
}

app.get("/csv", async (req, res) => {
  try {
    const [filteredJobs, manualReview] = await Promise.all([
      getLatestCSVData("filtered_jobs"),
      getLatestCSVData("manual_review")
    ]);

    res.json({
      filtered_jobs: filteredJobs || { filename: "", data: [] },
      manual_review: manualReview || { filename: "", data: [] }
    });
  } catch (err) {
    console.error("Error reading CSVs:", err);
    res.status(500).json({ error: "Failed to read CSV files" });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
