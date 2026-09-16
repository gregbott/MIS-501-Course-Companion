"""
Module 15: REST APIs & Data Acquisition - Worked Example Computations

This script reproduces every worked-example output in the Module 15 chapter
of the MIS501 Course Companion. Run with:

    pixi run -e compute python computations/module15_examples.py

DETERMINISM / OFFLINE NOTE: The teaching notebook calls the live
JSONPlaceholder API (jsonplaceholder.typicode.com) and httpbin.org with
`requests`. These demos make NO network calls. Each demo processes embedded
sample data that mirrors the real APIs' response shapes:

- SAMPLE_USERS mirrors GET /users (all 10 user records, same nested
  address/geo/company structure as the live API).
- SAMPLE_POSTS and SAMPLE_COMMENTS mirror GET /posts (100 records, 10 per
  user) and GET /comments (500 records, 5 per post). They are built
  deterministically at import time from small literal palettes so the file
  stays readable while matching the live API's scale and field names.
- SAMPLE_HEADERS_ECHO mirrors the httpbin.org/headers echo response.

The `requests` library is imported ONLY for its exception classes so the
error-handling demos use the exact `except` clauses the notebook teaches;
no request is ever sent. The caching demo writes only under the
deterministic relative path computations/_scratch/module15/.

References in Course Companion:
- demo_first_api_request()      -> Module 15, Section 15.1 (Making Your First API Request)
- demo_status_codes()           -> Module 15, Section 15.1 (Understanding HTTP Status Codes)
- demo_json_to_python()         -> Module 15, Section 15.2 (From JSON to Python Objects)
- demo_nested_json_navigation() -> Module 15, Section 15.2 (Navigating Nested JSON)
- demo_query_parameters()       -> Module 15, Section 15.2 (Query Parameters)
- demo_request_headers()        -> Module 15, Section 15.2 (Headers and Authentication)
- demo_error_handling()         -> Module 15, Section 15.3 (Two Layers of Error Handling)
- demo_rate_limited_fetch()     -> Module 15, Section 15.3 (Rate Limiting)
- demo_pagination_loop()        -> Module 15, Section 15.3 (Pagination)
- demo_fetch_all_pages()        -> Module 15, Section 15.3 (A Reusable Pagination Function)
- demo_response_caching()       -> Module 15, Section 15.3 (Caching Responses for Reproducible Analysis)
- demo_api_to_dataframe()       -> Module 15, Section 15.4 (From API Response to Polars DataFrame)
- demo_capstone_analysis()      -> Module 15, Section 15.4 (Capstone: Multi-Endpoint Analysis)

Last updated: 2026-07-23
"""

import json
import time
from pathlib import Path

import polars as pl
import requests  # imported for its exception classes only — no network calls

# ---------------------------------------------------------------------------
# Embedded sample data (mirrors jsonplaceholder.typicode.com response shapes)
# ---------------------------------------------------------------------------

# GET https://jsonplaceholder.typicode.com/users
# All 10 user records with the live API's nested structure.
SAMPLE_USERS = [
    {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz",
        "address": {
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "city": "Gwenborough",
            "zipcode": "92998-3874",
            "geo": {"lat": "-37.3159", "lng": "81.1496"},
        },
        "phone": "1-770-736-8031 x56442",
        "website": "hildegard.org",
        "company": {
            "name": "Romaguera-Crona",
            "catchPhrase": "Multi-layered client-server neural-net",
            "bs": "harness real-time e-markets",
        },
    },
    {
        "id": 2,
        "name": "Ervin Howell",
        "username": "Antonette",
        "email": "Shanna@melissa.tv",
        "address": {
            "street": "Victor Plains",
            "suite": "Suite 879",
            "city": "Wisokyburgh",
            "zipcode": "90566-7771",
            "geo": {"lat": "-43.9509", "lng": "-34.4618"},
        },
        "phone": "010-692-6593 x09125",
        "website": "anastasia.net",
        "company": {
            "name": "Deckow-Crist",
            "catchPhrase": "Proactive didactic contingency",
            "bs": "synergize scalable supply-chains",
        },
    },
    {
        "id": 3,
        "name": "Clementine Bauch",
        "username": "Samantha",
        "email": "Nathan@yesenia.net",
        "address": {
            "street": "Douglas Extension",
            "suite": "Suite 847",
            "city": "McKenziehaven",
            "zipcode": "59590-4157",
            "geo": {"lat": "-68.6102", "lng": "-47.0653"},
        },
        "phone": "1-463-123-4447",
        "website": "ramiro.info",
        "company": {
            "name": "Romaguera-Jacobson",
            "catchPhrase": "Face to face bifurcated interface",
            "bs": "e-enable strategic applications",
        },
    },
    {
        "id": 4,
        "name": "Patricia Lebsack",
        "username": "Karianne",
        "email": "Julianne.OConner@kory.org",
        "address": {
            "street": "Hoeger Mall",
            "suite": "Apt. 692",
            "city": "South Elvis",
            "zipcode": "53919-4257",
            "geo": {"lat": "29.4572", "lng": "-164.2990"},
        },
        "phone": "493-170-9623 x156",
        "website": "kale.biz",
        "company": {
            "name": "Robel-Corkery",
            "catchPhrase": "Multi-tiered zero tolerance productivity",
            "bs": "transition cutting-edge web services",
        },
    },
    {
        "id": 5,
        "name": "Chelsey Dietrich",
        "username": "Kamren",
        "email": "Lucio_Hettinger@annie.ca",
        "address": {
            "street": "Skiles Walks",
            "suite": "Suite 351",
            "city": "Roscoeview",
            "zipcode": "33263",
            "geo": {"lat": "-31.8129", "lng": "62.5342"},
        },
        "phone": "(254)954-1289",
        "website": "demarco.info",
        "company": {
            "name": "Keebler LLC",
            "catchPhrase": "User-centric fault-tolerant solution",
            "bs": "revolutionize end-to-end systems",
        },
    },
    {
        "id": 6,
        "name": "Mrs. Dennis Schulist",
        "username": "Leopoldo_Corkery",
        "email": "Karley_Dach@jasper.info",
        "address": {
            "street": "Norberto Crossing",
            "suite": "Apt. 950",
            "city": "South Christy",
            "zipcode": "23505-1337",
            "geo": {"lat": "-71.4197", "lng": "71.7478"},
        },
        "phone": "1-477-935-8478 x6430",
        "website": "ola.org",
        "company": {
            "name": "Considine-Lockman",
            "catchPhrase": "Synchronised bottom-line interface",
            "bs": "e-enable innovative applications",
        },
    },
    {
        "id": 7,
        "name": "Kurtis Weissnat",
        "username": "Elwyn.Skiles",
        "email": "Telly.Hoeger@billy.biz",
        "address": {
            "street": "Rex Trail",
            "suite": "Suite 280",
            "city": "Howemouth",
            "zipcode": "58804-1099",
            "geo": {"lat": "24.8918", "lng": "21.8984"},
        },
        "phone": "210.067.6132",
        "website": "elvis.io",
        "company": {
            "name": "Johns Group",
            "catchPhrase": "Configurable multimedia task-force",
            "bs": "generate enterprise e-tailers",
        },
    },
    {
        "id": 8,
        "name": "Nicholas Runolfsdottir V",
        "username": "Maxime_Nienow",
        "email": "Sherwood@rosamond.me",
        "address": {
            "street": "Ellsworth Summit",
            "suite": "Suite 729",
            "city": "Aliyaview",
            "zipcode": "45169",
            "geo": {"lat": "-14.3990", "lng": "-120.7677"},
        },
        "phone": "586.493.6943 x140",
        "website": "jacynthe.com",
        "company": {
            "name": "Abernathy Group",
            "catchPhrase": "Implemented secondary concept",
            "bs": "e-enable extensible e-tailers",
        },
    },
    {
        "id": 9,
        "name": "Glenna Reichert",
        "username": "Delphine",
        "email": "Chaim_McDermott@dana.io",
        "address": {
            "street": "Dayna Park",
            "suite": "Suite 449",
            "city": "Bartholomebury",
            "zipcode": "76495-3109",
            "geo": {"lat": "24.6463", "lng": "-168.8889"},
        },
        "phone": "(775)976-6794 x41206",
        "website": "conrad.com",
        "company": {
            "name": "Yost and Sons",
            "catchPhrase": "Switchable contextually-based project",
            "bs": "aggregate real-time technologies",
        },
    },
    {
        "id": 10,
        "name": "Clementina DuBuque",
        "username": "Moriah.Stanton",
        "email": "Rey.Padberg@karina.biz",
        "address": {
            "street": "Kattie Turnpike",
            "suite": "Suite 198",
            "city": "Lebsackbury",
            "zipcode": "31428-2261",
            "geo": {"lat": "-38.2386", "lng": "57.2232"},
        },
        "phone": "024-648-3804",
        "website": "ambrose.net",
        "company": {
            "name": "Hoeger LLC",
            "catchPhrase": "Centralized empowering task-force",
            "bs": "target end-to-end models",
        },
    },
]

# Title and body palettes used to build the 100-post sample. Entry 0 of each
# palette is the live API's actual post #1 content (body newlines replaced
# with spaces) so single-post demos match what students see in the notebook.
POST_TITLES = [
    "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "qui est esse",
    "ea molestias quasi exercitationem repellat qui ipsa sit aut",
    "eum et est occaecati",
    "nesciunt quas odio",
    "dolorem eum magni eos aperiam quia",
    "magnam facilis autem",
    "dolorem dolore est ipsam",
    "nesciunt iure omnis dolorem tempora et accusantium",
    "optio molestias id quia eum",
]

POST_BODIES = [
    "quia et suscipit suscipit recusandae consequuntur expedita et cum "
    "reprehenderit molestiae ut ut quas totam nostrum rerum est autem "
    "sunt rem eveniet architecto",
    "est rerum tempore vitae sequi sint nihil reprehenderit dolor beatae "
    "ea dolores neque fugiat blanditiis voluptate porro vel nihil "
    "molestiae ut reiciendis qui aperiam non debitis possimus qui neque "
    "nisi nulla",
    "et iusto sed quo iure voluptatem occaecati omnis eligendi aut ad "
    "voluptatem doloribus vel accusantium quis pariatur molestiae porro "
    "eius odio et labore et velit aut",
    "ullam et saepe reiciendis voluptatem adipisci sit amet autem "
    "assumenda provident rerum culpa quis hic commodi nesciunt rem "
    "tenetur doloremque ipsam iure quis sunt voluptatem rerum illo velit",
    "repudiandae veniam quaerat sunt sed alias aut fugiat sit autem sed "
    "est voluptatem omnis possimus esse voluptatibus quis est aut "
    "tenetur dolor neque",
]

# GET https://jsonplaceholder.typicode.com/posts
# Mirrors the live API's scale and shape: 100 posts, ids 1-100, exactly 10
# posts per user (posts 1-10 belong to user 1, 11-20 to user 2, ...).
SAMPLE_POSTS = [
    {
        "userId": (post_id - 1) // 10 + 1,
        "id": post_id,
        "title": POST_TITLES[(post_id - 1) % len(POST_TITLES)],
        "body": POST_BODIES[(post_id - 1) % len(POST_BODIES)],
    }
    for post_id in range(1, 101)
]

# Comment palettes. The email palette holds the live API's five post-1
# commenter emails; the nine body texts have deliberately different lengths
# so per-post discussion volume varies deterministically.
COMMENT_NAMES = [
    "id labore ex et quam laborum",
    "quo vero reiciendis velit similique earum",
    "odio adipisci rerum aut animi",
    "alias odio sit",
    "vero eaque aliquid doloribus et culpa",
]

COMMENT_EMAILS = [
    "Eliseo@gardner.biz",
    "Jayne_Kuhic@sydney.com",
    "Nikita@garfield.biz",
    "Lew@alysha.tv",
    "Hayden@althea.biz",
]

COMMENT_BODIES = [
    "laudantium enim quasi est quidem magnam voluptate ipsam eos tempora "
    "quo necessitatibus dolor quam autem quasi reiciendis et nam sapiente "
    "accusantium",
    "est natus enim nihil est dolore omnis voluptatem numquam et omnis "
    "occaecati quod ullam at voluptatem error expedita pariatur nihil "
    "sint nostrum voluptatem reiciendis et",
    "quia molestiae reprehenderit quasi aspernatur aut expedita occaecati "
    "aliquam eveniet laudantium omnis quibusdam delectus saepe quia "
    "accusamus maiores nam est cum et ducimus et vero voluptates "
    "excepturi deleniti ratione",
    "non et atque occaecati deserunt quas accusantium unde odit nobis qui "
    "voluptatem quia voluptas consequuntur itaque dolor et qui rerum "
    "deleniti ut occaecati",
    "harum non quasi et ratione tempore iure ex voluptates in ratione "
    "harum architecto fugit inventore cupiditate voluptates magni quo et",
    "doloribus at sed quis culpa deserunt consectetur qui praesentium "
    "accusamus fugiat dicta voluptatem rerum ut voluptate autem "
    "voluptatem repellendus aliquid quia",
    "maiores sed dolores similique labore et inventore et quasi "
    "temporibus esse sunt id et eos voluptatem aliquam aliquid ratione "
    "corporis molestiae mollitia quia et magnam et",
    "ut voluptatem corrupti velit ad voluptatem maiores et nisi velit "
    "vero accusantium maiores voluptas quia aut vel eos",
    "sapiente assumenda molestiae atque adipisci laborum distinctio "
    "aperiam et ab ut omnis et occaecati aspernatur odit sit rem "
    "expedita quas enim ipsam minus",
]

# GET https://jsonplaceholder.typicode.com/comments
# Mirrors the live API's scale and shape: 500 comments, ids 1-500, exactly
# 5 comments per post. Because 5 and len(COMMENT_BODIES)=9 share no common
# factor, the five bodies attached to a post shift with every post id, so
# discussion volume varies from post to post (deterministically).
SAMPLE_COMMENTS = [
    {
        "postId": (comment_id - 1) // 5 + 1,
        "id": comment_id,
        "name": COMMENT_NAMES[(comment_id - 1) % len(COMMENT_NAMES)],
        "email": COMMENT_EMAILS[(comment_id - 1) % len(COMMENT_EMAILS)],
        "body": COMMENT_BODIES[(comment_id - 1) % len(COMMENT_BODIES)],
    }
    for comment_id in range(1, 501)
]

# GET https://httpbin.org/headers — httpbin echoes back the headers it
# received (header names arrive capitalized; the Host header is added by
# the HTTP layer). The non-deterministic X-Amzn-Trace-Id header is omitted.
SAMPLE_HEADERS_ECHO = {
    "headers": {
        "Accept": "application/json",
        "Authorization": "Bearer my-secret-token-12345",
        "Host": "httpbin.org",
        "User-Agent": "MIS501-CourseProject/1.0",
        "X-Custom-Header": "hello-from-python",
    }
}


# ---------------------------------------------------------------------------
# Minimal offline stand-in for a requests.Response object
# ---------------------------------------------------------------------------

class _FakeResponse:
    """Offline stand-in exposing the response attributes the demos use."""

    def __init__(self, status_code, reason, payload, url):
        self.status_code = status_code
        self.reason = reason
        self.url = url
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        # Mirrors the message format requests uses for 4xx errors.
        if 400 <= self.status_code < 500:
            raise requests.exceptions.HTTPError(
                f"{self.status_code} Client Error: {self.reason} "
                f"for url: {self.url}"
            )
        if self.status_code >= 500:
            raise requests.exceptions.HTTPError(
                f"{self.status_code} Server Error: {self.reason} "
                f"for url: {self.url}"
            )


def _sample_get_user(user_id):
    """Return a _FakeResponse for GET /users/{user_id} using SAMPLE_USERS."""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    for user in SAMPLE_USERS:
        if user["id"] == user_id:
            return _FakeResponse(200, "OK", user, url)
    return _FakeResponse(404, "Not Found", {}, url)


# ---------------------------------------------------------------------------
# Section 15.1 — What Is a REST API?
# ---------------------------------------------------------------------------

def demo_first_api_request():
    """
    Inspect the response object returned by a GET request to /users, then
    parse the JSON body. Mirrors the notebook's first two request cells;
    the response is the embedded SAMPLE_USERS payload (same shape as the
    live JSONPlaceholder /users response).
    """
    # The notebook sends: requests.get(".../users", timeout=10)
    # Offline equivalent: a response carrying the embedded sample payload.
    response_text = json.dumps(SAMPLE_USERS, indent=2)

    # Inspect the response object
    print("Status code:  200")
    print("Content type: application/json; charset=utf-8")
    print("Encoding:     utf-8")
    print(f"Response size: {len(response_text)} characters")

    # Parse the JSON body — .json() returns a Python list of dictionaries
    users = json.loads(response_text)

    print(f"\nType: {type(users)}")
    print(f"Number of users: {len(users)}")
    print(f"\nFirst user (keys): {list(users[0].keys())}")
    print("\nFirst user preview:")
    print(f"  id:       {users[0]['id']}")
    print(f"  name:     {users[0]['name']}")
    print(f"  username: {users[0]['username']}")
    print(f"  email:    {users[0]['email']}")
    print(f"  city:     {users[0]['address']['city']}")


def demo_status_codes():
    """
    Show the status codes returned by a valid endpoint, a valid endpoint
    with a non-existent resource id, and a non-existent endpoint. The
    (status_code, reason) pairs mirror what the live API returns.
    """
    def sample_get(path):
        """Offline router mirroring JSONPlaceholder's routing behavior."""
        url = f"https://jsonplaceholder.typicode.com{path}"
        if path == "/posts/1":
            return _FakeResponse(200, "OK", SAMPLE_POSTS[0], url)
        # Unknown resource ids and unknown endpoints both return 404.
        return _FakeResponse(404, "Not Found", {}, url)

    ok = sample_get("/posts/1")
    print(f"Valid endpoint:   {ok.status_code} ({ok.reason})")

    not_found = sample_get("/posts/9999")
    print(f"Invalid post ID:  {not_found.status_code} ({not_found.reason})")

    bad_path = sample_get("/widgets")
    print(f"Invalid endpoint: {bad_path.status_code} ({bad_path.reason})")


# ---------------------------------------------------------------------------
# Section 15.2 — JSON Responses, Query Parameters, and Headers
# ---------------------------------------------------------------------------

def demo_json_to_python():
    """
    Fetch a single post (a JSON object) and show that it arrives as a
    Python dict. Uses the embedded post #1, which matches the live API's
    post #1 content.
    """
    post = SAMPLE_POSTS[0]  # GET /posts/1 returns this object

    print(f"Type: {type(post)}")
    print(f"\nPost #{post['id']}:")
    print(f"  User ID: {post['userId']}")
    print(f"  Title:   {post['title'][:60]}...")
    print(f"  Body:    {post['body'][:80]}...")


def demo_nested_json_navigation():
    """
    Navigate a user record with nested address, geo, and company objects.
    Uses the embedded user #1, which matches the live API's user #1.
    """
    user = SAMPLE_USERS[0]  # GET /users/1 returns this object

    # Top-level fields
    print(f"Name:    {user['name']}")
    print(f"Email:   {user['email']}")
    print(f"Phone:   {user['phone']}")

    # Nested: address is a dict inside the user dict
    addr = user["address"]
    print("\nAddress:")
    print(f"  Street: {addr['street']}")
    print(f"  City:   {addr['city']}")
    print(f"  Zip:    {addr['zipcode']}")

    # Deeply nested: geo is inside address
    geo = addr["geo"]
    print(f"  Lat/Lng: {geo['lat']}, {geo['lng']}")

    # Nested: company is a dict
    company = user["company"]
    print(f"\nCompany: {company['name']}")
    print(f"  Catch phrase: {company['catchPhrase']}")


def demo_query_parameters():
    """
    Filter server-side with query parameters: posts by user (?userId=1)
    and comments by post (?postId=1). The filtering applied here to the
    embedded samples is exactly what the server does before responding.
    """
    # requests.get(".../posts", params={"userId": 1}) — the server filters
    user_posts = [p for p in SAMPLE_POSTS if p["userId"] == 1]

    print(f"Posts by user 1: {len(user_posts)}")
    print("\nActual URL sent: https://jsonplaceholder.typicode.com/posts?userId=1")
    print("\nFirst 3 post titles:")
    for post in user_posts[:3]:
        print(f"  - [{post['id']}] {post['title'][:50]}...")

    # requests.get(".../comments", params={"postId": 1})
    comments = [c for c in SAMPLE_COMMENTS if c["postId"] == 1]

    print(f"\nComments on post 1: {len(comments)}")
    print("URL: https://jsonplaceholder.typicode.com/comments?postId=1")
    print()
    for comment in comments[:3]:
        print(f"  From: {comment['email']}")
        print(f"  Body: {comment['body'][:60]}...")
        print()


def demo_request_headers():
    """
    Send custom headers (including a bearer token) and show what the
    server receives. SAMPLE_HEADERS_ECHO mirrors httpbin.org/headers,
    which echoes back the request headers.
    """
    echoed = SAMPLE_HEADERS_ECHO  # response.json() from httpbin.org/headers

    print("Headers received by the server:")
    for key, value in echoed["headers"].items():
        print(f"  {key}: {value}")


# ---------------------------------------------------------------------------
# Section 15.3 — Robust Data Acquisition
# ---------------------------------------------------------------------------

def demo_error_handling():
    """
    Two layers of error handling: (1) checking status_code manually, and
    (2) a fetch_json() helper using raise_for_status() plus try/except.
    The transport is simulated offline; the handling logic is the
    notebook's, and the HTTPError message matches requests' format.
    """
    def sample_get(url, params=None):
        """Offline transport: routes /users/{id}; other paths return 404."""
        if url.endswith("/users/1"):
            return _sample_get_user(1)
        return _FakeResponse(404, "Not Found", {}, url)

    # Pattern 1: check status_code manually
    response = sample_get("https://jsonplaceholder.typicode.com/posts/9999")

    if response.status_code == 200:
        data = response.json()
        print(f"Success: received a {type(data).__name__}")
    elif response.status_code == 404:
        print("Error 404: Resource not found")
    else:
        print(f"Unexpected status: {response.status_code}")

    # Pattern 2: raise_for_status() + try/except
    def fetch_json(url, params=None):
        """Fetch JSON from a URL with error handling."""
        try:
            resp = sample_get(url, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            return None
        except requests.exceptions.Timeout:
            print(f"Timeout: {url} took too long to respond")
            return None
        except requests.exceptions.ConnectionError:
            print(f"Connection error: could not reach {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    data = fetch_json("https://jsonplaceholder.typicode.com/users/1")
    if data:
        print(f"Success: fetched user '{data['name']}'")

    print()
    bad = fetch_json("https://jsonplaceholder.typicode.com/posts/99999")
    if bad is None:
        print("Handled gracefully — no crash")


def demo_rate_limited_fetch():
    """
    Fetch three users with a polite delay, retrying with exponential
    backoff on a 429. The simulated server returns 429 on the first
    attempt for user 2 (then succeeds), so the retry path is exercised —
    something a live demo against JSONPlaceholder rarely shows.
    """
    call_count = {}  # tracks attempts per user id

    def sample_get(url, params=None):
        """Offline transport that rate-limits the first request for user 2."""
        user_id = int(url.rstrip("/").split("/")[-1])
        call_count[user_id] = call_count.get(user_id, 0) + 1
        if user_id == 2 and call_count[user_id] == 1:
            return _FakeResponse(429, "Too Many Requests", {}, url)
        return _sample_get_user(user_id)

    def fetch_with_rate_limit(url, params=None, delay=0.5, max_retries=3):
        """Fetch JSON with rate limiting and retry logic."""
        # range(max_retries + 1): one initial attempt plus max_retries retries
        for attempt in range(max_retries + 1):
            try:
                response = sample_get(url, params=params)

                if response.status_code == 429:
                    # Rate limited — wait longer and retry
                    wait = delay * (2 ** attempt)
                    print(
                        f"  Rate limited (status 429). Waiting {wait:.1f}s "
                        f"(attempt {attempt + 1}/{max_retries + 1})"
                    )
                    time.sleep(wait)
                    continue

                response.raise_for_status()
                time.sleep(delay)  # polite delay between requests
                return response.json()

            except requests.exceptions.RequestException as e:
                print(f"  Request error: {e}")
                return None

        print(f"  Failed after {max_retries} retries")
        return None

    print("Fetching users with rate limiting:")
    for uid in [1, 2, 3]:
        user = fetch_with_rate_limit(
            f"https://jsonplaceholder.typicode.com/users/{uid}",
            delay=0.3,
        )
        if user:
            print(f"  User {uid}: {user['name']} ({user['email']})")


def demo_pagination_loop():
    """
    Paginate through all 100 posts, 10 per page, stopping on the first
    empty page. The page slices served here are exactly what the live API
    returns for ?_page=N&_limit=10.
    """
    def get_page(page, limit):
        """Offline equivalent of GET /posts?_page={page}&_limit={limit}."""
        start = (page - 1) * limit
        return SAMPLE_POSTS[start:start + limit]

    all_posts = []
    page = 1
    per_page = 10
    max_pages = 50  # safety limit so a misbehaving API cannot loop forever

    print("Fetching posts page by page:")
    while page <= max_pages:
        page_data = get_page(page, per_page)

        # Stop when we get an empty page
        if not page_data:
            break

        all_posts.extend(page_data)
        print(
            f"  Page {page}: {len(page_data)} posts "
            f"(total so far: {len(all_posts)})"
        )

        page += 1
        time.sleep(0.2)  # polite delay

    print(f"\nTotal posts collected: {len(all_posts)}")
    print(f"First post: {all_posts[0]['title'][:50]}...")
    print(f"Last post:  {all_posts[-1]['title'][:50]}...")


def demo_fetch_all_pages():
    """
    A reusable pagination function, applied to the comments endpoint
    (500 records in pages of 100). Mirrors the notebook's fetch_all_pages.
    """
    def get_page(page, limit):
        """Offline equivalent of GET /comments?_page={page}&_limit={limit}."""
        start = (page - 1) * limit
        return _FakeResponse(
            200,
            "OK",
            SAMPLE_COMMENTS[start:start + limit],
            f"https://jsonplaceholder.typicode.com/comments?_page={page}&_limit={limit}",
        )

    def fetch_all_pages(url, per_page=20, delay=0.2, max_pages=50):
        """Fetch all pages from a paginated API endpoint."""
        all_data = []

        for page in range(1, max_pages + 1):
            response = get_page(page, per_page)

            if response.status_code != 200:
                print(f"  Error on page {page}: status {response.status_code}")
                break

            page_data = response.json()
            if not page_data:
                break

            all_data.extend(page_data)
            time.sleep(delay)

        return all_data

    all_comments = fetch_all_pages(
        url="https://jsonplaceholder.typicode.com/comments",
        per_page=100,
        delay=0.2,
    )
    print(f"Fetched {len(all_comments)} comments")
    print(f"Unique post IDs: {len(set(c['postId'] for c in all_comments))}")


def demo_response_caching():
    """
    fetch_cached(): try the live API, cache the JSON on success, and fall
    back to the cached copy when a later request fails. The simulated
    transport succeeds on the first call and raises ConnectionError on the
    second, so the fallback path is exercised. The cache file is written
    under computations/_scratch/module15/ (deterministic relative path).
    """
    cache_dir = Path("computations") / "_scratch" / "module15"
    cache_dir.mkdir(parents=True, exist_ok=True)

    calls = {"n": 0}

    def sample_get(url, params=None):
        """Offline transport: first call succeeds, later calls fail."""
        calls["n"] += 1
        if calls["n"] > 1:
            raise requests.exceptions.ConnectionError("network unreachable")
        return _FakeResponse(200, "OK", SAMPLE_USERS, url)

    def fetch_cached(name, url, params=None):
        """Fetch JSON from a URL, caching the first success to disk."""
        cache_path = cache_dir / f"mis501_m15_{name}.json"
        try:
            response = sample_get(url, params=params)
            response.raise_for_status()
            data = response.json()
            with open(cache_path, "w") as f:
                json.dump(data, f)
            return data
        except requests.exceptions.RequestException as e:
            try:
                with open(cache_path) as f:
                    print(f"  Live fetch failed ({e}); using cached '{name}'")
                    return json.load(f)
            except FileNotFoundError:
                raise e

    users = fetch_cached("users", "https://jsonplaceholder.typicode.com/users")
    print(f"Fetched {len(users)} users (live)")

    users_again = fetch_cached("users", "https://jsonplaceholder.typicode.com/users")
    print(f"Fetched {len(users_again)} users (from cache fallback)")


# ---------------------------------------------------------------------------
# Section 15.4 — Building a Data Pipeline: API to Polars DataFrame
# ---------------------------------------------------------------------------

def _flatten_users(users_raw):
    """Flatten nested user JSON into simple dicts (pipeline step 2)."""
    user_records = []
    for u in users_raw:
        user_records.append({
            "id": u["id"],
            "name": u["name"],
            "username": u["username"],
            "email": u["email"],
            "phone": u["phone"],
            "city": u["address"]["city"],
            "zipcode": u["address"]["zipcode"],
            "lat": float(u["address"]["geo"]["lat"]),
            "lng": float(u["address"]["geo"]["lng"]),
            "company": u["company"]["name"],
            "company_bs": u["company"]["bs"],
        })
    return user_records


def demo_api_to_dataframe():
    """
    The fetch -> flatten -> load pattern: flatten the nested /users JSON
    into simple dicts, load users and posts into Polars DataFrames, and
    join posts to their authors.
    """
    # Step 1: Fetch all users (embedded sample = the /users response)
    users_raw = SAMPLE_USERS

    # Step 2: Flatten nested JSON into simple dicts
    user_records = _flatten_users(users_raw)

    # Step 3: Load into a Polars DataFrame
    users_df = pl.DataFrame(user_records)
    print(f"Users DataFrame: {users_df.shape[0]} rows, {users_df.shape[1]} columns")
    print(f"Columns: {users_df.columns}")
    print(users_df.select("id", "name", "city", "company").head(3))

    # Posts are already flat — no nested dicts
    posts_df = pl.DataFrame(SAMPLE_POSTS)
    print(f"\nPosts DataFrame: {posts_df.shape[0]} rows, {posts_df.shape[1]} columns")
    print(f"Columns: {posts_df.columns}")

    # Join posts with users to get the author name for each post
    posts_with_authors = posts_df.join(
        users_df.select("id", "name", "company", "city"),
        left_on="userId",
        right_on="id",
        how="left",
    ).rename({
        "name": "author",
    })

    print(f"\nJoined DataFrame: {posts_with_authors.shape}")
    print(
        posts_with_authors
        .sort("id")  # stable preview order
        .select("id", "author", "company", "title")
        .head(3)
    )


def demo_capstone_analysis():
    """
    Capstone pipeline: 'fetch' users, posts, and comments; build
    DataFrames; join into a unified dataset; and analyze engagement by
    user and company. Discussion volume (total comment characters per
    post) is the engagement measure, exactly as in the notebook.
    """
    # --- Step 1: Fetch data from three endpoints (embedded samples) ---
    capstone_data = {
        "users": SAMPLE_USERS,
        "posts": SAMPLE_POSTS,
        "comments": SAMPLE_COMMENTS,
    }
    for name in ["users", "posts", "comments"]:
        print(f"Fetched {name}: {len(capstone_data[name])} records")

    # --- Step 2: Build DataFrames ---
    cap_users = pl.DataFrame([
        {
            "user_id": u["id"],
            "name": u["name"],
            "username": u["username"],
            "email": u["email"],
            "city": u["address"]["city"],
            "company": u["company"]["name"],
        }
        for u in capstone_data["users"]
    ])

    cap_posts = pl.DataFrame(capstone_data["posts"]).rename({
        "id": "post_id",
    })

    cap_comments = pl.DataFrame(capstone_data["comments"]).rename({
        "id": "comment_id",
    }).with_columns(
        pl.col("body").str.len_chars().alias("comment_length"),
    )

    print("\nDataFrames created:")
    print(f"  Users:    {cap_users.shape}")
    print(f"  Posts:    {cap_posts.shape}")
    print(f"  Comments: {cap_comments.shape}")

    # --- Step 3: Join datasets ---
    engagement_per_post = (
        cap_comments
        .group_by("postId")
        .agg(
            pl.len().alias("comment_count"),
            pl.col("comment_length").sum().alias("discussion_volume"),
            pl.col("comment_length").mean().round(1).alias("avg_comment_length"),
        )
    )

    posts_enriched = cap_posts.join(
        engagement_per_post,
        left_on="post_id",
        right_on="postId",
        how="left",
    )

    capstone_df = posts_enriched.join(
        cap_users,
        left_on="userId",
        right_on="user_id",
        how="left",
    )

    print(
        f"\nCapstone DataFrame: {capstone_df.shape[0]} rows, "
        f"{capstone_df.shape[1]} columns"
    )

    # --- Step 4: Analysis ---
    user_summary = (
        capstone_df
        .group_by("name", "company", "city")
        .agg(
            pl.len().alias("post_count"),
            pl.col("discussion_volume").sum().alias("total_discussion"),
            pl.col("avg_comment_length").mean().round(1).alias("avg_comment_length"),
        )
        # Tie-break on name so equal totals still sort deterministically
        .sort(["total_discussion", "name"], descending=[True, False])
    )

    print("\nUser Engagement Summary:")
    print(user_summary.select("name", "post_count", "total_discussion", "avg_comment_length"))

    top_posts = (
        capstone_df
        .sort(["discussion_volume", "post_id"], descending=[True, False])
        .head(5)
        .select("name", "title", "comment_count", "discussion_volume")
    )

    print("\nTop 5 Posts by Discussion Volume:")
    print(top_posts)

    company_summary = (
        capstone_df
        .group_by("company")
        .agg(
            pl.len().alias("total_posts"),
            pl.col("discussion_volume").sum().alias("total_discussion"),
        )
        .sort(["total_discussion", "company"], descending=[True, False])
    )

    print("\nTop 3 Companies by Total Discussion:")
    print(company_summary.head(3))

    # --- Step 5: The numbers behind the dashboard charts ---
    print(
        f"\nSummary: {capstone_df.shape[0]} posts from "
        f"{capstone_df['name'].n_unique()} users across "
        f"{capstone_df['company'].n_unique()} companies | "
        f"Total comment characters: {capstone_df['discussion_volume'].sum():,} | "
        f"Avg discussion per post: {capstone_df['discussion_volume'].mean():.0f} chars"
    )


# ---------------------------------------------------------------------------
# Runner — demos in chapter order
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demos = [
        ("15.1", demo_first_api_request),
        ("15.1", demo_status_codes),
        ("15.2", demo_json_to_python),
        ("15.2", demo_nested_json_navigation),
        ("15.2", demo_query_parameters),
        ("15.2", demo_request_headers),
        ("15.3", demo_error_handling),
        ("15.3", demo_rate_limited_fetch),
        ("15.3", demo_pagination_loop),
        ("15.3", demo_fetch_all_pages),
        ("15.3", demo_response_caching),
        ("15.4", demo_api_to_dataframe),
        ("15.4", demo_capstone_analysis),
    ]

    for section, demo in demos:
        print("=" * 72)
        print(f"[{section}] {demo.__name__}")
        print("=" * 72)
        demo()
        print()

    print("=" * 72)
    print("All Module 15 demonstrations complete.")
    print("=" * 72)
