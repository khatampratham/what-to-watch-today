import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "INSERT YOUR API KEY HERE, check readme for info"
BASE_URL = "https://api.themoviedb.org/3"

def search(movie):
    
    resp = requests.get(f"{BASE_URL}/search/movie?api_key={API_KEY}&query={movie}")
    data = resp.json()
    results = data.get('results', [])
    if not results:
        return None
    return results[0]['id']

def recommend():
    
    movie = inp.get().strip()
    if not movie:
        messagebox.showwarning("Input Required", "Please enter a movie!")
        return

    mid = search(movie)
    res.delete(1.0, tk.END)
    
    if not mid:
        messagebox.showerror("Error", f"No movie found for '{movie}'.")
        return

    resp = requests.get(f"{BASE_URL}/movie/{mid}/recommendations?api_key={API_KEY}")
    data = resp.json()
    recs = data.get('results', [])

    if not recs:
        res.insert(tk.END, f"No recommendations found for '{movie}'.")
        return

    res.insert(tk.END, f"Top 5 movies similar to '{movie}':\n\n")
    for m in recs[:5]:
        res.insert(tk.END, f"- {m['title']}\n")

root = tk.Tk()
root.title("Movie Recommendation")
root.geometry("500x300")

tk.Label(root, text="Enter a movie:", font=("Helvetica", 12)).pack(pady=10)

inp = tk.Entry(root, width=50)
inp.pack(pady=5)
inp.focus()

tk.Button(root, text="Get Recommendations", command=recommend, bg="#4CAF50", fg="white").pack(pady=10)

res = tk.Text(root, height=10, width=60, bg="#f9f9f9")
res.pack(pady=5)

root.mainloop()

