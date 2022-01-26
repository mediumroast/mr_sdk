// Import required modules
import StudiesJSON from './jsonServer.js' 


// TODO Consider a class/subclass relationship with Studies and baseobj
// NOTE Would potentially need to pass in this.serverType or add to the class.
//      Alternatively we'd create the controller in the sub-class and pass it in?
//      Some experimentation is needed to determine the best approach for code
//      minimization.  The simplicity of passing in the controller would be
//      significant.
class Studies {
    constructor (server, serverType) {
        this.server = server
        this.serverType = serverType
        this.controller = null
        if (this.serverType == 'json') {
            this.controller = new StudiesJSON(this.server)
        }
    }

    // Get all information about all studies
    async getAll () {
        return this.controller.getAll()
    }

    // Get only GUIDs for all studies
    async getAllGUIDs () {
        return this.controller.getAllGUIDs()
    }

    // Get only Names for all studies
    async getAllNames () {
        return this.controller.getAllNames()
    }

    // Get only Names -> GUIDs mappings for all studies
    async getNamesAndGUIDs () {
        return this.controller.getNamesAndGUIDs()
    }

    // For all studies filter in only the substudies and return
    async getAllSubstudies () {
        return this.controller.getAllSubstudies()
    }

    // Get all information about a single study using the study's name
    async getByName (name, subResource = '?studyName=') {
        return this.controller.getByName(name, subResource)
    }

    // Get all information about a single study using the study's GUID
    async getByGUID (guid, subResource = '?GUID=') {
        return this.controller.getByGUID(guid, subResource)
    }

    // Using the study GUID return the name
    async getNameByGUID (guid, subResource = '?GUID=') {
        return this.controller.getByGUID(guid, subResource)
    }

    // Using the study name return the GUID
    async getGUIDByName (name, subResource = '?studyName=') {
        return this.controller.getByName(name, subResource)
    }

}


export default Studies