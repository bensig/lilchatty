#!/usr/bin/env python3
import subprocess
import os
import time
import webbrowser
import threading
import socket
from flask import Flask, render_template_string, request, redirect, url_for, jsonify

app = Flask(__name__)

def find_available_port(start_port=5001, max_attempts=10):
    """Checks ports sequentially starting from start_port to find an available one."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port # Port is available
            except OSError:
                print(f"Port {port} is already in use, trying next...")
                continue # Port is in use, try the next one
    return None # No available port found

def open_browser(port):
    """Opens the browser to the specified port after a short delay."""
    time.sleep(1) # Give server a moment to start
    webbrowser.open_new_tab(f"http://127.0.0.1:{port}")

def get_system_memory_gb():
    """Get system memory in GB using sysctl."""
    try:
        mem_bytes = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip())
        return mem_bytes / (1024**3)  # Convert to GB
    except:
        return 16  # Default fallback

def is_docker_running():
    """Check if Docker is running."""
    try:
        subprocess.check_output(['docker', 'info'], stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def is_brew_installed():
    """Check if Homebrew is installed."""
    try:
        subprocess.check_output(['which', 'brew'])
        return True
    except:
        return False

def install_brew():
    """Install Homebrew."""
    try:
        install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        return subprocess.check_output(install_cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return e.output

def install_colima():
    """Install Colima using Homebrew."""
    try:
        return subprocess.check_output(['brew', 'install', 'colima'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return e.output

def start_colima():
    """Start Colima."""
    try:
        return subprocess.check_output(['colima', 'start'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return e.output

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lil' Chatty - Local, Free ChatGPT Alternative Setup</title>
    <meta name="description" content="Easy setup wizard for Lil' Chatty, your private, local AI chat assistant.">

    <!-- Favicons -->
    <link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='images/apple-touch-icon.png') }}">
    <link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='images/favicon-32x32.png') }}">
    <link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='images/favicon-16x16.png') }}">
    <link rel="shortcut icon" href="{{ url_for('static', filename='images/favicon.ico') }}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{ url_for('index', _external=True) }}"> <!-- Dynamic URL -->
    <meta property="og:title" content="Lil' Chatty - Local, Free ChatGPT Alternative">
    <meta property="og:description" content="Run your own private AI chat assistant locally!">
    <meta property="og:image" content="{{ url_for('static', filename='images/lilchatty-og.png', _external=True) }}">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{{ url_for('index', _external=True) }}"> <!-- Dynamic URL -->
    <meta property="twitter:title" content="Lil' Chatty - Local, Free ChatGPT Alternative">
    <meta property="twitter:description" content="Run your own private AI chat assistant locally!">
    <meta property="twitter:image" content="{{ url_for('static', filename='images/lilchatty-og.png', _external=True) }}">

    <style>
        body { 
            font-family: 'Arial', sans-serif; /* Consider a more modern font later */
            max-width: 800px; 
            margin: 40px auto; 
            padding: 20px;
            background-color: #FFF9F3; /* Cream White */
            color: #2E2E2E; /* Deep Charcoal */
        }
        .container { 
            border: 1px solid #C4CDD5; /* Cool Gray */
            border-radius: 8px; 
            padding: 30px; 
            margin-top: 30px; 
            background-color: white; /* Slight contrast */
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .btn { 
            background: #FF8B4D; /* Bright Orange */
            color: white; 
            padding: 12px 20px; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            margin-top: 15px; 
            font-weight: bold;
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
        }
        .btn:hover, .btn:focus {
            background-color: #ff7a3a; /* Slightly darker orange */
            box-shadow: 0 0 0 3px rgba(255, 139, 77, 0.2); /* Highlight Glow */
            outline: none;
        }
         .btn:disabled {
            background-color: #C4CDD5; /* Cool Gray */
            cursor: not-allowed;
        }
        .recommendation { 
            background: #e0f2f1; /* Lighter Teal */
            padding: 20px; 
            border-left: 5px solid #3CB4AC; /* Teal Green */
            margin: 25px 0; 
            border-radius: 4px;
        }
        .recommendation h3 {
             margin-top: 0;
             color: #3CB4AC; /* Teal Green */
        }
        .step { margin-top: 30px; }
        h1, h2, h3 { 
            color: #3CB4AC; /* Teal Green */
            font-weight: 600;
        }
        .tagline { color: #6c757d; font-style: italic; margin-top: 5px; margin-bottom: 20px; text-align: center; }
        input[type="radio"] { margin-right: 8px; accent-color: #3CB4AC; /* Teal Green */ }
        label { display: block; margin: 12px 0; background-color: #f8f9fa; padding: 10px 15px; border-radius: 4px; cursor: pointer; transition: background-color 0.2s ease; }
        label:hover { background-color: #e9ecef; }
        .logo-container { text-align: center; margin-bottom: 10px; }
        .logo-container img { max-width: 200px; height: auto; }
        .loading { display: none; margin: 20px 0; color: #3CB4AC; /* Teal Green */ }
        .spinner { 
            border: 4px solid #f0f0f0; /* Lighter gray */
            border-top: 4px solid #3CB4AC; /* Teal Green */
            border-radius: 50%; 
            width: 25px; 
            height: 25px; 
            animation: spin 1.5s linear infinite; 
            display: inline-block; 
            vertical-align: middle; 
            margin-right: 10px; 
        }
        pre { 
            background: #f0f0f0; /* Light Gray */
            padding: 15px; 
            overflow-x: auto; 
            border-radius: 6px; 
            border: 1px solid #C4CDD5; /* Cool Gray */
            color: #2E2E2E; /* Deep Charcoal */
            font-family: monospace;
            font-size: 0.9em;
            margin: 10px 0;
        }
        .status { 
            margin: 20px 0; 
            padding: 15px; 
            border-radius: 6px; 
            border: 1px solid transparent;
        }
        .success { 
            background: #d1f7e9; /* Lighter Success Green */
            color: #1a7d5a; /* Darker Success Green */
            border-color: #4DD9A3; /* Success/confirmation */
        }
        .error { 
            background: #ffd9d9; /* Lighter Error Red */
            color: #a71d1d; /* Darker Error Red */
            border-color: #FF6B6B; /* Error */
        }
        .warning { 
            background: #fff8e1; /* Lighter Warning Yellow */
            color: #8a6d3b; /* Darker Warning Yellow */
            border-color: #ffe5a0;
        }
        .status pre { margin-top: 10px; background-color: rgba(0,0,0,0.05); }
        a { color: #FF8B4D; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ol { padding-left: 20px; }
        ol li { margin-bottom: 10px; }
        ol ol { margin-top: 5px; }
        strong { font-weight: 600; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .copy-container {
            display: flex;
            align-items: center; /* Vertically align items in the center */
            margin-top: 10px;
            margin-bottom: 10px;
            gap: 10px; /* Add space between pre/code and button */
        }
        .copy-container pre, .copy-container code {
            flex-grow: 1; /* Allow text block to take available space */
            margin: 0; /* Remove default margins */
        }
        .copy-container .copy-btn {
            flex-shrink: 0; /* Prevent button from shrinking */
            padding: 8px 12px; /* Adjust padding */
            font-size: 0.9em;
            margin: 0; /* Remove default margins */
        }
        .code-box {
             background: #f0f0f0; 
             padding: 8px 12px; 
             border-radius: 4px; 
             border: 1px solid #C4CDD5; 
             display: inline-block; /* Or block if needed */
        }

        /* Responsive adjustments */
    </style>
    <script>
        function checkPrerequisites() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('prereqBtn').disabled = true;
            
            fetch('/check_prerequisites')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('prereqBtn').disabled = false;
                    document.getElementById('prereqStatus').innerHTML = data.message;
                    document.getElementById('prereqStatus').className = 'status ' + data.status;
                    
                    if (data.ready) {
                        document.getElementById('setupForm').style.display = 'block';
                    }
                });
        }

        // Simple copy-to-clipboard function
        function copyToClipboard(text, buttonElement) {
            navigator.clipboard.writeText(text).then(function() {
                const originalText = buttonElement.innerText;
                buttonElement.innerText = 'Copied!';
                setTimeout(() => {
                    buttonElement.innerText = originalText;
                }, 1500); // Reset text after 1.5 seconds
            }, function(err) {
                console.error('Could not copy text: ', err);
                alert('Failed to copy text.');
            });
        }
    </script>
</head>
<body>
    <div class="logo-container">
        <img src="{{ url_for('static', filename='images/lilchatty-logo.png') }}" alt="Lil' Chatty Logo">
    </div>
    <p class="tagline">Your friendly, local ChatGPT-like app</p>
    
    {% if step == 'start' %}
    <div class="container">
        <h2>Quick Setup Wizard</h2>
        <p>Detected RAM: <strong>{{ ram_gb }}GB</strong></p>
        
        <div class="step">
            <h3>Prerequisites Check</h3>
            <p>First, we need to check if your system has Docker or can run Colima.</p>
            <button id="prereqBtn" onclick="checkPrerequisites()" class="btn">Check Prerequisites</button>
            <div id="loading" class="loading">
                <div class="spinner"></div> Checking system requirements...
            </div>
            <div id="prereqStatus"></div>
        </div>
        
        <form id="setupForm" action="/setup" method="post" style="display: none;">
            <div class="step">
                <h3>1. Choose Your Setup</h3>
                <label><input type="radio" name="deployment" value="local" checked> 💻 Run AI Locally (Bundled Ollama)</label>
                <label><input type="radio" name="deployment" value="cloud"> ☁️ Run Web UI Only (Connect external AI later)</label>
            </div>
            
            <div class="step">
                <h3>2. Internet Access</h3>
                <label><input type="radio" name="search" value="yes" checked> 🌐 Enable internet search capabilities</label>
                <label><input type="radio" name="search" value="no"> 🧠 Use AI knowledge only (No Live Web)</label>
            </div>
            
            <button type="submit" class="btn">Get Started →</button>
        </form>
    </div>
    
    {% elif step == 'results' %}
    <div class="container">
        <h2>Your Lil' Chatty Setup</h2>
        
        <p>Follow these steps to get Lil' Chatty running:</p>

        <div class="step">
            <h3>1. Run the Setup Command</h3>
            <p>Copy and paste this command into your terminal:</p>
            <div class="copy-container">
                <pre id="dockerCommand">{{ docker_command }}</pre>
                <button 
                    class="btn copy-btn" 
                    onclick="copyToClipboard(document.getElementById('dockerCommand').innerText, this)"
                >Copy</button>
            </div>
            <p style="font-size: 0.9em;"><i>This starts the Open WebUI software in the background using Docker.</i></p>
        </div>

        <div class="step">
            <h3>2. Access the Web Interface</h3>
            <p>Wait a few moments for it to start, then open <a href="http://localhost:3000" target="_blank">http://localhost:3000</a> in your browser.</p>
        </div>

        {% if deployment == 'local' %}
        <div class="step">
            <h3>3. Download the Recommended AI Model</h3>
            <p>Go to settings via this link: <a href="http://localhost:3000/admin/settings" target="_blank">http://localhost:3000/admin/settings</a>.</p>
            <p>Click <strong>Models</strong> in the middle/sidebar. Then, near the top right (possibly next to "Manage Models"), click the <strong>Download icon</strong> <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 1em; height: 1em; vertical-align: text-bottom; display: inline-block;"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"></path></svg>.</p>
            <p>Paste the model name below into the field that appears, then click the download button:</p>
             <div class="copy-container">
                <code id="modelName" class="code-box">{{ recommended_model }}</code>
                <button 
                    class="btn copy-btn" 
                    onclick="copyToClipboard(document.getElementById('modelName').innerText, this)"
                >Copy</button>
            </div>
            <p>Click the download button and wait for it to complete. Then, select the model from the main chat screen.</p>
             <p style="font-size: 0.9em;"><i>Based on your {{ ram_gb }}GB RAM, we recommend this model for a good balance of performance and capability.</i></p>
             <p style="font-size: 0.9em;"><i>Many other models are available! Explore more at <a href="https://ollama.com/search" target="_blank">Ollama.com Models</a>.</i></p>
        </div>
        {% endif %}
        
        {% if deployment == 'cloud' %}
        <div class="step">
             <h3>3. Connect External APIs (Optional)</h3>
             <p>If you plan to use external services like OpenAI:</p>
             <ol style="margin-top: 5px; padding-left: 20px;">
                <li>Go to <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI API Keys</a> page and log in or sign up.</li>
                <li>Click "+ Create new secret key". Copy your new <strong>API key</strong>.</li>
                <li>Once Little Chatty is running at <a href="http://localhost:3000" target="_blank">http://localhost:3000</a>, navigate to <strong>Settings > Connections</strong> (or similar section).</li>
                <li>Paste your API key into the "OpenAI API Key" field and save.</li>
             </ol>
             <p style="font-size: 0.9em; margin-top: 5px;"><i>Note: Using OpenAI models may incur costs based on your usage.</i></p>
        </div>
        {% endif %}
        
        {% if search == 'yes' %}
        <div class="step">
            <h3>4. Configure Web Search (Optional):</h3>
            <p>To enable internet search within Little Chatty, you need a Google Programmable Search Engine (PSE) API Key and Engine ID.</p>
            <ol style="margin-top: 5px; padding-left: 20px;">
                <li>Go to the <a href="https://programmablesearchengine.google.com/" target="_blank">Google Programmable Search Engine</a> page and create a new search engine. Configure it to search the entire web. Note your <strong>Search engine ID</strong>.</li>
                <li>Go to the <a href="https://console.cloud.google.com/apis/library/customsearch.googleapis.com" target="_blank">Google Cloud Console Custom Search API page</a>.</li>
                <li>Create a new project or select an existing one. Enable the "Custom Search API".</li>
                <li>Go to "Credentials", click "+ CREATE CREDENTIALS", choose "API key". Copy your new <strong>API key</strong>. (You may want to restrict this key later for security).</li>
                <li>Once Little Chatty is running at <a href="http://localhost:3000" target="_blank">http://localhost:3000</a>, navigate to <strong>Settings > RAG > Web Search</strong>.</li>
                <li>Select "Google PSE" as the engine, paste your API Key into "Google PSE API Key", and your Engine ID into "Google PSE ID". Save the changes.</li>
            </ol>
        </div>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    ram_gb = round(get_system_memory_gb())
    return render_template_string(HTML_TEMPLATE, step='start', ram_gb=ram_gb)

@app.route('/check_prerequisites')
def check_prerequisites():
    if is_docker_running():
        return jsonify({
            'ready': True,
            'status': 'success',
            'message': '✅ Docker is running! You\'re ready to set up Lil\' Chatty.'
        })
    
    # Docker not running, check for Homebrew
    if not is_brew_installed():
        return jsonify({
            'ready': False,
            'status': 'warning',
            'message': '⚠️ Docker is not running and Homebrew is not installed. Please run this command in your terminal to install Homebrew first:<br><pre>/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"</pre><br>Then click \'Check Prerequisites\' again.'
        })
    
    # Check if Colima is installed
    try:
        subprocess.check_output(['which', 'colima'], stderr=subprocess.DEVNULL)
        return jsonify({
            'ready': False,
            'status': 'warning',
            'message': '⚠️ Docker is not running, but Colima is installed. Please start it in your terminal:<br><pre>colima start</pre><br>Wait for it to start, then click \'Check Prerequisites\' again.'
        })
    except:
        # Need to install Colima
        return jsonify({
            'ready': False,
            'status': 'warning',
            'message': '⚠️ Docker is not running and Colima is not installed. Please run this command in your terminal:<br><pre>brew install colima && colima start</pre><br>Wait for it to complete, then click \'Check Prerequisites\' again.'
        })

@app.route('/setup', methods=['POST'])
def setup():
    deployment = request.form.get('deployment')
    search = request.form.get('search')
    ram_gb = round(get_system_memory_gb())
    
    # Determine ONE recommended deepseek-r1 model based on RAM
    # Using the base tags as requested.
    if ram_gb <= 8:
        recommended_model = "deepseek-r1:1.5b" 
    elif ram_gb <= 16:
        recommended_model = "deepseek-r1:7b"  
    elif ram_gb <= 32:
         recommended_model = "deepseek-r1:14b" 
    else: # 32GB+
        recommended_model = "deepseek-r1:32b"

    # Construct Docker command based on docs (using ghcr.io)
    if deployment == 'local':
        # Use bundled Ollama image
        docker_command = "docker run -d -p 3000:8080 -v ollama:/root/.ollama -v open-webui:/app/backend/data --name lilchatty --restart always ghcr.io/open-webui/open-webui:ollama"
    else: # 'cloud' means run base webui, configure external connections later
        docker_command = "docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name lilchatty --restart always ghcr.io/open-webui/open-webui:main"
    
    return render_template_string(
        HTML_TEMPLATE,
        step='results',
        ram_gb=ram_gb,
        deployment=deployment,
        search=search,
        recommended_model=recommended_model,
        docker_command=docker_command
    )

if __name__ == '__main__':
    port = find_available_port()
    if port is None:
        print("Error: Could not find an available port between 5001 and 5010.")
        print("Please free up a port in this range and try again.")
        exit(1)

    print(f"\n🚀 Starting Lil' Chatty Setup on http://localhost:{port} 🚀")
    print(f"   Your friendly, local ChatGPT-like app setup wizard")
    print(f"   (Access this setup page from another device on your network via http://<your-local-ip>:{port})")

    # Open browser automatically after a short delay
    threading.Timer(1, open_browser, args=[port]).start()

    app.run(debug=False, host='0.0.0.0', port=port)