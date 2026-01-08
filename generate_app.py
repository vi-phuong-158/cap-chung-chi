import json
import os

def generate_html(json_path, output_path):
    # Read Data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to JS string
    data_js = json.dumps(data, ensure_ascii=False)
    
    # HTML Template
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edu-Support: Ôn thi Đấu Thầu 2025</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
            -webkit-tap-highlight-color: transparent;
        }}
        .option-card {{
            transition: all 0.2s ease;
        }}
        .option-card:active {{
            transform: scale(0.98);
        }}
        .selected-correct {{
            background-color: #dcfce7 !important;
            border-color: #22c55e !important;
            color: #15803d !important;
        }}
        .selected-wrong {{
            background-color: #fee2e2 !important;
            border-color: #ef4444 !important;
            color: #b91c1c !important;
        }}
        /* Animation for feedback */
        @keyframes shake {{
            0% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            50% {{ transform: translateX(5px); }}
            75% {{ transform: translateX(-5px); }}
            100% {{ transform: translateX(0); }}
        }}
        .animate-shake {{
            animation: shake 0.3s ease-in-out;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col max-w-2xl mx-auto bg-white shadow-xl min-h-screen relative">
    
    <!-- HEADER -->
    <header class="bg-blue-600 text-white p-4 sticky top-0 z-50 shadow-md">
        <div class="flex justify-between items-center mb-2">
            <h1 class="text-lg font-bold">Edu-Support Light</h1>
            <div class="text-sm font-medium">Câu <span id="current-q-num">1</span>/340</div>
        </div>
        
        <!-- Progress Bar -->
        <div class="w-full bg-blue-800 rounded-full h-2.5 mb-2">
            <div id="progress-bar" class="bg-yellow-400 h-2.5 rounded-full transition-all duration-300" style="width: 0%"></div>
        </div>

        <!-- Jump to question -->
        <div class="flex justify-between items-center text-xs">
            <span>Tiến độ: <span id="progress-percent">0%</span></span>
            <div class="flex gap-2 items-center">
                <span>Đến câu:</span>
                <input type="number" id="jump-input" class="w-16 px-2 py-1 rounded text-black text-center" min="1" max="340">
            </div>
        </div>
    </header>

    <!-- CONTENT -->
    <main class="flex-1 p-4 pb-24 overflow-y-auto">
        
        <div id="question-container" class="space-y-4">
            <!-- Question Content -->
            <div class="bg-blue-50 p-4 rounded-xl border border-blue-100">
                <h2 id="question-text" class="text-gray-800 font-semibold text-lg leading-relaxed">
                    <!-- Loading... -->
                </h2>
            </div>

            <!-- Options -->
            <div id="options-container" class="space-y-3">
                <!-- Options injected here -->
            </div>
            
            <!-- Explanation/Result Message -->
            <div id="feedback-msg" class="hidden text-center font-bold p-2 rounded-lg mt-4"></div>
        </div>

    </main>

    <!-- FOOTER NAV -->
    <footer class="fixed bottom-0 left-0 right-0 max-w-2xl mx-auto bg-white border-t border-gray-200 p-4 flex justify-between items-center z-50">
        <button id="btn-prev" class="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg font-medium active:bg-gray-200">Trước</button>
        
        <button id="btn-reset" class="px-4 py-2 text-red-500 font-medium text-sm">Làm lại từ đầu</button>
        
        <button id="btn-next" class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium shadow-lg shadow-blue-200 active:scale-95 transition-transform">Tiếp theo</button>
    </footer>

    <script>
        // --- DATA ---
        const DB = {data_js};
        
        // --- STATE ---
        const LS_KEY = 'edu_support_state';
        let state = {{
            currentIdx: 0,
            answers: {{}} // map id -> selected key (A, B, C, D)
        }};

        // --- ELEMENTS ---
        const elQNum = document.getElementById('current-q-num');
        const elQText = document.getElementById('question-text');
        const elOptions = document.getElementById('options-container');
        const elProgress = document.getElementById('progress-bar');
        const elProgressPercent = document.getElementById('progress-percent');
        const elJumpInput = document.getElementById('jump-input');
        const elFeedback = document.getElementById('feedback-msg');
        
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        const btnReset = document.getElementById('btn-reset');

        // --- INIT ---
        function init() {{
            loadState();
            renderQuestion();
            updateProgress();
        }}

        function loadState() {{
            const saved = localStorage.getItem(LS_KEY);
            if (saved) {{
                try {{
                    state = JSON.parse(saved);
                }} catch (e) {{
                    console.error("Load state error", e);
                }}
            }}
            // Clamp index
            if (state.currentIdx < 0) state.currentIdx = 0;
            if (state.currentIdx >= DB.length) state.currentIdx = DB.length - 1;
        }}

        function saveState() {{
            localStorage.setItem(LS_KEY, JSON.stringify(state));
        }}

        function updateProgress() {{
            const total = DB.length;
            const current = state.currentIdx + 1;
            const percent = ((current / total) * 100).toFixed(1);
            
            elQNum.textContent = current;
            elProgress.style.width = percent + '%';
            elProgressPercent.textContent = percent + '%';
            elJumpInput.value = current;
        }}

        function renderQuestion() {{
            const q = DB[state.currentIdx];
            if (!q) return;

            // Update Text
            // Handle newlines in question text if any
            elQText.innerHTML = q.question.replace(/\\n/g, '<br>');

            // Clear options
            elOptions.innerHTML = '';
            elFeedback.className = 'hidden text-center font-bold p-2 rounded-lg mt-4';
            elFeedback.textContent = '';

            const userAns = state.answers[q.id];
            
            // Render Options
            const keys = ['A', 'B', 'C', 'D'];
            keys.forEach(key => {{
                if (!q.options[key]) return; // Skip if option doesn't exist

                const btn = document.createElement('div');
                btn.className = 'option-card p-4 rounded-xl border-2 border-gray-100 bg-white cursor-pointer active:bg-gray-50 flex gap-3 items-start';
                btn.dataset.key = key;
                
                // Color Logic
                let isSelected = (userAns === key);
                let isCorrect = (q.answer === key);
                
                // Content
                btn.innerHTML = `
                    <div class="flex-shrink-0 w-8 h-8 rounded-full border-2 border-gray-300 flex items-center justify-center font-bold text-gray-500 option-circle">
                        ${{key}}
                    </div>
                    <div class="text-gray-700 font-medium pt-1">${{q.options[key]}}</div>
                `;

                // Interaction
                if (!userAns) {{
                    btn.onclick = () => handleSelect(q.id, key, q.answer);
                }} else {{
                    // Already answered mode
                    if (isSelected) {{
                        if (key === q.answer) {{
                            // User Correct
                            applyCorrectStyle(btn);
                        }} else {{
                            // User Wrong
                            applyWrongStyle(btn);
                        }}
                    }} else if (key === q.answer) {{
                        // Show correct if user was wrong
                         applyCorrectStyle(btn);
                    }} else {{
                        // Dim other options
                        btn.classList.add('opacity-50');
                    }}
                }}

                elOptions.appendChild(btn);
            }});
        }}

        function applyCorrectStyle(el) {{
            el.classList.add('selected-correct');
            const circle = el.querySelector('.option-circle');
            circle.classList.remove('border-gray-300', 'text-gray-500');
            circle.classList.add('border-green-500', 'bg-green-100', 'text-green-600');
            circle.innerHTML = '✓';
        }}

        function applyWrongStyle(el) {{
            el.classList.add('selected-wrong', 'animate-shake');
            const circle = el.querySelector('.option-circle');
            circle.classList.remove('border-gray-300', 'text-gray-500');
            circle.classList.add('border-red-500', 'bg-red-100', 'text-red-600');
            circle.innerHTML = '✕';
        }}

        function handleSelect(qId, key, correctKey) {{
            // Save answer
            state.answers[qId] = key;
            saveState();
            
            // Re-render to show feedback
            renderQuestion();

            if (key === correctKey) {{
                // Auto next after 1s
                setTimeout(() => {{
                    // Check if we are still on the same question (user didn't click prev/next manually)
                    const currentQ = DB[state.currentIdx];
                    if (currentQ.id === qId) {{
                        goNext();
                    }}
                }}, 1000);
            }}
        }}

        function goNext() {{
            if (state.currentIdx < DB.length - 1) {{
                state.currentIdx++;
                saveState();
                renderQuestion();
                updateProgress();
                window.scrollTo(0, 0);
            }}
        }}

        function goPrev() {{
            if (state.currentIdx > 0) {{
                state.currentIdx--;
                saveState();
                renderQuestion();
                updateProgress();
                window.scrollTo(0, 0);
            }}
        }}

        function goJump(val) {{
            const idx = parseInt(val) - 1;
            if (idx >= 0 && idx < DB.length) {{
                state.currentIdx = idx;
                saveState();
                renderQuestion();
                updateProgress();
                window.scrollTo(0, 0);
            }}
        }}

        function doReset() {{
            if (confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử học tập?')) {{
                localStorage.removeItem(LS_KEY);
                state.currentIdx = 0;
                state.answers = {{}};
                init();
                window.scrollTo(0, 0);
            }}
        }}

        // --- LISTENERS ---
        btnNext.addEventListener('click', goNext);
        btnPrev.addEventListener('click', goPrev);
        btnReset.addEventListener('click', doReset);
        
        elJumpInput.addEventListener('change', (e) => goJump(e.target.value));

        // Start
        init();

    </script>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_html("340_cau_hoi.json", "index.html")
