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

    addressRow() {
        // Set the base URL for Google Maps
        const addressBits = [
            this.company.streetAddress, 
            this.company.city, 
            this.company.stateProvince, 
            this.company.zipPostal, 
            this.company.country
        ]
        let baseURL = 'https://www.google.com/maps/place/'
        let search = ""
        for (const element in addressBits) {
            let tmpString = addressBits[element]
            tmpString = tmpString.replace(' ', '+')
            search+='+' + tmpString
        }

        const addressString = addressBits[0] + ', ' +
            addressBits[1] + ', ' + addressBits[2] + ' ' + addressBits[3] + ', ' +
            addressBits[4]

        const mapURL = new docx.ExternalHyperlink({
            children: [
                new docx.TextRun({
                    text: `${addressString}`,
                    style: 'Hyperlink'
                })
            ],
            link: baseURL + encodeURIComponent(search)
        })

        return new docx.TableRow({
            children: [
                new docx.TableCell({
                    width: {
                        size: 20,
                        type: docx.WidthType.PERCENTAGE
                    },
                    children: [new docx.Paragraph('Location')]
                }),
                new docx.TableCell({
                    width: {
                        size: 80,
                        type: docx.WidthType.PERCENTAGE
                    },
                    children: [new docx.Paragraph({
                        children: [mapURL]
                    })]
                })
            ]
        })
    }

    // Create the website row
    urlRow() {
        // define the link to the company's website
        const companyURL = new docx.ExternalHyperlink({
            children: [
                new docx.TextRun({
                    text: `${this.company.url}`,
                    style: 'Hyperlink'
                })
            ],
            link: this.company.url
        })

        // return the row
        return new docx.TableRow({
            children: [
                new docx.TableCell({
                    width: {
                        size: 20,
                        type: docx.WidthType.PERCENTAGE
                    },
                    children: [new docx.Paragraph('Website')]
                }),
                new docx.TableCell({
                    width: {
                        size: 80,
                        type: docx.WidthType.PERCENTAGE
                    },
                    children: [new docx.Paragraph({children:[companyURL]})]
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
        // define the blank table
        const myTable = new docx.Table({
            columnWidths: [20, 80],
            rows: [
                this.basicRow('Name', this.company.companyName),
                this.basicRow('Description', this.company.description),
                this.urlRow(),
                this.basicRow('Industry', this.company.industry),
                this.addressRow(),
                this.basicRow('Region', this.region),
                this.basicRow('Phone', this.company.phone),
                this.basicRow('Type', this.companyType),
                this.basicRow('Stock Symbol', this.company.stockSymbol),
                this.basicRow('CIK', this.company.cik),
                this.basicRow('No. Interactions', String(this.company.totalInteractions)),
                this.basicRow('No. Studies', String(this.company.totalStudies)),
                //TODO Add URLs for current interaction and study
            ],
            width: {
                size: 100,
                type: docx.WidthType.PERCENTAGE
            }
        })

        return myTable
    }

    makeParagraph (paragraph) {
        return new docx.Paragraph({
            children: [
                new docx.TextRun({
                    text: paragraph,
                })
            ]
        })
    }

    makeTitle(title) {
        return new docx.Paragraph({
            text: title,
            heading: docx.HeadingLevel.HEADING_1
        })
    }

    // Generate a page with all company firmographics 
    doc() {

        return [
            this.makeTitle('Introduction'), // Intro title
            this.makeParagraph(this.company.document.Introduction), // Introduction for the document
            this.makeTitle('Purpose'), // Intro title
            this.makeParagraph(this.company.document.Purpose), // Introduction for the document
            // TODO unpack actions
            this.makeTitle('Firmographics'), // Firmographics title 
            this.docTable() // Table containing firmographics
        ]
    }



}

export default Firmographics