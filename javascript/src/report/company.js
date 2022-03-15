// Import required modules

import docx from 'docx'

class Firmographics {
    // Consider a switch between HTML and DOCX
    // NOTE This may not be needed for the HTML version more thinking needed
    constructor(company) {
        // Decode the regions
        const regions = {
            AMER: 'Americas',
            EMEA: 'Europe, Middle East and Africa',
            APAC: 'Asia Pacific and Japan'
        }

        // Set the company Type
        company[0].stockSymbol === 'Unknown' && company[0].cik === 'Unknown' ? 
            this.companyType = 'Private' :
            this.companyType = 'Public'

        this.company = company[0]
        this.region = regions[company[0].region]
        this.companyDoc = this.doc()
    }

    // Define the CIK and link it to an EDGAR search if available
    stockSymbolRow () {
        if (this.company.stockSymbol === 'Unknown') {
            return this.basicRow('Stock Symbol', this.company.stockSymbol)
        } else {
            const baseURL = 'https://www.bing.com/search?q='
            return this.urlRow('Stock Symbol', this.company.stockSymbol, baseURL + this.company.stockSymbol)
        }
    }

    // Define the CIK and link it to an EDGAR search if available
    cikRow () {
        if (this.company.cik === 'Unknown') {
            return this.basicRow('CIK', this.company.cik)
        } else {
            const baseURL = 'https://www.sec.gov/edgar/search/#/ciks='
            return this.urlRow('CIK', this.company.cik, baseURL + this.company.cik)
        }
    }

    // Create the website row
    urlRow(category, name, link) {
        // define the link to the target URL
        const myUrl = new docx.ExternalHyperlink({
            children: [
                new docx.TextRun({
                    text: name,
                    style: 'Hyperlink'
                })
            ],
            link: link
        })

        // return the row
        return new docx.TableRow({
            children: [
                new docx.TableCell({
                    width: {
                        size: 20,
                        type: docx.WidthType.PERCENTAGE
                    },
                    children: [new docx.Paragraph(category)]
                }),
                new docx.TableCell({
                    width: {
                        size: 80,
                        type: docx.WidthType.PERCENTAGE
                    },
                    children: [new docx.Paragraph({children:[myUrl]})]
                })
            ]
        })
    }

    // Basic row to produce a name/value pair
    basicRow (name, data) {
        // return the row
        return new docx.TableRow({
            children: [
                new docx.TableCell({
                    width: {
                        size: 20,
                        type: docx.WidthType.PERCENTAGE
                    },
                    children: [new docx.Paragraph(name)]
                }),
                new docx.TableCell({
                    width: {
                        size: 80,
                        type: docx.WidthType.PERCENTAGE
                    },
                    children: [new docx.Paragraph(data)]
                })
            ]
        })
    }

    // Create the table for the doc
    docTable() {
        // Define the address string
        const addressBits = [
            this.company.streetAddress, 
            this.company.city, 
            this.company.stateProvince, 
            this.company.zipPostal, 
            this.company.country
        ]
        const addressBaseUrl = 'https://www.google.com/maps/place/'
        let addressSearch = ""
        for (const element in addressBits) {
            let tmpString = addressBits[element]
            tmpString = tmpString.replace(' ', '+')
            addressSearch+='+' + tmpString
        }
        const addressUrl = addressBaseUrl + encodeURIComponent(addressSearch)
        const addressString = addressBits[0] + ', ' +
            addressBits[1] + ', ' + addressBits[2] + ' ' + addressBits[3] + ', ' +
            addressBits[4]


        // define the table with firmographics
        const myTable = new docx.Table({
            columnWidths: [20, 80],
            rows: [
                this.basicRow('Name', this.company.companyName),
                this.basicRow('Description', this.company.description),
                this.urlRow('Website', this.company.url, this.company.url),
                this.basicRow('Role', this.company.role),
                this.basicRow('Industry', this.company.industry),
                this.urlRow('Location', addressString, addressUrl),
                this.basicRow('Region', this.region),
                this.basicRow('Phone', this.company.phone),
                this.basicRow('Type', this.companyType),
                this.stockSymbolRow(),
                this.cikRow(),
                this.basicRow('No. Interactions', String(this.company.totalInteractions)),
                this.basicRow('No. Studies', String(this.company.totalStudies)),
                // TODO Add Rows and maybe URLs for current interaction and study
                // NOTE this requires the URL for the mr_backend
            ],
            width: {
                size: 100,
                type: docx.WidthType.PERCENTAGE
            }
        })

        return myTable
    }

    // For a section of prose create a paragraph
    makeParagraph (paragraph) {
        return new docx.Paragraph({
            children: [
                new docx.TextRun({
                    text: paragraph,
                })
            ]
        })
    }

    // Create a title of heading style 1
    makeTitle(title) {
        return new docx.Paragraph({
            text: title,
            heading: docx.HeadingLevel.HEADING_1
        })
    }

    makeActions () {
        // TODO inherit bullet and numbering styles in doc_company
        let actionArray = []
        for (const action in this.company.document.Action) {
            if (action === 'text') { continue }
            const protoAction = this.company.document.Action[action]
            const [actionTect, actionStatus] = protoAction.split('|')
            // TODO make paragraph of level 1
            // TODO make paragraph of level 2
            // TODO append paragraphs to array
        }
        return actionArray
    }

    // Generate a page with all company firmographics 
    doc() {
        // NOTE it is likely we will need to create the array up to actions, add the actions, and
        // then add the the table
        console.log(this.company.document.Action)
        return [
            this.makeTitle('Introduction'), // Intro title
            this.makeParagraph(this.company.document.Introduction), // Introduction paragraph
            this.makeTitle('Purpose'), // Intro title
            this.makeParagraph(this.company.document.Purpose), // Purpose paragraph
            this.makeTitle('Actions'), // Actions title
            this.makeParagraph(this.company.document.Action.text),
            // TODO unpack actions
            this.makeTitle('Firmographics'), // Firmographics title 
            this.docTable() // Table containing firmographics
        ]
    }



}

export default Firmographics