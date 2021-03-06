#!/usr/bin/env node

// Import required modules
import {Interactions} from '../src/api/highLevel.js'
import program from 'commander'

// Parse the cli options
function parseCLIArgs() {
   // Define commandline options
   program
      .version('0.7.5')
      .description('A CLI for mediumroast.io Interaction objects, without options: list all Interactions.')
   program
      .option('-g --get_guids', 'List all Interactions by Name')
      .option('-n --get_names', 'List all Interactions by GUID')
      .option('-m --get_map', 'List all Interactions by {Name:GUID}')
      .option('--get_by_name <name>', 'Get an individual Interaction by name')
      .option('--get_by_guid <GUID>', 'Get an individual Interaction by GUID')
      .requiredOption('-s --server <server>', 'Specify the server URL', 'http://mr-01:3000')
      .requiredOption('-t --server_type <type>', 'Specify the server type as [json || mr_server]','json')
      .requiredOption('-c --config_file <file>', 'Path to the configuration file','~/.mr_config')
   program.parse(process.argv)
   const options = program.opts()
   return options
}

// The business end of the cli
const byNameResource = '?interactionName='
const opts = parseCLIArgs()
const serverType = opts.server_type // TODO eventually augment with the CLI config file
const mrServer = opts.server // TODO eventually augment with the CLI config file
const control = new Interactions(mrServer, serverType)
let results = null
if (opts.get_guids) {
   results = await control.getAllGUIDs()
} else if (opts.get_names) {
   results = await control.getAllNames()
} else if (opts.get_map) {
   results = await control.getNamesAndGUIDs()
} else if (opts.get_by_guid) {
   results = await control.getByGUID(opts.get_by_guid)
} else if (opts.get_by_name) {
   results = await control.getByName(opts.get_by_name, byNameResource)
} else {
   results = await control.getAll()
}

console.log(results)
