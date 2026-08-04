@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

echo ==========================================
echo    رفع تحديثات FastAPI إلى GitHub
echo ==========================================
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo خطأ: ضع هذا الملف داخل مجلد fastapi-backend الذي عملت له Clone.
    echo مثال:
    echo C:\Users\lenovo\Documents\GitHub\fastapi-backend
    pause
    exit /b 1
)

git add -A

git diff --cached --quiet
if not errorlevel 1 (
    echo لا توجد ملفات جديدة أو تعديلات لرفعها.
    pause
    exit /b 0
)

echo الملفات التي سيتم رفعها:
git status --short
echo.

git commit -m "Update FastAPI backend"
if errorlevel 1 (
    echo.
    echo حدث خطأ أثناء إنشاء Commit.
    pause
    exit /b 1
)

git pull --rebase origin main
if errorlevel 1 (
    echo.
    echo تعذر دمج تحديثات GitHub. قد يوجد تعارض في الملفات.
    echo افتح GitHub Desktop لمعالجة التعارض ثم أعد تشغيل الملف.
    pause
    exit /b 1
)

git push origin main
if errorlevel 1 (
    echo.
    echo فشل الرفع إلى GitHub. تأكد من الإنترنت وتسجيل الدخول.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo تم رفع التحديثات إلى GitHub بنجاح.
echo سيبدأ Render النشر تلقائيا إذا كان Auto-Deploy مفعلا.
echo ==========================================
pause
