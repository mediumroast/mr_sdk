// Import modules
import docx from 'docx'

class Utilities {
    constructor (copyright, font, size) {
        this.copyright = copyright
        this.font = font
        this.size = size
    }

    // Initialize and return the document object with the default set
    initDoc (title, description, creator = 'mediumroast.io', ) {
        return new docx.Document({
            creator: creator,
            title: title,
            description: description,
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