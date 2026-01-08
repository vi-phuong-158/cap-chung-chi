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
        .hidden-important {{
            display: none !important;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col max-w-2xl mx-auto bg-white shadow-xl min-h-screen relative">
    
    <!-- LOVE INVOICE MODAL -->
    <div id="love-invoice-modal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/60 backdrop-blur-sm transition-opacity duration-300 opacity-0 hidden-important">
        <div class="bg-white rounded-2xl p-8 max-w-sm w-full mx-4 shadow-2xl transform transition-all duration-300 scale-95 border-4 border-pink-200">
            <div class="flex flex-col items-center text-center space-y-4">
                <div class="text-6xl animate-bounce">💎</div>
                
                <!-- Title removed as requested -->
                
                <div class="text-gray-700 space-y-3 font-medium text-lg leading-relaxed">
                    <p>Ứng dụng này được thiết kế bằng vô vàn yêu thương và mong muốn Vợ học tập tốt.</p>
                    <p>Tấm lòng này tuy không gì có thể đong đếm được, nhưng nếu Vợ thực sự muốn định giá...</p>
                    <p class="text-xl font-bold text-pink-500">...thì giá của nó là 2 củ nhé! 💸</p>
                </div>
                
                <button onclick="closeLoveInvoice()" class="w-full bg-pink-500 hover:bg-pink-600 text-white font-bold py-3 rounded-full shadow-lg shadow-pink-200 active:scale-95 transition-all mt-4 text-lg">
                    Đồng ý thanh toán 💋
                </button>
                
                <p class="text-xs text-gray-400 italic mt-2">*Bấm nút trên đồng nghĩa với việc đồng ý chi tiền.</p>
            </div>
        </div>
    </div>
    
    <!-- START SCREEN -->
    <div id="start-screen" class="absolute inset-0 z-[100] bg-white flex flex-col items-center justify-center p-6 space-y-8">
        <h1 class="text-3xl font-bold text-blue-700 text-center">Edu-Support<br><span class="text-xl text-gray-500">Ôn thi Đấu Thầu 2025</span></h1>
        
        <div class="w-full max-w-sm bg-blue-50 p-6 rounded-xl space-y-4 shadow-sm border border-blue-100">
            <div>
                <label class="block text-gray-700 font-medium mb-2">Chọn số lượng câu hỏi mà Vợ muốn ở đây</label>
                <input type="number" id="config-count" class="w-full p-2 border border-gray-300 rounded-lg text-center font-bold text-lg" value="340" min="1" max="340">
                <p class="text-xs text-gray-500 mt-1 text-center">Tối đa 340 câu</p>
            </div>
            
            <div class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-gray-700 font-medium mb-2">Vợ có muốn thử thách bằng việc việc trộn đáp án không?</label>
                <div class="flex items-center space-x-6">
                    <label class="flex items-center space-x-2 cursor-pointer">
                        <input type="radio" name="shuffle_option" id="shuffle-yes" class="w-5 h-5 text-blue-600" checked>
                        <span>Có</span>
                    </label>
                    <label class="flex items-center space-x-2 cursor-pointer">
                        <input type="radio" name="shuffle_option" id="shuffle-no" class="w-5 h-5 text-gray-400">
                        <span>Không</span>
                    </label>
                </div>
            </div>
        </div>

        <button onclick="startNewExam()" class="w-full max-w-sm bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl shadow-lg transition-transform active:scale-95 text-xl">
            BẮT ĐẦU LÀM BÀI
        </button>
        
        <button onclick="continueExam()" id="btn-continue" class="hidden text-blue-600 font-medium underline">
            Tiếp tục bài đang làm dở
        </button>
    </div>

    <!-- MAIN APP HEADER -->
    <header class="bg-blue-600 text-white p-4 sticky top-0 z-50 shadow-md">
        <div class="flex justify-between items-center mb-2">
            <h1 class="text-lg font-bold">Edu-Support Light</h1>
            <div class="text-sm font-medium">Câu <span id="current-q-num">1</span>/<span id="total-q-num">--</span></div>
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
                <input type="number" id="jump-input" class="w-16 px-2 py-1 rounded text-black text-center" min="1">
            </div>
        </div>
    </header>

    <!-- RESULT SCREEN -->
    <div id="result-screen" class="absolute inset-0 z-[100] bg-white hidden-important flex flex-col items-center justify-center p-6 space-y-6">
        <h2 class="text-3xl font-bold text-blue-700">Kết Quả</h2>
        
        <div class="bg-blue-50 p-8 rounded-2xl border border-blue-100 flex flex-col items-center space-y-2 shadow-sm w-full max-w-sm">
            <div class="text-gray-500 font-medium">Bạn đã trả lời đúng</div>
            <div class="text-5xl font-extrabold text-blue-600">
                <span id="score-correct">0</span>/<span id="score-total">0</span>
            </div>
            <div id="score-percent" class="text-gray-400 font-medium text-sm">0%</div>
        </div>

        <div class="flex flex-col w-full max-w-sm space-y-3">
            <button onclick="reviewExam()" class="w-full bg-white border-2 border-blue-600 text-blue-600 font-bold py-3 rounded-xl hover:bg-blue-50 transition-colors">
                Xem lại bài thi
            </button>
            <button onclick="exitExam()" class="w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 shadow-lg transition-transform active:scale-95">
                Thoát / Làm bài mới
            </button>
        </div>
    </div>

    <!-- CONTENT -->
    <main class="flex-1 p-4 pb-24 overflow-y-auto">
        <div id="question-container" class="space-y-4">
            <!-- Question Content -->
            <div class="bg-blue-50 p-4 rounded-xl border border-blue-100 relative">
                <span class="absolute top-2 right-2 text-xs font-bold text-gray-400">ID: <span id="q-original-id"></span></span>
                <h2 id="question-text" class="text-gray-800 font-semibold text-lg leading-relaxed mt-2">
                    <!-- Loading... -->
                </h2>
            </div>

            <!-- Options -->
            <div id="options-container" class="space-y-3">
                <!-- Options injected here -->
            </div>
        </div>
    </main>

    <!-- FOOTER NAV -->
    <footer class="fixed bottom-0 left-0 right-0 max-w-2xl mx-auto bg-white border-t border-gray-200 p-4 flex justify-between items-center z-50">
        <button id="btn-prev" class="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg font-medium active:bg-gray-200">Trước</button>
        
        <button id="btn-exit" class="px-4 py-2 text-red-500 font-medium text-sm">Thoát</button>
        
        <button id="btn-next" class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium shadow-lg shadow-blue-200 active:scale-95 transition-transform">Tiếp theo</button>
    </footer>

    <script>
        // --- DATA ---
        // DB contains all 340 questions
        const DB = {data_js};
        
        // --- STATE ---
        const LS_KEY = 'edu_support_state_v2';
        let state = {{
            active: false,
            currentIdx: 0,
            questions: [], // The selected subset for this exam
            answers: {{}}, // map questionId -> selectedOptionIndex (0,1,2,3) NOT A/B/C/D key
            finished: false
        }};

        // --- ELEMENTS ---
        const elStartScreen = document.getElementById('start-screen');
        const elResultScreen = document.getElementById('result-screen');
        const elBtnContinue = document.getElementById('btn-continue');
        
        const elQNum = document.getElementById('current-q-num');
        const elTotalQNum = document.getElementById('total-q-num');
        
        const elQText = document.getElementById('question-text');
        const elQOrigId = document.getElementById('q-original-id');
        const elOptions = document.getElementById('options-container');
        
        const elProgress = document.getElementById('progress-bar');
        const elProgressPercent = document.getElementById('progress-percent');
        const elJumpInput = document.getElementById('jump-input');
        
        // Score elements
        const elScoreCorrect = document.getElementById('score-correct');
        const elScoreTotal = document.getElementById('score-total');
        const elScorePercent = document.getElementById('score-percent');
        
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        const btnExit = document.getElementById('btn-exit');

        // --- INIT ---
        function init() {{
            // Show Love Invoice Modal
            const modal = document.getElementById('love-invoice-modal');
            modal.classList.remove('hidden-important');
            // Trigger animation after slight delay
            setTimeout(() => {{
               modal.classList.remove('opacity-0');
               modal.querySelector('div').classList.remove('scale-95');
               modal.querySelector('div').classList.add('scale-100');
            }}, 100);

            loadState();
            if (state.active && state.questions.length > 0) {{
                if (state.finished) {{
                     showResult();
                }} else {{
                    elBtnContinue.classList.remove('hidden');
                }}
            }}
        }}

        function closeLoveInvoice() {{
             const modal = document.getElementById('love-invoice-modal');
             modal.classList.add('opacity-0');
             modal.querySelector('div').classList.remove('scale-100');
             modal.querySelector('div').classList.add('scale-95');
             
             setTimeout(() => {{
                 modal.classList.add('hidden-important');
             }}, 300);
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
        }}

        function saveState() {{
            localStorage.setItem(LS_KEY, JSON.stringify(state));
        }}

        // --- CORE LOGIC ---

        function startNewExam() {{
            const countInput = document.getElementById('config-count');
            
            let count = parseInt(countInput.value) || 340;
            if (count > DB.length) count = DB.length;
            if (count < 1) count = 1;
            
            const doShuffle = document.getElementById('shuffle-yes').checked;

            // 1. Select Questions
            // Create list of indices [0, 1, ... 339]
            let indices = Array.from({{length: DB.length}}, (_, i) => i);
            
            // Shuffle indices using Fisher-Yates
            for (let i = indices.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [indices[i], indices[j]] = [indices[j], indices[i]];
            }}
            
            // Pick first 'count'
            const selectedIndices = indices.slice(0, count);
            
            // 2. Build Exam Data
            const examQuestions = selectedIndices.map(idx => {{
                const original = DB[idx];
                
                // Process Options
                // Original: Object with keys A, B, C, D
                // We want array: Array of objects with key/content
                let optsArr = [];
                ['A', 'B', 'C', 'D'].forEach(k => {{
                    if (original.options[k]) {{
                        optsArr.push({{
                            key: k, // Original key (A, B...)
                            content: original.options[k]
                        }});
                    }}
                }});
                
                // Shuffle Options if requested (and if question is not marked as fixed)
                if (doShuffle && !original.fixedOptions) {{
                    for (let i = optsArr.length - 1; i > 0; i--) {{
                        const j = Math.floor(Math.random() * (i + 1));
                        [optsArr[i], optsArr[j]] = [optsArr[j], optsArr[i]];
                    }}
                }}
                
                return {{
                    id: original.id,
                    question: original.question,
                    correctKey: original.answer, // e.g. "A"
                    displayOptions: optsArr
                }};
            }});

            // 3. Update State
            state = {{
                active: true,
                currentIdx: 0,
                questions: examQuestions,
                answers: {{}}
            }};
            
            saveState();
            enterExamMode();
        }}

        function continueExam() {{
            enterExamMode();
        }}

        function enterExamMode() {{
            elStartScreen.classList.add('hidden-important');
            elResultScreen.classList.add('hidden-important');
            updateProgress();
            renderQuestion();
        }}
        
        function exitExam() {{
            if (confirm("Bạn có muốn thoát về màn hình chính?")) {{
                state.active = false;
                state.finished = false;
                saveState();
                
                elResultScreen.classList.add('hidden-important');
                elStartScreen.classList.remove('hidden-important');
                elBtnContinue.classList.add('hidden');
                
                // Reset inputs?
                document.getElementById('config-count').value = 340;
            }}
        }}
        
        function finishExam() {{
            state.finished = true;
            saveState();
            showResult();
        }}
        
        function showResult() {{
            // Calculate score
            let correctCount = 0;
            state.questions.forEach(q => {{
                const userAnsIdx = state.answers[q.id];
                if (userAnsIdx !== undefined) {{
                    const selectedOpt = q.displayOptions[userAnsIdx];
                    if (selectedOpt && selectedOpt.key === q.correctKey) {{
                        correctCount++;
                    }}
                }}
            }});
            
            const total = state.questions.length;
            const percent = ((correctCount / total) * 100).toFixed(1);
            
            elScoreCorrect.textContent = correctCount;
            elScoreTotal.textContent = total;
            elScorePercent.textContent = percent + '%';
            
            elResultScreen.classList.remove('hidden-important');
        }}

        function reviewExam() {{
            elResultScreen.classList.add('hidden-important');
             // Just show the current question (usually last one)
             // or go to first question? Let's go to first to review.
             state.currentIdx = 0;
             renderQuestion();
             updateProgress();
        }}

        // --- RENDER ---

        function updateProgress() {{
            const total = state.questions.length;
            const current = state.currentIdx + 1;
            const percent = ((current / total) * 100).toFixed(0);
            
            elQNum.textContent = current;
            elTotalQNum.textContent = total;
            
            elProgress.style.width = percent + '%';
            elProgressPercent.textContent = percent + '%';
            
            elJumpInput.value = current;
            elJumpInput.max = total;
        }}

        function renderQuestion() {{
            const q = state.questions[state.currentIdx];
            if (!q) return;

            // Update Text
            elQOrigId.textContent = q.id;
            elQText.innerHTML = q.question.replace(/\\n/g, '<br>');

            // Clear options
            elOptions.innerHTML = '';
            
            // User Answer for this question (index in displayOptions array)
            const userAnsIdx = state.answers[q.id]; 

            // Render Options
            const labels = ['A', 'B', 'C', 'D'];
            
            q.displayOptions.forEach((opt, idx) => {{
                // opt has key and content
                // key is the original key. q.correctKey is the correct original key.
                
                const btn = document.createElement('div');
                btn.className = 'option-card p-4 rounded-xl border-2 border-gray-100 bg-white cursor-pointer active:bg-gray-50 flex gap-3 items-start';
                
                const isCorrect = (opt.key === q.correctKey);
                const isSelected = (userAnsIdx === idx);
                const hasAnswered = (userAnsIdx !== undefined);
                
                // Color Logic
                let circleClass = 'border-gray-300 text-gray-500';
                let circleContent = labels[idx]; // Always show A, B, C, D in order
                let extraClass = '';

                if (hasAnswered) {{
                   // Reveal phase
                   if (isCorrect) {{
                       // This is the correct answer
                       extraClass = 'selected-correct';
                       circleClass = 'border-green-500 bg-green-100 text-green-600';
                       circleContent = '✓';
                   }} else if (isSelected) {{
                       // User picked this, but it's wrong (since we are in else of isCorrect)
                       extraClass = 'selected-wrong animate-shake';
                       circleClass = 'border-red-500 bg-red-100 text-red-600';
                       circleContent = '✕';
                   }} else {{
                       // Neither selected nor correct -> Dim it
                       extraClass = 'opacity-50';
                   }}
                }}

                btn.className += ' ' + extraClass;
                
                btn.innerHTML = `
                    <div class="flex-shrink-0 w-8 h-8 rounded-full border-2 flex items-center justify-center font-bold option-circle ${{circleClass}}">
                        ${{circleContent}}
                    </div>
                    <div class="text-gray-700 font-medium pt-1">${{opt.content}}</div>
                `;

                // Interaction
                if (!hasAnswered) {{
                    btn.onclick = () => handleSelect(q.id, idx, isCorrect);
                }}

                elOptions.appendChild(btn);
            }});
            
            // Update Next button text if last question
            if (state.currentIdx === state.questions.length - 1) {{
                btnNext.textContent = "Hoàn thành";
            }} else {{
                btnNext.textContent = "Tiếp theo";
            }}
        }}

        function handleSelect(qId, optIdx, isCorrect) {{
            // Save answer (store the index of the option clicked)
            state.answers[qId] = optIdx;
            saveState();
            
            // Re-render to show feedback
            renderQuestion();

            if (isCorrect) {{
                // Auto next after 1s
                setTimeout(() => {{
                    // Ensure we haven't moved already
                    if (state.questions[state.currentIdx].id === qId) {{
                        goNext();
                    }}
                }}, 1000);
            }}
        }}

        function goNext() {{
            if (state.currentIdx < state.questions.length - 1) {{
                state.currentIdx++;
                saveState();
                renderQuestion();
                updateProgress();
                window.scrollTo(0, 0);
            }} else {{
                finishExam();
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
            if (idx >= 0 && idx < state.questions.length) {{
                state.currentIdx = idx;
                saveState();
                renderQuestion();
                updateProgress();
                window.scrollTo(0, 0);
            }}
        }}

        // --- LISTENERS ---
        btnNext.addEventListener('click', goNext);
        btnPrev.addEventListener('click', goPrev);
        btnExit.addEventListener('click', exitExam);
        
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
