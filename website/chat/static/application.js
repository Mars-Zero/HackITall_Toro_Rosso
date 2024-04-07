const submitButton = document.querySelector('#submit')
const inputElement = document.querySelector('input')
const outputElement = document.querySelector('#output')
const historyElement = document.querySelector('.history')
const buttonElement = document.querySelector('button')

function changeInput(value) {
    console.log(value)
    clearInput
    // const inputElement = document.querySelector('input')
    // inputElement.value = value
}

async function getMessage() {
    const options = {
        "input": inputElement.value
    };
    try {
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(options)
        };
        console.log('JSON options:', JSON.stringify(options));
        // outputElement.textContent = inputElement.value
        outputElement.append(inputElement.value + "\n\n")
        // outputElement.setAttribute('style', 'white-space: pre;');
        // outputElement.append(String.fromCharCode(10));
        const response = await fetch('/execute-python-script', requestOptions);
        const data = await response.json();
        // console.log('Output from Python script:', data.output);
        //outputElement.textContent = data.output
        outputElement.append(data.output)
        outputElement.innerHTML = outputElement.textContent.replace(/\r/g, '').replace(/\n/g, '<br>');
        // console.log(data)
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

buttonElement.addEventListener('click', clearInput)