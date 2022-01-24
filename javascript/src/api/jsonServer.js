// Import required modules
import axios from "axios"


// Private functions
const getObj = async(target, server = "http://mr-01:3000", head = { 'Accept': 'application/json' }) => {
    const myURL = server + target
    try {
        const resp = await axios.get(myURL)
        return (true, resp.data)
    } catch (err) {
        console.error(err)
        return (false, err)
    }
}

// Public functions

// Studies
// Get all information about all studies
const getAllStudies = async () => {
    const restTarget = "/studies"
    return getObj(restTarget)
}

// Get all information about a single study using the study's name
const getStudyByName = async (name) => {
    const restTarget = '/studies?studyName=' + name
    return getObj(restTarget)
}

// Get all information about a single study using the study's GUID
const getStudyByGUID = async (guid) => {
    const restTarget = '/studies?GUID=' + guid
    return getObj(restTarget)
}

export default getAllStudies