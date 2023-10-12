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

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/upload", upload.single("csvFile"), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send("No file uploaded.");
    }

    const uploadedFilePath = req.file.path;

    const pythonProcess = spawn("python", ["model.py", uploadedFilePath]);

    pythonProcess.stdout.on("data", (data) => {
      const jsonData = JSON.parse(data.toString());
      res.json(jsonData);
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
