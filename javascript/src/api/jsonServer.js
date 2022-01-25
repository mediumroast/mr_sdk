// Import required modules
import axios from "axios"
import Utils from '../helpers.js'


// TODO this is deprecated and moved to helpers remove after testing
/* const getObj = async(target, server = "http://mr-01:3000") => {
    const myURL = server + target
    try {
        const resp = await axios.get(myURL)
        return (true, resp.data)
    } catch (err) {
        console.error(err)
        return (false, err)
    }
} 
*/

// Study methods
class Studies {
    constructor (resource = '/studies') {
        this.resource = resource
        this.util = Utils()
    }
    
    // Get all information about all studies
    async getAll () {
        return this.util.getObj(this.resource)
    }

    // Get only GUIDs -> Name mappings for all studies
    async getAllGUIDs () {
        const response = this.util.getObj(this.resource)
        let filteredList = Array()
        for (const study in response.data) {
            filteredList.push({'GUID': study.GUID})
        }
        return filteredList
    }

    // Get only Names-> GUIDs mappings for all studies
    async getAllNames () {
        const response = this.util.getObj(this.resource)
        let filteredList = Array()
        for (const study in response.data) {
            filteredList.push({'studyName': study.studyName})
        }
        return filteredList
    }

    // Get all information about a single study using the study's name
    async getStudyByName (name) {
        const restTarget = this.resource + '?studyName=' + name
        return this.util.getObj(restTarget)
    }

    // Get all information about a single study using the study's GUID
    async getStudyByGUID (guid) {
        const restTarget = this.resource + '?GUID=' + guid
        return this.util.getObj(restTarget)
    }

    // Using the study GUID return the name
    async getNameByGUID (guid) {
        const restTarget = this.resource + '?GUID=' + guid
        const response = this.util.getObj(restTarget)
        return {'studyName': response.data.studyName, 'GUID': response.data.GUID}
    }

    // Using the study name return the GUID
    async getGUIDByName (name) {
        const restTarget = this.resource + '?studyName=' + name
        const response = this.util.getObj(restTarget)
        return {'GUID': response.data.GUID, 'studyName': response.data.studyName}
    }
}

export default Studies