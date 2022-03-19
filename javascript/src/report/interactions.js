// Import required modules
import docx from 'docx'


class References {
    constructor(interactions, objectName, objectType, characterLimit = 500) {

        // NOTE creation of a ZIP package is something we likely need some workspace for
        //      since the documents should be downloaded and then archived.  Therefore,
        //      the CLI is a likely place to do this for now.  Suspect for the web_ui
        //      we will need some server side logic to make this happen.

        // TODO enable the baseURL to be either native or replaced
        
        this.interactions = interactions
        this.characterLimit = characterLimit
        this.introduction = 'The mediumroast.io system has automatically generated this section.' +
            ' It includes key metadata from each interaction associated to the object ' + objectName +
            '.  If this report document is produced as a package, instead of standalone, then the' + ' hyperlinks are active and will link to documents on the local folder after the' +
            ' package is opened.'
        this.objectName = objectName
        this.objectType = objectType
        this.font = 'Avenir Next' // We need to pass this in from the config file
        this.fontSize = 10 // We need to pass this in from the config file
        this.protoDoc = this.createRefs()
    }

    // Create the entire section as a proto document to be fed to a format like docx, ..., html.
    createRefs() {
        let protoDoc = {
            intro: this.introduction,
            references: {}
        }
        for (const item in this.interactions) {
            // NOTE this might be wrong could be we need this.interactions[item]
            protoDoc.references[this.interactions[item].interactionName] = this.createRef(this.interactions[item])
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
        const [year, month, day] = [myDate.substring(0, 4), myDate.substring(4, 6), myDate.substring(6, 8)]

        // Decode the time
        const myTime = interaction[timeKey]
        const [hour, min] = [myTime.substr(0, 2), myTime.substr(2, 4)]

        // Detect the repository type and replace it with http
        const repoType = interaction.url.split('://')[0]
        const myURL = interaction.url.replace(repoType, httpType)

        // Create the reference
        let reference = {
            type: interaction.interactionType, // TODO There is a bug here in the ingestion
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

    // Create a paragraph
    makeParagraph (paragraph, size, bold) {
        return new docx.Paragraph({
            children: [
                new docx.TextRun({
                    text: paragraph,
                    font: this.font,
                    size: size ? size : 20,
                    bold: bold ? bold : false, 
                })
            ]
        })
    }

    // Create a title of heading style 2
    makeTitle(title) {
        return new docx.Paragraph({
            text: title,
            heading: docx.HeadingLevel.HEADING_2
        })
    }

    // Create a text run
    makeTextrun(text) {
        return new docx.TextRun({
            text: text,
            font: this.font,
            size: 1.5 * this.fontSize,
        })
    }

    makeURL(name, link) {
        return new docx.ExternalHyperlink({
            children: [
                new docx.TextRun({
                    text: name,
                    style: 'Hyperlink',
                    font: this.font,
                    size: 1.5 * this.fontSize
                })
            ],
            link: link
        })
    }

    // Return the proto document as a docx formatted section
    makeDocx() {
        let finaldoc = [this.makeParagraph(this.protoDoc.intro)]
        for (const myReference in this.protoDoc.references) {
            // console.log(this.protoDoc[myReference])
            finaldoc.push(this.makeTitle(myReference))
            finaldoc.push(this.makeParagraph(
                this.protoDoc.references[myReference].abstract,
                1.5 * this.fontSize))
            const permaLink = this.makeURL(
                'Document link', 
                this.protoDoc.references[myReference].url)

            finaldoc.push(
                new docx.Paragraph({
                    children:[
                        this.makeTextrun('[ '),
                        permaLink,
                        this.makeTextrun(' | Date: ' + this.protoDoc.references[myReference].date + ' | '), 
                        this.makeTextrun('Time: ' + this.protoDoc.references[myReference].time + ' | '), 
                        this.makeTextrun('Type: ' + this.protoDoc.references[myReference].type),
                        this.makeTextrun(' ]'),
                    ]
                })
            )
        }
        return finaldoc
    }

    // Return the proto document as a html formatted section
    makeHtml() {
        return false
    }
}

export default References