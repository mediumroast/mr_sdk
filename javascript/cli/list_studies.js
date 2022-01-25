#!/usr/bin/env node

// Import required modules
import Studies from '../src/api/jsonServer.js'
import program from 'commander'

// Parse the cli options
function parseCLIArgs() {
   // Define commandline options
   program.version('0.7.5')
   program
      .option('-g --get_guids', 'List all Studies by Name')
      .option('-n --get_names', 'List all Studies by GUID')
      .option('-m --get_map', 'List all Studies by {Name:GUID}')
      .option('--get_by_name <name>', 'Get an individual Study by name')
      .option('--get_by_guid <GUID>', 'Get an individual Study by GUID')
      .option('-s --server <server>', 'Specify the server URL')
   program.parse(process.argv)
   const options = program.opts()
   return options
}

// The business end of the cli
const opts = parseCLIArgs()
const studiesControl = new Studies()
let results = null
if (opts.get_guids) {
   results = await studiesControl.getAllGUIDs()
} else if (opts.get_names) {
   results = await studiesControl.getAllNames()
} else if (opts.get_map) {
   results = await studiesControl.getNamesAndGUIDs()
} else if (opts.get_by_guid) {
   results = await studiesControl.getByGUID(opts.get_by_guid)
} else if (opts.get_by_name) {
   results = await studiesControl.getByName(opts.get_by_name)
} else {
   results = await studiesControl.getAll()
}

console.log(results)
