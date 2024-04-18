API Error Troubleshooting

You might encounter errors with accessing Genius API's server for searching lyrics:
403 Client Error: Forbidden for url: https://genius.com/api/search/multi?q=Corduroy+Dreams+Rex+Orange+County

This is because some IP addresses trigger Genius's strict captcha service, which is likely to block VPS and proxy users, or any IP address it deems suspicious. 
Most home WIFI networks should work, but if you are experiencing issues, try using a VPN. Some VPN servers are also flagged as suspicious, so try different servers until one works. 

More on the issue here: https://github.com/johnwmillr/LyricsGenius/discussions/191