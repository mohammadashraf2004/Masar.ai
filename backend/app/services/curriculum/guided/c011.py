"""COURSE-011 Cloud Deployment and CI/CD for AI Engineers: guided lab files.

These labs run on the learner's own machine (shell, Git, Docker, Terraform,
kubectl). The practice sandbox does not execute them; each completed line is
compared with the expected command or setting, ignoring extra spaces.
"""
from . import Guided

READ_NOTE = (
    "Shell commands and configuration files are checked by reading them: each completed line is compared with the expected command, ignoring extra spaces. Run them on your own machine to see the result.",
    "تُفحص أوامر الصدفة وملفات الإعداد بقراءتها: يُقارن كل سطر مكتمل بالأمر المتوقع مع تجاهل المسافات الزائدة. شغّلها على جهازك لترى النتيجة.",
)
COMMIT_MESSAGE = r're:"[^"\n]{5,}"'
DOCKER_USER = r"[a-z0-9][a-z0-9._-]*"

EXERCISES = {
    "COURSE-011.M01.L01.EX03": Guided(
        goal=("Create a small project structure from the command line and verify every change.",
              "أنشئ بنية مشروع صغيرة من سطر الأوامر وتحقّق من كل تغيير."),
        steps=(
            ("Create the project folder with its three sub-folders.", "أنشئ مجلد المشروع مع مجلداته الفرعية الثلاثة."),
            ("Write the heading into README.md (overwrite, do not append).", "اكتب العنوان في README.md (استبدال لا إلحاق)."),
            ("List the whole structure recursively.", "اعرض البنية كاملة بشكل تعاودي."),
            ("Copy the README into docs.", "انسخ ملف README إلى docs."),
            ("Rename app.txt to application.txt.", "أعد تسمية app.txt إلى application.txt."),
        ),
        starter='''# Step 1: the project folder plus src, docs and scripts in one command (-p creates parents, no error if present)
mkdir -p ___
cd ~/devops-practice
touch README.md src/app.txt scripts/deploy.sh
# Step 2: put the heading into README.md
echo '# DevOps Practice' ___ README.md
pwd
# Step 3: list everything, recursively
___
# Step 4: copy the README into docs
___ README.md docs/README-copy.md
# Step 5: rename src/app.txt
___ src/app.txt src/application.txt
''',
        answers=("~/devops-practice/{src,docs,scripts}", ">", "ls -R", "cp", "mv"),
        alternatives={
            1: ("~/devops-practice/src ~/devops-practice/docs ~/devops-practice/scripts",
                "$HOME/devops-practice/{src,docs,scripts}"),
            3: ("ls -R .", "ls -lR", "ls -laR", "find .", "tree"),
        },
        blanks=(
            ("use `~/devops-practice/{src,docs,scripts}` - brace expansion creates all three.", "استخدم `~/devops-practice/{src,docs,scripts}` - توسيع الأقواس ينشئ الثلاثة."),
            ("`>` writes the file from scratch (`>>` would append).", "يكتب `>` الملف من البداية (أما `>>` فيُلحق)."),
            ("`ls -R` lists every folder recursively.", "يعرض `ls -R` كل المجلدات تعاوديًا."),
            ("`cp` copies a file.", "ينسخ `cp` الملف."),
            ("`mv` moves - and therefore renames - a file.", "ينقل `mv` الملف - وبذلك يعيد تسميته."),
        ),
        hints=(
            ("`mkdir -p` creates missing parent folders and is safe to repeat.", "ينشئ `mkdir -p` المجلدات الأم المفقودة، وتكراره آمن."),
            ("Redirection: `>` replaces a file's content, `>>` adds to the end.", "إعادة التوجيه: يستبدل `>` محتوى الملف، ويضيف `>>` إلى نهايته."),
            ("`cp source target` copies; `mv old new` renames.", "`cp source target` ينسخ، و`mv old new` يعيد التسمية."),
        ),
        success=("Correct! `mkdir -p`, `touch` and `ls` are safe to repeat; `cp`, `mv` and `>` overwrite their target, so a wrong path there destroys data.",
                 "صحيح! تكرار `mkdir -p` و`touch` و`ls` آمن، أما `cp` و`mv` و`>` فتكتب فوق هدفها، فيدمّر المسار الخاطئ هنا البيانات."),
        expected=READ_NOTE,
        language="bash",
    ),
    "COURSE-011.M01.L01.EX04": Guided(
        goal=("Verify your DevOps workstation with one command per tool, and know what each successful result proves.",
              "تحقّق من محطة عمل DevOps بأمر واحد لكل أداة، واعرف ما يثبته كل نجاح."),
        steps=(
            ("Print the installed Git version.", "اطبع إصدار Git المثبّت."),
            ("List your global Git configuration.", "اعرض إعدادات Git العامة."),
            ("Print the Docker version.", "اطبع إصدار Docker."),
            ("Run Docker's hello-world container.", "شغّل حاوية hello-world من Docker."),
        ),
        starter='''# Step 1: is Git installed?
___
# Step 2: who will your commits be attributed to?
___
# Open VS Code here and check the integrated terminal works
code .
# Step 3: is the Docker CLI installed?
___
# Step 4: can the Docker engine pull and run a container? (Docker Desktop must be running)
___
''',
        answers=("git --version", "git config --global --list", "docker --version", "docker run hello-world"),
        alternatives={2: ("git config --global -l", "git config --list --global")},
        blanks=(
            ("`git --version` proves Git is installed and on your PATH.", "يثبت `git --version` أن Git مثبّت وموجود في PATH."),
            ("`git config --global --list` shows your name and email.", "يعرض `git config --global --list` اسمك وبريدك الإلكتروني."),
            ("`docker --version` proves the CLI is installed.", "يثبت `docker --version` أن واجهة السطر مثبّتة."),
            ("`docker run hello-world` proves the engine can pull and run images.", "يثبت `docker run hello-world` أن المحرّك يستطيع سحب الصور وتشغيلها."),
        ),
        hints=(
            ("Most tools print their version with `--version`.", "تطبع معظم الأدوات إصدارها بـ `--version`."),
            ("`git config` has a `--global` scope and a `--list` action.", "لـ `git config` نطاق `--global` وإجراء `--list`."),
            ("`docker run IMAGE` pulls the image if needed and starts a container.", "يسحب `docker run IMAGE` الصورة عند الحاجة ويبدأ حاوية."),
        ),
        success=("Correct! A version proves a tool is installed; only `docker run hello-world` proves the Docker engine actually works.",
                 "صحيح! يثبت الإصدار أن الأداة مثبّتة، ولا يثبت أن محرّك Docker يعمل فعلًا إلا `docker run hello-world`."),
        expected=READ_NOTE,
        reflect=("Pick a cloud provider for future labs and write two cost-safety rules you will follow before creating any resource.",
                 "اختر مزوّدًا سحابيًا للمختبرات القادمة، واكتب قاعدتين للأمان المالي ستتبعهما قبل إنشاء أي مورد."),
        language="bash",
    ),
    "COURSE-011.M02.L01.EX01": Guided(
        goal=("Move changes deliberately through Git's working directory, staging area and repository.",
              "انقل التغييرات عمدًا عبر مجلد العمل ومنطقة التجهيز والمستودع في Git."),
        steps=(
            ("Initialize the repository.", "هيّئ المستودع."),
            ("Stage only README.md.", "جهّز README.md وحده."),
            ("Commit it with a meaningful message.", "احفظه (commit) برسالة ذات معنى."),
            ("Show the history.", "اعرض السجل."),
        ),
        starter='''mkdir git-three-trees-lab && cd git-three-trees-lab
# Step 1: turn this folder into a Git repository
___
echo "Project overview" > README.md
echo "Private notes" > notes.txt
git status
# Step 2: stage ONLY README.md
___
git status            # README.md is staged; notes.txt is still only in the working directory
# Step 3: record the staged snapshot with a meaningful message in quotes
git commit -m ___
git status
# Step 4: show the commit history
___
''',
        answers=("git init", "git add README.md", '"Add project README"', "git log"),
        alternatives={3: (COMMIT_MESSAGE,), 4: ("git log --oneline",)},
        blanks=(
            ("run `git init`.", "شغّل `git init`."),
            ("stage just the one file: `git add README.md`.", "جهّز الملف الواحد فقط: `git add README.md`."),
            ("write a short message in double quotes, e.g. `\"Add project README\"`.", "اكتب رسالة قصيرة بين علامتي اقتباس مزدوجتين، مثل `\"Add project README\"`."),
            ("run `git log`.", "شغّل `git log`."),
        ),
        hints=(
            ("Every repository starts with the one Git command that creates the hidden .git folder.", "يبدأ كل مستودع بأمر Git واحد ينشئ المجلد المخفي .git."),
            ("`git add <file>` stages exactly that file - not `git add .`.", "يجهّز `git add <file>` ذلك الملف تحديدًا - لا `git add .`."),
            ("A commit message describes what the change does.", "تصف رسالة الحفظ ما يفعله التغيير."),
        ),
        success=("Correct! README.md moved working directory → staging area → repository, while notes.txt is still untracked in the working directory only.",
                 "صحيح! انتقل README.md من مجلد العمل إلى منطقة التجهيز ثم إلى المستودع، بينما بقي notes.txt غير متتبَّع في مجلد العمل فقط."),
        expected=READ_NOTE,
        language="bash",
    ),
    "COURSE-011.M02.L01.EX03": Guided(
        goal=("Go from a cloned repository to a reviewable pull request on a feature branch.",
              "انتقل من مستودع مستنسَخ إلى طلب دمج (pull request) قابل للمراجعة على فرع ميزة."),
        steps=(
            ("Create and switch to the feature branch.", "أنشئ فرع الميزة وانتقل إليه."),
            ("Stage the new file.", "جهّز الملف الجديد."),
            ("Commit with a descriptive message.", "احفظ برسالة وصفية."),
            ("Push the branch and set upstream tracking.", "ادفع الفرع واضبط تتبّع المنبع."),
            ("Open the pull request.", "افتح طلب الدمج."),
        ),
        starter='''git clone https://github.com/<you>/practice-repo.git
cd practice-repo
# Step 1: a new branch for this feature
___
echo "Practice project for the DevOps course." > ABOUT.md
git status
# Step 2: stage the new file
___
# Step 3: describe the change
git commit -m ___
# Step 4: publish the branch and remember origin as its upstream
___
# Step 5: open a pull request (GitHub CLI) - or use "Compare & pull request" on GitHub
___
''',
        answers=("git switch -c feature/add-about-section", "git add ABOUT.md", '"Add ABOUT section"',
                 "git push -u origin feature/add-about-section", "gh pr create --fill"),
        alternatives={
            1: ("git checkout -b feature/add-about-section",),
            3: (COMMIT_MESSAGE,),
            4: ("git push --set-upstream origin feature/add-about-section",),
            5: (r"re:gh pr create( .*)?",),
        },
        blanks=(
            ("`git switch -c feature/add-about-section` creates and switches in one step.", "ينشئ `git switch -c feature/add-about-section` الفرع وينتقل إليه في خطوة واحدة."),
            ("run `git add ABOUT.md`.", "شغّل `git add ABOUT.md`."),
            ("write a descriptive message in double quotes.", "اكتب رسالة وصفية بين علامتي اقتباس مزدوجتين."),
            ("`git push -u origin feature/add-about-section` sets the upstream.", "يضبط `git push -u origin feature/add-about-section` المنبع."),
            ("`gh pr create` opens the pull request (add `--fill` to reuse the commit message).", "يفتح `gh pr create` طلب الدمج (أضف `--fill` لإعادة استخدام رسالة الحفظ)."),
        ),
        hints=(
            ("`-c` (or `checkout -b`) creates the branch before switching to it.", "ينشئ `-c` (أو `checkout -b`) الفرع قبل الانتقال إليه."),
            ("`-u` remembers the remote branch, so later `git push` needs no arguments.", "يتذكّر `-u` الفرع البعيد، فلا يحتاج `git push` لاحقًا إلى وسائط."),
            ("The pull request is where a reviewer sees what changed, why, and how to verify it.", "طلب الدمج هو المكان الذي يرى فيه المراجع ما تغيّر ولماذا وكيف يتحقق منه."),
        ),
        success=("Correct! The change lives on its own branch, so main only changes after someone has reviewed the pull request.",
                 "صحيح! يعيش التغيير على فرعه الخاص، فلا يتغير main إلا بعد أن يراجع أحدٌ طلب الدمج."),
        expected=READ_NOTE,
        reflect=("Why is merging through the pull request safer than pushing the feature straight to main?",
                 "لماذا يكون الدمج عبر طلب الدمج أكثر أمانًا من دفع الميزة مباشرة إلى main؟"),
        language="bash",
    ),
    "COURSE-011.M02.L01.EX04": Guided(
        goal=("Create a merge conflict on purpose and resolve it with the text you actually intend.",
              "أنشئ تعارض دمج عمدًا وحلّه بالنص الذي تقصده فعلًا."),
        steps=(
            ("Merge the second branch to trigger the conflict.", "ادمج الفرع الثاني لإحداث التعارض."),
            ("Write the resolved line, without conflict markers.", "اكتب السطر المحلول دون علامات التعارض."),
            ("Stage the resolved file.", "جهّز الملف المحلول."),
            ("Complete the merge commit.", "أكمل حفظ الدمج."),
        ),
        starter='''echo "Deployment status: pending" > README.md && git add README.md && git commit -m "Add status"
git switch -c ready && echo "Deployment status: ready for staging" > README.md && git commit -am "Ready"
git switch main && git switch -c blocked && echo "Deployment status: blocked by tests" > README.md && git commit -am "Blocked"
git switch main && git merge ready
# Step 1: merge the other branch - both changed the same line, so Git stops with a conflict
___
# README.md now shows <<<<<<< HEAD (main's line) ======= (the incoming line) >>>>>>> blocked
# Step 2: write ONE final line that states the real situation (no markers left)
echo ___ > README.md
# Step 3: mark the conflict as resolved
___
# Step 4: finish the merge
___
git status && git log --oneline --graph
''',
        answers=("git merge blocked", '"Deployment status: blocked by tests"', "git add README.md", "git commit"),
        alternatives={
            2: (r're:"Deployment status: [^"<>=\n]{3,}"',),
            4: ("git commit --no-edit", COMMIT_MESSAGE.replace('re:"', 're:git commit -m "'), "git merge --continue"),
        },
        blanks=(
            ("merge the second branch: `git merge blocked`.", "ادمج الفرع الثاني: `git merge blocked`."),
            ("write one real status in quotes, e.g. `\"Deployment status: blocked by tests\"` - no `<<<<<<<`, `=======` or `>>>>>>>`.",
             "اكتب حالة حقيقية واحدة بين علامتي اقتباس، مثل `\"Deployment status: blocked by tests\"` - دون `<<<<<<<` أو `=======` أو `>>>>>>>`."),
            ("`git add README.md` tells Git the conflict is resolved.", "يخبر `git add README.md` Git بأن التعارض حُلّ."),
            ("`git commit` (or `git merge --continue`) creates the merge commit.", "ينشئ `git commit` (أو `git merge --continue`) حفظ الدمج."),
        ),
        hints=(
            ("The conflict appears on the second merge, because the first one already changed the line.", "يظهر التعارض في الدمج الثاني، لأن الأول غيّر السطر بالفعل."),
            ("The HEAD block is what main has now; the block after ======= is what is coming in.", "كتلة HEAD هي ما لدى main الآن، والكتلة بعد ======= هي الوافدة."),
            ("After editing, stage the file and commit - Git then records a merge commit.", "بعد التعديل، جهّز الملف واحفظه - فيسجّل Git حفظ دمج."),
        ),
        success=("Correct! You chose the final wording yourself; Git could not, because both branches changed the same line in contradictory ways.",
                 "صحيح! اخترت الصياغة النهائية بنفسك؛ ولم يكن Git قادرًا على ذلك لأن الفرعين غيّرا السطر نفسه بطريقتين متناقضتين."),
        expected=READ_NOTE,
        language="bash",
    ),
    "COURSE-011.M03.L01.EX02": Guided(
        goal=("Write the lesson's Flask Dockerfile and know why each instruction is there.",
              "اكتب ملف Dockerfile لتطبيق Flask كما في الدرس، واعرف سبب وجود كل تعليمة."),
        steps=(
            ("Start from the slim Python 3.9 image.", "ابدأ من صورة Python 3.9 المصغّرة."),
            ("Work in `/app`.", "اعمل داخل `/app`."),
            ("Copy `requirements.txt` before the source.", "انسخ `requirements.txt` قبل الكود."),
            ("Document port 8080.", "وثّق المنفذ 8080."),
            ("Start Gunicorn on 0.0.0.0:8080.", "شغّل Gunicorn على 0.0.0.0:8080."),
        ),
        starter='''# Step 1: the base image
FROM ___
# Step 2: every following path is relative to /app
WORKDIR ___
# Step 3: dependencies first, so source edits do not reinstall them
COPY ___
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Step 4: the port the app listens on
EXPOSE ___
# Step 5: the production server, reachable from outside the container
CMD ["gunicorn", "--bind", ___, "app:app"]
''',
        answers=("python:3.9-slim", "/app", "requirements.txt .", "8080", '"0.0.0.0:8080"'),
        alternatives={1: (r"re:python:3\.\d+-slim",), 3: ("requirements.txt ./", "./requirements.txt .")},
        blanks=(
            ("use `python:3.9-slim`.", "استخدم `python:3.9-slim`."),
            ("set `WORKDIR /app`.", "اضبط `WORKDIR /app`."),
            ("copy `requirements.txt .` first.", "انسخ `requirements.txt .` أولًا."),
            ("expose `8080`.", "اعرض المنفذ `8080`."),
            ("bind to `\"0.0.0.0:8080\"`.", "اربط على `\"0.0.0.0:8080\"`."),
        ),
        hints=(
            ("Slim images keep the image small.", "تُبقي الصور المصغّرة حجم الصورة صغيرًا."),
            ("Layer order decides what Docker can reuse from cache.", "يحدد ترتيب الطبقات ما يستطيع Docker إعادة استخدامه من الذاكرة المؤقتة."),
            ("Inside a container, 0.0.0.0 means 'every interface'.", "داخل الحاوية يعني 0.0.0.0 «كل الواجهات»."),
        ),
        success=("Correct! On a second build after editing only app.py, Docker reuses every layer up to `RUN pip install` and rebuilds only from `COPY . .`.",
                 "صحيح! في البناء الثاني بعد تعديل app.py فقط، يعيد Docker استخدام كل الطبقات حتى `RUN pip install` ويعيد البناء بدءًا من `COPY . .`."),
        expected=READ_NOTE,
        reflect=("Write a .dockerignore that excludes .git, __pycache__, *.pyc, venv/ and .env. Why does each one matter?",
                 "اكتب ملف .dockerignore يستبعد .git و__pycache__ و*.pyc وvenv/ و.env. لماذا يهم كلٌّ منها؟"),
        language="dockerfile",
    ),
    "COURSE-011.M03.L01.EX03": Guided(
        goal=("Turn a long `docker run` command into a Compose service with port mapping and a live code mount.",
              "حوّل أمر `docker run` طويلًا إلى خدمة Compose مع ربط المنافذ وربط حي للكود."),
        steps=(
            ("Build the image from the current folder.", "ابنِ الصورة من المجلد الحالي."),
            ("Map host port 4000 to container port 8080.", "اربط منفذ المضيف 4000 بمنفذ الحاوية 8080."),
            ("Mount the project folder at /app.", "اربط مجلد المشروع بـ /app."),
        ),
        starter='''services:
  web:
    # Step 1: build from the Dockerfile in this folder
    build: ___
    ports:
      # Step 2: host 4000 -> container 8080
      - ___
    volumes:
      # Step 3: the project folder, live inside the container
      - ___
# Then: docker compose up --build    |   docker compose logs web   |   docker compose down
''',
        answers=(".", '"4000:8080"', ".:/app"),
        alternatives={1: ("./",), 2: ("4000:8080",), 3: ("./:/app",)},
        blanks=(
            ("`build: .` uses the Dockerfile here.", "يستخدم `build: .` ملف Dockerfile هنا."),
            ("`\"4000:8080\"` is host:container.", "`\"4000:8080\"` بصيغة host:container."),
            ("`.:/app` mounts the current folder at /app.", "يربط `.:/app` المجلد الحالي بـ /app."),
        ),
        hints=(
            ("Each line replaces one `docker run` flag: `-p` becomes `ports`, `-v` becomes `volumes`.", "يحل كل سطر محل خيار من `docker run`: يصبح `-p` هو `ports`، ويصبح `-v` هو `volumes`."),
            ("Quote port mappings so YAML does not misread them.", "ضع ربط المنافذ بين علامتي اقتباس كي لا يسيء YAML قراءته."),
            ("A bind mount is `host_path:container_path`.", "الربط بصيغة `host_path:container_path`."),
        ),
        success=("Correct! `docker compose up` now replaces the whole `docker run -p ... -v ...` command, and edits to app.py appear in the running container through the mount.",
                 "صحيح! أصبح `docker compose up` يحل محل أمر `docker run -p ... -v ...` كاملًا، وتظهر تعديلات app.py في الحاوية العاملة عبر الربط."),
        expected=READ_NOTE,
        language="yaml",
    ),
    "COURSE-011.M03.L01.EX04": Guided(
        goal=("Tag, push and run a versioned image - the steps a CI pipeline will automate later.",
              "وسم صورة بإصدار ودفعها وتشغيلها - وهي الخطوات التي سيؤتمتها خط CI لاحقًا."),
        steps=(
            ("Tag the local image as `<your-user>/simple-flask-app:1.0.0`.", "ضع على الصورة المحلية الوسم `<your-user>/simple-flask-app:1.0.0`."),
            ("Log in to Docker Hub.", "سجّل الدخول إلى Docker Hub."),
            ("Push the versioned tag.", "ادفع الوسم ذا الإصدار."),
            ("Run that exact version on another machine.", "شغّل هذا الإصدار تحديدًا على جهاز آخر."),
        ),
        starter='''docker images simple-flask-app
# Step 1: a second name for the same image ID, in your Docker Hub namespace, version 1.0.0
___
docker images            # both tags point to the same IMAGE ID
# Step 2: authenticate (CI should use an access token, never your password)
___
# Step 3: upload the versioned tag
___
# Step 4: what another machine runs to get exactly this version
___
''',
        answers=("docker tag simple-flask-app yourusername/simple-flask-app:1.0.0", "docker login",
                 "docker push yourusername/simple-flask-app:1.0.0",
                 "docker run -p 4000:8080 yourusername/simple-flask-app:1.0.0"),
        alternatives={
            1: (rf"re:docker tag simple-flask-app(:latest)? {DOCKER_USER}/simple-flask-app:1\.0\.0",),
            2: (rf"re:docker login( -u {DOCKER_USER})?",),
            3: (rf"re:docker push {DOCKER_USER}/simple-flask-app:1\.0\.0",),
            4: (rf"re:docker run (-d )?-p 4000:8080 (-d )?{DOCKER_USER}/simple-flask-app:1\.0\.0",),
        },
        blanks=(
            ("`docker tag simple-flask-app <user>/simple-flask-app:1.0.0`.", "`docker tag simple-flask-app <user>/simple-flask-app:1.0.0`."),
            ("run `docker login`.", "شغّل `docker login`."),
            ("`docker push <user>/simple-flask-app:1.0.0`.", "`docker push <user>/simple-flask-app:1.0.0`."),
            ("`docker run -p 4000:8080 <user>/simple-flask-app:1.0.0`.", "`docker run -p 4000:8080 <user>/simple-flask-app:1.0.0`."),
        ),
        hints=(
            ("A tag is just another name for the same image ID.", "الوسم مجرد اسم آخر لمعرّف الصورة نفسه."),
            ("Push the tag that includes your namespace and version.", "ادفع الوسم الذي يتضمن مساحة اسمك وإصدارك."),
            ("Pinning `:1.0.0` guarantees every machine runs the same build.", "يضمن تثبيت `:1.0.0` أن كل جهاز يشغّل البناء نفسه."),
        ),
        success=("Correct! The image is published under a fixed version, so any machine can run exactly the same build - the foundation of repeatable deployments.",
                 "صحيح! نُشرت الصورة بإصدار ثابت، فيستطيع أي جهاز تشغيل البناء نفسه تمامًا - وهذا أساس عمليات النشر القابلة للتكرار."),
        expected=READ_NOTE,
        reflect=("Why should a CI system log in with an access token instead of your account password?",
                 "لماذا يجب أن يسجّل نظام CI الدخول برمز وصول بدل كلمة مرور حسابك؟"),
        language="bash",
    ),
    "COURSE-011.M04.L01.EX02": Guided(
        goal=("Write your first Terraform configuration: the AWS provider and one tagged S3 bucket.",
              "اكتب أول إعداد Terraform لك: مزوّد AWS وحاوية S3 واحدة ذات وسوم."),
        steps=(
            ("Name the provider source.", "اذكر مصدر المزوّد."),
            ("Choose the region.", "اختر المنطقة."),
            ("Declare an `aws_s3_bucket` resource named `my_bucket`.", "صرّح بمورد `aws_s3_bucket` اسمه `my_bucket`."),
            ("Give the bucket a globally unique name.", "امنح الحاوية اسمًا فريدًا عالميًا."),
        ),
        starter='''terraform {
  required_providers {
    aws = {
      # Step 1: where Terraform downloads the AWS provider from
      source  = ___
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  # Step 2: the region the bucket is created in
  region = ___
}

# Step 3: resource type, then the local name Terraform uses for it
resource ___ {
  # Step 4: must be unique across all of AWS
  bucket = ___
  tags = {
    Environment = "Dev"
    ManagedBy   = "Terraform"
  }
}
''',
        answers=('"hashicorp/aws"', '"us-east-1"', '"aws_s3_bucket" "my_bucket"', '"masar-devops-practice-2026"'),
        alternatives={2: (r're:"[a-z]{2}-[a-z]+-\d"',), 4: (r're:"[a-z0-9][a-z0-9.-]{2,62}"',)},
        blanks=(
            ("`\"hashicorp/aws\"` is the official provider.", "`\"hashicorp/aws\"` هو المزوّد الرسمي."),
            ("a region such as `\"us-east-1\"`.", "منطقة مثل `\"us-east-1\"`."),
            ("`\"aws_s3_bucket\" \"my_bucket\"` - the type, then your local name.", "`\"aws_s3_bucket\" \"my_bucket\"` - النوع ثم اسمك المحلي."),
            ("a unique lowercase bucket name in quotes.", "اسم حاوية فريد بأحرف صغيرة بين علامتي اقتباس."),
        ),
        hints=(
            ("Provider sources look like `namespace/name`.", "تبدو مصادر المزوّدين بالشكل `namespace/name`."),
            ("A resource block has two labels: the type and a name you choose.", "لكتلة المورد وسمان: النوع واسم تختاره."),
            ("S3 bucket names are global: lowercase letters, digits, dots and hyphens.", "أسماء حاويات S3 عالمية: أحرف صغيرة وأرقام ونقاط وشرطات."),
        ),
        success=("Correct! Terraform now knows which provider to download, where to create things, and exactly one resource to manage. Credentials stay outside this file.",
                 "صحيح! يعرف Terraform الآن أي مزوّد ينزّل، وأين ينشئ الموارد، ومَوردًا واحدًا بعينه يديره. وتبقى بيانات الاعتماد خارج هذا الملف."),
        expected=READ_NOTE,
        reflect=("Add a .gitignore with .terraform/, *.tfstate and *.tfstate.backup. Why must credentials and state stay out of the repository?",
                 "أضف ملف .gitignore فيه .terraform/ و*.tfstate و*.tfstate.backup. لماذا يجب أن تبقى بيانات الاعتماد والحالة خارج المستودع؟"),
        language="hcl",
    ),
    "COURSE-011.M04.L01.EX03": Guided(
        goal=("Run Terraform's init → plan → apply → destroy lifecycle and read each plan before confirming it.",
              "نفّذ دورة Terraform: init ثم plan ثم apply ثم destroy، واقرأ كل خطة قبل تأكيدها."),
        steps=(
            ("Initialize the working directory.", "هيّئ مجلد العمل."),
            ("Preview the changes.", "استعرض التغييرات مسبقًا."),
            ("Apply them after reviewing the plan.", "طبّقها بعد مراجعة الخطة."),
            ("Destroy everything when the lab is done.", "أزِل كل شيء عند انتهاء المختبر."),
        ),
        starter='''cd terraform-s3-bucket
# Step 1: download the provider and prepare .terraform/
___
# Step 2: preview - "+" means create, "~" update in place, "-" destroy
___
# Step 3: show the plan again, then create the bucket after you type "yes"
___
ls terraform.tfstate          # Terraform now remembers what it manages
# (change a tag in main.tf, run the plan again: it proposes "~" update in-place)
# Step 4: when you are done, review the destruction plan and remove everything
___
''',
        answers=("terraform init", "terraform plan", "terraform apply", "terraform destroy"),
        blanks=(
            ("run `terraform init`.", "شغّل `terraform init`."),
            ("run `terraform plan`.", "شغّل `terraform plan`."),
            ("run `terraform apply`.", "شغّل `terraform apply`."),
            ("run `terraform destroy`.", "شغّل `terraform destroy`."),
        ),
        hints=(
            ("init is needed once per folder, and again when providers change.", "يلزم init مرة لكل مجلد، ومرة أخرى عند تغيّر المزوّدين."),
            ("plan changes nothing; it only shows what would happen.", "لا يغيّر plan أي شيء؛ إنه يعرض فقط ما سيحدث."),
            ("Both apply and destroy print a plan and wait for `yes`.", "يطبع apply وdestroy كلاهما خطة وينتظران `yes`."),
        ),
        success=("Correct! Every change goes through a readable plan first - before creating and before destroying - which is what keeps infrastructure changes safe.",
                 "صحيح! يمر كل تغيير أولًا عبر خطة مقروءة - قبل الإنشاء وقبل الإزالة - وهذا ما يُبقي تغييرات البنية التحتية آمنة."),
        expected=READ_NOTE,
        reflect=("Why is reviewing the plan just as important before `destroy` as before `apply`?",
                 "لماذا تكون مراجعة الخطة قبل `destroy` بالأهمية نفسها قبل `apply`؟"),
        language="bash",
    ),
    "COURSE-011.M04.L01.EX04": Guided(
        goal=("Move hard-coded Terraform values into input variables and expose the bucket's ARN as an output.",
              "انقل قيم Terraform المكتوبة يدويًا إلى متغيرات إدخال، واعرض ARN الخاص بالحاوية بوصفه مُخرجًا."),
        steps=(
            ("Give `aws_region` a default of us-east-1.", "امنح `aws_region` القيمة الافتراضية us-east-1."),
            ("Use the region variable in the provider.", "استخدم متغير المنطقة في المزوّد."),
            ("Use the bucket-name variable in the resource.", "استخدم متغير اسم الحاوية في المورد."),
            ("Output the bucket's ARN.", "أخرج ARN الحاوية."),
        ),
        starter='''# ---- variables.tf ----
variable "aws_region" {
  type    = string
  # Step 1: a sensible default
  default = ___
}

variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name (set in terraform.tfvars)"
}

# ---- main.tf ----
provider "aws" {
  # Step 2: no more hard-coded region
  region = ___
}

resource "aws_s3_bucket" "my_bucket" {
  # Step 3: the name comes from terraform.tfvars
  bucket = ___
}

# ---- outputs.tf ----
output "s3_bucket_arn" {
  # Step 4: printed after terraform apply
  value = ___
}
''',
        answers=('"us-east-1"', "var.aws_region", "var.bucket_name", "aws_s3_bucket.my_bucket.arn"),
        alternatives={1: (r're:"[a-z]{2}-[a-z]+-\d"',)},
        blanks=(
            ("the default is `\"us-east-1\"`.", "القيمة الافتراضية `\"us-east-1\"`."),
            ("reference the variable: `var.aws_region`.", "أشِر إلى المتغير: `var.aws_region`."),
            ("reference `var.bucket_name`.", "أشِر إلى `var.bucket_name`."),
            ("`aws_s3_bucket.my_bucket.arn` - type, name, attribute.", "`aws_s3_bucket.my_bucket.arn` - النوع ثم الاسم ثم الخاصية."),
        ),
        hints=(
            ("Inside expressions, variables are read as `var.<name>`.", "داخل التعابير تُقرأ المتغيرات بالشكل `var.<name>`."),
            ("A resource attribute is `<type>.<local name>.<attribute>`.", "خاصية المورد بالشكل `<type>.<local name>.<attribute>`."),
            ("terraform.tfvars supplies `bucket_name = \"...\"` without changing the code.", "يوفّر terraform.tfvars القيمة `bucket_name = \"...\"` دون تغيير الكود."),
        ),
        success=("Correct! The same code now works for any region and bucket name: inputs come in through variables, results come out through outputs.",
                 "صحيح! أصبح الكود نفسه يعمل لأي منطقة واسم حاوية: تدخل المدخلات عبر المتغيرات وتخرج النتائج عبر المُخرجات."),
        expected=READ_NOTE,
        reflect=("Where does each variable value come from during `terraform plan`, and how would you reuse this for a staging bucket?",
                 "من أين تأتي قيمة كل متغير أثناء `terraform plan`؟ وكيف ستعيد استخدام هذا لحاوية بيئة staging؟"),
        language="hcl",
    ),
    "COURSE-011.M05.L01.EX02": Guided(
        goal=("Complete the lesson's GitHub Actions CI workflow that tests every push and pull request to main.",
              "أكمل سير عمل GitHub Actions للتكامل المستمر في الدرس، الذي يختبر كل دفع وطلب دمج إلى main."),
        steps=(
            ("Run the workflow on pull requests too.", "شغّل سير العمل عند طلبات الدمج أيضًا."),
            ("Run the job on an Ubuntu runner.", "شغّل المهمة على خادم Ubuntu."),
            ("Check out the repository first.", "استخرج المستودع أولًا."),
            ("Run the tests.", "شغّل الاختبارات."),
        ),
        starter='''name: Continuous Integration

on:
  push:
    branches: [ "main" ]
  # Step 1: also test proposed changes
  ___:
    branches: [ "main" ]

jobs:
  build-and-test:
    # Step 2: a fresh Linux machine for every run
    runs-on: ___
    steps:
      - name: Check out code
        # Step 3: get the repository's files onto the runner
        uses: ___
      - name: Set up Python 3.9
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests with pytest
        # Step 4: the command whose exit code decides pass or fail
        run: ___
''',
        answers=("pull_request", "ubuntu-latest", "actions/checkout@v3", "pytest"),
        alternatives={3: ("actions/checkout@v4",), 4: ("python -m pytest",)},
        blanks=(
            ("the event is `pull_request`.", "الحدث هو `pull_request`."),
            ("use `ubuntu-latest`.", "استخدم `ubuntu-latest`."),
            ("use `actions/checkout@v3`.", "استخدم `actions/checkout@v3`."),
            ("run `pytest`.", "شغّل `pytest`."),
        ),
        hints=(
            ("`on` lists the events that start the workflow.", "يسرد `on` الأحداث التي تبدأ سير العمل."),
            ("`runs-on` picks the runner image.", "يختار `runs-on` صورة الخادم المشغِّل."),
            ("The checkout action always comes first - the runner starts empty.", "يأتي إجراء checkout أولًا دائمًا - فالخادم يبدأ فارغًا."),
        ),
        success=("Correct! Every push and pull request to main now checks out the code, installs dependencies and runs pytest; a failing test fails the run.",
                 "صحيح! أصبح كل دفع وطلب دمج إلى main يستخرج الكود ويثبّت التبعيات ويشغّل pytest؛ ويُفشل الاختبارُ الفاشل التشغيلَ."),
        expected=READ_NOTE,
        reflect=("Which step runs first, which runs last, and what in the Actions UI proves the tests passed?",
                 "أي خطوة تعمل أولًا وأيها أخيرًا؟ وما الذي يثبت في واجهة Actions أن الاختبارات نجحت؟"),
        language="yaml",
    ),
    "COURSE-011.M06.L01.EX02": Guided(
        goal=("Complete the Deployment and Service manifests that run two Flask Pods and expose them through a NodePort.",
              "أكمل ملفي Deployment وService اللذين يشغّلان Podين لتطبيق Flask ويعرضانهما عبر NodePort."),
        steps=(
            ("Run 2 replicas.", "شغّل نسختين."),
            ("Use your Docker Hub image, version 1.0.0.", "استخدم صورتك في Docker Hub، الإصدار 1.0.0."),
            ("Declare the container port 8080.", "صرّح بمنفذ الحاوية 8080."),
            ("Forward Service port 80 to container port 8080.", "حوّل منفذ الخدمة 80 إلى منفذ الحاوية 8080."),
            ("Make the Service a NodePort.", "اجعل الخدمة من نوع NodePort."),
        ),
        starter='''apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-deployment
spec:
  # Step 1: desired number of Pods
  replicas: ___
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app            # must match the selector above and the Service below
    spec:
      containers:
        - name: web-server
          # Step 2: your image from Docker Hub
          image: ___
          ports:
            # Step 3: where Gunicorn listens inside the container
            - containerPort: ___
---
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - port: 80
      # Step 4: traffic is forwarded to this container port
      targetPort: ___
  # Step 5: reachable on a port of the node (minikube service flask-app-service)
  type: ___
''',
        answers=("2", "yourusername/simple-flask-app:1.0.0", "8080", "8080", "NodePort"),
        alternatives={2: (rf"re:{DOCKER_USER}/simple-flask-app:1\.0\.0",)},
        blanks=(
            ("set `replicas: 2`.", "اضبط `replicas: 2`."),
            ("use `<your-user>/simple-flask-app:1.0.0`.", "استخدم `<your-user>/simple-flask-app:1.0.0`."),
            ("the container listens on `8080`.", "تستمع الحاوية على `8080`."),
            ("`targetPort: 8080` sends traffic to the container port.", "يرسل `targetPort: 8080` الحركة إلى منفذ الحاوية."),
            ("set `type: NodePort`.", "اضبط `type: NodePort`."),
        ),
        hints=(
            ("The Deployment's selector, the Pod labels and the Service selector all say `app: flask-app`.", "يقول محدِّد Deployment ووسوم الـ Pod ومحدِّد الخدمة كلها `app: flask-app`."),
            ("`port` is the Service's own port; `targetPort` is the container's port.", "`port` هو منفذ الخدمة نفسها، و`targetPort` هو منفذ الحاوية."),
            ("NodePort exposes the Service on every node, which minikube can open for you.", "يعرض NodePort الخدمة على كل عقدة، ويستطيع minikube فتحها لك."),
        ),
        success=("Correct! Browser → node port → Service (port 80) → a Pod chosen by the `app: flask-app` label → container port 8080 → Gunicorn.",
                 "صحيح! المتصفح ← منفذ العقدة ← الخدمة (المنفذ 80) ← Pod يُختار بالوسم `app: flask-app` ← منفذ الحاوية 8080 ← Gunicorn."),
        expected=READ_NOTE,
        language="yaml",
    ),
    "COURSE-011.M06.L01.EX03": Guided(
        goal=("Scale a Deployment, roll out a new image, watch the rollout and roll it back.",
              "وسّع Deployment، وانشر صورة جديدة، وراقب النشر، ثم تراجع عنه."),
        steps=(
            ("Scale to 5 replicas.", "وسّع إلى 5 نسخ."),
            ("Switch the container to image version 2.0.0.", "بدّل الحاوية إلى الإصدار 2.0.0 من الصورة."),
            ("Follow the rollout until it finishes.", "تابع النشر حتى ينتهي."),
            ("Roll back if the new version misbehaves.", "تراجع إذا أساء الإصدار الجديد التصرف."),
        ),
        starter='''# Step 1: desired state 2 -> 5 Pods
___
kubectl get pods                  # three new Pods appear; the Service finds them by label
# Step 2: container "web-server" gets the new image tag
___
# Step 3: watch the rolling update until it completes
___
# Step 4: the new version is broken - go back to the previous ReplicaSet
___
''',
        answers=(
            "kubectl scale deployment flask-app-deployment --replicas=5",
            "kubectl set image deployment/flask-app-deployment web-server=yourusername/simple-flask-app:2.0.0",
            "kubectl rollout status deployment/flask-app-deployment",
            "kubectl rollout undo deployment/flask-app-deployment",
        ),
        alternatives={
            1: ("kubectl scale deployment/flask-app-deployment --replicas=5", "kubectl scale --replicas=5 deployment/flask-app-deployment"),
            2: (rf"re:kubectl set image deployment[/ ]flask-app-deployment web-server={DOCKER_USER}/simple-flask-app:2\.0\.0",),
            3: ("kubectl rollout status deployment flask-app-deployment",),
            4: ("kubectl rollout undo deployment flask-app-deployment",),
        },
        blanks=(
            ("`kubectl scale deployment flask-app-deployment --replicas=5`.", "`kubectl scale deployment flask-app-deployment --replicas=5`."),
            ("`kubectl set image deployment/flask-app-deployment web-server=<user>/simple-flask-app:2.0.0`.", "`kubectl set image deployment/flask-app-deployment web-server=<user>/simple-flask-app:2.0.0`."),
            ("`kubectl rollout status deployment/flask-app-deployment`.", "`kubectl rollout status deployment/flask-app-deployment`."),
            ("`kubectl rollout undo deployment/flask-app-deployment`.", "`kubectl rollout undo deployment/flask-app-deployment`."),
        ),
        hints=(
            ("`kubectl scale` changes the replica count in the desired state.", "يغيّر `kubectl scale` عدد النسخ في الحالة المرغوبة."),
            ("`set image` takes `container-name=image:tag`.", "يأخذ `set image` الصيغة `container-name=image:tag`."),
            ("`rollout status` and `rollout undo` act on `deployment/<name>`.", "يعمل `rollout status` و`rollout undo` على `deployment/<name>`."),
        ),
        success=("Correct! You only ever changed the desired state; Kubernetes reconciled it by creating, replacing or restoring Pods - and the Service followed them by label.",
                 "صحيح! لم تغيّر إلا الحالة المرغوبة؛ وطابقها Kubernetes بإنشاء الـ Pods أو استبدالها أو استعادتها - وتبعتها الخدمة بالوسم."),
        expected=READ_NOTE,
        language="bash",
    ),
    "COURSE-011.M06.L01.EX04": Guided(
        goal=("Separate a reusable Helm template from environment-specific values for dev, staging and production.",
              "افصل قالب Helm القابل لإعادة الاستخدام عن القيم الخاصة بكل بيئة: dev وstaging وproduction."),
        steps=(
            ("Read the replica count from the values.", "اقرأ عدد النسخ من القيم."),
            ("Read the image tag from the values.", "اقرأ وسم الصورة من القيم."),
            ("Set production's replica count.", "اضبط عدد النسخ في production."),
            ("Set production's image tag.", "اضبط وسم الصورة في production."),
        ),
        starter='''# ---- templates/deployment.yaml (excerpt): the same for every environment ----
spec:
  # Step 1
  replicas: {{ ___ }}
  template:
    spec:
      containers:
        - name: web-server
          # Step 2
          image: "{{ .Values.image.repository }}:{{ ___ }}"
          resources:
            limits:
              memory: {{ .Values.resources.memoryLimit }}

# ---- values-prod.yaml: only what differs in production ----
# Step 3: at least three Pods
replicaCount: ___
image:
  repository: yourusername/simple-flask-app
  # Step 4: a pinned release, never "latest"
  tag: ___
resources:
  memoryLimit: 512Mi
''',
        answers=(".Values.replicaCount", ".Values.image.tag", "3", '"1.0.0"'),
        alternatives={3: (r"re:([3-9]|[1-9]\d+)",), 4: (r're:"\d+\.\d+\.\d+"', r"re:\d+\.\d+\.\d+")},
        blanks=(
            ("use `.Values.replicaCount`.", "استخدم `.Values.replicaCount`."),
            ("use `.Values.image.tag`.", "استخدم `.Values.image.tag`."),
            ("production runs at least 3 replicas.", "تعمل بيئة production بثلاث نسخ على الأقل."),
            ("pin a version such as `\"1.0.0\"`.", "ثبّت إصدارًا مثل `\"1.0.0\"`."),
        ),
        hints=(
            ("Templates read values with `{{ .Values.<key> }}`.", "تقرأ القوالب القيم بالشكل `{{ .Values.<key> }}`."),
            ("Nested keys use dots: `.Values.image.tag`.", "تُستخدم النقاط للمفاتيح المتداخلة: `.Values.image.tag`."),
            ("A pinned semantic version makes production deployments repeatable.", "يجعل الإصدار الدلالي المثبّت نشر production قابلًا للتكرار."),
        ),
        success=("Correct! One chart plus three small values files replaces three copied manifest folders: `helm install` renders the same templates with each environment's values.",
                 "صحيح! يحل مخطط واحد مع ثلاثة ملفات قيم صغيرة محل ثلاثة مجلدات منسوخة من الملفات؛ إذ يعرض `helm install` القوالب نفسها بقيم كل بيئة."),
        expected=READ_NOTE,
        reflect=("Explain the difference between a Chart, a Helm repository and a release.",
                 "اشرح الفرق بين المخطط (Chart) ومستودع Helm والإصدار (release)."),
        language="yaml",
    ),
    "COURSE-011.M08.L06.EX02": Guided(
        goal=("Write the Subject Alternative Name list so one certificate secures the primary domain and three subdomains.",
              "اكتب قائمة الأسماء البديلة للموضوع (SAN) كي تؤمّن شهادة واحدة النطاق الرئيسي وثلاثة نطاقات فرعية."),
        steps=(
            ("Point the extension at the `alt_names` section.", "اجعل الامتداد يشير إلى قسم `alt_names`."),
            ("List the primary domain.", "اذكر النطاق الرئيسي."),
            ("List the API subdomain.", "اذكر النطاق الفرعي للواجهة البرمجية."),
            ("List the app and docs subdomains.", "اذكر النطاقين الفرعيين للتطبيق والوثائق."),
        ),
        starter='''[req_ext]
# Step 1: take the names from the section below
subjectAltName = @___

[alt_names]
# Step 2: the primary domain
DNS.1 = ___
# Step 3
DNS.2 = ___
# Step 4
DNS.3 = app.example.org
DNS.4 = ___
''',
        answers=("alt_names", "example.org", "api.example.org", "docs.example.org"),
        blanks=(
            ("reference the section name `alt_names`.", "أشِر إلى اسم القسم `alt_names`."),
            ("the primary domain is `example.org`.", "النطاق الرئيسي هو `example.org`."),
            ("`api.example.org`.", "`api.example.org`."),
            ("`docs.example.org`.", "`docs.example.org`."),
        ),
        hints=(
            ("`@section` tells OpenSSL to read the list from that section.", "يخبر `@section` OpenSSL بقراءة القائمة من ذلك القسم."),
            ("Every hostname the certificate must secure needs its own DNS.N line.", "يحتاج كل اسم مضيف يجب أن تؤمّنه الشهادة إلى سطر DNS.N خاص به."),
            ("The primary domain is listed too - it is not added automatically.", "يُذكر النطاق الرئيسي أيضًا - فهو لا يُضاف تلقائيًا."),
        ),
        success=("Correct! The certificate request now names all four hostnames explicitly.",
                 "صحيح! أصبح طلب الشهادة يذكر أسماء المضيفات الأربعة صراحةً."),
        expected=READ_NOTE,
        reflect=("What should `openssl req -noout -text -in server.csr` confirm before you submit the CSR?",
                 "ما الذي يجب أن يؤكده `openssl req -noout -text -in server.csr` قبل إرسال طلب الشهادة؟"),
        language="ini",
    ),
}
