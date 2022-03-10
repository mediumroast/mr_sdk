#!/usr/bin/env node

// Import required modules
import { Companies, Interactions } from '../src/api/highLevel.js'
import {Reports as IntReports} from '../src/report/interactions.js'
import program from 'commander'

// Parse the cli options
function parseCLIArgs() {
    // Define commandline options
    program
        .version('0.7.5')
        .description('A CLI to generate a document report for mediumroast.io Company objects.')
    program
        .requiredOption('-g --guid', 'The GUID for the company to construct a report for.')
        .option('-n --report_path', 'The full path name for the report')
        // TODO Create a boolean option for building a ZIP package
        .requiredOption('-s --server <server>', 'Specify the server URL', 'http://mr-01:3000')
        .requiredOption('-t --server_type <type>', 'Specify the server type as [json || mr_server]', 'json')
        .requiredOption('-c --config_file <file>', 'Path to the configuration file', '~/.mr_config')
    program.parse(process.argv)
    const options = program.opts()
    return options
}

function filterInteractions(interactions, guid) {
    let myInteractions = []
    for (const interaction in interactions) {
        //TODO finish the filtering
        null
    }
    return myInteractions
}

// The business end of the cli
const opts = parseCLIArgs()
const serverType = opts.server_type // TODO augment with the CLI config file
const mrServer = opts.server // TODO augment with the CLI config file
// TODO set the default output file name

// Set up the control objects
const companyCtl = new Companies(mrServer, serverType)
const interactionCtl = new Interactions(mrServer, serverType)

// Get the company in question and all interactions
const company = await companyCtl.getByGUID(opts.guid)
const interactions = filterInteractions(await interactionCtl.getAll(), guid)