import os, time, requests, threading, json
import credentials as cfg

API_KEY = cfg.api_key
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'
TRACKING_CFG = './tracking.cfg'
url_tracking_lock = threading.Lock()
SESSION = requests.Session()


def read_tracking_file():
    try:
        with open(TRACKING_CFG, "r") as tracking_file:
            return json.load(tracking_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_tracking_file(tracking: list):
    with open(TRACKING_CFG, "w") as tracking_file:
        json.dump(tracking, tracking_file)


def track_url():
    with url_tracking_lock:
        tracking = read_tracking_file()
        while True:  # To track not more than 1000 requests per hour
            tracking = [t for t in tracking if time.time() - t <= 3600]
            if len(tracking) < 1000:
                tracking.append(time.time())
                write_tracking_file(tracking)
                break
            else:
                time.sleep(10)


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    params = {"api_key": API_KEY,
              "start_date": start_date,
              "end_date": end_date,
              }
    track_url()
    response = SESSION.get(APOD_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json()


def download_img(url: str, title: str):
    track_url()
    print(f"{title}: {url}")
    response = SESSION.get(url)
    if response.status_code == 200:
        with open(f'{OUTPUT_IMAGES}/{url.split("/")[-1]}', "wb") as img:
            img.write(response.content)


def download_apod_images(metadata: list):
    start = time.time()

    threads = []
    for item in metadata:
        if item["media_type"] == 'image':
            if not os.path.exists(f'{OUTPUT_IMAGES}/{item["hdurl"].split("/")[-1]}'):
                thread = threading.Thread(target=download_img, args=(item["hdurl"], item["title"]))
                thread.start()
                threads.append(thread)

    [t.join() for t in threads]

    print(f"Downloaded in {time.time() - start}")


def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)

    main()


