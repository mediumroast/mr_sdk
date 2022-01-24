#!/usr/bin/env node

// Import required modules
import axios from "axios"
import chalk from "chalk"

// Define program wide variables
const server = "http://mr-01:3000"
const resource = "/studies"
const meth = "get"
const head = {
    'Accept': 'application/json'
}



// Make a RESTful call to the jsonserver
axios({
    method: meth,
    url: server + resource,
    headers: head
}).then(response => {
    const output = chalk.green(JSON.stringify(response.data, null, 2))
    console.log(output)
 }).catch(error => {
    const output = chalk.red(error)
    console.log(output)
 })
