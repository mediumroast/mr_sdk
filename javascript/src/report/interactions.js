// Import required modules



class Reports {
    constructor(interactions, objectName, objectType, characterLimit = 500, title = 'References') {

        // NOTE creation of a ZIP package is something we likely need some workspace for
        //      since the documents should be downloaded and then archived.  Therefore,
        //      the CLI is a likely place to do this for now.  Suspect for the web_ui
        //      we will need some server side logic to make this happen.
        
        this.interactions = interactions
        this.characterLimit = characterLimit
        this.introduction = 'The mediumroast.io system has automatically generated this section.' +
            'It includes key metadata from each interaction associated to the object ' + objectName +
            '.  If this report document is produced as a package, instead of standalone, then the' + 'hyperlinks are active and will link to documents on the local folder after the ' +
            'package is opened.'
        this.title = title
        this.objectName = objectName
        this.objectType = objectType
        // TODO call createRefs
    }

    // Create the entire section as a proto document to be fed to a format like docx, ..., html.
    createRefs() {
        let protoDoc = {
            title: this.title,
            intro: this.introduction,
            references: {}
        }
        for (const item in this.interactions) {
            // NOTE this might be wrong could be we need this.interactions[item]
            protoDoc.references[item.interactionName] = self.createRef(item)
        }
        return protoDoc
    }

    // Create an individual reference from an interaction
    createRef(interaction, dateKey = 'date', timeKey = 'time', httpType = 'http') {
        // NOTE need to think about the URL and how to properly unpack it
        //      example, swap to from X to http and then preserve it as a 
        //      part of the protoDoc

        // Decode the date
        const myDate = interaction[dateKey]
        const [year, month, day] = [myDate.substring(0, 4), myDate.substring(5, 6), myDate.substring(7, 8)]

        // Decode the time
        const myTime = interaction[timeKey]
        const [hour, min] = [myTime.substr(0, 2), myTime.substr(3, 4)]

        // Detect the repository type and replace it with http
        const repoType = interaction.url.split('://')[0]
        const myURL = interaction.url.replace(repoType, httpType)

        // Create the reference
        let reference = {
            type: interaction.type,
            abstract: interaction.abstract.substr(0, this.characterLimit) + '...',
            date: year + '-' + month + '-' + day,
            time: hour + ':' + min,
            url: myURL,
            repo: repoType
        }
        // Set the object type and name
        reference[this.objectType] = this.objectName

        return reference
    }

    // Return the proto document as a docx formatted section
    makeDocx(protoDoc) {

    }

    // Return the proto document as a html formatted section
    makeHtml(protoDoc) {

    }
}

export default Reports