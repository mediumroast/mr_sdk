// Import required modules


class Reports {
    constructor(interactions, objectName, characterLimit = 500, title='References') {
        this.interactions = interactions
        this.characterLimit = characterLimit
        this.introduction = 'The mediumroast.io system has automatically generated this document.' +
            'It includes key metadata from each interaction associated to the object ' + objectName +
            '.  If this report document is produced as a package, instead of standalone, then the' + 'hyperlinks are active and will link to documents on the local folder after the ' +
            'package is opened.'
        this.title = title
    }

    // Create the entire section as a proto document to be fed to a format like docx, ..., html.
    createRefs() {
        let protoDoc = {
            title: this.title,
            intro: this.introduction,
            references: {}
        }
        for (const item in this.interactions) {
            protoDoc.references[item.interactionName] = self.createRef(item)
        }
        return protoDoc
    }

    // Create an individual reference from an interaction
    createRef(interaction) {
        return {
            type: interaction.type,
            abstract: interaction.abstract.substr(0, this.characterLimit) + '...',
        }
    }

    // Return the proto document as a docx formatted section
    makeDocx(protoDoc) {

    }

    // Return the proto document as a html formatted section
    makeHtml(protoDoc) {

    }
}

export default Reports