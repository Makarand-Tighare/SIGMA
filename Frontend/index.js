const express = require("express");
const path = require("path");

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.set('view engine', 'ejs');

app.use(express.static("public"));

app.get("/", (req, res) => {
    res.render("website");
});


app.get("/ind", (req, res) => {
    res.render("ind"); 
});

const port = 4000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
