from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def sanitize_search_term(term):
    """
    Sanitize input to prevent XSS and SQL injection.
    Allows only alphanumerics, spaces, underscores, hyphens.
    """
    term = term.strip()
    if len(term) > 100:
        raise ValueError("Search term too long")

    # Block dangerous characters and patterns
    if re.search(r"[<>'\";=()]", term) or re.search(r"\b(SELECT|DROP|INSERT|DELETE|UPDATE|UNION|--|#)\b", term, re.IGNORECASE):
        raise ValueError("Potential SQL injection detected")

    if not re.match(r'^[\w\s-]*$', term):
        raise ValueError("Invalid characters in search term")

    return term

@app.route('/api/search')
def search():
    term = request.args.get('term', '')

    try:
        sanitized_term = sanitize_search_term(term).lower()
    except ValueError as e:
        return jsonify(error=str(e)), 400

    # Your static dataset
    items = ["Flask", "MySQL", "Gitea", "Docker", "Nginx", "Adminer"]

    # Filter items based on sanitized input
    filtered = [item for item in items if sanitized_term in item.lower()] if sanitized_term else items

    return jsonify(filtered)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
