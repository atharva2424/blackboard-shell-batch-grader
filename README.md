# Blackboard Shell Batch Grader

Simple Python tool that auto‑grades **count_lines.sh** assignments exported from Blackboard.

## Steps
1. Export submissions from Blackboard as `submissions.zip`.
2. Run:  

   ```bash
   python batch_grader.py submissions.zip
   ```

3. Upload **scores.csv** to Grade Centre.
   `detailed_results.json` contains rubric‑aligned feedback.

## Extend
* Add more test files in `tests/` and update `rubric.json`.
* Adjust `points` per criterion for weighting.

---
