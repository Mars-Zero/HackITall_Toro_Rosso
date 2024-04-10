source ./../../.venv/bin/activate

if [ $? -ne 0 ]; then
    echo "No virtual environment found! Run ./install.sh"
    exit 1
fi

pip install flask
pip install torch
pip install sentence_transformers
pip install openai

echo -e "\n\n-------- DO NOT FORGET TO ADD A OPENAI API KEY ------------\n\n"

export FLASK_APP=app
export FLASK_DEBUG=True
flask run

