const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { spawn } = require('child_process');

const app = express();
const port = 3000;

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  },
});

const upload = multer({ storage: storage });

app.use(express.static('public'));
app.use(express.static('uploads'));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/upload', upload.single('csvFile'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('No file uploaded.');
    }

    const uploadedFilePath = req.file.path;

    const results = [];

    fs.createReadStream(uploadedFilePath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => {
        // Send the CSV data back as a response
        res.json(results);
      });

  } catch (error) {
    res.status(500).send(`Error processing CSV file: ${error}`);
  }
});

app.post('/run-model', upload.single('csvFile'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  const uploadedFilePath = req.file.path;
  const pythonProcess = spawn('python', ['model.py', uploadedFilePath]);

  let output = '';

  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Error from Python Script: ${data}`);
    res.status(500).send('Error running the model.');
  });

  pythonProcess.on('close', (code) => {
    if (code === 0) {
      res.send(output);
    } else {
      res.status(500).send('Model execution failed.');
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
