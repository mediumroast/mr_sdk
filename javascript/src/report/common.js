// Import modules
import docx from 'docx'

class Utilities {
    constructor (copyright, font, size) {
        this.copyright = copyright
        this.font = font
        this.size = size
    }

    // Initialize and return the document object with the default set
    initDoc (title, creator = 'mediumroast.io', description = 'A report snapshot of company data for: ') {
        return new docx.Document({
            creator: creator + ' barista robot',
            company: creator,
            title: title + ' Company Report',
            description: description + title,
            sections: [],
            styles: {
                default: {
                    heading1: {
                        run: {
                            size: 2 * this.size,
                            bold: true,
                            font: this.font,
                        },
                        paragraph: {
                            spacing: {
                                after: 120,
                            },
                        },
                    },
                    heading2: {
                        run: {
                            size: 1.5 * this.size,
                            bold: true,
                            font: this.font,
                        },
                        paragraph: {
                            spacing: {
                                before: 240,
                                after: 120,
                            },
                        },
                    },
                    heading3: {
                        run: {
                            size: 1.2 * this.size,
                            bold: true,
                            font: this.font,
                        },
                        paragraph: {
                            spacing: {
                                before: 240,
                                after: 120,
                            },
                        },
                    },
                }
            }
        })

    }

}

export default Utilities