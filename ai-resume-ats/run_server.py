import subprocess
import time
import sys

def start_server():
    print("🚀 Starting HTTP API Server...")
    
    server_path = r"C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\http_api_server.py"
    
    try:
        # Start the server process
        process = subprocess.Popen([sys.executable, server_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        print(f"✅ Server started with PID: {process.pid}")
        print("📍 Server URL: http://127.0.0.1:7000")
        print("🌐 Your frontend can now connect!")
        print("\n⚠️  Keep this terminal open to keep the server running")
        print("🔄 Press Ctrl+C to stop the server")
        
        # Keep the process running
        try:
            while True:
                time.sleep(1)
                # Check if process is still running
                if process.poll() is not None:
                    print("❌ Server process ended unexpectedly")
                    break
        except KeyboardInterrupt:
            print("\n🔄 Stopping server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped")
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

if __name__ == "__main__":
    start_server()