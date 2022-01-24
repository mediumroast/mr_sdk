#!/usr/bin/env node

// Import required modules
import chalk from "chalk"
import getAllStudies from '../src/api/jsonServer.js'

// Make a RESTful call to the jsonserver
/* getAllStudies().then(response => {
    const data = JSON.stringify(response.data, null, 10)
    const output = chalk.green(data)
    console.log(output)
 }).catch(error => {
    const output = chalk.red(error)
    console.log(output)
 }) */

 const results = getAllStudies()
 console.log(results)
