const { deploy } = require('publish-avrae');
const prodSourceMap = require('./sourcemap.json');

const sourceMap = prodSourceMap;

console.log('Starting Deployment');
deploy(sourceMap)
  .then(() => console.log('Deployment Sucessful'))
  .catch((e) => {
    console.error(e);
    console.log('Deployment Failed');
    process.exit(1);
  });
