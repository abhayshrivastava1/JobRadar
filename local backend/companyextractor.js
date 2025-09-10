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

  // Case 1: "X is hiring"
  let match = text.match(/(\w+)\s+is hiring/i);
  if (match) return match[1].trim();

  // Case 2: "at X"
  match = text.match(/\bat\s+(\w+)/i);
  if (match) return match[1].trim();

  return "Unknown";
}

module.exports = { extractCompany };
