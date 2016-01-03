--#!/user/bin/lua
-- HTTP GET request to server to check if current config is the latest
require "config"

local http = require("socket.http")

print(URL)

body, code, headers, status = http.request{
    url = "https://example.com",
    method = "GET"
}

