import subprocess
import sys
import os
import time

ROOT = os.path.abspath(os.path.dirname(__file__))


def run_script(folder, script):

    folder_path = os.path.join(ROOT, folder)
    script_path = os.path.join(folder_path, script)

    if not os.path.isdir(folder_path):
        print(f"\n❌ Folder not found:\n{folder_path}")
        sys.exit(1)

    if not os.path.isfile(script_path):
        print(f"\n❌ Script not found:\n{script_path}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print(f"Running: {script_path}")
    print("=" * 70)

    start = time.time()

    result = subprocess.run(
        [sys.executable, script],
        cwd=folder_path
    )

    if result.returncode != 0:
        print(f"\n❌ Error while running {script}")
        sys.exit(result.returncode)

    elapsed = time.time() - start

    print(f"\n✅ Finished {script}")
    print(f"⏱ Time: {elapsed:.2f} seconds")


def main():

    total_start = time.time()

    print("\n" + "=" * 70)
    print("FAMILY DIABETES AI PIPELINE")
    print("=" * 70)

    # Step 1 - Generate Population
    run_script(
        os.path.join("models", "generator"),
        "generate_population.py"
    )

    # Step 2 - Merge Datasets
    run_script(
        "data_integration",
        "merge_datasets.py"
    )

    # Step 3 - Train Model
    run_script(
        "training",
        "ultimate_training.py"
    )

    total_time = time.time() - total_start

    print("\n" + "=" * 70)
    print("PIPELINE FINISHED SUCCESSFULLY")
    print("=" * 70)
    print(f"Total Execution Time: {total_time / 60:.2f} minutes")


if __name__ == "__main__":
    main()