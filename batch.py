import os
import subprocess

BATCH_SIZE = 100
EXTENSION = ".mp4"
COMMIT_PREFIX = "Add batch"

def run_git_command(args):
    subprocess.run(["git"] + args, check=True)

def batch_commit_and_push(files):
    for i in range(0, len(files), BATCH_SIZE):
        batch = files[i:i + BATCH_SIZE]
        batch_number = i // BATCH_SIZE + 1
        print(f"\n→ Committing and pushing batch {batch_number} with {len(batch)} files")

        try:
            run_git_command(["add"] + batch)
            run_git_command(["commit", "-m", f"{COMMIT_PREFIX} {batch_number}"])
            run_git_command(["push"])
        except subprocess.CalledProcessError:
            print(f"❌ Error in batch {batch_number}, skipping...")

def main():
    all_files = sorted(f for f in os.listdir(".") if (f.endswith(EXTENSION) or f.endswith(".mov")) and os.path.isfile(f))
    print(f"📁 Found {len(all_files)} .mp4 files")

    if not all_files:
        print("⚠️  No matching files found.")
        return

    batch_commit_and_push(all_files)
    print("\n✅ All batches committed and pushed.")

if __name__ == "__main__":
    main()

