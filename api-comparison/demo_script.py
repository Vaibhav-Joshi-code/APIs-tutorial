import requests
import json

# ─── REST API DEMO ───────────────────────────────────────────
print("=" * 60)
print("REST API — We want only the user's name, but extra data will also come")
print("=" * 60)

# REST: Fetching a single user — notice ALL fields come back
rest_response = requests.get("http://localhost:5000/users/1")
data = rest_response.json()
print("REST Response (everything came — age, city too):")
print(json.dumps(data, indent=2))

# REST: Need posts? Make a SECOND separate request
print("\nFor posts, we had to make a separate request:")
posts_response = requests.get("http://localhost:5000/users/1/posts")
print(json.dumps(posts_response.json(), indent=2))

# ─── GraphQL DEMO ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("GraphQL — We asked only for name and post titles")
print("=" * 60)

# GraphQL: We define EXACTLY what we want in the query
graphql_query = """
{
  user(id: 1) {
    name
    posts {
      title
    }
  }
}
"""

# GraphQL always uses POST, query is sent in the request body
gql_response = requests.post(
    "http://localhost:5001/graphql",
    json={"query": graphql_query}
)
print("GraphQL Response (exactly what we asked for — nothing extra):")
print(json.dumps(gql_response.json(), indent=2))

# ─── FINAL SUMMARY ────────────────────────────────────────────
print("\n REST  → 2 requests needed + extra unwanted data came")
print("✅ GraphQL → 1 request + exactly what we asked for")