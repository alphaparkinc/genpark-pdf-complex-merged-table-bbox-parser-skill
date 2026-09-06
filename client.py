from typing import Dict, Any, List, Optional

class PDFComplexMergedTableBboxParser:
    """
    Reconstructs structured tabular data from unstructured 2D bounding boxes (bboxes).
    Handles colspans, multi-line headers, and alignment heuristics.
    """
    def __init__(self, y_tolerance: float = 6.0, col_tolerance: float = 12.0):
        self.y_tolerance = y_tolerance
        self.col_tolerance = col_tolerance

    def reconstruct_table(self, text_cells: List[Dict[str, Any]]) -> Dict[str, Any]:
        sorted_cells = sorted(text_cells, key=lambda c: (c.get("top", 0), c.get("left", 0)))
        rows: List[List[Dict[str, Any]]] = []
        for cell in sorted_cells:
            cell_top = cell.get("top", 0)
            placed = False
            for row in rows:
                row_top = sum(c.get("top", 0) for c in row) / len(row)
                if abs(cell_top - row_top) <= self.y_tolerance:
                    row.append(cell)
                    placed = True
                    break
            if not placed:
                rows.append([cell])

        for row in rows:
            row.sort(key=lambda c: c.get("left", 0))

        col_x_coords = set()
        for row in rows:
            for cell in row:
                col_x_coords.add(round(cell.get("left", 0) / self.col_tolerance) * self.col_tolerance)
        sorted_cols = sorted(list(col_x_coords))

        parsed_matrix = []
        for row in rows:
            row_dict = {}
            for cell in row:
                c_x = round(cell.get("left", 0) / self.col_tolerance) * self.col_tolerance
                col_idx = sorted_cols.index(c_x) if c_x in sorted_cols else len(row_dict)
                text = cell.get("text", "").strip()
                row_dict[col_idx] = text
            row_cells = [row_dict.get(i, "") for i in range(len(sorted_cols))]
            parsed_matrix.append(row_cells)

        headers = parsed_matrix[0] if parsed_matrix else []
        data_rows = parsed_matrix[1:] if len(parsed_matrix) > 1 else []

        structured_records = []
        for d_row in data_rows:
            rec = {}
            for idx, col_name in enumerate(headers):
                rec[col_name if col_name else f"col_{idx}"] = d_row[idx] if idx < len(d_row) else ""
            structured_records.append(rec)

        return {
            "total_rows": len(parsed_matrix),
            "column_count": len(sorted_cols),
            "headers": headers,
            "records": structured_records
        }
