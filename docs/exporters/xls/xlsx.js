import ExcelJS from "exceljs";
import fs from "file-saver";
import ExcelStyles from "./ExcelStyles";

/*
Common functions to process the excel files
*/

/* parameters:
 * colIndex: the index of column, start from 1 (equivalent  to colum 'A')
 * return the name of column
 */
export function getColumnName(colIndex) {
    let quotient = colIndex;
    let remainder = 0;
    let columnName = "";
  
    // The cellName in reverse other
    do {
      quotient -= 1;
      remainder = quotient % 26;
      columnName = String.fromCharCode(65 + remainder) + columnName;
      quotient = Math.floor(quotient / 26);
    } while (quotient > 0);
    return columnName;
  }
  
  /* parameters:
   * colIndex: the index of column, start from 1 (equivalent  to colum 'A')
   * row: the index of row
   */
  export function getCellName(colIndex, row) {
    return getColumnName(colIndex) + row;
  }
  
  /* parameters:
   * cell: the exceljs cell object
   * return the color in argb format
   */
  export function cellColor(cell) {
    return cell.style && cell.style.fill && cell.style.fill.bgColor
      ? cell.style.fill.bgColor.argb
      : null;
  }
  
  export function cellString(cell) {
    return cell && cell.value ? cell.value.toString().trim() : null;
  }
  
  export function cellItalic(cell) {
    return cell && cell.style && cell.style.font && cell.style.font.italic
      ? true
      : false;
  }
  
  export function cellBold(cell) {
    return cell && cell.style && cell.style.font && cell.style.font.bold
      ? true
      : false;
  }

export async function toExcel(
    data,
    sheetName=null,
    filename=null,
    fields=null,
    translate=null,
    options=null
) {
  const workbook = new ExcelJS.Workbook();
  workbook.creator = "Alpha";
  workbook.lastModifiedBy = "Alpha";
  const now = new Date();
  workbook.created = now;
  workbook.modified = now;
  workbook.lastPrinted = now;
  workbook.properties.date1904 = true;

  const defaultColWidth = options && options.defaultColWidth ? options.defaultColWidth : 25;
  const worksheet = workbook.addWorksheet(sheetName || 'data');
  worksheet.properties.defaultColWidth = defaultColWidth;

  let current_row = 1;
  let current_col = 1;

  // Column names
  let columns = [];
  // If the list of fields were specified, we just export these fields
  if (fields && typeof fields === 'object') {
    const columnEntries = Object.entries(fields);
    columnEntries.forEach(([k,v]) => {
      if (translate) {
        try {
          columns = [ ...columns, { key: k, name: translate(k) }];
        } catch(err) {
          columns = [ ...columns, { key: k, name: k.split("_").join(" ") }];
        } 
      } else {
        columns = [ ...columns, { key: k, name: k.split("_").join(" ")}];
      }
    })
  } else { // just export direct fields
    let namesSet =  new Set();
    data.forEach((item) => {
      const keys = Object.entries(item)
        .filter(([k,v]) => typeof v !== 'object')
        .forEach(([k,v]) => {
          namesSet.add(k);
        });
    })
    columns = Array.from(namesSet).map((name) => {
      if (translate) {
        try {
          return { key: name, name: translate(name) };
        } catch(err) {
          return { key: name, name: name.split("_").join(" ") };
        } 
      } else {
        return { key: name, name: name.split("_").join(" ") };
      }
    });
  }
  //Header cells
  columns.forEach((column, index) => {
    const cellName = getCellName(current_col + index, current_row);
    const cell = worksheet.getCell(cellName);
    cell.value = {
      richText: [{ font: ExcelStyles.whiteHeaderFont, text: column.name }],
    };
    cell.alignment = ExcelStyles.centerAlignment;
    cell.fill = ExcelStyles.headerFill;
    cell.border = ExcelStyles.headerBorder;
  })

  //Fill data
  current_col = 1;
  data.forEach((item) => {
    current_row ++;
    columns.forEach((column, i) => {
      const cellName = getCellName(current_col + i, current_row);
      const cell = worksheet.getCell(cellName);
      const value = fields && fields[column.key] && typeof fields[column.key] === 'function'
        ? fields[column.key](item)
        : item[column.key];
      cell.value = value;
      cell.border = ExcelStyles.border;
    })
  })
  const path = filename ? filename: `data-${now.toLocaleDateString()}.xlsx`;

  workbook.xlsx.writeBuffer().then((data) => {
    const blob = new Blob([data], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    fs.saveAs(blob, path);
  });
}
