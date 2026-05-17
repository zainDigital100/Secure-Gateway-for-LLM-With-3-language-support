import pandas as pd
import requests
import json
import os
import time

CSV_PATH = "data/final_eval.csv"
API_URL = "http://127.0.0.1:5000/analyze"

def calculate_metrics(res_df):
    correct = (res_df['expected'] == res_df['actual']).sum()
    accuracy = correct / len(res_df)

    y_true = res_df['expected'] == 'BLOCK'
    y_pred = res_df['actual'] == 'BLOCK'

    tp = ((y_pred == True) & (y_true == True)).sum()
    fp = ((y_pred == True) & (y_true == False)).sum()
    fn = ((y_pred == False) & (y_true == True)).sum()
    tn = ((y_pred == False) & (y_true == False)).sum()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    multi_recall = {}
    if 'language' in res_df.columns:
        for lang in res_df['language'].unique():
            lang_df = res_df[res_df['language'] == lang]
            l_true = lang_df['expected'] == 'BLOCK'
            l_pred = lang_df['actual'] == 'BLOCK'
            l_tp = ((l_pred == True) & (l_true == True)).sum()
            l_fn = ((l_pred == False) & (l_true == True)).sum()
            multi_recall[lang] = l_tp / (l_tp + l_fn) if (l_tp + l_fn) > 0 else 0

    latencies = res_df['latency']
    mean_latency = latencies.mean()
    median_latency = latencies.median()

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "multilingual_recall": multi_recall,
        "mean_latency": mean_latency,
        "median_latency": median_latency,
        "confusion_matrix": {"tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn)}
    }

def run_eval():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    df = pd.read_csv(CSV_PATH)
    results_data = []
    
    print(f"🚀 Starting Hybrid Security Gateway Evaluation...")
    print(f"Total Samples: {len(df)}")
    print("-" * 40)

    for index, row in df.iterrows():
        payload = {"text": row['prompt'], "input_id": str(row.get('id', index))}
        try:
            start_wall = time.time()
            resp = requests.post(API_URL, json=payload, timeout=30)
            end_wall = time.time()
            
            if resp.status_code == 200:
                data = resp.json()
                results_data.append({
                    "id": row.get('id', index),
                    "language": row.get('language', 'en'),
                    "expected": row['expected_policy'],
                    "actual": data['decision'],
                    "risk": data['final_risk'],
                    "latency": data['latency_ms'],
                    "rtt_ms": (end_wall - start_wall) * 1000
                })
                print(f"[{index+1}/{len(df)}] ID: {row.get('id', index)} | Decision: {data['decision']} | Latency: {data['latency_ms']}ms")
            else:
                print(f"[{index+1}/{len(df)}] Failed with status: {resp.status_code}")
        except Exception as e:
            print(f"[{index+1}/{len(df)}] Connection Error: {str(e)}")
            continue

    if not results_data:
        print("No results collected.")
        return

    res_df = pd.DataFrame(results_data)
    metrics = calculate_metrics(res_df)

    print("-" * 40)
    print(f"✅ EVALUATION SUMMARY")
    print(f"Accuracy:  {metrics['accuracy']:.2%}")
    print(f"Precision: {metrics['precision']:.2%}")
    print(f"Recall:    {metrics['recall']:.2%}")
    print(f"F1-Score:  {metrics['f1_score']:.2%}")
    print("-" * 20)
    print(f"Mean Latency:   {metrics['mean_latency']:.2f}ms")
    print(f"Median Latency: {metrics['median_latency']:.2f}ms")
    print("-" * 20)
    print("Multilingual Recall:")
    for lang, val in metrics['multilingual_recall'].items():
        print(f"  - {lang}: {val:.2%}")

    if not os.path.exists("results"):
        os.makedirs("results")
    
    res_df.to_csv("results/evaluation_results.csv", index=False)
    with open("results/metrics_summary.json", "w") as f:
        json.dump(metrics, f, indent=4)
    
    print("-" * 40)
    print(f"Results saved to 'results/' directory.")

if __name__ == "__main__":
    run_eval()