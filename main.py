from flask import Flask, render_template, request, jsonify, abort
import subprocess


POWERSHELL_PATH = "powershell.exe"  # POWERSHELL EXE PATH
ps_script_path = "C:\\Zerodha"  # YOUR POWERSHELL FILE PATH

app = Flask(__name__)


# Give some documentation regarding the API on the root page i.e. "/"
@app.route("/")
def root():
    return render_template("root.html")


# Execute a local PS1 script when this API is called
@app.route("/_apis/v1/script/<script_name>")
def script(script_name):        # SCRIPT PATH = POWERSHELL SCRIPT PATH
    commandline_options = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted',
                           f"{ps_script_path}\\{script_name}"]  # ADD POWERSHELL EXE AND EXECUTION POLICY TO COMMAND VARIABLE
    process_result = subprocess.run(commandline_options, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)  # CALL PROCESS
    with open("ps-output.txt", "r") as f:
        output = f.readlines()
    return output


# Extract the payload for an incoming API call; needs Content-Type set to "application/json" with valid JSON payload
@app.route("/_apis/v1/extractapipayload", methods=['POST'])
def extract():
    reqlist = ['name', 'age', 'authkey']
    data = request.json
    payload = str(data)
    with open("C:\\tmp\\payload.txt", "w") as f:
        f.writelines(payload)
    for i in reqlist:
        if i not in data.keys():
            abort(400, f'Mandatory item missing - {i}')
    return data


# Testing the incoming request
@app.route("/_apis/v1/reqtest", methods=['GET', 'POST'])
def reqtest():
    data = dir(request)
    return data


if __name__ == "__main__":
    app.run(debug=True, port=8888)
