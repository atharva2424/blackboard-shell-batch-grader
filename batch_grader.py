#!/usr/bin/env python3
"""Batch‑grade shell scripts downloaded from Blackboard submissions.

Usage:
    python batch_grader.py submissions.zip
"""
import zipfile, subprocess, csv, json, tempfile, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
RUBRIC = json.loads((ROOT / "rubric.json").read_text())

def run_test(script_path, test):
    inp = ROOT / test["input"]
    expected = test["expected"]
    try:
        BASH = r"C:\\Program Files\\Git\\bin\\bash.exe"
        proc = subprocess.run(
            [BASH, str(script_path), str(inp)],
            capture_output=True, text=True, timeout=5
        )
        output = proc.stdout.strip()
        if output == expected:
            return test["points"], ""
        else:
            return 0, f"Expected {expected}, got {output}"
    except Exception as e:
        return 0, f"Error: {e}"

def grade_script(script_path):
    total = 0
    details = []
    for test in RUBRIC["criteria"]:
        score, fb = run_test(script_path, test)
        total += score
        details.append({
            "name": test["name"],
            "score": score,
            "points": test["points"],
            "feedback": fb
        })
    return total, details

def main(zip_path):
    # results dict for JSON feedback
    results = {}
    # rows for csv
    rows = [("Username", "Score")]

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmpdir)
        for student_folder in pathlib.Path(tmpdir).iterdir():
            if not student_folder.is_dir():
                continue
            username = student_folder.name
            scripts = list(student_folder.rglob("count_lines.sh"))
            print(f"DEBUG: {username} scripts found →", scripts)
            if scripts:
                score, detail = grade_script(scripts[0])
            else:
                score, detail = 0, [{
                    "name": t["name"],
                    "score": 0,
                    "points": t["points"],
                    "feedback": "count_lines.sh not found"
                } for t in RUBRIC["criteria"]]
            rows.append((username, score))
            results[username] = {
                "total": score,
                "max_points": sum(t["points"] for t in RUBRIC["criteria"]),
                "criteria": detail
            }

    with open("scores.csv", "w", newline="") as f:
        csv.writer(f).writerows(rows)
    with open("detailed_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("✓ Done. scores.csv and detailed_results.json generated.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python batch_grader.py submissions.zip")
        sys.exit(1)
    main(sys.argv[1])
