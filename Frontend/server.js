const express = require("express");
const multer = require("multer");
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const app = express();
const port = 3000;

app.use(express.json());

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads/");
  },
  filename: function (req, file, cb) {
    cb(null, file.fieldname + "-" + Date.now() + path.extname(file.originalname));
  },
});

const upload = multer({ storage: storage });

app.use(express.static("public"));
app.use(express.static("uploads"));
app.use(express.static("downloads")); // Serve the downloads directory

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});
app.get("/table", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "table.html"));
});
app.get("/analyse", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "analyse.html"));
});

app.get("/new", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "new.html"));
});
app.get("/predictor", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "predictor.html"));
});

app.get("/chat", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "chat.html"));
});

app.post("/upload", upload.single("csvFile"), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send("No file uploaded.");
    }

    const uploadedFilePath = req.file.path;

    const pythonProcess = spawn("python", ["model.py", uploadedFilePath]);

    let jsonData = "";

    pythonProcess.stdout.on("data", (data) => {
      jsonData += data.toString();
    });

    pythonProcess.stdout.on("end", () => {
      const parsedData = JSON.parse(jsonData);
      // Generate a unique filename for the JSON file
      const filename = `output-${Date.now()}.json`;
      const filePath = path.join(__dirname, "downloads", filename);

      // Write the JSON data to the file
      fs.writeFileSync(filePath, JSON.stringify(parsedData, null, 2));

      // Create a download link for the JSON file
      const downloadLink = `/downloads/${filename}`;

      res.json({ jsonData, downloadLink });
    });

    pythonProcess.stderr.on("data", (data) => {
      res.status(500).json({ error: data.toString() });
    });
  } catch (error) {
    res.status(500).send(`Error processing CSV file: ${error}`);
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
