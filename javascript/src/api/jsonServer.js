// Import required modules
import axios from "axios"


// Private functions
function _getObj(target, meth = 'get', server = "http://mr-01:3000", head = { 'Accept': 'application/json' }) {
    axios({
        method: meth,
        url: server + target,
        headers: head
    }).then(response => {
        const output = {'status': true, 'data': response.data}
        return output
    }).catch(error => {
        const output = {'status': false, 'data': error}
        return output
    })
}

// Public functions

// Studies
const getAllStudies = () => {
    const restTarget = "/studies"
    const results =  _getObj(restTarget)
    console.log(results.data)
    return results
}

export default getAllStudies