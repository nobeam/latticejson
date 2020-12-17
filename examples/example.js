const fs = require('fs');
const data = JSON.parse(fs.readFileSync("fodo.json"));

const elementName = "Q1";
const [type, { length }] = data.elements[elementName];
console.log(`The element ${elementName} is a ${type} and is ${length} meters long.`);
