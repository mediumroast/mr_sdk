// Import modules
import docx from 'docx'

class Utilities {
    constructor (copyright, font, size) {
        this.copyright = copyright
        this.font = font
        this.size = size
        this.styling = this.initStyles()
    }

    // Initialize the common styles for the doc
    initStyles () {
        return {
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
                },
                numbering: {
                    config: [
                        {
                            reference: 'number-styles',
                            levels: [
                                {
                                    level: 0,
                                    format: LevelFormat.UPPER_ROMAN,
                                    text: "%1",
                                    alignment: AlignmentType.START,
                                    style: {
                                        paragraph: {
                                            indent: { left: convertInchesToTwip(0.5), hanging: convertInchesToTwip(0.18) },
                                        },
                                    },
                                },
                                {
                                    level: 1,
                                    format: LevelFormat.DECIMAL,
                                    text: "%2.",
                                    alignment: AlignmentType.START,
                                    style: {
                                        paragraph: {
                                            indent: { left: convertInchesToTwip(1), hanging: convertInchesToTwip(0.68) },
                                        },
                                    },
                                },
                                {
                                    level: 2,
                                    format: LevelFormat.LOWER_LETTER,
                                    text: "%3)",
                                    alignment: AlignmentType.START,
                                    style: {
                                        paragraph: {
                                            indent: { left: convertInchesToTwip(1.5), hanging: convertInchesToTwip(1.18) },
                                        },
                                    },
                                },
                                {
                                    level: 3,
                                    format: LevelFormat.UPPER_LETTER,
                                    text: "%4)",
                                    alignment: AlignmentType.START,
                                    style: {
                                        paragraph: {
                                            indent: { left: 2880, hanging: 2420 },
                                        },
                                    },
                                },
                            ]
                        },
                        {
                            reference: "bullet-styles",
                            levels: [
                                {
                                    level: 0,
                                    format: LevelFormat.BULLET,
                                    text: "\u1F60",
                                    alignment: AlignmentType.LEFT,
                                    style: {
                                        paragraph: {
                                            indent: { left: convertInchesToTwip(0.5), hanging: convertInchesToTwip(0.25) },
                                        },
                                    },
                                },
                                {
                                    level: 1,
                                    format: LevelFormat.BULLET,
                                    text: "\u00A5",
                                    alignment: AlignmentType.LEFT,
                                    style: {
                                        paragraph: {
                                            indent: { left: convertInchesToTwip(1), hanging: convertInchesToTwip(0.25) },
                                        },
                                    },
                                },
                                {
                                    level: 2,
                                    format: LevelFormat.BULLET,
                                    text: "\u273F",
                                    alignment: AlignmentType.LEFT,
                                    style: {
                                        paragraph: {
                                            indent: { left: 2160, hanging: convertInchesToTwip(0.25) },
                                        },
                                    },
                                },
                                {
                                    level: 3,
                                    format: LevelFormat.BULLET,
                                    text: "\u267A",
                                    alignment: AlignmentType.LEFT,
                                    style: {
                                        paragraph: {
                                            indent: { left: 2880, hanging: convertInchesToTwip(0.25) },
                                        },
                                    },
                                },
                                {
                                    level: 4,
                                    format: LevelFormat.BULLET,
                                    text: "\u2603",
                                    alignment: AlignmentType.LEFT,
                                    style: {
                                        paragraph: {
                                            indent: { left: 3600, hanging: convertInchesToTwip(0.25) },
                                        },
                                    },
                                },
                            ]
                        }
                    ]}
            }
    }

}

export default Utilities