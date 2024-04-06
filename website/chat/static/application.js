const submitButton = document.querySelector('#submit')
const inputElement = document.querySelector('input')

async function getMessage() {
    console.log('clicked');

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
        const response = await fetch('/execute-python-script', requestOptions);
        console.log(response);
        const data = await response.json();
        console.log('Output from Python script:', data.output);
    } catch (error) {
        console.error('Error:', error);
    }
}

submitButton.addEventListener('click', getMessage);