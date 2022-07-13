import requests

# response = requests.post("http://127.0.0.1:8080/api/bank/",
#                         json={'accountName': 'Adamessa', 'accountWallet': 526.05})
response = requests.get("http://127.0.0.1:8080/test-api/bank/1")


# response = requests.delete("http://127.0.0.1:8080/api/bank/")

                        
# response = requests.put("http://127.0.0.1:8080/api/bank/1",
#                         json={'accountName': 'Abraham new', 'accountWallet': 526.05})
                        
                        
# response = requests.put("http://127.0.0.1:8080/api/bank/1",
#                         json={'accountName':'old fogey','accountWallet': 120})
                        
                        
# response = requests.delete("http://127.0.0.1:8080/api/bank/3")

print(response.json())
