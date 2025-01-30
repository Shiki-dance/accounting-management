document.addEventListener("DOMContentLoaded", () => {
    const text = "Welcome to DLC";
    const target = document.getElementById("welcome-text");
    let index = 0;

    function typeWriter() {
        if (index < text.length) {
            target.innerHTML += text.charAt(index);
            index++;
            setTimeout(typeWriter, 200);
        }
    }

    typeWriter();
});
