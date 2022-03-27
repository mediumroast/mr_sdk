// Import modules
import docx from 'docx'
import Utilities from './common.js'

class KeyThemes {
    constructor (themeType, themes) {
        this.type = themeType
        this.themes = themes
        this.font = 'Avenir Next' // We need to pass this in from the config file
        this.fontSize = 10 // We need to pass this in from the config file
        this.fontFactor = 1.5
        this.util = new Utilities()
        this.introduction = 'The mediumroast.io system has automatically generated this section. ' +
            'If this section is for a summary theme, then two tables are included: ' + 
            '1. Information for the summary theme including key words, score and rank. ' +
            '2. Excerpts from the interactions within the sub-study and links to each interaction reference.'
    }

    basicThemeRow (theme, score, rank, bold) {
        // return the row
        return new docx.TableRow({
            children: [
                new docx.TableCell({
                    width: {
                        size: 60,
                        type: docx.WidthType.PERCENTAGE,
                        font: this.font,
                    },
                    children: [this.util.makeParagraph(theme, this.fontFactor * this.fontSize, bold ? true : false)]
                }),
                new docx.TableCell({
                    width: {
                        size: 20,
                        type: docx.WidthType.PERCENTAGE,
                        font: this.font,
                    },
                    children: [this.util.makeParagraph(score, this.fontFactor * this.fontSize, bold ? true : false)]
                }),
                new docx.TableCell({
                    width: {
                        size: 20,
                        type: docx.WidthType.PERCENTAGE,
                        font: this.font,
                    },
                    children: [this.util.makeParagraph(rank, this.fontFactor * this.fontSize, bold ? true : false)]
                }),
            ]
        })
    }

    // Create the table for the doc
    summaryThemeTable(themes) {
        let myRows = [this.basicThemeRow('Topic Keywords', 'Score', 'Rank', true)]
        for (const theme in themes) {
            myRows.push(this.basicThemeRow(theme, themes[theme].score.toFixed(2), themes[theme].rank))
        }
        // define the table with the summary theme information
        const myTable = new docx.Table({
            columnWidths: [60, 20, 20],
            rows: myRows,
            width: {
                size: 100,
                type: docx.WidthType.PERCENTAGE
            }
        })

        return myTable
    }

    makeDocx () {
        if (this.type === 'summary') {
            return [
                this.util.pageBreak(),
                this.util.makeHeading1('Summary Theme'),
                this.util.makeParagraph(this.introduction),
                this.summaryThemeTable(this.themes)
            ]
        } else {
            return []
        }

    }
}

export default KeyThemes