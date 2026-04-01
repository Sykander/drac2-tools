/**
 * This script takes the gvars listed in the sourcemap
 * and quickly converts them all into a dictionary for use in the 
 * `env` gvar
 */
const { readFileSync, writeFileSync } = require("fs");
const prodSourceMap = require('./sourcemap.prod.json');
const devSourceMap = require('./sourcemap.dev.json');

const environmentToUpdate = process.env.ENVIRONMENT === "Production"
  ? "Production"
  : "Development";

console.log(`${environmentToUpdate} starting update of env file.`);

const envFile = environmentToUpdate === "Production"
  ? "src/gvars/env.prod.gvar"
  : "src/gvars/env.dev.gvar";

const { gvars } = environmentToUpdate === "Production"
  ? prodSourceMap
  : devSourceMap;

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
