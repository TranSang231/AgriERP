import fs from "file-saver";

export async function toJson(
    data,
    filename=null
) {
  const now = new Date();
  const json = JSON.stringify(data, null, 2)
  const path = filename ? filename: `data-${now.toLocaleDateString()}.json`;

  const blob = new Blob([json], {
    type: 'text/plain'
  });

  fs.saveAs(blob, path);
}
