const express = require("express");
const cors = require("cors");
const routes = require("./routes");

const app = express();
app.use(cors());
app.use(routes);

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
