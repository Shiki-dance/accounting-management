document.addEventListener("DOMContentLoaded", () => {
    const text = "Welcome to DLC";
    const target = document.getElementById("welcome-text");
    target.innerHTML = ""; // 既存のテキストをクリア
    let index = 0;

    function typeWriter() {
        if (index < text.length) {
            let span = document.createElement("span");
            span.textContent = text.charAt(index);
            span.style.opacity = "0";
            span.style.animation = "fadeIn 0.3s ease forwards"; // フェードイン効果を適用
            target.appendChild(span);
            index++;
            setTimeout(typeWriter, 150); // 表示間隔を短めに
        }
    }

    typeWriter();
});

