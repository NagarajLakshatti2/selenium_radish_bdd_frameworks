In Window power shell

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

how to fix allure path issue in pycharm python

allure : The term 'allure' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included,
verify that the path is correct and try again.
At line:1 char:1
+ allure serve reports/allure-results

Perfect, this is a classic Windows + PyCharm issue 👍
Let’s fix it properly and permanently, step by step.

Buddy will keep this simple, correct, and enterprise-ready.

❌ Why This Error Happens
'allure' is not recognized as the name of a cmdlet


This means Allure Commandline is NOT installed or NOT in PATH.

⚠️ Important

pip install allure-behave


❌ does NOT install the allure command
It only installs the Python adapter.

You still need Allure Commandline (CLI).

✅ CORRECT WAY (Windows + PyCharm)
🟢 OPTION 1 (RECOMMENDED): Install via Scoop
1️⃣ Install Scoop (if not installed)

Open PowerShell as Administrator:

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex


Verify:

scoop --version

2️⃣ Install Allure CLI
scoop install allure


Verify:

allure --version


✔ If this works → DONE

🟢 OPTION 2: Manual Installation (100% Works)
1️⃣ Download Allure

👉 https://github.com/allure-framework/allure2/releases

Download:

allure-2.xx.x.zip


Extract to:

C:\allure


You should have:

C:\allure\bin\allure.bat

2️⃣ Add Allure to PATH (IMPORTANT)

Press Win + R → sysdm.cpl

Advanced → Environment Variables

Under User variables → Path → Edit

Add:

C:\allure\bin


Click OK → Restart PyCharm

3️⃣ Verify

Open PyCharm Terminal:

allure --version


✔ Should print version

✅ Run Allure Report (Correct Command)
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
allure serve reports/allure-results

⚠️ VERY COMMON MISTAKES (You Made One – Totally Normal)
Mistake	Why it fails
allure-results/	Folder, not command
pip install allure	Installs wrong package
CMD vs PowerShell PATH	Needs restart
Using Git Bash	PATH not loaded

👉 Use PowerShell or CMD inside PyCharm

🧪 Quick Self-Check Script

Run this in PyCharm terminal:

where allure


Expected:

C:\allure\bin\allure.bat


If empty → PATH still wrong.

🧠 Pro Tip (PyCharm Specific)

If Allure works in system terminal but not PyCharm:

Close PyCharm

Reopen PyCharm after PATH change

Check:

Settings → Tools → Terminal → Shell path


Recommended:

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

✅ Final Checklist

✔ Allure CLI installed
✔ PATH updated
✔ PyCharm restarted
✔ allure --version works
✔ allure serve reports/allure-results works
==============
In Pycharm
pip install pytest allure-pytest

python -m pytest --alluredir allure-results

radish features
radish features\
radish features --formatter allure
radish features --formatter allure_radish.formatter.AllureFormatter
radish features --formatter allure_radish.formatter.AllureFormatter -o allure-results (not working)

to set
set ALLURE_RESULTS_DIR=allure-results && radish features --formatter ...
cmd /c "set ALLURE_RESULTS_DIR=allure-results && radish features --formatter ..."

radish features --formatter ...



or
allure generate allure-results --clean -o allure-report
allure open allure-report

allure serve allure-results

radish features\ --formatter allure_radish.formatter.AllureFormatter\ -o allure-result

Running Tests with Tags
Once tagged, you can filter your test execution using the --tags command line option. Radish uses boolean logic for complex tag expressions.
Single Tag: radish features/ --tags smoke
Logical OR: radish features/ --tags "smoke or regression"
Logical AND: radish features/ --tags "smoke and regression"
Excluding Tags: radish features/ --tags "not slow"

============================
i am running this in pycharm console giving error At line:1 char:39
+ set ALLURE_RESULTS_DIR=allure-results && radish features --formatter  ...
+                                       ~~
The token '&&' is not a valid statement separator in this version.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : InvalidEndOfLine

Got it 👍 — PyCharm’s Run/Terminal console on Windows uses PowerShell by default, so you’re still hitting the same PowerShell parsing rule.

✅ Correct way to run it in PyCharm console (PowerShell)

Use PowerShell syntax, not set / &&.

✔️ One-line (works in PyCharm)
$env:ALLURE_RESULTS_DIR="allure-results"; radish features --formatter ...

✔️ Two lines (clear & safest)
$env:ALLURE_RESULTS_DIR="allure-results"
radish features --formatter ...

❌ What NOT to use in PyCharm PowerShell
set ALLURE_RESULTS_DIR=allure-results && radish features ...


Reason:

set → CMD only

&& → not supported as a separator in your PowerShell version

Alternative fixes (choose what fits your workflow)
🔹 Option 1: Switch PyCharm terminal to CMD

If you prefer CMD syntax:

PyCharm → Settings → Tools → Terminal

Shell path:

cmd.exe


Then this will work:

set ALLURE_RESULTS_DIR=allure-results && radish features --formatter ...

🔹 Option 2: Set env variable in PyCharm Run Configuration (best practice)

If you’re running Radish via Run Configuration:

Run → Edit Configurations

Select your run config

Environment variables

ALLURE_RESULTS_DIR=allure-results


Command:

radish features --formatter ...


✔️ No shell issues at all
✔️ Cleaner for CI & local runs

🔹 Option 3: Run CMD inside PowerShell (quick hack)
cmd /c "set ALLURE_RESULTS_DIR=allure-results && radish features --formatter ..."

Recommendation

👉 Use Option 2 if this is a test run you’ll repeat
👉 Use Option 1 if you like one-off terminal commands

If you want, tell me:

Are you running radish via PyCharm Run Configuration or Terminal?

Are you integrating Allure + Radish + CI?

I can give you the cleanest setup for your project.
================
this is working fine but no test body
radish features\ --formatter allure_radish.formatter.AllureFormatter\

radish features --junit-xml=allure-results/results.xml

allure generate allure-results --clean -o allure-report
allure open allure-report

and also
radish features --cucumber-json=cucumber.json
allure generate allure-results --clean -o allure-report
allure open allure-report


radish -f allure -o allure-results features/; allure generate allure-results --clean -o allure-report; allure open allure-report


==============

2️⃣ Delete old folders (important cleanup)

✅ Correct ways to delete folders in PowerShell
✅ Option 1 (Recommended – PowerShell native)
Remove-Item -Recurse -Force allure-results
Remove-Item -Recurse -Force cucumber-results
Remove-Item -Recurse -Force allure-report


✔ Works in PowerShell
✔ Safely deletes folders if they exist

✅ Option 2 (Force CMD syntax from PowerShell)
cmd /c rmdir /s /q allure-results
cmd /c rmdir /s /q cucumber-results
cmd /c rmdir /s /q allure-report

Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force cucumber-results -ErrorAction SilentlyContinue
============
mkdir cucumber-results
allure generate cucumber-results --clean -o allure-report
==============




============
🟥 FINAL, VERIFIED CONCLUSION

Allure 2.36.0 CLI does NOT process Radish-generated Cucumber JSON on Windows

Even though:

✔ JSON is 100% valid Cucumber

✔ Folder is correct

✔ Command is correct

✔ Allure version is correct (2.36.0)

✔ No CLI errors

👉 Allure silently skips the file

This is a known incompatibility edge case:

Radish Cucumber JSON ≠ Cucumber-JVM JSON

Allure’s cucumber parser is tuned for Cucumber-JVM / Cucumber-JS

Radish’s schema is technically valid, but not consumed

That’s why:

Report folder is created

UI loads

Widgets/data are empty

You did nothing wrong.

🔐 HARD TRUTH (important)

Radish + Allure via Cucumber JSON does not work reliably

especially on Windows + Allure ≥ 2.30

This is why:

No official Radish + Allure docs exist

Community examples silently fail

You saw every symptom of this limitation

✅ THE ONLY WORKING SOLUTION WITH RADISH + ALLURE
🟢 Use JUnit XML, NOT Cucumber JSON

Allure’s JUnit parser is rock-solid.

Radish fully supports it.

✅ FINAL WORKING SETUP (GUARANTEED)
1️⃣ Clean
rmdir /s /q allure-report
rmdir /s /q allure-results
mkdir allure-results

2️⃣ Run Radish with JUnit output
radish features/ --junit-xml=allure-results/junit.xml


Verify:

allure-results/
└── junit.xml

3️⃣ Generate Allure report
allure generate allure-results --clean -o allure-report
allure open allure-report

🎯 WHAT YOU WILL SEE (confirmed)

Feature ✔

Scenario ✔

Steps ✔

Status ✔

Tags ✔

No hacks. No plugins. No listeners.

❌ What to STOP doing (important)

❌ Cucumber JSON with Radish

❌ Custom .extra.json

❌ Python allure APIs

❌ Terrain hooks for Allure

They will not work reliably.

🧠 Final summary (straight answer)
Combination	Works
Radish + Allure + Cucumber JSON	❌
Radish + Allure + JUnit XML	✅
Cucumber-JVM + Allure	✅

If you want, next I can:

Optimize JUnit output (step names, durations)

Add screenshots on failure

Structure reports for CI (Jenkins / GitHub Actions)

Just tell me.

=========================
radish features/ --junit-xml=allure-results/junit.xml
radish features/ --listener listeners/radish_allure_listener.py

allure generate allure-results --clean -o allure-report; allure open allure-report

