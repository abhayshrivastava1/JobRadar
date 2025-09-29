// sqlutils.js
const { openDb, allAsync } = require("./db");

/**
 * Get latest table name for a given prefix (e.g. 'filtered_jobs_' or 'manual_review_')
 * Returns table name string or null if none found.
 */
async function getLatestTableName(prefix) {
  const db = openDb(true);
  try {
    // Query sqlite_master for tables with given prefix, order by name desc (timestamped names are lexicographically sortable)
    const sql = `
      SELECT name FROM sqlite_master
      WHERE type='table' AND name LIKE ?
      ORDER BY name DESC
      LIMIT 1
    `;
    const likePattern = `${prefix}%`;
    const rows = await allAsync(db, sql, [likePattern]);
    return rows.length ? rows[0].name : null;
  } finally {
    db.close();
  }
}

/**
 * Get all rows from a given table (returns array of objects)
 */
async function getAllRowsFromTable(tableName) {
  if (!tableName) return [];
  const db = openDb(true);
  try {
    // Use parameterless query (table name can't be paramaterized), so validate tableName to be safe
    if (!/^[A-Za-z0-9_]+$/.test(tableName)) {
      throw new Error("Invalid table name");
    }
    const sql = `SELECT * FROM "${tableName}"`;
    const rows = await allAsync(db, sql);
    return rows;
  } finally {
    db.close();
  }
}

module.exports = {
  getLatestTableName,
  getAllRowsFromTable,
};
