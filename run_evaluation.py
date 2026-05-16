import pandas as pd
import requests
import json
import os

# To be generated based on requirements
CSV_PATH = "data/final_eval.csv"
API_URL = "http://127.0.0.1:5000/analyze"

def run_eval():
    if not os.path.exists(CSV_PATH):
        print("Error: data/final_eval.csv not found.")
        return

    df = pd.read_csv(CSV_PATH)
    results = []
    
    print(f"Starting evaluation on {len(df)} samples...")

    for index, row in df.iterrows():
        payload = {"text": row['prompt'], "input_id": row['id']}
        try:
            resp = requests.post(API_URL, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                results.append({
                    "id": row['id'],
                    "expected": row['expected_policy'],
                    "actual": data['decision'],
                    "risk": data['final_risk'],
                    "latency": data['latency_ms']
                })
        except:
            continue

    res_df = pd.DataFrame(results)
    
    # Calculate Metrics
    correct = (res_df['expected'] == res_df['actual']).sum()
    accuracy = correct / len(res_df)
    
    print(f"--- Evaluation Complete ---")
    print(f"Total: {len(res_df)}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Mean Latency: {res_df['latency'].mean():.2f}ms")
    
    res_df.to_csv("results/evaluation_results.csv", index=False)

if __name__ == "__main__":
    run_eval()