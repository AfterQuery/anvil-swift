

cd /app
# If .git/ is missing (e.g. repo uploaded as zip without git history),
# initialize a git repo so git apply can work
if [ ! -d .git ]; then
    git init -q
    git add -A
    git commit -q -m "init" --allow-empty
fi
git reset --hard fa320f1cc5cfe1e58ac538c22e5165a08dc34b8a 2>/dev/null || true
git checkout fa320f1cc5cfe1e58ac538c22e5165a08dc34b8a 2>/dev/null || true
git apply -v --ignore-whitespace /workspace/patch.diff 2>&1 || \
patch -p1 --forward --reject-file=- --no-backup-if-mismatch < /workspace/patch.diff 2>&1 || true

bash /workspace/run_script.sh tasks/task-4/task_tests.py > /workspace/stdout.log 2> /workspace/stderr.log
python3 /workspace/parser.py /workspace/stdout.log /workspace/stderr.log /workspace/output.json
