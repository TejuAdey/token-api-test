from flask import Flask, render_template, request
import requests
import os
import time

app = Flask(__name__)

def format_address(address):
    if len(address) > 7:
        return f"{address[:3]}...{address[-4:]}"
    return address

@app.route('/', methods=['GET', 'POST'])
def display_tokens():
    search_term = request.form.get('search_term', 'tao')  
    url = f"https://api.0x.org/tokens/v1/symbolOrName/{search_term}?limit=20"
    api_key = os.environ.get('OX_API_KEY')
    
    headers = {
        '0x-api-key': api_key
    }
    
    start_time = time.time()  # Start timing
    response = requests.get(url, headers=headers)
    end_time = time.time()  # End timing
    
    api_response_time = end_time - start_time  # Calculate response time
    
    if response.status_code == 200:
        data = response.json().get("data", [])
        tokens = [{"name": token["name"], 
                   "address": token["address"],
                   "formatted_address": format_address(token["address"]),
                   "symbol": token["symbol"],
                   "decimals": token.get("decimals", "N/A")}
                  for token in data]
        print (f"Search term: {search_term}")
        print(f"API Response Time: {api_response_time:.2f} seconds")  # Print response time
        return render_template('index.html', tokens=tokens, search_term=search_term, api_response_time=api_response_time)
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Error fetching tokens", 500

if __name__ == "__main__":
    app.run(debug=True)
