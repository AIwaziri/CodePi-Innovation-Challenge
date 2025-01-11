let currentLevel = 0;
let score = 0;
let currentQuestion = {};
let questionCount = 0;
const questionsPerLevel = 5;

document.getElementById("start-game").addEventListener("click", startGame);
document.getElementById("submit-answer").addEventListener("click", submitAnswer);
document.getElementById("hint-button").addEventListener("click", showHint);

function startGame() {
    currentLevel = 0;
    score = 0;
    questionCount = 0;
    updateProgress();
    resetUI();
    generateQuestion();
}

function resetUI() {
    document.getElementById("answer").style.display = "inline-block";
    document.getElementById("submit-answer").style.display = "inline-block";
    document.getElementById("hint-button").style.display = "inline-block";
    document.getElementById("start-game").style.display = "none";
}

function generateQuestion() {
    if (questionCount < questionsPerLevel) {
        switch (currentLevel) {
            case 0:
                currentQuestion = generateLevel1Question();
                break;
            case 1:
                currentQuestion = generateLevel2Question();
                break;
            case 2:
                currentQuestion = generateLevel3Question();
                break;
            case 3:
                currentQuestion = generateLevel4Question();
                break;
            default:
                endGame();
                return;
        }
        document.getElementById("question").innerText = currentQuestion.text;
        document.getElementById("answer").value = "";
    } else {
        currentLevel++;
        questionCount = 0;
        if (currentLevel < 4) {
            alert(`Great job! Proceeding to Level ${currentLevel + 1}.`);
            generateQuestion();
        } else {
            endGame();
        }
    }
}

function generateLevel1Question() {
    const num1 = Math.floor(Math.random() * 10) + 1;
    const num2 = Math.floor(Math.random() * 10) + 1;
    const operations = ["+", "-", "*", "/"];
    const operation = operations[Math.floor(Math.random() * operations.length)];
    let questionText = `Solve ${num1} ${operation} ${num2}`;
    let answer, hint;

    switch (operation) {
        case "+":
            answer = (num1 + num2).toString();
            hint = "Add the two numbers.";
            break;
        case "-":
            answer = (num1 - num2).toString();
            hint = "Subtract the second number from the first.";
            break;
        case "*":
            answer = (num1 * num2).toString();
            hint = "Multiply the two numbers.";
            break;
        case "/":
            answer = (num1 / num2).toFixed(1);
            hint = "Divide the first number by the second. Round to one decimal places if necessary.";
            break;
    }
    return { text: questionText, answer: answer, hint: hint };
}

function generateLevel2Question() {
    const questionTypes = [
        { type: "area", shape: "rectangle" },
        { type: "perimeter", shape: "square" }
    ];
    const selected = questionTypes[Math.floor(Math.random() * questionTypes.length)];

    let questionText, answer, hint;

    if (selected.type === "area" && selected.shape === "rectangle") {
        const length = Math.floor(Math.random() * 10) + 1;
        const width = Math.floor(Math.random() * 10) + 1;
        questionText = `Find the area of a rectangle with length ${length} and width ${width}.`;
        answer = (length * width).toString();
        hint = "Use the formula: length * width.";
    } else if (selected.type === "perimeter" && selected.shape === "square") {
        const side = Math.floor(Math.random() * 10) + 1;
        questionText = `Find the perimeter of a square with side length ${side}.`;
        answer = (4 * side).toString();
        hint = "Use the formula: 4 * side length.";
    }
    return { text: questionText, answer: answer, hint: hint };
}

function generateLevel3Question() {
    const x = Math.floor(Math.random() * 10) + 1;
    return {
        text: `Solve for x: x + 5 = ${x + 5}`,
        answer: x.toString(),
        hint: "Isolate x by subtracting 5 from both sides."
    };
}

function generateLevel4Question() {
    const coefficient = Math.floor(Math.random() * 5) + 1;
    return {
        text: `Differentiate y = ${coefficient}x^2`,
        answer: `${2 * coefficient}x`,
        hint: "Use the power rule: d/dx of ax^n = n * ax^(n-1)."
    };
}

function submitAnswer() {
    const userAnswer = document.getElementById("answer").value.trim();
    if (userAnswer === currentQuestion.answer) {
        score += 10;
        questionCount++;
        updateProgress();
        generateQuestion();
        showFeedback("Correct! Great job!", "success");
    } else {
        showFeedback("Incorrect. Try again!", "error");
    }
}

function showHint() {
    document.getElementById("hint").innerText = currentQuestion.hint;
}

function updateProgress() {
    document.getElementById("progress").innerText = `Level: ${currentLevel + 1} | Question: ${questionCount}/${questionsPerLevel} | Score: ${score}`;
}

function showFeedback(message, type) {
    const feedbackElement = document.createElement("p");
    feedbackElement.innerText = message;
    feedbackElement.style.color = type === "success" ? "green" : "red";
    document.body.appendChild(feedbackElement);
    setTimeout(() => feedbackElement.remove(), 3000);
}

function endGame() {
    document.getElementById("question").innerText = "Congratulations! You've completed the game.";
    document.getElementById("answer").style.display = "none";
    document.getElementById("submit-answer").style.display = "none";
    document.getElementById("hint-button").style.display = "none";

    const startOverButton = document.createElement("button");
    startOverButton.innerText = "Start Over";
    startOverButton.addEventListener("click", startGame);

    const quitButton = document.createElement("button");
    quitButton.innerText = "Quit";
    quitButton.addEventListener("click", () => alert("Thanks for playing MathQuest!"));

    document.body.appendChild(startOverButton);
    document.body.appendChild(quitButton);
}