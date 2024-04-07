const submitButton = document.querySelector('#submit')
const inputElement = document.querySelector('input')
const outputElement = document.querySelector('#output')
const historyElement = document.querySelector('.history')
const buttonElement = document.querySelector('button')
// const feedbackElement = document.querySelector('#feedback')

function changeInput(value) {
    console.log(value)
    clearInput
    // const inputElement = document.querySelector('input')
    // inputElement.value = value
}

async function getMessage() {
    // Disable submit button to prevent multiple clicks
    if(inputElement.value === '')
    {
        showFeedback('Nu ai pus nici o intrebare.');
        return; 
    }
    submitButton.disabled = true;

    const options = {
        "input": inputElement.value
    };
    try {
        showFeedback('Procesam cererea ta...');

        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(options)
        };

        const response = await fetch('/execute-python-script', requestOptions);
        const data = await response.json();
        outputElement.textContent = data.output;
        if (data.output) {
            const divElement = document.createElement('div');
            divElement.classList.add('history-item');
            const inputParagraph = document.createElement('p');
            inputParagraph.textContent = inputElement.value;
            divElement.appendChild(inputParagraph);
            const outputParagraph = document.createElement('p');
            outputParagraph.textContent = data.output;
            divElement.appendChild(outputParagraph);
            divElement.addEventListener('click', () => changeInput(inputElement.value));
            historyElement.appendChild(divElement);
        }
        clearInput();
    } catch (error) {
        console.error('Error:', error);
        showFeedback('Am intampinat o eroare. Incearca din nou mai tarziu.');
    } finally {
        // Enable submit button after processing
        submitButton.disabled = false;
    }
}

submitButton.addEventListener('click', getMessage);
inputElement.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      getMessage();
    }
  });

function clearInput () {
    inputElement.value = ''
}

function showFeedback(message) {
    outputElement.textContent = message;
}

function hideFeedback() {
    outputElement.textContent = '';
}

buttonElement.addEventListener('click', clearInput)