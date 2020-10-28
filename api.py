import requests

def main():
    book = "0441172717"
    #res = requests.get("https://www.goodreads.com/book/isbn/?format=json&user_id=101982751}",params={"isbn":book})
    res=requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "PGKpdo40NGG3UYKK15b1rQ", "isbns":book})
    data = res.json()
    rate = data["books"][0]["average_rating"]
    num = data["books"][0]["work_ratings_count"]
    print(f"rate={rate} and count = {num}")
if __name__ == "__main__":
    main()
