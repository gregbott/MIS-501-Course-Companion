# Module 15: REST APIs & Data Acquisition

## Introduction

Module 14 showed you how to pull data out of web pages built for human eyes. This module covers the professional alternative: **REST APIs**, which are interfaces built specifically so that *programs* can request data. When a market-data vendor publishes stock prices, when your company's CRM exposes customer records, or when a government agency shares economic indicators, the delivery mechanism is almost always an API returning structured JSON. Knowing how to request, parse, and pipeline that data into a Polars DataFrame turns the entire connected world into a potential data source for your analyses — and it is the acquisition skill you are most likely to use in the capstone project and on the job.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Explain** what a REST API is and when to use an API instead of web scraping
2. **Make** GET requests with query parameters and headers using the `requests` library
3. **Parse** JSON responses and navigate nested data structures
4. **Handle** API errors, status codes, and rate limiting gracefully
5. **Paginate** through multi-page API responses to collect complete datasets
6. **Build** a complete data acquisition pipeline from API response to Polars DataFrame

---

## 15.1 What Is a REST API?

A **REST API** (Representational State Transfer Application Programming Interface) is a structured way for programs to request data from a server over the internet. Think of it as a **menu at a restaurant**: the menu lists what is available (endpoints), you place an order (request), and the kitchen sends back your meal (response).

REST is an architectural style built on a few key principles:

- **Client-server** — the client (your Python code) sends requests; the server processes them and returns responses
- **Stateless** — each request is independent; the server does not remember previous requests
- **Resource-based** — data is organized into resources (users, posts, orders) identified by URLs
- **Standard HTTP methods** — GET (read), POST (create), PUT (update), DELETE (remove)

For data acquisition, you will use **GET** requests almost exclusively — you are reading data, not creating or modifying it.

### API vs. Web Scraping

| Criterion | REST API | Web Scraping |
|-----------|----------|--------------|
| **Data format** | Structured JSON | Raw HTML |
| **Reliability** | Stable endpoints with versioning | Breaks when site redesigns |
| **Speed** | Fast — server sends only data | Slower — sends full HTML pages |
| **Permission** | Explicitly permitted | May violate Terms of Service |
| **Parsing** | `.json()` — done | BeautifulSoup — complex |
| **Authentication** | Often requires API key | Rarely needed |
| **When to use** | API is available | No API exists |

**Rule of thumb:** Always prefer an API when one is available. Use web scraping only as a last resort.

### The Request-Response Cycle

Every API interaction follows the same pattern:

1. **You build a request** — choose the endpoint URL, add query parameters, set headers
2. **You send the request** — `requests.get(url, params=..., headers=...)`
3. **The server processes it** — looks up the data, applies filters
4. **The server returns a response** — a JSON body plus a status code

```
Client (Python)                         Server (API)
──────────────                         ─────────────
GET /posts?userId=1        ──────►     Look up posts for user 1
                           ◄──────     200 OK + JSON body
```

**Key vocabulary:**

- **Endpoint** — the URL that identifies a resource (e.g., `https://jsonplaceholder.typicode.com/posts`)
- **Query parameters** — key-value pairs appended to the URL to filter or customize the response (`?userId=1&_limit=5`)
- **Headers** — metadata sent with the request (authentication tokens, content type, user agent)
- **Response body** — the JSON data returned by the server
- **Status code** — a number indicating success or failure (200, 404, etc.)

### Making Your First API Request

The course uses **JSONPlaceholder** (`jsonplaceholder.typicode.com`), a free public API designed for testing. It provides six resources with no authentication required:

| Endpoint | Resource | Records |
|----------|----------|---------|
| `/users` | User profiles | 10 |
| `/posts` | Blog posts | 100 |
| `/comments` | Post comments | 500 |
| `/todos` | To-do items | 200 |
| `/albums` | Photo albums | 100 |
| `/photos` | Album photos | 5000 |

The `requests.get()` call returns a **response object** that carries everything the server sent back: the status code, the response headers, and the body. Calling `.json()` on it parses the JSON body into ordinary Python lists and dictionaries.

!!! example "Worked Example: Your First API Request"

    ```python
    import requests

    # Make a GET request to fetch all users
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=10,
    )

    # Inspect the response object
    print(f"Status code:  {response.status_code}")
    print(f"Content type: {response.headers.get('Content-Type', 'unknown')}")
    print(f"Encoding:     {response.encoding}")
    print(f"Response size: {len(response.text)} characters")

    # Parse the JSON body — .json() returns a Python list of dictionaries
    users = response.json()

    print(f"\nType: {type(users)}")
    print(f"Number of users: {len(users)}")
    print(f"\nFirst user (keys): {list(users[0].keys())}")
    print("\nFirst user preview:")
    print(f"  id:       {users[0]['id']}")
    print(f"  name:     {users[0]['name']}")
    print(f"  username: {users[0]['username']}")
    print(f"  email:    {users[0]['email']}")
    print(f"  city:     {users[0]['address']['city']}")
    ```

    **Output:**

    ```
    Status code:  200
    Content type: application/json; charset=utf-8
    Encoding:     utf-8
    Response size: 5645 characters

    Type: <class 'list'>
    Number of users: 10

    First user (keys): ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']

    First user preview:
      id:       1
      name:     Leanne Graham
      username: Bret
      email:    Sincere@april.biz
      city:     Gwenborough
    ```

    **Interpretation:** One request delivered all ten user records as clean, structured data — no HTML parsing required. The status code 200 confirms success, and `.json()` hands you a familiar list of dictionaries that you already know how to navigate with the dictionary and JSON skills from earlier modules.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_first_api_request()`*

### Understanding HTTP Status Codes

Every HTTP response includes a numeric **status code** that tells you whether the request succeeded or failed — and why.

| Code | Name | Meaning |
|------|------|---------|
| **200** | OK | Request succeeded — data is in the response body |
| **201** | Created | A new resource was created (after a POST request) |
| **400** | Bad Request | Your request was malformed (wrong parameters) |
| **401** | Unauthorized | Authentication required — missing or invalid API key |
| **403** | Forbidden | You do not have permission for this resource |
| **404** | Not Found | The endpoint or resource does not exist |
| **429** | Too Many Requests | You hit the rate limit — slow down |
| **500** | Internal Server Error | Something broke on the server side |

**Quick rule:** Codes in the **200s** mean success. **400s** mean you made an error. **500s** mean the server has a problem. Always check the status code before parsing the response.

!!! example "Worked Example: Reading Status Codes"

    ```python
    # Successful request
    ok = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)
    print(f"Valid endpoint:   {ok.status_code} ({ok.reason})")

    # Non-existent resource (404)
    not_found = requests.get("https://jsonplaceholder.typicode.com/posts/9999", timeout=10)
    print(f"Invalid post ID:  {not_found.status_code} ({not_found.reason})")

    # Non-existent endpoint (404)
    bad_path = requests.get("https://jsonplaceholder.typicode.com/widgets", timeout=10)
    print(f"Invalid endpoint: {bad_path.status_code} ({bad_path.reason})")
    ```

    **Output:**

    ```
    Valid endpoint:   200 (OK)
    Invalid post ID:  404 (Not Found)
    Invalid endpoint: 404 (Not Found)
    ```

    **Interpretation:** Both a request for a post id that does not exist and a request for a completely wrong endpoint (`/widgets`) return 404. The server responded in every case — a 404 is a *successful conversation* with an unhappy answer, which is why your code must check the code rather than assume data arrived.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_status_codes()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "An API request downloads a web page, just like a browser." | A GET request to an API returns only structured JSON data — no HTML, styling, or images. That is why APIs are faster and easier to parse than scraped pages. |
| "If I got a response, the request worked." | The server can respond with an error status (404, 429, 500). A response object always comes back; check `response.status_code` before trusting the body. |
| "A 404 or 500 means my Python code has a bug." | 4xx codes signal a problem with the *request* (wrong URL, missing key); 5xx codes signal a problem on the *server*. Your Python ran fine — the server declined or failed. |
| "APIs work like JSONPlaceholder: no key, no limits." | JSONPlaceholder is a free practice API. Most production APIs require authentication and enforce rate limits. |
| "The server remembers my previous request." | REST is stateless. Every request must carry everything the server needs (parameters, authentication) — nothing is remembered between calls. |

---

## 15.2 JSON Responses, Query Parameters, and Headers

API responses come back as JSON. This section covers how JSON maps onto Python objects, how to navigate nested structures, and how to shape the *request* itself with query parameters and headers.

### From JSON to Python Objects

The `response.json()` method parses the JSON string into Python objects automatically:

| JSON | Python |
|------|--------|
| `{}` object | `dict` |
| `[]` array | `list` |
| `"text"` | `str` |
| `123` | `int` |
| `1.5` | `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

You navigate the result using standard dictionary and list indexing — the same skills from Modules 7 and 8.

!!! example "Worked Example: Parsing a Single Record"

    ```python
    # Fetch a single post — the response is a dictionary
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=10,
    )
    post = response.json()

    print(f"Type: {type(post)}")
    print(f"\nPost #{post['id']}:")
    print(f"  User ID: {post['userId']}")
    print(f"  Title:   {post['title'][:60]}...")
    print(f"  Body:    {post['body'][:80]}...")
    ```

    **Output:**

    ```
    Type: <class 'dict'>

    Post #1:
      User ID: 1
      Title:   sunt aut facere repellat provident occaecati excepturi optio...
      Body:    quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit ...
    ```

    **Interpretation:** Requesting a *collection* (`/posts`) returns a list, but requesting a *single resource* (`/posts/1`) returns one dictionary. Knowing which shape to expect determines whether you index with `post["title"]` or loop over records first.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_json_to_python()`*

### Navigating Nested JSON

Real API responses are rarely flat. A user record from JSONPlaceholder nests an `address` dictionary inside the user, a `geo` dictionary inside the address, and a `company` dictionary alongside — three levels deep. You reach inner values by chaining bracket lookups.

!!! example "Worked Example: Navigating Nested Structures"

    ```python
    # Fetch a user with nested data — address and company are dicts
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users/1",
        timeout=10,
    )
    user = response.json()

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
    ```

    **Output:**

    ```
    Name:    Leanne Graham
    Email:   Sincere@april.biz
    Phone:   1-770-736-8031 x56442

    Address:
      Street: Kulas Light
      City:   Gwenborough
      Zip:    92998-3874
      Lat/Lng: -37.3159, 81.1496

    Company: Romaguera-Crona
      Catch phrase: Multi-layered client-server neural-net
    ```

    **Interpretation:** Assigning intermediate levels to their own variables (`addr`, `geo`, `company`) keeps the lookups readable — the alternative, `user["address"]["geo"]["lat"]`, works but gets hard to scan. This navigation skill is the foundation of the *flattening* step in the data pipeline later in this module.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_nested_json_navigation()`*

!!! question "Try It Yourself: Exploring the Todos Endpoint"

    Fetch the list of todos from `https://jsonplaceholder.typicode.com/todos`. Then answer:

    1. How many todos are there in total?
    2. How many are marked as `completed: true`?
    3. What is the title of todo #42?

### Query Parameters

Query parameters let you **filter, sort, and limit** the data returned by an API — so you download only what you need instead of the entire dataset. Parameters are appended to the URL after a `?` and separated by `&`:

```
https://jsonplaceholder.typicode.com/posts?userId=1&_limit=5
```

With `requests`, you pass parameters as a dictionary to the `params` argument. This is cleaner and handles URL encoding automatically — spaces and special characters in values are escaped for you, and the library builds the final URL.

!!! example "Worked Example: Filtering with Query Parameters"

    ```python
    # Fetch posts by a specific user using query parameters
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        params={"userId": 1},
        timeout=10,
    )
    user_posts = response.json()

    print(f"Posts by user 1: {len(user_posts)}")
    print(f"\nActual URL sent: {response.url}")
    print("\nFirst 3 post titles:")
    for post in user_posts[:3]:
        print(f"  - [{post['id']}] {post['title'][:50]}...")

    # Filter comments down to a single post
    response = requests.get(
        "https://jsonplaceholder.typicode.com/comments",
        params={"postId": 1},
        timeout=10,
    )
    comments = response.json()

    print(f"\nComments on post 1: {len(comments)}")
    print(f"URL: {response.url}")
    print()
    for comment in comments[:3]:
        print(f"  From: {comment['email']}")
        print(f"  Body: {comment['body'][:60]}...")
        print()
    ```

    **Output:**

    ```
    Posts by user 1: 10

    Actual URL sent: https://jsonplaceholder.typicode.com/posts?userId=1

    First 3 post titles:
      - [1] sunt aut facere repellat provident occaecati excep...
      - [2] qui est esse...
      - [3] ea molestias quasi exercitationem repellat qui ips...

    Comments on post 1: 5
    URL: https://jsonplaceholder.typicode.com/comments?postId=1

      From: Eliseo@gardner.biz
      Body: laudantium enim quasi est quidem magnam voluptate ipsam eos ...

      From: Jayne_Kuhic@sydney.com
      Body: est natus enim nihil est dolore omnis voluptatem numquam et ...

      From: Nikita@garfield.biz
      Body: quia molestiae reprehenderit quasi aspernatur aut expedita o...
    ```

    **Interpretation:** The filter runs *on the server*: instead of downloading the full hundred-post catalog and discarding most of it, you receive only user 1's ten posts. On production APIs charging per record or per megabyte, server-side filtering saves both time and money.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_query_parameters()`*

### Headers and Authentication

**Headers** are key-value metadata sent with your request. Common uses:

- **Authentication** — sending an API key or token
- **Content type** — telling the server what format you expect
- **User agent** — identifying your application

Authentication patterns you will encounter:

| Pattern | Where the key goes | Example |
|---------|-------------------|---------|
| **API key in header** | `Authorization: Bearer <key>` | Most modern APIs |
| **API key in URL** | `?api_key=<key>` | Some older APIs |
| **Basic auth** | Username + password | Internal APIs |
| **No auth** | Nothing needed | Public APIs like JSONPlaceholder |

JSONPlaceholder requires no authentication, but `httpbin.org/headers` — a testing service that echoes back whatever you send — shows how headers travel with a request.

!!! example "Worked Example: Sending Custom Headers"

    ```python
    # httpbin.org/headers echoes back the headers you send
    headers = {
        "Authorization": "Bearer my-secret-token-12345",
        "Accept": "application/json",
        "User-Agent": "MIS501-CourseProject/1.0",
        "X-Custom-Header": "hello-from-python",
    }

    response = requests.get(
        "https://httpbin.org/headers",
        headers=headers,
        timeout=10,
    )

    echoed = response.json()
    print("Headers received by the server:")
    for key, value in echoed["headers"].items():
        print(f"  {key}: {value}")
    ```

    **Output:**

    ```
    Headers received by the server:
      Accept: application/json
      Authorization: Bearer my-secret-token-12345
      Host: httpbin.org
      User-Agent: MIS501-CourseProject/1.0
      X-Custom-Header: hello-from-python
    ```

    **Interpretation:** Every header you set arrived at the server, plus a `Host` header the HTTP layer adds automatically. This is exactly how an API key reaches a real provider — which is also why keys must be kept out of shared code and version control: anyone holding the header value holds your access.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_request_headers()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`response.json()` and `json.loads()` are unrelated tools." | They do the same job on different inputs: `.json()` parses a response *body*; `json.loads()` parses any JSON *string*. The result — Python dicts and lists — is identical. |
| "JSON's `null`, `true`, and `false` show up literally in Python." | Parsing converts them to `None`, `True`, and `False`. Test with `is None`, not `== "null"`. |
| "Build query strings by gluing text onto the URL." | Pass a dict to `params=`. Manual concatenation breaks on spaces and special characters; `requests` encodes them correctly and keeps the code readable. |
| "Chained lookups like `user['address']['geo']` are risky magic." | Each bracket is an ordinary dict lookup returning the next level. Assign intermediate levels to variables when chains get long. |
| "If a field might be missing, bracket indexing is still fine." | A missing key raises `KeyError` and stops the program. Use `.get("key", default)` when the API does not guarantee the field. |

---

## 15.3 Robust Data Acquisition: Errors, Rate Limits, and Pagination

Network requests can fail for many reasons: the server is down, your internet is out, the endpoint moved, or you hit a rate limit. A script that works once in a demo is not the same as a pipeline you can rerun every morning. This section covers the four habits that make acquisition code dependable: layered error handling, rate-limit etiquette, pagination, and caching.

### Two Layers of Error Handling

1. **Network errors** — use `try`/`except` to catch connection failures
2. **HTTP errors** — check `response.status_code` before parsing

The `response.raise_for_status()` method raises an exception if the status code indicates an error (4xx or 5xx), which lets you handle HTTP errors and network errors in the same `try`/`except` block. One ordering detail matters: catch `Timeout` *before* `ConnectionError`, because a connect-timeout exception is a subclass of both — the connection handler would otherwise swallow it and hide that the request actually timed out.

!!! example "Worked Example: Handling Errors Without Crashing"

    ```python
    # Pattern 1: check the status code manually
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/9999",
        timeout=10,
    )

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
            resp = requests.get(url, params=params, timeout=10)
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
    ```

    **Output:**

    ```
    Error 404: Resource not found
    Success: fetched user 'Leanne Graham'

    HTTP error: 404 Client Error: Not Found for url: https://jsonplaceholder.typicode.com/posts/99999
    Handled gracefully — no crash
    ```

    **Interpretation:** `fetch_json()` converts every failure mode — bad status, timeout, dead network — into a `None` return and a readable message, so a nightly pipeline logs the problem and moves on instead of crashing mid-run. Returning `None` also gives calling code a single, simple condition to test.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_error_handling()`*

!!! question "Try It Yourself: safe_fetch_user"

    Write a function called `safe_fetch_user(user_id)` that:

    1. Fetches a user from `https://jsonplaceholder.typicode.com/users/{user_id}`
    2. Returns a dictionary with keys `name`, `email`, and `city` if successful
    3. Returns `None` if the request fails or the user does not exist

    Test it with `user_id=3` (valid) and `user_id=999` (invalid).

### Rate Limiting

APIs limit how many requests you can make in a given time window to protect their servers. If you send requests too fast, the API returns a **429 Too Many Requests** status code.

Strategies for respecting rate limits:

1. **Add a delay** between requests with `time.sleep(seconds)`
2. **Check response headers** — many APIs include rate limit info: `X-RateLimit-Limit` (max requests allowed), `X-RateLimit-Remaining` (requests left in the window), `X-RateLimit-Reset` (when the window resets)
3. **Retry with backoff** — if you get a 429, wait and try again, doubling the wait each attempt

JSONPlaceholder advertises a generous budget of 1000 requests per window through those `X-RateLimit-*` headers, but many real APIs set much tighter limits. The pattern below is the one to follow everywhere.

!!! example "Worked Example: Polite Fetching with Retry and Backoff"

    ```python
    import time

    def fetch_with_rate_limit(url, params=None, delay=0.5, max_retries=3):
        """Fetch JSON with rate limiting and retry logic."""
        # range(max_retries + 1): one initial attempt plus max_retries retries
        for attempt in range(max_retries + 1):
            try:
                response = requests.get(url, params=params, timeout=10)

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
    ```

    **Output:**

    ```
    Fetching users with rate limiting:
      User 1: Leanne Graham (Sincere@april.biz)
      Rate limited (status 429). Waiting 0.3s (attempt 1/4)
      User 2: Ervin Howell (Shanna@melissa.tv)
      User 3: Clementine Bauch (Nathan@yesenia.net)
    ```

    **Interpretation:** The request for user 2 hit a 429, backed off briefly, retried, and succeeded — the caller never noticed. Exponential backoff doubles the wait on every rate-limited attempt, giving a congested server progressively more breathing room; hammering it with instant retries is the fastest way to get your key blocked.

    *Note: output produced from an embedded sample response that returns one simulated 429, so the retry path is exercised reproducibly offline.*

    *Source: `computations/module15_examples.py` — `demo_rate_limited_fetch()`*

### Pagination

Many APIs return data in **pages** rather than all at once. If an endpoint has 500 records but returns 100 per page, you need to make 5 requests to get everything.

| Pattern | How it works | Example parameters |
|---------|-------------|-------------------|
| **Page number** | Request page 1, 2, 3... | `?_page=1&_limit=10` |
| **Offset** | Skip N records, take M | `?_start=0&_limit=10` |
| **Cursor** | Server provides a "next" token | `?cursor=abc123` |

JSONPlaceholder supports page-based pagination with `_page` and `_limit` parameters. The loop below collects all 100 posts, 10 at a time, and stops at the first empty page.

!!! example "Worked Example: Paginating Through All Posts"

    ```python
    all_posts = []
    page = 1
    per_page = 10
    max_pages = 50  # safety limit so a misbehaving API cannot loop forever

    print("Fetching posts page by page:")
    while page <= max_pages:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts",
            params={
                "_page": page,
                "_limit": per_page,
            },
            timeout=10,
        )

        page_data = response.json()

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
    ```

    **Output:**

    ```
    Fetching posts page by page:
      Page 1: 10 posts (total so far: 10)
      Page 2: 10 posts (total so far: 20)
      Page 3: 10 posts (total so far: 30)
      Page 4: 10 posts (total so far: 40)
      Page 5: 10 posts (total so far: 50)
      Page 6: 10 posts (total so far: 60)
      Page 7: 10 posts (total so far: 70)
      Page 8: 10 posts (total so far: 80)
      Page 9: 10 posts (total so far: 90)
      Page 10: 10 posts (total so far: 100)

    Total posts collected: 100
    First post: sunt aut facere repellat provident occaecati excep...
    Last post:  optio molestias id quia eum...
    ```

    **Interpretation:** Ten requests assembled the complete 100-post dataset. The empty-page check is the natural stop condition, and `max_pages` is the seatbelt — if a buggy API kept returning data, the loop would still end rather than run (and bill) forever.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_pagination_loop()`*

### A Reusable Pagination Function

Since pagination logic is the same for every endpoint, it belongs in a function you can point at any URL.

!!! example "Worked Example: fetch_all_pages()"

    ```python
    def fetch_all_pages(url, per_page=20, delay=0.2, max_pages=50):
        """Fetch all pages from a paginated API endpoint."""
        all_data = []

        for page in range(1, max_pages + 1):
            response = requests.get(
                url,
                params={
                    "_page": page,
                    "_limit": per_page,
                },
                timeout=10,
            )

            if response.status_code != 200:
                print(f"  Error on page {page}: status {response.status_code}")
                break

            page_data = response.json()
            if not page_data:
                break

            all_data.extend(page_data)
            time.sleep(delay)

        return all_data

    # Fetch all comments (500 total) in pages of 100
    all_comments = fetch_all_pages(
        url="https://jsonplaceholder.typicode.com/comments",
        per_page=100,
        delay=0.2,
    )
    print(f"Fetched {len(all_comments)} comments")
    print(f"Unique post IDs: {len(set(c['postId'] for c in all_comments))}")
    ```

    **Output:**

    ```
    Fetched 500 comments
    Unique post IDs: 100
    ```

    **Interpretation:** Five requests of 100 records each collected the full comments dataset, and the quick uniqueness check confirms the comments span all 100 posts. Wrapping the loop in a function means the todos, posts, and albums endpoints are each one call away.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_fetch_all_pages()`*

!!! question "Try It Yourself: Paginating the Todos Endpoint"

    Use the `fetch_all_pages` function to fetch all 200 todos from `https://jsonplaceholder.typicode.com/todos` in pages of 50. Then calculate:

    1. Total number of todos fetched
    2. Number completed vs. not completed
    3. Which user has the most incomplete todos?

### Caching Responses for Reproducible Analysis

A pipeline that fetches live data every run is fragile: during a long analysis, a single dropped connection breaks every step downstream. A simple safeguard is to **cache** each response the first time it succeeds — try the live API, save the JSON to a local file, and fall back to that saved copy if a later request fails. This reuses the JSON file skills from Module 8, and it means a network hiccup degrades to yesterday's numbers instead of a crash.

!!! example "Worked Example: fetch_cached() with Fallback"

    ```python
    import json

    def fetch_cached(name, url, params=None):
        """Fetch JSON from a URL, caching the first success to disk."""
        cache_path = f"mis501_m15_{name}.json"
        try:
            response = requests.get(url, params=params, timeout=10)
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

    # First call: the network is up — fetch live and cache
    users = fetch_cached("users", "https://jsonplaceholder.typicode.com/users")
    print(f"Fetched {len(users)} users (live)")

    # Later call: the network is down — fall back to the cache
    users_again = fetch_cached("users", "https://jsonplaceholder.typicode.com/users")
    print(f"Fetched {len(users_again)} users (from cache fallback)")
    ```

    **Output:**

    ```
    Fetched 10 users (live)
      Live fetch failed (network unreachable); using cached 'users'
    Fetched 10 users (from cache fallback)
    ```

    **Interpretation:** The first call cached the response to disk; when the second call's network failed, the function quietly served the saved copy. For business reporting this is the difference between "the dashboard shows yesterday's data with a warning" and "the dashboard is blank."

    *Note: output produced from an embedded sample response with a simulated network failure on the second call, so both paths run reproducibly offline.*

    *Source: `computations/module15_examples.py` — `demo_response_caching()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`try`/`except` around `requests.get()` catches a 404." | A 404 is a *completed* request — no exception is raised unless you call `raise_for_status()`. Network exceptions and HTTP error codes are two separate failure layers. |
| "Omitting `timeout` is fine; requests gives up eventually." | `requests` has no default timeout. A hung server can hang your program indefinitely. Always pass `timeout=`. |
| "A 429 means the API has banned me." | 429 is temporary: you exceeded the request budget for the current window. Wait (ideally with backoff) and retry. Ignoring 429s repeatedly is what gets keys banned. |
| "One GET returns the whole dataset." | Many APIs cap each response at a page of records. Without a pagination loop you silently analyze only page 1. |
| "The pagination loop will always stop on its own." | It stops only when your stop condition fires. Guard with a `max_pages` limit so a misbehaving API cannot loop your script forever. |

---

## 15.4 Building a Data Pipeline: API to Polars DataFrame

The real power of API data acquisition comes when you load the data into a Polars DataFrame for analysis. The pattern is:

1. **Fetch** — call the API and collect JSON data
2. **Flatten** — extract the fields you need into a list of flat dicts
3. **Load** — pass the list of dicts to `pl.DataFrame()`
4. **Clean** — cast types, rename columns, handle nulls
5. **Analyze** — use Polars operations and visualize with Plotly Express

The flattening step is the one that trips people up: `pl.DataFrame()` expects a list of *simple* dictionaries, so nested structures like `address.geo.lat` must be pulled up to top-level keys first.

### From API Response to Polars DataFrame

!!! example "Worked Example: Fetch, Flatten, Load, Join"

    ```python
    import polars as pl

    # Step 1: Fetch all users (fetch_cached from the previous section)
    users_raw = fetch_cached(
        "users",
        "https://jsonplaceholder.typicode.com/users",
    )

    # Step 2: Flatten nested JSON into simple dicts
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

    # Step 3: Load into a Polars DataFrame
    users_df = pl.DataFrame(user_records)
    print(f"Users DataFrame: {users_df.shape[0]} rows, {users_df.shape[1]} columns")
    print(f"Columns: {users_df.columns}")
    print(users_df.select("id", "name", "city", "company").head(3))

    # Posts are already flat — no nested dicts
    posts_raw = fetch_cached(
        "posts",
        "https://jsonplaceholder.typicode.com/posts",
    )
    posts_df = pl.DataFrame(posts_raw)
    print(f"\nPosts DataFrame: {posts_df.shape[0]} rows, {posts_df.shape[1]} columns")
    print(f"Columns: {posts_df.columns}")

    # Step 4: Join posts with users to get the author for each post
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
    ```

    **Output:**

    ```
    Users DataFrame: 10 rows, 11 columns
    Columns: ['id', 'name', 'username', 'email', 'phone', 'city', 'zipcode', 'lat', 'lng', 'company', 'company_bs']
    shape: (3, 4)
    ┌─────┬──────────────────┬───────────────┬────────────────────┐
    │ id  ┆ name             ┆ city          ┆ company            │
    │ --- ┆ ---              ┆ ---           ┆ ---                │
    │ i64 ┆ str              ┆ str           ┆ str                │
    ╞═════╪══════════════════╪═══════════════╪════════════════════╡
    │ 1   ┆ Leanne Graham    ┆ Gwenborough   ┆ Romaguera-Crona    │
    │ 2   ┆ Ervin Howell     ┆ Wisokyburgh   ┆ Deckow-Crist       │
    │ 3   ┆ Clementine Bauch ┆ McKenziehaven ┆ Romaguera-Jacobson │
    └─────┴──────────────────┴───────────────┴────────────────────┘

    Posts DataFrame: 100 rows, 4 columns
    Columns: ['userId', 'id', 'title', 'body']

    Joined DataFrame: (100, 7)
    shape: (3, 4)
    ┌─────┬───────────────┬─────────────────┬─────────────────────────────────┐
    │ id  ┆ author        ┆ company         ┆ title                           │
    │ --- ┆ ---           ┆ ---             ┆ ---                             │
    │ i64 ┆ str           ┆ str             ┆ str                             │
    ╞═════╪═══════════════╪═════════════════╪═════════════════════════════════╡
    │ 1   ┆ Leanne Graham ┆ Romaguera-Crona ┆ sunt aut facere repellat provi… │
    │ 2   ┆ Leanne Graham ┆ Romaguera-Crona ┆ qui est esse                    │
    │ 3   ┆ Leanne Graham ┆ Romaguera-Crona ┆ ea molestias quasi exercitatio… │
    └─────┴───────────────┴─────────────────┴─────────────────────────────────┘
    ```

    **Interpretation:** Flattening turned three levels of nesting into an 11-column table, and one left join attached each post to its author's name and company — the same enrich-by-joining move you used with Polars in Module 10, now fed by an API instead of a CSV. Note `left_on="userId", right_on="id"`: join keys do not need matching names.

    *Note: output produced from an embedded sample response so results are reproducible offline.*

    *Source: `computations/module15_examples.py` — `demo_api_to_dataframe()`*

!!! question "Try It Yourself: Measuring Discussion Volume"

    Every post on JSONPlaceholder happens to have exactly five comments, so "the post with the most comments" is a hundred-way tie. A more informative engagement measure is **discussion volume** — the total length of all the comments a post receives. Build a pipeline that:

    1. Fetches all comments from `/comments`
    2. Loads them into a Polars DataFrame and adds a `comment_length` column
    3. Sums `comment_length` per post (`postId`) into a `discussion_volume`
    4. Finds the post that generated the most discussion

    Hint: add `pl.col("body").str.len_chars()` as `comment_length`, then `group_by("postId").agg(pl.col("comment_length").sum())`.

### Capstone: Multi-Endpoint Analysis

The capstone brings everything together in a complete data acquisition and analysis project: fetch three endpoints, build DataFrames from each, join them into a unified dataset, and analyze engagement.

**Business question:** *Whose content sparks the most discussion, and which individual posts attract the longest comment threads?*

Because every post on this API has exactly five comments, engagement is measured by **discussion volume** — the total length of the comments a post receives — rather than by a comment count that never varies.

!!! example "Worked Example: The Complete Capstone Pipeline"

    ```python
    # --- Step 1: Fetch data from three endpoints ---
    base_url = "https://jsonplaceholder.typicode.com"
    endpoints = {
        "users": "/users",
        "posts": "/posts",
        "comments": "/comments",
    }

    capstone_data = {}
    for name, path in endpoints.items():
        capstone_data[name] = fetch_cached(name, base_url + path)
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
    ```

    **Output:**

    ```
    Fetched users: 10 records
    Fetched posts: 100 records
    Fetched comments: 500 records

    DataFrames created:
      Users:    (10, 6)
      Posts:    (100, 4)
      Comments: (500, 6)

    Capstone DataFrame: 100 rows, 12 columns

    User Engagement Summary:
    shape: (10, 4)
    ┌──────────────────────────┬────────────┬──────────────────┬────────────────────┐
    │ name                     ┆ post_count ┆ total_discussion ┆ avg_comment_length │
    │ ---                      ┆ ---        ┆ ---              ┆ ---                │
    │ str                      ┆ u32        ┆ u32              ┆ f64                │
    ╞══════════════════════════╪════════════╪══════════════════╪════════════════════╡
    │ Nicholas Runolfsdottir V ┆ 10         ┆ 7926             ┆ 158.5              │
    │ Chelsey Dietrich         ┆ 10         ┆ 7918             ┆ 158.4              │
    │ Clementine Bauch         ┆ 10         ┆ 7916             ┆ 158.3              │
    │ Clementina DuBuque       ┆ 10         ┆ 7905             ┆ 158.1              │
    │ Leanne Graham            ┆ 10         ┆ 7905             ┆ 158.1              │
    │ Mrs. Dennis Schulist     ┆ 10         ┆ 7887             ┆ 157.7              │
    │ Patricia Lebsack         ┆ 10         ┆ 7839             ┆ 156.8              │
    │ Ervin Howell             ┆ 10         ┆ 7830             ┆ 156.6              │
    │ Kurtis Weissnat          ┆ 10         ┆ 7815             ┆ 156.3              │
    │ Glenna Reichert          ┆ 10         ┆ 7814             ┆ 156.3              │
    └──────────────────────────┴────────────┴──────────────────┴────────────────────┘

    Top 5 Posts by Discussion Volume:
    shape: (5, 4)
    ┌──────────────────┬─────────────────────────────────┬───────────────┬───────────────────┐
    │ name             ┆ title                           ┆ comment_count ┆ discussion_volume │
    │ ---              ┆ ---                             ┆ ---           ┆ ---               │
    │ str              ┆ str                             ┆ u32           ┆ u32               │
    ╞══════════════════╪═════════════════════════════════╪═══════════════╪═══════════════════╡
    │ Leanne Graham    ┆ dolorem dolore est ipsam        ┆ 5             ┆ 841               │
    │ Ervin Howell     ┆ magnam facilis autem            ┆ 5             ┆ 841               │
    │ Clementine Bauch ┆ dolorem eum magni eos aperiam … ┆ 5             ┆ 841               │
    │ Patricia Lebsack ┆ nesciunt quas odio              ┆ 5             ┆ 841               │
    │ Chelsey Dietrich ┆ eum et est occaecati            ┆ 5             ┆ 841               │
    └──────────────────┴─────────────────────────────────┴───────────────┴───────────────────┘

    Top 3 Companies by Total Discussion:
    shape: (3, 3)
    ┌────────────────────┬─────────────┬──────────────────┐
    │ company            ┆ total_posts ┆ total_discussion │
    │ ---                ┆ ---         ┆ ---              │
    │ str                ┆ u32         ┆ u32              │
    ╞════════════════════╪═════════════╪══════════════════╡
    │ Abernathy Group    ┆ 10          ┆ 7926             │
    │ Keebler LLC        ┆ 10          ┆ 7918             │
    │ Romaguera-Jacobson ┆ 10          ┆ 7916             │
    └────────────────────┴─────────────┴──────────────────┘

    Summary: 100 posts from 10 users across 10 companies | Total comment characters: 78,755 | Avg discussion per post: 788 chars
    ```

    **Interpretation:** Three API responses became one 100-row, 12-column analytical dataset, and two group-bys answered the business question: Nicholas Runolfsdottir V (Abernathy Group) leads total discussion at 7,926 characters, though the spread across users is narrow. Several posts tie at 841 characters of discussion, so the ranking breaks ties by post id — an explicit tie-break is what keeps a report reproducible run to run.

    *Note: output produced from an embedded sample response so results are reproducible offline; on the live API the engagement values differ, but the pipeline is identical.*

    *Source: `computations/module15_examples.py` — `demo_capstone_analysis()`*

### Visualizing the Results

The notebook finishes the capstone with a four-chart Plotly Express dashboard built from these summary tables. The pattern for each chart is the same: convert the Polars summary to pandas with `.to_pandas()`, then hand it to a `px` function. The user-engagement bar chart, for example:

```python
import plotly.express as px

user_fig = px.bar(
    user_summary.to_pandas(),
    x="name",
    y="total_discussion",
    color="company",
    title="Total Discussion Volume per User",
    labels={
        "total_discussion": "Total Discussion (chars)",
        "name": "User",
        "company": "Company",
    },
    text="total_discussion",
)
user_fig.update_traces(textposition="outside")
user_fig.update_layout(height=450, xaxis_tickangle=-45)
user_fig
```

The other three charts follow identically: average comment length per user (bar, colored by city), total engagement by company (bar), and the distribution of discussion volume across posts (`px.histogram` with `nbins=10`). The numbers each chart displays are exactly the values in the capstone output above.

!!! question "Try It Yourself: Capstone Challenge — Todos and Engagement"

    Extend the analysis by fetching the **todos** endpoint and answering:

    1. How many todos does each user have? How many are completed?
    2. Do users whose posts attract more discussion also complete more of their own todos?

    Join the todo summary with `user_summary` and create a scatter plot of `avg_comment_length` (engagement) vs. `completion_rate`. Both quantities vary across the ten users, so the relationship is well defined — unlike post count, which is exactly 10 for everyone.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`pl.DataFrame()` flattens nested JSON for me." | Nested dicts become awkward struct columns (or errors). Flatten each record into a simple dict — one level, plain values — before loading. |
| "Join columns must have the same name in both DataFrames." | `left_on=` / `right_on=` join `userId` to `id` directly. Renaming first is optional, not required. |
| "API data is analysis-ready as soon as it loads." | Expect cleaning: string dates need casting, numbers may arrive as strings (like `lat`/`lng` here), and left joins can introduce nulls. Step 4 of the pipeline exists for a reason. |
| "Group-by output comes back in a reliable order." | Group order is not guaranteed. Sort explicitly — and add a tie-break column — before reporting "top" anything. |
| "Charts need their own data fetch." | The chart is the last step of the same pipeline: the summary DataFrame you printed is the one you pass (via `.to_pandas()`) to Plotly Express. |

---

## Reflection Questions

1. Your team needs daily competitor pricing data. The competitor's website shows prices, and a commercial data vendor offers a priced API for the same information. What factors would you weigh in choosing between scraping the site and paying for the API?
2. REST APIs are stateless — the server remembers nothing between requests. What does that force *your* code to carry on every request, and why does statelessness make APIs easier to scale?
3. A colleague's script worked all week, then crashed Saturday night with an unhandled exception during a server outage. Which specific practices from §15.3 would have kept the pipeline alive, and what would "alive" mean for Monday's report?
4. An API returns 100 records per page and your query matches roughly 25,000 records. Sketch the pagination plan: how many requests, what stop condition, what politeness measures, and what safety limit?
5. Rate limits feel like an obstacle when you are collecting data. From the API provider's point of view, what are they protecting, and how does respecting them serve your own long-term interests?
6. The `fetch_cached()` pattern trades freshness for reliability. For which business analyses is a cached (possibly day-old) response acceptable, and for which would it be a serious problem?

---

## Your Assignment

The Module 15 assignment is worth **100 points plus a 10-point bonus**. You complete it in a **marimo notebook (`.py` file)** and submit the file to **Blackboard**. A final reflection section is not graded separately — it counts toward participation.

One design note: every task provides its API data **inline as JSON strings** (parsed with `json.loads()`), so you practice the parsing, navigation, error-handling, and pipeline skills without needing a network connection. In a real pipeline, `requests.get(...).json()` would hand you the same structures.

**Task 1 — Parse a Simple JSON Response (10 points).** A weather API's response for one city arrives as a JSON string. Parse it, extract the city, temperature, condition, and humidity fields, print them in a specified format, and store the city name in a named variable. Concepts: §15.2 (From JSON to Python Objects).

**Task 2 — Navigate Nested JSON Structures (15 points).** An e-commerce product record nests pricing, dimensions, and reviews (including a list of recent reviews) inside the product object. You build a flat dictionary by pulling eight values from several nesting levels — including the text of the first review in a list — and print each key-value pair. Concepts: §15.2 (Navigating Nested JSON), with the flattening mindset from §15.4.

**Task 3 — Filter Results Using Query Parameters (15 points).** A job-listings response contains multiple postings. You simulate server-side query parameters by filtering in Python on a boolean field and a salary threshold, keep a subset of fields, load the matches into a Polars DataFrame, and sort by salary. Concepts: §15.2 (Query Parameters) and §15.4 (loading records into Polars).

**Task 4 — Handle Error Codes and Missing Data (15 points).** A list of simulated flight-status responses mixes successful (200) responses with error responses (404, 429, 500), and some successful bodies omit fields. You loop over the responses, report and skip the errors, parse the successes using `.get()` defaults for missing fields, collect the results into a DataFrame, and print a processed/error summary. Concepts: §15.1 (status codes), §15.3 (error handling), §15.4 (building the DataFrame).

**Task 5 — Paginate Through Multi-Page API Responses (20 points).** A provided function simulates a paginated conference-events API whose responses include `page` and `total_pages` metadata. You write the pagination loop with a metadata-based stop condition, report progress per page, collect all events into a Polars DataFrame, and print the total collected. Concepts: §15.3 (Pagination), §15.4.

**Task 6 — Full Data Pipeline: Fetch, Flatten, Clean, Analyze, Visualize (25 points).** A financial API's JSON holds daily stock records with a nested prices object. Step 1: parse, flatten each record, build a DataFrame, and cast the date column to a proper date type. Step 2: compute a daily-return column, aggregate average return by sector, and present the result as a Plotly Express bar chart (converting with `.to_pandas()`). Concepts: §15.4 end to end, with the nested navigation of §15.2.

**Task 7 — Creative API Data Analysis, Bonus (10 points).** A city-transportation API provides bus-route records (type, district, time period, ridership, delays). You design your own analysis: load the data into Polars, clean or transform at least one column, perform at least one aggregation, build at least one Plotly Express chart, and explain your question and findings in a `mo.md()` cell. Concepts: §15.4.

Before submitting, confirm the notebook runs top to bottom without errors and that cell-scoped variables follow the underscore convention the instructions describe.

---

## Chapter Summary

A REST API is a structured, reliable way for programs to request data from a server: resources live at endpoint URLs, GET requests retrieve them, and responses return JSON plus a status code. When an API exists, prefer it over web scraping — the data arrives already structured, the interface is versioned and permitted, and `.json()` replaces an entire HTML-parsing step. Query parameters filter data on the server so you download only what you need, and headers carry metadata such as the authentication tokens most production APIs require.

Robust acquisition code treats failure as normal. Status codes distinguish success (200s) from client mistakes (400s) and server problems (500s); `raise_for_status()` plus layered `try`/`except` converts every failure into a handled path instead of a crash. Rate limiting with polite delays and exponential backoff keeps you within the provider's request budget, pagination loops (with a safety limit) assemble datasets that arrive one page at a time, and caching responses to disk makes long analyses survive network hiccups.

The destination of all this acquisition work is analysis. The pipeline pattern — fetch, flatten, load, clean, analyze — turns nested JSON into Polars DataFrames, joins records across endpoints exactly as you joined tables in Module 10, and feeds summary tables to Plotly Express. The capstone example combined users, posts, and comments into a single engagement analysis, which is precisely the shape of work your capstone project will demand: acquire real data, structure it, and answer a business question with it.

---

## What's Next

Module 16 begins your **Capstone Project: Proposal & Data Acquisition**. You will choose a real-world dataset — from a file, an API, or web scraping — define a research question worth answering, and build a project proposal with initial data exploration. Everything from this module applies directly: if your capstone data comes from an API, your proposal's acquisition section will be a `requests` pipeline with the error handling, pagination, and caching habits you just practiced.
