

cd /app
# If .git/ is missing (e.g. repo uploaded as zip without git history),
# initialize a git repo so git apply can work
if [ ! -d .git ]; then
    git init -q
    git add -A
    git commit -q -m "init" --allow-empty
fi
git reset --hard 3d3ae151d854187f5e0090dc08faf4246473df7d 2>/dev/null || true
git checkout 3d3ae151d854187f5e0090dc08faf4246473df7d 2>/dev/null || true
git apply -v --ignore-whitespace /workspace/patch.diff 2>&1 || \
patch -p1 --forward --reject-file=- --no-backup-if-mismatch < /workspace/patch.diff 2>&1 || true

bash /workspace/run_script.sh tasks/task-1/task_tests.py > /workspace/stdout.log 2> /workspace/stderr.log
python3 /workspace/parser.py /workspace/stdout.log /workspace/stderr.log /workspace/output.json
