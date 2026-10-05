
from pathlib import Path
import csv
import zipfile
import xml.etree.ElementTree as ET

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return {
            "format": "csv",
            "sheets": {"default": list(csv.DictReader(f))}
        }

def read_xlsx(path):
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))

        relmap = {
            r.attrib["Id"]: r.attrib["Target"]
            for r in rels
        }

        shared = []
        try:
            ss = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in ss.findall(f"{{{MAIN}}}si"):
                shared.append(
                    "".join(
                        t.text or ""
                        for t in si.iter(f"{{{MAIN}}}t")
                    )
                )
        except KeyError:
            pass

        sheets = {}

        for sheet in wb.findall(f".//{{{MAIN}}}sheet"):
            name = sheet.attrib["name"]
            rid = sheet.attrib[f"{{{REL}}}id"]
            target = relmap[rid]

            if not target.startswith("xl/"):
                target = "xl/" + target

            root = ET.fromstring(z.read(target))
            matrix = []

            for row in root.findall(
                f".//{{{MAIN}}}sheetData/{{{MAIN}}}row"
            ):
                values = []

                for cell in row.findall(f"{{{MAIN}}}c"):
                    if cell.attrib.get("t") == "inlineStr":
                        value = "".join(
                            t.text or ""
                            for t in cell.iter(f"{{{MAIN}}}t")
                        )
                    else:
                        v = cell.find(f"{{{MAIN}}}v")
                        value = v.text if v is not None else ""

                        if cell.attrib.get("t") == "s" and value:
                            value = shared[int(value)]

                    values.append(value)

                if values:
                    matrix.append(values)

            if not matrix:
                sheets[name] = []
                continue

            headers = [str(x).strip() for x in matrix[0]]
            rows = []

            for values in matrix[1:]:
                values += [""] * (len(headers) - len(values))
                rows.append({
                    headers[i]: values[i]
                    for i in range(len(headers))
                })

            sheets[name] = rows

    return {
        "format": "xlsx",
        "sheets": sheets
    }

def ingest(path):
    path = Path(path)

    if path.suffix.lower() == ".csv":
        return read_csv(path)

    if path.suffix.lower() == ".xlsx":
        return read_xlsx(path)

    raise ValueError(f"Unsupported format: {path.suffix}")
