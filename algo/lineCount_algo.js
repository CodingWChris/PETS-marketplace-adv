// algorithm written in JavaScript/Node.js, based on Node.js v14

const fs = require('fs')

const inputFolder = '/data/inputs'
const outputFolder = '/data/outputs'

async function countrows(file) {
  console.log('Start counting for ' + file)
  const fileBuffer = fs.readFileSync(file)
  const toString = fileBuffer.toString()
  const splitLines = toString.split('\n')
  const rows = splitLines.length - 1
  fs.appendFileSync(outputFolder + '/output.log', file + ',' + rows + '\r\n')
  console.log('Finished. We have ' + rows + ' lines')
}

async function processfolder(folder) {
  const files = fs.readdirSync(folder)

  for (const i = 0; i < files.length; i++) {
    const file = files[i]
    const fullpath = folder + '/' + file
    if (fs.statSync(fullpath).isDirectory()) {
      await processfolder(fullpath)
    } else {
      await countrows(fullpath)
    }
  }
}

processfolder(inputFolder)