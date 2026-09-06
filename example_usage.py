import json
from client import PDFComplexMergedTableBboxParser

def main():
    parser = PDFComplexMergedTableBboxParser()
    sample_cells = [
        {"text": "Fiscal Quarter", "top": 100, "left": 50, "width": 80, "height": 15},
        {"text": "Revenue (USD)", "top": 100, "left": 200, "width": 80, "height": 15},
        {"text": "Net Margin", "top": 100, "left": 350, "width": 60, "height": 15},
        {"text": "Q1 2026", "top": 125, "left": 50, "width": 50, "height": 15},
        {"text": "$14.2M", "top": 125, "left": 200, "width": 50, "height": 15},
        {"text": "24.5%", "top": 125, "left": 350, "width": 40, "height": 15},
        {"text": "Q2 2026", "top": 148, "left": 50, "width": 50, "height": 15},
        {"text": "$18.9M", "top": 148, "left": 200, "width": 50, "height": 15},
        {"text": "27.1%", "top": 148, "left": 350, "width": 40, "height": 15}
    ]
    result = parser.reconstruct_table(sample_cells)
    print("Reconstructed Table:")
    print(json.dumps(result, indent=2))
    assert result["total_rows"] == 3
    assert len(result["records"]) == 2
    assert result["records"][0]["Fiscal Quarter"] == "Q1 2026"
    print("Table bbox parser verification: PASS")

if __name__ == "__main__":
    main()
