// Import required modules
import Utils from '../helpers.js'

// Study methods
class MRObjectJSON {
    constructor (resource, server = 'http://mr-01:3000') {
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
    async getByName (name, subResource) {
        const restTarget = this.resource + subResource + name
        return this.util.getObj(restTarget)
    }

    // Get all information about a single study using the study's GUID
    async getByGUID (guid, subResource = '?GUID=') {
        const restTarget = this.resource + subResource + guid
        return this.util.getObj(restTarget)
    }

    // Using the study GUID return the name
    async getNameByGUID (guid, subResource = '?GUID=') {
        const restTarget = this.resource + subResource + guid
        const response = await this.util.getObj(restTarget)
        return {'studyName': response.data.studyName, 'GUID': response.data.GUID}
    }

    // Using the study name return the GUID
    async getGUIDByName (name, subResource = '?studyName=') {
        const restTarget = this.resource + subResource + name
        const response = await this.util.getObj(restTarget)
        return {'GUID': response.data.GUID, 'studyName': response.data.studyName}
    }

    // TODO implement patch and put functions to add and update resources
    // NOTE highLevel should implement methods that do things like affect all
    //      objects in a class.
    //
    // NOTE As we are thinking about the test suite for this module we'd need to
    //      follow the approach of implementing:
    //          1. put, read, check
    //          2. patch, read, check
    //          3. delete, read, check
    //      This would be done by specifying the min object for insertion.  We will
    //      also need to take care of which kind of backend is added.  When we start
    //      to create tests the backend server needs to be operable, and this doc needs
    //      to be moved to the right location.
}

// Studies implementation of the MRObject base class
export class StudiesJSON extends MRObjectJSON {
    constructor(server, resource = '/studies') {
        super(resource, server)
    }

    // For all studies filter in only the substudies and return
    async getAllSubstudies () {
        const response = await this.util.getObj(this.resource)
        let filteredList = Array()
        for (const study in response) {
            let entry = {}
            entry[response[study].studyName] = response[study].substudies
            filteredList.push(entry)
        }
        return filteredList
    }
}

// Companies implementation of the MRObject base class
export class CompaniesJSON extends MRObjectJSON {
    constructor(server, resource = '/companies') {
        super(resource, server)
    }
}

// Interactions implementation of the MRObject base class
export class InteractionsJSON extends MRObjectJSON {
    constructor(server, resource = '/interactions') {
        super(resource, server)
    }
}

// Users implementation of the MRObject base class
// TODO consider if this will be a separate standalone class
export class UsersJSON extends MRObjectJSON {
    constructor(server, resource = '/users') {
        super(resource, server)
    }

    // For all users return the requested user info
    async getUser (userName) {

        const response = await this.util.getObj(this.resource)
        for (const user in response) {
            
            if (response[user].username == userName){
                return {
                    userName: response[user].username,
                    token: response[user].password
                }
            } else {
                continue
            }
        }
        return filteredList
    }
}

// Export classes for consumers
export default { StudiesJSON, InteractionsJSON, CompaniesJSON, UsersJSON }