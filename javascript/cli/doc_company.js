#!/usr/bin/env node

// Import required modules
import { Companies, Interactions } from '../src/api/highLevel.js'
//import { Reports as IntReports } from '../src/report/interactions.js'
import Utilities from '../src/report/common.js'
import program from 'commander'
import ConfigParser from 'configparser'
import * as fs from "fs"
import docx from 'docx'


//  ______   __  __     __   __     ______     ______   __     ______     __   __     ______    
// /\  ___\ /\ \/\ \   /\ "-.\ \   /\  ___\   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   /\  ___\   
// \ \  __\ \ \ \_\ \  \ \ \-.  \  \ \ \____  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  \ \___  \  
//  \ \_\    \ \_____\  \ \_\\"\_\  \ \_____\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\  \/\_____\ 
//   \/_/     \/_____/   \/_/ \/_/   \/_____/     \/_/   \/_/   \/_____/   \/_/ \/_/   \/_____/ 
                                                                                             
// Parse the cli options
function parseCLIArgs() {
    // Define commandline options
    program
        .version('0.7.5')
        .description('A CLI to generate a document report for mediumroast.io Company objects.')
    program
        .requiredOption('-g --guid <guid>', 'The GUID for the company to construct a report for.')
        .option('-r --report_dir <directory>', 'Directory to write the report to', 'Documents')
        .option('-w --work_dir <directory>', 'Directory to use for creating a ZIP package', '~/Documents')
        .option('-z --zip_package', 'Create a zip package with interactions')
        .option('-s --server <server>', 'Specify the server URL', 'http://mr-01:3000')
        .option('-t --server_type <type>', 'Specify the server type as [json || mr_server]', 'json')
        .option('-c --config_file <file>', 'Path to the configuration file', '.mr_config')
    program.parse(process.argv)
    const options = program.opts()
    return options
}

// Filter objects by the GUID of the Company
function filterInteractions(objects, guid) {
    let myInteractions = []
    for (const object in objects) {
        const allCompanies = Object.values(objects[object].linkedCompanies)
        if (allCompanies.includes(guid)) {
            myInteractions.push(objects[object])
        }
    }
    return myInteractions
}


//  ______     ______     __   __     ______   __     ______    
// /\  ___\   /\  __ \   /\ "-.\ \   /\  ___\ /\ \   /\  ___\   
// \ \ \____  \ \ \/\ \  \ \ \-.  \  \ \  __\ \ \ \  \ \ \__ \  
//  \ \_____\  \ \_____\  \ \_\\"\_\  \ \_\    \ \_\  \ \_____\ 
//   \/_____/   \/_____/   \/_/ \/_/   \/_/     \/_/   \/_____/ 
                                                                    
// Get the configuration objects
const opts = parseCLIArgs() // CLI arguments and options
const config = new ConfigParser() // Config file
config.read(process.env.HOME + '/' + opts.config_file)

// Set the server type
let serverType = null
config.hasKey('DEFAULT', 'server_type') ? serverType = config.get('DEFAULT', 'server_type') : serverType = opts.server_type

// Set the server url
let mrServer = null
config.hasKey('DEFAULT', 'server') ? mrServer = config.get('DEFAULT', 'server') : mrServer = opts.server

// Set the working directory
let workDir = null
config.hasKey('DEFAULT', 'working_dir') ? workDir = config.get('DEFAULT', 'working_dir') : workDir = opts.work_dir

// Set the output directory
let outputDir = null
config.hasKey('DEFAULT', 'output_dir') ? outputDir = process.env.HOME + '/' + config.get('DEFAULT', 'output_dir') : outputDir = process.env.HOME + '/' + opts.output_dir


// Determine if we need to create a zip package or not
let createZIP = null
opts.zip ? createZIP = true : createZIP = false

// Set up the control objects
const companyCtl = new Companies(mrServer, serverType)
const interactionCtl = new Interactions(mrServer, serverType)
const docCtl = new Utilities(
    config.get('document_notices', 'copyright'),
    config.get('document_settings', 'font_type'),
    parseInt(config.get('document_settings', 'font_size'))
)

// Get the company in question and all interactions
const company = await companyCtl.getByGUID(opts.guid)
const interactions = filterInteractions(await interactionCtl.getAll(), opts.guid)

//  __    __     ______     __     __   __        ______     __         __    
// /\ "-./  \   /\  __ \   /\ \   /\ "-.\ \      /\  ___\   /\ \       /\ \   
// \ \ \-./\ \  \ \  __ \  \ \ \  \ \ \-.  \     \ \ \____  \ \ \____  \ \ \  
//  \ \_\ \ \_\  \ \_\ \_\  \ \_\  \ \_\\"\_\     \ \_____\  \ \_____\  \ \_\ 
//   \/_/  \/_/   \/_/\/_/   \/_/   \/_/ \/_/      \/_____/   \/_____/   \/_/ 

const outputFile = outputDir + '/' + company.companyName 
const outputDocFileName = outputFile + '.docx'
const doc = docCtl.initDoc(
    company.companyName, 
    company.description
)

doc.sections=[{
    //properties: {},
    children: [
        new docx.Paragraph({text: company.companyName})
    ]
}]

// If needed create the zip package
if (createZIP) {
    const outputPackage = outputFile + '.zip'
} else {
    docx.Packer.toBuffer(doc).then((buffer) => {
        fs.writeFileSync(outputDocFileName, buffer)
    });
}