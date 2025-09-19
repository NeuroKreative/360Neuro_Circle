def format_posts(posts):
    return "\n".join([f"- {post['title']}: {post['body'][:200]}..." for post in posts])
