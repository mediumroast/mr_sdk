// Import required modules
import { StudiesJSON, CompaniesJSON, InteractionsJSON, UsersJSON } from './jsonServer.js'


// TODO Consider a class/subclass relationship with Studies and baseobj
// NOTE Would potentially need to pass in this.serverType or add to the class.
//      Alternatively we'd create the controller in the sub-class and pass it in?
//      Some experimentation is needed to determine the best approach for code
//      minimization.  The simplicity of passing in the controller would be
//      significant.
class MRObject {
    constructor(controller) {
        this.controller = controller
    }

    // Get all information about all objects
    async getAll() {
        return this.controller.getAll()
    }

    // Get only GUIDs for all objects
    async getAllGUIDs() {
        return this.controller.getAllGUIDs()
    }

    // Get only Names for all objects
    async getAllNames() {
        return this.controller.getAllNames()
    }

    // Get only Names -> GUIDs mappings for all objects
    async getNamesAndGUIDs() {
        return this.controller.getNamesAndGUIDs()
    }

    // Get all information about a single object using the object's name
    async getByName(name, subResource = '?studyName=') {
        return this.controller.getByName(name, subResource)
    }

    // Get all information about a single object using the objects's GUID
    async getByGUID(guid, subResource = '?GUID=') {
        return this.controller.getByGUID(guid, subResource)
    }

    // Using the object GUID return the name
    async getNameByGUID(guid, subResource = '?GUID=') {
        return this.controller.getByGUID(guid, subResource)
    }

    // Using the object name return the GUID
    async getGUIDByName(name, subResource = '?studyName=') {
        return this.controller.getByName(name, subResource)
    }

}

// Create the studies subclass
export class Studies extends MRObject {
    constructor(server, serverType) {
        let controller = null
        if (serverType == 'json') {
            controller = new StudiesJSON(server)
        }
        super(controller)
    }

    // For all studies filter in only the substudies and return
    async getAllSubstudies() {
        return this.controller.getAllSubstudies()
    }
}

// Create the companies subclass
export class Companies extends MRObject {
    constructor(server, serverType) {
        let controller = null
        if (serverType == 'json') {
            controller = new CompaniesJSON(server)
        }
        super(controller)
    }
}

// Create the interactions subclass
export class Interactions extends MRObject {
    constructor(server, serverType) {
        let controller = null
        if (serverType == 'json') {
            controller = new InteractionsJSON(server)
        }
        super(controller)
    }
}

// Create the interactions subclass
export class Users extends MRObject {
    constructor(server, serverType) {
        let controller = null
        if (serverType == 'json') {
            controller = new UsersJSON(server)
        }
        super(controller)
    }

    async getUser (userName) {
        return this.controller.getUser(userName)
    }
}


export default { Studies, Companies, Interactions, Users }