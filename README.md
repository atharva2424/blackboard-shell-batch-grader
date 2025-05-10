# Blackboard Shell Batch Grader

This is a **tiny Python tool** that grades students’ `count_lines.sh` shell–scripts that you exported from Blackboard.  It runs each script on a couple of test files, writes a gradebook CSV you can upload straight back into Blackboard, and saves detailed feedback in a JSON file.

---

## What’s in this folder

| Item                     | Purpose                                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------------- |
| `batch_grader.py`        | The main Python script you will run.                                                                    |
| `rubric.json`            | Says **which tests** to run and **how many points** each is worth.                                      |
| `tests/`                 | Test files used by the rubric.  We ship two: `sample_42.txt` (42 lines) and `sample_10.txt` (10 lines). |
| `sample_submissions.zip` | A practice export with 3 example students so you can see how grading works.                             |
| `scores.csv`             | (Created after you run the grader) – ready‑to‑upload gradebook.                                         |
| `detailed_results.json`  | (Created after you run the grader) – full per‑student feedback.                                         |


## Quick start (60 seconds)

1. **Open a terminal inside this folder.**
2. Make sure you have **Python 3.8+**:

   ```bash
   python --version   # or  python3 --version
   ```
3. **Grade the sample data**:

   ```bash
   python batch_grader.py sample_submissions.zip
   ```
4. The script prints a ✓ and creates two new files:

   * **`scores.csv`** – looks like

     ```csv
     Username,Score
     jsmith1,2
     rlee4,0
     kpatel3,0
     ```
   * **`detailed_results.json`** – shows exactly why each student lost points.
5. Open `scores.csv` in Excel **or** upload it to Blackboard → *Grade Centre → Upload Grades*.

That’s it – you have working autograding.

---

## Grading real Blackboard export

1. In Blackboard, go to the assignment → **Download All Submissions**.  Blackboard gives you a file like `submissions.zip`.
2. Move that zip into this folder.
3. Run:

   ```bash
   python batch_grader.py submissions.zip
   ```
4. Upload the new **`scores.csv`** back into Grade Centre.  If you want to show students detailed feedback, copy‑paste from `detailed_results.json` or attach it as a file.

---

## How it works

* `batch_grader.py` un‑zips each student folder into a temporary place.
* It looks for **`count_lines.sh`** inside that folder.
* For every criterion in **`rubric.json`** it runs:

  ```bash
  bash count_lines.sh tests/<file>
  ```

  and compares the output to the `expected` value.
* Scores add up; everything is saved into the JSON and CSV files.

---

## Changing the tests / points

1. Drop a new test file into **`tests/`**, e.g. `sample_100.txt`.
2. Open **`rubric.json`** and add a block:

   ```json
   {
     "name": "100‑line file",
     "description": "Correct line count for the 100‑line file.",
     "points": 1,
     "input": "tests/sample_100.txt",
     "expected": "100"
   }
   ```
3. Save and run the grader again – no other code changes needed.

(To weight a test more heavily, just change its `points` number.)

---

## Common errors & fixes

| Message in `detailed_results.json` | Meaning                                                | How to fix                                                           |
| ---------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------- |
| `count_lines.sh not found`         | Student uploaded the wrong file name or zipped folder. | Ask them to resubmit or adjust the filename inside the grader.       |
| `Expected 42, got …`               | Script produced the wrong answer.                      | Student bug – score stays 0 for that test.                           |
| `Error: [WinError 2]`              | Your Windows terminal can’t find **bash**.             | Open Git‑Bash **or** set the full path to bash in `batch_grader.py`. |
