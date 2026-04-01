/**
 * This script takes the gvars listed in the sourcemap
 * and quickly converts them all into a dictionary for use in the 
 * `env` gvar
 */
const { readFileSync, writeFileSync } = require("fs");
const prodSourceMap = require('./sourcemap.json');

const environmentToUpdate = "Production";

console.log(`${environmentToUpdate} starting update of env file.`);

const envFile = "src/gvars/env.gvar";

const { gvars } = prodSourceMap;

const envDict = gvars.reduce((acc, {id, name}) => {
    acc[name] = id;
    return acc
}, {})

const jsonEnvDict = JSON.stringify(envDict)

const envFileContents = readFileSync(envFile).toString()

const gvarRegex = /gvars\s=\s\{.*\}/ig

const newEnvFileContents = envFileContents.replace(gvarRegex, `gvars = ${jsonEnvDict}`)

writeFileSync(envFile, newEnvFileContents);

console.log(`${environmentToUpdate} env file updated.`);
