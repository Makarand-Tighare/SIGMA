const express = require("express");
const path = require("path");
const multer = require("multer");
const csv = require("csv-parser");
const fs = require("fs");
const ejs = require("ejs");
const regression = require("regression"); // For linear regression
const { plot } = require("nodeplotlib"); // For plotting

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views')); // Set the views directory
app.use(express.static(path.join(__dirname, 'public'))); // Serve static files from the "public" directory

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads');
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    }
});

const upload = multer({ storage });

app.get("/", (req, res) => {
    res.render("website");
});

app.post("/upload-csv", upload.single('csvFile'), (req, res) => {
    const filePath = req.file.path;
    // Implement the generateVisualization function
    generateVisualization(filePath)
        .then(visualizationData => {
            res.render("visualization", { visualizationData });
        })
        .catch(err => {
            res.send("Error generating visualization: " + err);
        });
});

app.get("/visualization", (req, res) => {
    res.render("visualization");
});

const port = 4000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

async function generateVisualization(filePath) {
    const data = await readCSVFile(filePath);

    // Prepare data for visualization (e.g., regression)
    const x = data.map(row => parseFloat(row.mpg));
    const y = data.map(row => parseFloat(row.hp));

    // Perform linear regression
    const result = regression.linear(x.map((value, index) => [value, y[index]]));

    // Extract regression line data
    const regressionData = result.points.map(point => ({ x: point[0], y: point[1] }));

    // Plot the data and regression line
    const chart = [
        { x: x, y: y, mode: 'markers', type: 'scatter', name: 'Data' },
        { x: regressionData.map(point => point.x), y: regressionData.map(point => point.y), mode: 'lines', type: 'scatter', name: 'Regression Line' }
    ];

    plot(chart);
    // You can save the plot to a file or return it as an image depending on your requirements.

    return `data:image/png;base64,${plot()}`; // Update this with the actual data
}

function readCSVFile(filePath) {
    return new Promise((resolve, reject) => {
        const results = [];

        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (data) => results.push(data))
            .on('end', () => {
                resolve(results);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}
