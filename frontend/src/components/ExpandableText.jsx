import React, { useState } from "react";

export default function ExpandableText({ text }) {
  const [expanded, setExpanded] = useState(false);

  if (!text) return null;

  // 1. "Apply now" (with optional ":") remove only if just before a link
  let cleanedText = text.replace(/Apply\s+now:?\s*(?=https?:\/\/)/gi, "");

  // 2. Remove all https:// links and everything till next space
  cleanedText = cleanedText.replace(/https?:\/\/\S+/gi, "");

  const words = cleanedText.trim().split(/\s+/);
  const isLong = words.length > 30;
  const preview = words.slice(0, 30).join(" ") + (isLong ? "..." : "");

  return (
    <div>
      <span>{expanded || !isLong ? cleanedText : preview}</span>
      {isLong && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="ml-2 text-blue-600 hover:underline text-xs"
        >
          {expanded ? "Read Less" : "Read More"}
        </button>
      )}
    </div>
  );
}
