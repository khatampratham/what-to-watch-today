import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

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
        messagebox.showwarning("Input Required", "Enter a movie!")
        return

    mid = search(movie)
    res.delete(1.0, tk.END)
    img_label.config(image="")  # Clear previous image

    if not mid:
        messagebox.showerror("Error", f"No movie found for '{movie}'.")
        return

    resp = requests.get(f"{BASE_URL}/movie/{mid}/recommendations?api_key={API_KEY}")
    data = resp.json()
    recs = data.get('results', [])

    if not recs:
        res.insert(tk.END, f"No recommendations found for '{movie}'.")
        return

    first = recs[0]
    title = first['title']
    rating = first['vote_average']
    poster_path = first['poster_path']
    res.insert(tk.END, f"Top Recommendation:\nTitle: {title}\nRating: {rating}\n\n")

    # Display poster
    if poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
        response = requests.get(poster_url)
        img_data = Image.open(BytesIO(response.content))
        img_data = img_data.resize((200, 300))
        img = ImageTk.PhotoImage(img_data)
        img_label.config(image=img)
        img_label.image = img

root = tk.Tk()
root.title("Movie Recommender GUI")
root.geometry("500x600")

tk.Label(root, text="Enter a movie:").pack(pady=10)
inp = tk.Entry(root, width=50)
inp.pack(pady=5)
inp.focus()

tk.Button(root, text="Get Recommendation", command=recommend, bg="#4CAF50", fg="white").pack(pady=10)

res = tk.Text(root, height=5, width=60)
res.pack(pady=5)

img_label = tk.Label(root)
img_label.pack(pady=5)

root.mainloop()

