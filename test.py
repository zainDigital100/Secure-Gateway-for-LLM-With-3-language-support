import requests
import time
import sys

def find_active_server():
    ports = [8000, 5000, 8080]
    hosts = ["127.0.0.1", "localhost"]
    
    print("Searching for active API server...")
    for port in ports:
        for host in hosts:
            url = f"http://{host}:{port}/analyze"
            try:
                resp = requests.post(url, json={"input_id": "ping", "prompt": "test", "text": "test"}, timeout=5)
                print(f"✅ Connected successfully to {url}\n")
                return url
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.RequestException:
                print(f"✅ Connected successfully to {url}\n")
                return url
                
    print("❌ Could not detect a running server on standard ports.")
    print("Please check your server terminal to confirm the URL and port.\n")
    return "http://127.0.0.1:8000/analyze"

def run_interactive_test():
    url = find_active_server()
    
    print("Interactive LLM Security Gateway Tester")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 50)
    
    while True:
        try:
            user_prompt = input("\nEnter your prompt: ")
        except EOFError:
            break
            
        if user_prompt.strip().lower() in ['exit', 'quit']:
            print("Exiting...")
            break
            
        if not user_prompt.strip():
            continue
            
        payload = {
            "input_id": "interactive_test", 
            "prompt": user_prompt,
            "text": user_prompt,
            "input_text": user_prompt
        }
        start_t = time.time()
        
        try:
            resp = requests.post(url, json=payload, timeout=60)
            
            if not resp.ok:
                print(f"\nServer Error ({resp.status_code}): {resp.text}")
                print("Tip: Check if your server expects different JSON keys.")
                continue
                
            res_data = resp.json()
            lat = (time.time() - start_t) * 1000
            
            print("\n" + "="*50)
            print("METRICS OVERVIEW:")
            print(f"Decision:     {res_data.get('decision')}")
            print(f"Final Risk:   {res_data.get('final_risk')}")
            
            reasons = res_data.get('reason_codes')
            reasons_str = ", ".join(reasons) if reasons else "None"
            print(f"Reasons:      {reasons_str}")
            
            print(f"Latency:      {round(lat, 2)} ms")
            print(f"Language:     {res_data.get('language')}")
            
            safe_text = res_data.get('safe_text')
            if safe_text:
                print(f"Safe Text:    {safe_text}")
                
            print("="*50)
            
        except requests.exceptions.ConnectionError:
            print(f"\nConnection Error: The server at {url} went offline.")
        except requests.exceptions.RequestException as e:
            print(f"\nAPI Error: {e}")

if __name__ == "__main__":
    run_interactive_test()
