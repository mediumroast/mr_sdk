// Import required modules
import Utils from '../helpers.js'

// Study methods
class Studies {
    constructor (resource = '/studies', server = 'http://mr-01:3000') {
        this.resource = resource
        this.server = server
        this.util = new Utils(server = this.server)
    }
    
    // Get all information about all studies
    async getAll () {
        return this.util.getObj(this.resource)
    }

    // Get only GUIDs for all studies
    async getAllGUIDs () {
        const response = await this.util.getObj(this.resource)
        let filteredList = Array()
        for (const study in response) {
            filteredList.push({'GUID': response[study].GUID})
        }
        return filteredList
    }

    // TODO Consider how to make the above a base case and then Studies et al become subclasses

    // Get only Names for all studies
    async getAllNames () {
        const response = await this.util.getObj(this.resource)
        let filteredList = Array()
        for (const study in response) {
            filteredList.push({'studyName': response[study].studyName})
        }
        return filteredList
    }

    // Get only Names -> GUIDs mappings for all studies
    async getNamesAndGUIDs () {
        const response = await this.util.getObj(this.resource)
        let filteredList = Array()
        for (const study in response) {
            let entry = {}
            entry[response[study].studyName] = response[study].GUID
            filteredList.push(entry)
        }
        return filteredList
    }

    // Get all information about a single study using the study's name
    async getByName (name) {
        const restTarget = this.resource + '?studyName=' + name
        return this.util.getObj(restTarget)
    }

    // Get all information about a single study using the study's GUID
    async getByGUID (guid) {
        const restTarget = this.resource + '?GUID=' + guid
        return this.util.getObj(restTarget)
    }

    // Using the study GUID return the name
    async getNameByGUID (guid) {
        const restTarget = this.resource + '?GUID=' + guid
        const response = await this.util.getObj(restTarget)
        return {'studyName': response.data.studyName, 'GUID': response.data.GUID}
    }

    // Using the study name return the GUID
    async getGUIDByName (name) {
        const restTarget = this.resource + '?studyName=' + name
        const response = await this.util.getObj(restTarget)
        return {'GUID': response.data.GUID, 'studyName': response.data.studyName}
    }
}



export default Studies