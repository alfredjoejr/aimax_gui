from flask import Flask, render_template, jsonify
import subprocess
import platform
import os
import shutil

app = Flask(__name__)

def launch_linux_terminal(script_path):
    """Hunts for the available Linux terminal and launches the script."""
    # A list of common terminals, prioritizing Fedora's modern defaults
    terminals = [
        ['ptyxis', '--', 'python3', script_path],          # Fedora 40+ default
        ['kgx', '-e', f'python3 {script_path}'],           # GNOME Console (recent Fedora/Ubuntu)
        ['gnome-terminal', '--', 'python3', script_path],  # Older GNOME
        ['konsole', '-e', 'python3', script_path],         # KDE Plasma
        ['xfce4-terminal', '-x', 'python3', script_path],  # XFCE
        ['xterm', '-e', 'python3', script_path]            # Universal fallback
    ]

    for term_cmd in terminals:
        # shutil.which checks if the program is actually installed on your system
        if shutil.which(term_cmd[0]):
            try:
                # kgx requires the command to be passed slightly differently
                if term_cmd[0] == 'kgx':
                    subprocess.Popen(['kgx', '-e', f'python3 {script_path}'])
                else:
                    subprocess.Popen(term_cmd)
                return f"Launched using {term_cmd[0]}"
            except Exception as e:
                print(f"Tried {term_cmd[0]} but failed: {e}")
                continue # Try the next one in the list
                
    raise FileNotFoundError("Could not find any standard Linux terminal installed.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-script-1', methods=['POST'])
def run_script_1():
    script_path = os.path.abspath("script1.py")
    current_os = platform.system()
    
    try:
        if current_os == "Windows":
            subprocess.Popen(['start', 'cmd', '/k', 'python', script_path], shell=True)
            msg = "Script 1 launched in Windows CMD!"
            
        elif current_os == "Linux":
            success_msg = launch_linux_terminal(script_path)
            msg = f"Script 1 {success_msg}!"
            
        elif current_os == "Darwin": 
            subprocess.Popen(['open', '-a', 'Terminal', script_path])
            msg = "Script 1 launched in macOS Terminal!"
            
        return jsonify({"status": "success", "message": msg})
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to launch: {str(e)}"})

@app.route('/run-script-2', methods=['POST'])
def run_script_2():
    script_path = os.path.abspath("script2.py")
    current_os = platform.system()
    
    try:
        if current_os == "Windows":
            subprocess.Popen(['start', 'cmd', '/k', 'python', script_path], shell=True)
            msg = "Script 2 launched in Windows CMD!"
            
        elif current_os == "Linux":
            success_msg = launch_linux_terminal(script_path)
            msg = f"Script 2 {success_msg}!"
            
        return jsonify({"status": "success", "message": msg})
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to launch: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)