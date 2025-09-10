const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");
const { extractCompany } = require("./companyextractor");

function getLatestFile(folderPath, prefix) {
  const files = fs
    .readdirSync(folderPath)
    .filter((file) => file.startsWith(prefix) && file.endsWith(".csv"))
    .map((file) => ({
      name: file,
      time: fs.statSync(path.join(folderPath, file)).mtime.getTime(),
    }))
    .sort((a, b) => b.time - a.time);

  return files.length ? files[0].name : null;
}

async function readCSVWithCompany(folder, prefix) {
  const latestFile = getLatestFile(folder, prefix);
  if (!latestFile) return null;

  const results = [];
  const stream = fs.createReadStream(path.join(folder, latestFile)).pipe(csv());

  for await (const data of stream) {
    data.Company = extractCompany(data["Message"]);
    results.push(data);
  }

  return results;
}

module.exports = { getLatestFile, readCSVWithCompany };
