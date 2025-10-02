const ExcelStyles = {
  headerBorder: {
    top: { style: "thin" },
    left: { style: "thin" },
    bottom: { style: "thin" },
    right: { style: "thin" },
    color: { argb: "B62132" },
  },
  headerFill: {
    type: "pattern",
    pattern: "solid",
    fgColor: { argb: "B62132" },
  },
  headerFont: {
    size: 10,
    bold: true,
    color: { argb: "B62132" },
    name: "Calibri",
    family: 2,
    scheme: "minor",
  },
  whiteHeaderFont: {
    bold: true,
    size: 10,
    color: { argb: "FFFFFFFF" },
    name: "Calibri",
    family: 2,
    scheme: "minor",
  },
  fill: {
    type: "pattern",
    pattern: "darkVertical",
    fgColor: { argb: "FF46BDC6" },
  },
  border: {
    top: { style: "thin" },
    left: { style: "thin" },
    bottom: { style: "thin" },
    right: { style: "thin" },
    color: { argb: "B62132" },
  },
  alignment: {
    wrapText: true,
    vertical: "distributed",
  },
  labelFont: {
    size: 10,
    color: { argb: "FF9C7083" },
    name: "Calibri",
    family: 2,
    scheme: "minor",
  },
  centerAlignment: {
    vertical: "middle",
    horizontal: "center",
  },
  bodyFont: {
    size: 10,
    color: { argb: "FF631839" },
    name: "Calibri",
    family: 2,
    scheme: "minor",
  },
  tips: {
    bold: true,
    size: 10,
    color: { argb: "FFF40104" },
    name: "Calibri",
    family: 2,
    scheme: "minor",
  },
  headerTitle: {
    bold: true,
    size: 18,
    color: { argb: "FF081C14" },
    name: "Calibri",
    family: 2,
    scheme: "minor",
  },
};

export default ExcelStyles;
