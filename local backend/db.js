// db.js
const sqlite3 = require("sqlite3").verbose();
const path = require("path");


const DB_PATH = path.join(__dirname, "output", "JobRadar.sqlite");

// open readonly by default for queries; use normal for writes
function openDb(readonly = true) {
  const mode = readonly
    ? sqlite3.OPEN_READONLY
    : sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE;
  return new sqlite3.Database(DB_PATH, mode);
}

/**
 * Run a query that returns all rows (promisified)
 */
function allAsync(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) return reject(err);
      resolve(rows);
    });
  });
}

/**
 * Run a query that returns single row
 */
function getAsync(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) return reject(err);
      resolve(row);
    });
  });
}

module.exports = {
  openDb,
  allAsync,
  getAsync,
  DB_PATH,
};
