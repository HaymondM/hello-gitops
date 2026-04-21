from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Hello World</title>
<style>
body {
    background: #32CD32;
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}
h1 {
    color: white;
    font-size: 4em;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>
"""
