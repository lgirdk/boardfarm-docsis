<div id="top_nav">

[\|\|\|](# "Toggle sidebar")

# [Boardfarm Docsis documentation](# "Go to homepage")

<a href="#" id="mode_toggle" data-@click.prevent="handleClick" :title="mode"><img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB2aWV3Ym94PSIwIDAgNzkgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgc3R5bGU9ImZpbGwtcnVsZTpldmVub2RkO2NsaXAtcnVsZTpldmVub2RkO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2UtbWl0ZXJsaW1pdDoyOyI+PGcgaWQ9Im1vZGVfbGlnaHQiPjxyZWN0IGlkPSJCb3VuZHMiIHg9IjAiIHk9Ii0wIiB3aWR0aD0iNzguNjIzIiBoZWlnaHQ9Ijc5LjA0OSIgc3R5bGU9ImZpbGw6bm9uZTsiPjwvcmVjdD48Y2lyY2xlIGN4PSIzOS4zMTEiIGN5PSIzOS41MjQiIHI9IjE1LjczNCIgc3R5bGU9ImZpbGw6I2ZmZjsiPjwvY2lyY2xlPjxnIGlkPSJiZWFtcyI+PGcgaWQ9ImJlYW0iPjxwYXRoIGlkPSJiZWFtMSIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik00NC4yMTIsNC45MDFjMCwtMi43MDUgLTIuMTk2LC00LjkwMSAtNC45MDEsLTQuOTAxYy0yLjcwNCwtMCAtNC45LDIuMTk2IC00LjksNC45MDFsLTAsOS42MTRjLTAsMi43MDUgMi4xOTYsNC45MDEgNC45LDQuOTAxYzIuNzA1LDAgNC45MDEsLTIuMTk2IDQuOTAxLC00LjkwMWwwLC05LjYxNFoiIHN0eWxlPSJmaWxsOiNmZmY7Ij48L3BhdGg+PC9nPjxnIGlkPSJiZWFtMiIgc2VyaWY6aWQ9ImJlYW0iPjxwYXRoIGlkPSJiZWFtMyIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik02Ny40OCwxOC4wNzNjMS45MTMsLTEuOTEyIDEuOTEzLC01LjAxOCAwLC02LjkzMWMtMS45MTIsLTEuOTEyIC01LjAxOCwtMS45MTIgLTYuOTMxLDBsLTYuNzk4LDYuNzk5Yy0xLjkxMiwxLjkxMiAtMS45MTIsNS4wMTggMCw2LjkzMWMxLjkxMywxLjkxMiA1LjAxOCwxLjkxMiA2LjkzMSwtMGw2Ljc5OCwtNi43OTlaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTQiIHNlcmlmOmlkPSJiZWFtIj48cGF0aCBpZD0iYmVhbTUiIHNlcmlmOmlkPSJiZWFtIiBkPSJNMjUuNzI4LDYxLjEwOGMxLjkxMiwtMS45MTMgMS45MTIsLTUuMDE4IC0wLC02LjkzMWMtMS45MTMsLTEuOTEzIC01LjAxOSwtMS45MTMgLTYuOTMxLC0wbC02Ljc5OSw2Ljc5OGMtMS45MTIsMS45MTMgLTEuOTEyLDUuMDE5IDAsNi45MzFjMS45MTMsMS45MTMgNS4wMTksMS45MTMgNi45MzEsMGw2Ljc5OSwtNi43OThaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTYiIHNlcmlmOmlkPSJiZWFtIj48cGF0aCBpZD0iYmVhbTciIHNlcmlmOmlkPSJiZWFtIiBkPSJNNjAuNjgyLDU0LjE3N2MtMS45MTMsLTEuOTEzIC01LjAxOCwtMS45MTMgLTYuOTMxLC0wYy0xLjkxMiwxLjkxMyAtMS45MTIsNS4wMTggMCw2LjkzMWw2Ljc5OCw2Ljc5OGMxLjkxMywxLjkxMyA1LjAxOSwxLjkxMyA2LjkzMSwwYzEuOTEzLC0xLjkxMiAxLjkxMywtNS4wMTggMCwtNi45MzFsLTYuNzk4LC02Ljc5OFoiIHN0eWxlPSJmaWxsOiNmZmY7Ij48L3BhdGg+PC9nPjxnIGlkPSJiZWFtOCIgc2VyaWY6aWQ9ImJlYW0iPjxwYXRoIGlkPSJiZWFtOSIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik00LjkwMSwzNC42MjNjLTIuNzA1LDAgLTQuOTAxLDIuMTk2IC00LjkwMSw0LjkwMWMwLDIuNzA1IDIuMTk2LDQuOTAxIDQuOTAxLDQuOTAxbDkuNjE0LDBjMi43MDUsMCA0LjkwMSwtMi4xOTYgNC45MDEsLTQuOTAxYzAsLTIuNzA1IC0yLjE5NiwtNC45MDEgLTQuOTAxLC00LjkwMWwtOS42MTQsMFoiIHN0eWxlPSJmaWxsOiNmZmY7Ij48L3BhdGg+PC9nPjxnIGlkPSJiZWFtMTAiIHNlcmlmOmlkPSJiZWFtIj48cGF0aCBpZD0iYmVhbTExIiBzZXJpZjppZD0iYmVhbSIgZD0iTTQ0LjIxMiw2NC41MzRjMCwtMi43MDUgLTIuMTk2LC00LjkwMSAtNC45MDEsLTQuOTAxYy0yLjcwNCwtMCAtNC45LDIuMTk2IC00LjksNC45MDFsLTAsOS42MTRjLTAsMi43MDUgMi4xOTYsNC45MDEgNC45LDQuOTAxYzIuNzA1LC0wIDQuOTAxLC0yLjE5NiA0LjkwMSwtNC45MDFsMCwtOS42MTRaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTEyIiBzZXJpZjppZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW0xMyIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik0xOC45MjksMTEuMTQyYy0xLjkxMiwtMS45MTIgLTUuMDE4LC0xLjkxMiAtNi45MzEsMGMtMS45MTIsMS45MTMgLTEuOTEyLDUuMDE5IDAsNi45MzFsNi43OTksNi43OTljMS45MTIsMS45MTIgNS4wMTgsMS45MTIgNi45MzEsLTBjMS45MTIsLTEuOTEzIDEuOTEyLC01LjAxOSAtMCwtNi45MzFsLTYuNzk5LC02Ljc5OVoiIHN0eWxlPSJmaWxsOiNmZmY7Ij48L3BhdGg+PC9nPjxnIGlkPSJiZWFtMTQiIHNlcmlmOmlkPSJiZWFtIj48cGF0aCBpZD0iYmVhbTE1IiBzZXJpZjppZD0iYmVhbSIgZD0iTTY0LjEwOCwzNC42MjNjLTIuNzA1LDAgLTQuOTAxLDIuMTk2IC00LjkwMSw0LjkwMWMtMCwyLjcwNSAyLjE5Niw0LjkwMSA0LjkwMSw0LjkwMWw5LjYxNCwwYzIuNzA1LDAgNC45MDEsLTIuMTk2IDQuOTAxLC00LjkwMWMtMCwtMi43MDUgLTIuMTk2LC00LjkwMSAtNC45MDEsLTQuOTAxbC05LjYxNCwwWiIgc3R5bGU9ImZpbGw6I2ZmZjsiPjwvcGF0aD48L2c+PC9nPjwvZz48L3N2Zz4=" /> <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB2aWV3Ym94PSIwIDAgNzkgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgc3R5bGU9ImZpbGwtcnVsZTpldmVub2RkO2NsaXAtcnVsZTpldmVub2RkO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2UtbWl0ZXJsaW1pdDoyOyI+PGcgaWQ9Im1vZGVfZGFyayI+PHJlY3QgaWQ9IkJvdW5kcyIgeD0iMCIgeT0iLTAiIHdpZHRoPSI3OC42MjMiIGhlaWdodD0iNzkuMDQ5IiBzdHlsZT0iZmlsbDpub25lOyI+PC9yZWN0PjxjaXJjbGUgY3g9IjM5LjMxMSIgY3k9IjM5LjUyNCIgcj0iMTUuNzM0IiBzdHlsZT0iZmlsbDojZmZmOyI+PC9jaXJjbGU+PGcgaWQ9ImJlYW1zIj48ZyBpZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW0xIiBzZXJpZjppZD0iYmVhbSIgZD0iTTQ0LjIxMiwxNC41MTVjMCwtMi43MDUgLTIuMTk2LC00LjkwMSAtNC45MDEsLTQuOTAxYy0yLjcwNCwwIC00LjkwMSwyLjE5NiAtNC45MDEsNC45MDFjMCwyLjcwNSAyLjE5Nyw0LjkwMSA0LjkwMSw0LjkwMWMyLjcwNSwwIDQuOTAxLC0yLjE5NiA0LjkwMSwtNC45MDFaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTIiIHNlcmlmOmlkPSJiZWFtIj48cGF0aCBpZD0iYmVhbTMiIHNlcmlmOmlkPSJiZWFtIiBkPSJNNjAuNjYyLDI0Ljg5MmMxLjkwMiwtMS45MDIgMS45MDIsLTQuOTkgMCwtNi44OTJsLTAuMDQsLTAuMDM5Yy0xLjkwMSwtMS45MDIgLTQuOTg5LC0xLjkwMiAtNi44OTEsLTBjLTEuOTAxLDEuOTAxIC0xLjkwMSw0Ljk4OSAwLDYuODkxbDAuMDQsMC4wNGMxLjkwMiwxLjkwMSA0Ljk4OSwxLjkwMSA2Ljg5MSwtMFoiIHN0eWxlPSJmaWxsOiNmZmY7Ij48L3BhdGg+PC9nPjxnIGlkPSJiZWFtNCIgc2VyaWY6aWQ9ImJlYW0iPjxwYXRoIGlkPSJiZWFtNSIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik0yNS43MzIsNjEuMTAzYzEuOTEsLTEuOTEgMS45MSwtNS4wMTEgMCwtNi45MjFsLTAuMDA5LC0wLjAxYy0xLjkxLC0xLjkxIC01LjAxMiwtMS45MSAtNi45MjEsLTBjLTEuOTEsMS45MSAtMS45MSw1LjAxMSAtMCw2LjkyMWwwLjAxLDAuMDFjMS45MDksMS45MSA1LjAxMSwxLjkxIDYuOTIsLTBaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTYiIHNlcmlmOmlkPSJiZWFtIj48cGF0aCBpZD0iYmVhbTciIHNlcmlmOmlkPSJiZWFtIiBkPSJNNjAuNjcyLDU0LjE2N2MtMS45MDcsLTEuOTA3IC01LjAwNCwtMS45MDcgLTYuOTExLDBsLTAuMDIsMC4wMmMtMS45MDcsMS45MDcgLTEuOTA3LDUuMDA0IDAsNi45MTFjMS45MDcsMS45MDcgNS4wMDQsMS45MDcgNi45MTEsLTBsMC4wMiwtMC4wMmMxLjkwNywtMS45MDcgMS45MDcsLTUuMDA0IDAsLTYuOTExWiIgc3R5bGU9ImZpbGw6I2ZmZjsiPjwvcGF0aD48L2c+PGcgaWQ9ImJlYW04IiBzZXJpZjppZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW05IiBzZXJpZjppZD0iYmVhbSIgZD0iTTE0LjUyLDM0LjYyM2MtMi43MDIsMCAtNC44OTYsMi4xOTQgLTQuODk2LDQuODk2bDAsMC4wMWMwLDIuNzAyIDIuMTk0LDQuODk2IDQuODk2LDQuODk2YzIuNzAyLDAgNC44OTYsLTIuMTk0IDQuODk2LC00Ljg5NmwtMCwtMC4wMWMtMCwtMi43MDIgLTIuMTk0LC00Ljg5NiAtNC44OTYsLTQuODk2WiIgc3R5bGU9ImZpbGw6I2ZmZjsiPjwvcGF0aD48L2c+PGcgaWQ9ImJlYW0xMCIgc2VyaWY6aWQ9ImJlYW0iPjxwYXRoIGlkPSJiZWFtMTEiIHNlcmlmOmlkPSJiZWFtIiBkPSJNNDQuMjEyLDY0LjUzNGMwLC0yLjcwNSAtMi4xOTYsLTQuOTAxIC00LjkwMSwtNC45MDFjLTIuNzA0LC0wIC00LjkwMSwyLjE5NiAtNC45MDEsNC45MDFjMCwyLjcwNCAyLjE5Nyw0LjkgNC45MDEsNC45YzIuNzA1LDAgNC45MDEsLTIuMTk2IDQuOTAxLC00LjlaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTEyIiBzZXJpZjppZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW0xMyIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik0yNS43MywxNy45NDNjLTEuOTExLC0xLjkxMSAtNS4wMTUsLTEuOTExIC02LjkyNiwwbC0wLjAwNSwwLjAwNWMtMS45MTEsMS45MTEgLTEuOTExLDUuMDE1IDAsNi45MjZjMS45MTEsMS45MTEgNS4wMTUsMS45MTEgNi45MjYsMGwwLjAwNSwtMC4wMDVjMS45MTEsLTEuOTExIDEuOTExLC01LjAxNCAtMCwtNi45MjZaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTE0IiBzZXJpZjppZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW0xNSIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik02NC4wOTgsMzQuNjIzYy0yLjY5OSwwIC00Ljg5MSwyLjE5MiAtNC44OTEsNC44OTJsLTAsMC4wMTljLTAsMi42OTkgMi4xOTIsNC44OTEgNC44OTEsNC44OTFjMi43LDAgNC44OTIsLTIuMTkyIDQuODkyLC00Ljg5MWwwLC0wLjAxOWMwLC0yLjcgLTIuMTkyLC00Ljg5MiAtNC44OTIsLTQuODkyWiIgc3R5bGU9ImZpbGw6I2ZmZjsiPjwvcGF0aD48L2c+PC9nPjwvZz48L3N2Zz4=" /> <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB2aWV3Ym94PSIwIDAgNzkgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgc3R5bGU9ImZpbGwtcnVsZTpldmVub2RkO2NsaXAtcnVsZTpldmVub2RkO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2UtbWl0ZXJsaW1pdDoyOyI+PGcgaWQ9Im1vZGVfZGFya2VzdCI+PHJlY3QgaWQ9IkJvdW5kcyIgeD0iMCIgeT0iLTAiIHdpZHRoPSI3OC42MjMiIGhlaWdodD0iNzkuMDQ5IiBzdHlsZT0iZmlsbDpub25lOyI+PC9yZWN0PjxwYXRoIGQ9Ik0zOS4zMTUsMjMuNzkxYzguNjg0LC0wIDE1LjczNCw3LjA1IDE1LjczNCwxNS43MzNjMCw4LjY4NCAtNy4wNSwxNS43MzQgLTE1LjczNCwxNS43MzRjLTguNjgzLDAgLTE1LjczMywtNy4wNSAtMTUuNzMzLC0xNS43MzRjLTAsLTguNjgzIDcuMDUsLTE1LjczMyAxNS43MzMsLTE1LjczM1ptMCw0LjczN2M2LjA2OSwwIDEwLjk5Nyw0LjkyNyAxMC45OTcsMTAuOTk2Yy0wLDYuMDY5IC00LjkyOCwxMC45OTYgLTEwLjk5NywxMC45OTZjLTYuMDY4LDAgLTEwLjk5NiwtNC45MjcgLTEwLjk5NiwtMTAuOTk2YzAsLTYuMDY5IDQuOTI4LC0xMC45OTYgMTAuOTk2LC0xMC45OTZaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjxnIGlkPSJiZWFtcyI+PGcgaWQ9ImJlYW0iPjxwYXRoIGlkPSJiZWFtMSIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik00NC4yMTYsMTQuNTE1YzAsLTIuNzA1IC0yLjE5NiwtNC45MDEgLTQuOTAxLC00LjkwMWMtMi43MDQsMCAtNC45LDIuMTk2IC00LjksNC45MDFjLTAsMi43MDUgMi4xOTYsNC45MDEgNC45LDQuOTAxYzIuNzA1LDAgNC45MDEsLTIuMTk2IDQuOTAxLC00LjkwMVoiIHN0eWxlPSJmaWxsOiNmZmY7Ij48L3BhdGg+PC9nPjxnIGlkPSJiZWFtMiIgc2VyaWY6aWQ9ImJlYW0iPjxwYXRoIGlkPSJiZWFtMyIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik02MC42NjYsMjQuODkyYzEuOTAyLC0xLjkwMiAxLjkwMiwtNC45OSAwLC02Ljg5MmwtMC4wNCwtMC4wMzljLTEuOTAxLC0xLjkwMiAtNC45ODksLTEuOTAyIC02Ljg5MSwtMGMtMS45MDEsMS45MDEgLTEuOTAxLDQuOTg5IDAsNi44OTFsMC4wNCwwLjA0YzEuOTAyLDEuOTAxIDQuOTksMS45MDEgNi44OTEsLTBaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTQiIHNlcmlmOmlkPSJiZWFtIj48cGF0aCBpZD0iYmVhbTUiIHNlcmlmOmlkPSJiZWFtIiBkPSJNMjUuNzM3LDYxLjEwM2MxLjkwOSwtMS45MSAxLjkwOSwtNS4wMTEgLTAsLTYuOTIxbC0wLjAxLC0wLjAxYy0xLjkxLC0xLjkxIC01LjAxMSwtMS45MSAtNi45MjEsLTBjLTEuOTEsMS45MSAtMS45MSw1LjAxMSAtMCw2LjkyMWwwLjAxLDAuMDFjMS45MSwxLjkxIDUuMDExLDEuOTEgNi45MjEsLTBaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTYiIHNlcmlmOmlkPSJiZWFtIj48cGF0aCBpZD0iYmVhbTciIHNlcmlmOmlkPSJiZWFtIiBkPSJNNjAuNjc2LDU0LjE2N2MtMS45MDcsLTEuOTA3IC01LjAwNCwtMS45MDcgLTYuOTExLDBsLTAuMDIsMC4wMmMtMS45MDcsMS45MDcgLTEuOTA3LDUuMDA0IDAsNi45MTFjMS45MDcsMS45MDcgNS4wMDQsMS45MDcgNi45MTEsLTBsMC4wMiwtMC4wMmMxLjkwNywtMS45MDcgMS45MDcsLTUuMDA0IDAsLTYuOTExWiIgc3R5bGU9ImZpbGw6I2ZmZjsiPjwvcGF0aD48L2c+PGcgaWQ9ImJlYW04IiBzZXJpZjppZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW05IiBzZXJpZjppZD0iYmVhbSIgZD0iTTE0LjUyNCwzNC42MjNjLTIuNzAyLDAgLTQuODk2LDIuMTk0IC00Ljg5Niw0Ljg5NmwwLDAuMDFjMCwyLjcwMiAyLjE5NCw0Ljg5NiA0Ljg5Niw0Ljg5NmMyLjcwMiwwIDQuODk2LC0yLjE5NCA0Ljg5NiwtNC44OTZsMCwtMC4wMWMwLC0yLjcwMiAtMi4xOTQsLTQuODk2IC00Ljg5NiwtNC44OTZaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTEwIiBzZXJpZjppZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW0xMSIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik00NC4yMTYsNjQuNTM0YzAsLTIuNzA1IC0yLjE5NiwtNC45MDEgLTQuOTAxLC00LjkwMWMtMi43MDQsLTAgLTQuOSwyLjE5NiAtNC45LDQuOTAxYy0wLDIuNzA0IDIuMTk2LDQuOSA0LjksNC45YzIuNzA1LDAgNC45MDEsLTIuMTk2IDQuOTAxLC00LjlaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTEyIiBzZXJpZjppZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW0xMyIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik0yNS43MzQsMTcuOTQzYy0xLjkxMSwtMS45MTEgLTUuMDE1LC0xLjkxMSAtNi45MjYsMGwtMC4wMDUsMC4wMDVjLTEuOTExLDEuOTExIC0xLjkxMSw1LjAxNSAwLDYuOTI2YzEuOTExLDEuOTExIDUuMDE1LDEuOTExIDYuOTI2LDBsMC4wMDUsLTAuMDA1YzEuOTExLC0xLjkxMSAxLjkxMSwtNS4wMTQgMCwtNi45MjZaIiBzdHlsZT0iZmlsbDojZmZmOyI+PC9wYXRoPjwvZz48ZyBpZD0iYmVhbTE0IiBzZXJpZjppZD0iYmVhbSI+PHBhdGggaWQ9ImJlYW0xNSIgc2VyaWY6aWQ9ImJlYW0iIGQ9Ik02NC4xMDMsMzQuNjIzYy0yLjcsMCAtNC44OTIsMi4xOTIgLTQuODkyLDQuODkybC0wLDAuMDE5Yy0wLDIuNjk5IDIuMTkyLDQuODkxIDQuODkyLDQuODkxYzIuNjk5LDAgNC44OTEsLTIuMTkyIDQuODkxLC00Ljg5MWwwLC0wLjAxOWMwLC0yLjcgLTIuMTkyLC00Ljg5MiAtNC44OTEsLTQuODkyWiIgc3R5bGU9ImZpbGw6I2ZmZjsiPjwvcGF0aD48L2c+PC9nPjwvZz48L3N2Zz4=" /></a>

[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCA2NSA2NCIgZmlsbC1ydWxlPSJldmVub2RkIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBzdHJva2UtbWl0ZXJsaW1pdD0iMiI+CiAgICAgICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0xNC44NzMgNDAuMDA5Yy0yLjMxNS0zLjk0My0zLjY0Mi04LjUzMi0zLjY0Mi0xMy40MjlDMTEuMjMxIDExLjkxIDIzLjE0MSAwIDM3LjgxMSAwczI2LjU4IDExLjkxIDI2LjU4IDI2LjU4LTExLjkxIDI2LjU4LTI2LjU4IDI2LjU4YTI2LjQ0IDI2LjQ0IDAgMCAxLTE0LjI3Ny00LjE2MUw5LjczOSA2Mi43OTRhMy4xMiAzLjEyIDAgMCAxLTQuNDEzIDBMLjkxMyA1OC4zODJjLTEuMjE3LTEuMjE4LTEuMjE3LTMuMTk2IDAtNC40MTNsMTMuOTYtMTMuOTZ6TTM3LjgxMSA4LjA1NGMxMC4yMjUgMCAxOC41MjYgOC4zMDEgMTguNTI2IDE4LjUyNnMtOC4zMDEgMTguNTI2LTE4LjUyNiAxOC41MjYtMTguNTI2LTguMzAxLTE4LjUyNi0xOC41MjZTMjcuNTg2IDguMDU0IDM3LjgxMSA4LjA1NHoiIGZpbGw9IiNmZmYiPjwvcGF0aD4KICAgICAgICAgICAgICAgICAgICA8L3N2Zz4=)](search.html "Search")

<div class="searchbox_wrapper">

</div>

</div>

<div class="sphinxsidebar" role="navigation" aria-label="Main">

<div class="sphinxsidebarwrapper">

<span class="caption-text">Use Cases</span>

-   <a href="#document-connectivity" class="reference internal">Connectivity Use Cases</a>
-   <a href="#document-docsis" class="reference internal">Docsis Use Cases</a>
-   <a href="#document-erouter" class="reference internal">Erouter Use Cases</a>
-   <a href="#document-net_tools" class="reference internal">Net_tools Use Cases</a>
-   <a href="#document-snmp" class="reference internal">SNMP Use Cases</a>
-   <a href="#document-tr069" class="reference internal">TR069 Use Cases</a>

</div>

</div>

<div class="document">

<div class="documentwrapper">

<div class="bodywrapper">

<div class="body" role="main">

<div id="boardfarm3-docsis-suite-use-cases-documentation" class="section">

# Boardfarm3_docsis suite Use Cases documentation<a href="#boardfarm3-docsis-suite-use-cases-documentation" class="headerlink" title="Link to this heading">¶</a>

<div class="toctree-wrapper compound">

<span id="document-connectivity"></span>

<div id="connectivity-use-cases" class="section">

## Connectivity Use Cases<a href="#connectivity-use-cases" class="headerlink" title="Link to this heading">¶</a>

<div id="module-boardfarm3_docsis.use_cases.connectivity" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3_docsis<a href="#module-boardfarm3_docsis.use_cases.connectivity" class="headerlink" title="Link to this heading">¶</a>

Use Cases to handle getting the CPE online.

<span class="sig-name descname"><span class="pre">enable_tunnel_iface</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">aftr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">AFTR</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.enable_tunnel_iface" class="headerlink" title="Link to this definition">¶</a>
Enable tunnel iface by configuring AFTR post mode switch.

<div class="admonition hint">

Hint

This use case to be used:

-   When modem reprovisioning is done with ipv6 mode.

Note: not to be used if board is booted with ipv6 mode.

</div>

Parameters<span class="colon">:</span>
-   **aftr** (*AFTR*) – AFTR device instance

-   **board** (*CPE,* *optional*) – cpe device instance, defaults to None

-   **wan** (*WAN,* *optional*) – WAN client, defaults to None

<!-- -->

<span class="sig-name descname"><span class="pre">get_interface_mtu_size</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">LAN</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">WLAN</span></span>*, *<span class="n"><span class="pre">interface</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.get_interface_mtu_size" class="headerlink" title="Link to this definition">¶</a>
Return the MTU size of the interface in bytes.

Parameters<span class="colon">:</span>
-   **device** (*CPE* *\|* *LAN* *\|* *WAN* *\|* *WLAN*) – device instance

-   **interface** (*str*) – name of the interface

Returns<span class="colon">:</span>
MTU size of the interface in bytes

Return type<span class="colon">:</span>
int

<!-- -->

<span class="sig-name descname"><span class="pre">get_interface_status</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">LAN</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">interface</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPEInterfaces</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">HostInterfaces</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.get_interface_status" class="headerlink" title="Link to this definition">¶</a>
Return the status of the Linux interface.

If the interface link is up or down on the device.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Check that the \[\] interface is up

</div>

Parameters<span class="colon">:</span>
-   **device** (*LAN* *\|* *WAN* *\|* *CPE*) – device class object

-   **interface** (*CPEInterfaces* *\|* *HostInterfaces* *\|* *PONCPEInterface*) – enum for possible values for interfaces definition

Raises<span class="colon">:</span>
**UseCaseFailure** – when device doesn’t have attribute mapped in enum

Returns<span class="colon">:</span>
True if interface is up else False

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="sig-name descname"><span class="pre">get_subnet_mask</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">LAN</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">WLAN</span></span>*, *<span class="n"><span class="pre">interface</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.get_subnet_mask" class="headerlink" title="Link to this definition">¶</a>
Get the subnet mask of the interface.

Parameters<span class="colon">:</span>
-   **device** (*LAN* *\|* *WAN* *\|* *WLAN*) – device instance

-   **interface** (*str*) – name of the inerface

Returns<span class="colon">:</span>
subnet mask of the interface

Return type<span class="colon">:</span>
str

<!-- -->

<span class="sig-name descname"><span class="pre">has_ipv6_tunnel_interface_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.has_ipv6_tunnel_interface_address" class="headerlink" title="Link to this definition">¶</a>
Check for the tunnel interface on DUT console.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Check for the tunnel interface on DUT console.

</div>

Parameters<span class="colon">:</span>
**board** (*CPE* *\|* *None,* *optional*) – the board object, defaults to None

Returns<span class="colon">:</span>
True if tunnel interface is present else False

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="sig-name descname"><span class="pre">is_board_online_after_reset</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.is_board_online_after_reset" class="headerlink" title="Link to this definition">¶</a>
Check board online after reset.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Verify CPE comes online after the factory reset

-   Verify DUT comes back online

</div>

Returns<span class="colon">:</span>
True if board is online else false

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="sig-name descname"><span class="pre">is_wan_accessible_on_client</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">who_access</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">LAN</span></span>*, *<span class="n"><span class="pre">port</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">is_ipv6</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.is_wan_accessible_on_client" class="headerlink" title="Link to this definition">¶</a>
Ping the WAN IP address max with 2 retries from the lan/wifi client.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Check that the connected LAN client is able to access the internet

-   Verify LAN Client is able to reach the internet

</div>

Parameters<span class="colon">:</span>
-   **who_access** (*LAN*) – name of the client who wants to ping wan side

-   **port** (*int*) – port to which to perform the curl on wan client

-   **is_ipv6** (*bool*) – whether to ping ipv4 or ipv6 address for wan

-   **wan** (*WAN* *\|* *None*) – WAN client to be pinged

Returns<span class="colon">:</span>
True if ping returns a success

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="sig-name descname"><span class="pre">power_cycle</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.power_cycle" class="headerlink" title="Link to this definition">¶</a>
Power cycle the board.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Perform a reboot on the CPE

-   Reboot the DUT

-   Do power cycle of DUT

</div>

Turn OFF and turn ON the board and wait for the boot to start This method is preferred to wait_for_board_boot_start as the power cycle and wait for the board boot is handled in this use case

Parameters<span class="colon">:</span>
**board** (*CPE* *\|* *None,* *optional*) – the board object, defaults to None

<!-- -->

<span class="sig-name descname"><span class="pre">reset_board_via_cmts</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.reset_board_via_cmts" class="headerlink" title="Link to this definition">¶</a>
Reset the board via CMTS.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Reset the board via CMTS.

</div>

Parameters<span class="colon">:</span>
-   **board** (*CPE*) – cpe device instance

-   **cmts** (*CMTS*) – cmts device instance

<!-- -->

<span class="sig-name descname"><span class="pre">wait_for_board_boot_start</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.connectivity.wait_for_board_boot_start" class="headerlink" title="Link to this definition">¶</a>
Wait for the board boot to start.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Verify that DUT comes online.

</div>

The usage if this directly in the test would be depecrated in favour of power_cycle() as it would handle both board turn OFF and ON and wait for board boot to start

Parameters<span class="colon">:</span>
**board** (*CPE* *\|* *None,* *optional*) – the board object, defaults to None

</div>

</div>

<span id="document-docsis"></span>

<div id="docsis-use-cases" class="section">

## Docsis Use Cases<a href="#docsis-use-cases" class="headerlink" title="Link to this heading">¶</a>

<div id="module-boardfarm3_docsis.use_cases.docsis" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3_docsis<a href="#module-boardfarm3_docsis.use_cases.docsis" class="headerlink" title="Link to this heading">¶</a>

Use Cases to interact with DOCSIS devices such as CMTS and CM.

<span class="sig-name descname"><span class="pre">add_tlvs_to_bootfile</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">multiline_tlv</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">config_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.add_tlvs_to_bootfile" class="headerlink" title="Link to this definition">¶</a>
Add TLVs to the boot file in the env_hepler.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Add TLVs to the boot file in the env_hepler.

</div>

Adds/appends TLVs (as multiline string) at the end of the boot file, just before
the CmMic comment line

Parameters<span class="colon">:</span>
-   **multiline_tlv** (*str*) – a string with embedded newlines with the TLVs to be added

-   **config_file** (*str* *\|* *None*) – updated config file

-   **board** (*CableModem*) – Cable Modem device instance

Raises<span class="colon">:</span>
**ValueError** – if the string hook was not found in the bootfile

Returns<span class="colon">:</span>
a copy of the env_helper bootfile with the TLVs added

Return type<span class="colon">:</span>
str

<!-- -->

<span class="sig-name descname"><span class="pre">are_boot_logs_successful</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.are_boot_logs_successful" class="headerlink" title="Link to this definition">¶</a>
Collect the boot logs and validate the boot stages and provisioning.

Parameters<span class="colon">:</span>
-   **timeout** (*int*) – time value to collect the logs for

-   **board** (*CableModem*) – Cable Modem device instance

Returns<span class="colon">:</span>
True if boot stages are verified and provisioning is successful else False

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="sig-name descname"><span class="pre">get_cable_modem_channels</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.get_cable_modem_channels" class="headerlink" title="Link to this definition">¶</a>
Get the CM channel values from the CMTS.

<div class="highlight-python notranslate">

<div class="highlight">

    # example output
    {
        "US": "1(2,3,4,5,6,7,8)",
        "DS": "9(1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)",
    }

</div>

</div>

Parameters<span class="colon">:</span>
-   **board** (*CableModem*) – Cable Modem device instance

-   **cmts** (*CMTS*) – CMTS device instance

Returns<span class="colon">:</span>
Cable Modem channel values

Return type<span class="colon">:</span>
dict\[str, str\]

<!-- -->

<span class="sig-name descname"><span class="pre">get_downstream_bonded_channel</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.get_downstream_bonded_channel" class="headerlink" title="Link to this definition">¶</a>
Get the Downstream bonded channel value from the CMTS.

<div class="highlight-python notranslate">

<div class="highlight">

    # example output
    "9"

</div>

</div>

Parameters<span class="colon">:</span>
-   **board** (*CableModem*) – Cable Modem device instance

-   **cmts** (*CMTS*) – CMTS device instance

Returns<span class="colon">:</span>
Downstream bonded channel value

Return type<span class="colon">:</span>
str

<!-- -->

<span class="sig-name descname"><span class="pre">get_ds_frequecy_list</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.get_ds_frequecy_list" class="headerlink" title="Link to this definition">¶</a>
Return the frequency list of CableModem.

Get the Downstream frequency list from the CableModem device.

<div class="highlight-python notranslate">

<div class="highlight">

    # example output:
    [
        "137000000",
        "242000000",
        "274000000",
        "300000000",
        "305000000",
        "306750000",
        "330250000",
        "330750000",
        "331000000",
        "370750000",
        "338000000",
        "338750000",
        "339000000",
        "402000000",
        "402750000",
        "410000000",
        "418000000",
        "426000000",
        "434000000",
        "442000000",
        "450000000",
        "458000000",
        "466000000",
        "474000000",
        "482000000",
        "490000000",
        "498000000",
        "578000000",
        "586750000",
        "594000000",
        "618000000",
        "634000000",
        "666000000",
        "730000000",
        "754000000",
        "778000000",
        "786000000",
        "810000000",
        "826000000",
        "842000000",
    ]

</div>

</div>

Parameters<span class="colon">:</span>
**board** (*CableModem*) – CableModem device instance

Returns<span class="colon">:</span>
frequency list of CPE

Return type<span class="colon">:</span>
list\[str\]

<!-- -->

<span class="sig-name descname"><span class="pre">get_upstream_bonded_channel</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.get_upstream_bonded_channel" class="headerlink" title="Link to this definition">¶</a>
Get the upstream bonded channel value from the CMTS.

<div class="highlight-python notranslate">

<div class="highlight">

    # example output
    "8"

</div>

</div>

Parameters<span class="colon">:</span>
-   **board** (*CableModem*) – Cable Modem device instance

-   **cmts** (*CMTS*) – CMTS device instance

Returns<span class="colon">:</span>
Upstream bonded channel value

Return type<span class="colon">:</span>
str

<!-- -->

<span class="sig-name descname"><span class="pre">get_vendor_id_from_cm_bootfile</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.get_vendor_id_from_cm_bootfile" class="headerlink" title="Link to this definition">¶</a>
Fetch the vendor identifier hexadecimal value from CM bootfile.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Fetch the vendor identifier hexadecimal value from CM bootfile.

</div>

Parameters<span class="colon">:</span>
**board** (*CableModem*) – Cable Modem device instance

Returns<span class="colon">:</span>
hexadecimal value of vendor identifier

Return type<span class="colon">:</span>
str

<!-- -->

<span class="sig-name descname"><span class="pre">is_bpi_privacy_disabled</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.is_bpi_privacy_disabled" class="headerlink" title="Link to this definition">¶</a>
Fetch the GlobalPrivacy TLV value in CM config file.

Return True if GlobalPrivacyEnable inside config file is set to Integer 0. By default, BPI privacy is enabled in CM config file.

This use case will be used for scenarios where BPI+ encyption is not used. i.e. Multicast

Parameters<span class="colon">:</span>
**board** (*CableModem*) – CableModem device instance, defaults to None

Raises<span class="colon">:</span>
-   **ValueError** – when the board object is None

-   **ValueError** – when the bootfile is an empty string

Returns<span class="colon">:</span>
True if BPI is disabled.

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="sig-name descname"><span class="pre">is_route_present_on_cmts</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">route</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">IPv4Network</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">IPv6Network</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.is_route_present_on_cmts" class="headerlink" title="Link to this definition">¶</a>
Check if routing table of CMTS router contains a route.

Perfrom `ip route` command on a router, collect the routes and check if route is present in table output.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Verify that the CMTS learns route

-   Make sure that the packets can be captured between CPE and CMTS

</div>

<div class="highlight-python notranslate">

<div class="highlight">

    # example usage
    status = is_route_present_on_cmts(
        route=ipaddress.ip_network("192.168.101.0/24"),
    )

</div>

</div>

Parameters<span class="colon">:</span>
-   **route** (*IPv4Network* *\|* *IPv6Network*) – route to be looked up on CMTS

-   **cmts** (*CMTS*) – CMTS to be used

Returns<span class="colon">:</span>
True if route is present on CMTS

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="sig-name descname"><span class="pre">override_boot_files</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">cm_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">mta_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.override_boot_files" class="headerlink" title="Link to this definition">¶</a>
Configure the boot file.

This method implements what in Boardfarm v2 was configure_boot_file(), but does not update the objects’ configuration anymore. In Boardfarm v2, the CPE object needed update before a call to the provisioning Use Cases was made. As such, it is deprecated in favour of passing the files explicitly to the appropriate Use Case.

In Boardfarm v3 the user should choose between provision_docsis_board() and provision_docsis_board_and_reboot_it()

Parameters<span class="colon">:</span>
-   **board** (*CableModem*) – the Cable Modem to be provisioned

-   **cm_boot_file** (*str* *\|* *None,* *optional*) – Cable Modem config, defaults to None

-   **mta_boot_file** (*str* *\|* *None,* *optional*) – eMTA config, defaults to None

Returns<span class="colon">:</span>
the two configuration files in string format

Return type<span class="colon">:</span>
tuple\[str, str\]

<!-- -->

<span class="sig-name descname"><span class="pre">provision_board_w\_boot_files</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">provisioner</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Provisioner</span></span>*, *<span class="n"><span class="pre">tftp</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cm_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">mta_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.provision_board_w_boot_files" class="headerlink" title="Link to this definition">¶</a>
Provision Cable Modem with given boot files.

This Use Case is deprecated in favour of provision_docsis_board_and_reboot_it(). Said Use Case forces us to be more explicit.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Initialize DUT using boot file with below parameters

</div>

Parameters<span class="colon">:</span>
-   **board** (*CableModem*) – the Cable Modem to be provisioned

-   **provisioner** (*Provisioner*) – the Provisioner

-   **tftp** (*WAN*) – the TFTP device

-   **cm_boot_file** – Cable Modem boot file, defaults to None

-   **cm_boot_file** – str \| None

-   **mta_boot_file** – MTA boot file, defaults to None

-   **mta_boot_file** – str \| None

<!-- -->

<span class="sig-name descname"><span class="pre">provision_cable_modem</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">provisioner</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Provisioner</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cm_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">emta_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.provision_cable_modem" class="headerlink" title="Link to this definition">¶</a>
Provision the Cable Modem.

With this function, the CM and eMTA boot files can be None. This function is deprecated; prefer to use provision_docsis_board() instead. That ensures that we are explicit, rather than implicit.

Parameters<span class="colon">:</span>
-   **board** (*CableModem*) – the CM to be provisioned

-   **provisioner** (*Provisioner*) – the Provisioner

-   **wan** (*WAN*) – the TFTP device

-   **cm_boot_file** (*str* *\|* *None*) – content of the CM boot file, defaults to None

-   **emta_boot_file** (*str* *\|* *None*) – content of the eMTA boot file, defaults to None

<!-- -->

<span class="sig-name descname"><span class="pre">provision_docsis_board</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">provisioner</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Provisioner</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cm_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">emta_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.provision_docsis_board" class="headerlink" title="Link to this definition">¶</a>
Provision the Cable Modem with the given CM and eMTA boot files.

Parameters<span class="colon">:</span>
-   **board** (*CableModem*) – the Cable Modem to be provisioned

-   **provisioner** (*Provisioner*) – DOCSIS provisioner

-   **wan** (*WAN*) – TFTP server

-   **cm_boot_file** (*str*) – Cable Modem config

-   **emta_boot_file** (*str*) – eMTA config

<!-- -->

<span class="sig-name descname"><span class="pre">provision_docsis_board_and_reboot_it</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">provisioner</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Provisioner</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cm_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">emta_boot_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.provision_docsis_board_and_reboot_it" class="headerlink" title="Link to this definition">¶</a>
Provision the Cable Modem with the given bootfiles and reboot it.

This Use Case performs a CPE-triggered software reboot.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Initialize DUT using boot file with below parameters

</div>

Parameters<span class="colon">:</span>
-   **board** (*CableModem*) – the Cable Modem to be provisioned

-   **provisioner** (*Provisioner*) – DOCSIS provisioner

-   **wan** (*WAN*) – TFTP server

-   **cm_boot_file** (*str*) – Cable Modem config

-   **emta_boot_file** (*str*) – eMTA config

<!-- -->

<span class="sig-name descname"><span class="pre">update_erouter_mode</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">bootfile</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a href="#boardfarm3_docsis.use_cases.docsis.update_erouter_mode" class="headerlink" title="Link to this definition">¶</a>
Switch the bootfile eRouter config in the env_helper to given mode.

If the mode has to be switched multiple times then the bootfile param to be used. bootfile param should be the current eRouter config and not the one in env_helper.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Switch to modem mode using config file

-   Switch the provisioning mode via config file

-   Switch back to IPv4 provisioning mode using config file

</div>

Parameters<span class="colon">:</span>
-   **mode** (*str*) – one of “none”, “disabled”, “ipv4”, “ipv6”, “dual”

-   **board** (*CableModem*) – Cable Modem device instance

-   **bootfile** (*str*) – config file to be used before updating mode

Raises<span class="colon">:</span>
**ValueError** – if mode is not valid

Returns<span class="colon">:</span>
a copy of the env_helper bootfile with the new mode

Return type<span class="colon">:</span>
str

</div>

</div>

<span id="document-erouter"></span>

<div id="erouter-use-cases" class="section">

## Erouter Use Cases<a href="#erouter-use-cases" class="headerlink" title="Link to this heading">¶</a>

<div id="module-boardfarm3_docsis.use_cases.erouter" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3_docsis<a href="#module-boardfarm3_docsis.use_cases.erouter" class="headerlink" title="Link to this heading">¶</a>

eRouter use cases.

<span class="sig-name descname"><span class="pre">get_board_guest_ip_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span><a href="#boardfarm3_docsis.use_cases.erouter.get_board_guest_ip_address" class="headerlink" title="Link to this definition">¶</a>
Get the board’s Guest IP addresses.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Verify that the guest interface acquires an IPv4/IPv6 address.

</div>

Parameters<span class="colon">:</span>
-   **board** (*CPE*) – instance of CPE

-   **retry_count** (*int*) – number of retries

Returns<span class="colon">:</span>
IPAddress of guest interface

Return type<span class="colon">:</span>
IPAddresses

<!-- -->

<span class="sig-name descname"><span class="pre">get_board_lan_ip_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span><a href="#boardfarm3_docsis.use_cases.erouter.get_board_lan_ip_address" class="headerlink" title="Link to this definition">¶</a>
Get the board’s LAN IP addresses.

Parameters<span class="colon">:</span>
-   **board** (*CPE*) – instance of CPE

-   **retry_count** (*int*) – number of retries

Returns<span class="colon">:</span>
IPAddress of LAN interface

Return type<span class="colon">:</span>
IPAddresses

<!-- -->

<span class="sig-name descname"><span class="pre">get_erouter_addresses</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">retry_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span><a href="#boardfarm3_docsis.use_cases.erouter.get_erouter_addresses" class="headerlink" title="Link to this definition">¶</a>
Get erouter IPv4, IPv6 addresses.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Check if eRouter gets an IP address.

-   Check if the eRouter WAN Interface acquires IPv4 and IPv6 address

</div>

Parameters<span class="colon">:</span>
-   **retry_count** (*int*) – number of retries to get IPs

-   **board** (*CPE*) – CPE device instance

Returns<span class="colon">:</span>
erouter IP addresses data class

Return type<span class="colon">:</span>
IPAddresses

<!-- -->

<span class="sig-name descname"><span class="pre">get_erouter_iface_ipv6_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPv6Address</span></span></span><a href="#boardfarm3_docsis.use_cases.erouter.get_erouter_iface_ipv6_address" class="headerlink" title="Link to this definition">¶</a>
Get eRouter interface IPv6 address.

Parameters<span class="colon">:</span>
**board** (*CPE*) – CPE device instance

Returns<span class="colon">:</span>
IPv6 address of eRouter interface

Return type<span class="colon">:</span>
IPv6Address

<!-- -->

<span class="sig-name descname"><span class="pre">get_mta_iface_ip_addresses</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span><a href="#boardfarm3_docsis.use_cases.erouter.get_mta_iface_ip_addresses" class="headerlink" title="Link to this definition">¶</a>
Get the voice interface IP addresses.

Parameters<span class="colon">:</span>
-   **board** (*CPE*) – CPE device instance

-   **retry_count** (*int*) – number of retries

Returns<span class="colon">:</span>
IP addresses of voice interface

Return type<span class="colon">:</span>
IPAddresses

<!-- -->

<span class="sig-name descname"><span class="pre">get_wan_iface_ip_addresses</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span><a href="#boardfarm3_docsis.use_cases.erouter.get_wan_iface_ip_addresses" class="headerlink" title="Link to this definition">¶</a>
Get the management interface IP addresses.

Parameters<span class="colon">:</span>
-   **board** (*CPE*) – CPE device instance

-   **retry_count** (*int*) – number of retries

Returns<span class="colon">:</span>
IP addresses of management interface

Return type<span class="colon">:</span>
IPAddresses

<!-- -->

<span class="sig-name descname"><span class="pre">verify_erouter_ip_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.erouter.verify_erouter_ip_address" class="headerlink" title="Link to this definition">¶</a>
Verify the eRouter interface has the correct IP addresses for the specified mode.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Verify eRouter gets an IP address.

-   Check if the eRouter WAN Interface acquires IPv4 and/or IPv6 address

</div>

Parameters<span class="colon">:</span>
-   **mode** (*str*) – mode could be IPv4, IPv6/DSLite, Dual, disabled/bridge/modem

-   **board** (*CPE*) – CPE device instance

-   **retry** (*int*) – number of retries in order to fetch the erouter IP, defaults to 1

Returns<span class="colon">:</span>
True if the eRouter has correct IPv4/IPv6 address based on the mode passed

Return type<span class="colon">:</span>
bool

</div>

</div>

<span id="document-net_tools"></span>

<div id="net-tools-use-cases" class="section">

## Net_tools Use Cases<a href="#net-tools-use-cases" class="headerlink" title="Link to this heading">¶</a>

<div id="module-boardfarm3_docsis.use_cases.net_tools" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3_docsis<a href="#module-boardfarm3_docsis.use_cases.net_tools" class="headerlink" title="Link to this heading">¶</a>

Network utility helper use cases.

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">DNS</span></span><a href="#boardfarm3_docsis.use_cases.net_tools.DNS" class="headerlink" title="Link to this definition">¶</a>
DNS use cases.

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">get_dns_record</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">domain_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.DNS.get_dns_record" class="headerlink" title="Link to this definition">¶</a>
Perform nslookup and return the parsed results.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **domain_name** (*str*) – domain name to perform nslookup on

Returns<span class="colon">:</span>
parsed nslookup results as dictionary

Return type<span class="colon">:</span>
dict\[str, Any\]

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">nslookup_AAAA_record</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">domain_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-q=AAAA'</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.DNS.nslookup_AAAA_record" class="headerlink" title="Link to this definition">¶</a>
Perform nslookup for AAAA records and return the parsed results.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **domain_name** (*str*) – domain name to perform nslookup on

-   **opts** (*str*) – nslookup command line options

-   **extra_opts** (*str*) – nslookup additional command line options

Returns<span class="colon">:</span>
parsed nslookup results as dictionary

Return type<span class="colon">:</span>
dict\[str, Any\]

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">nslookup_A\_record</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">domain_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-q=A'</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.DNS.nslookup_A_record" class="headerlink" title="Link to this definition">¶</a>
Perform nslookup for A records and return the parsed results.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **domain_name** (*str*) – domain name to perform nslookup on

-   **opts** (*str*) – nslookup command line options

-   **extra_opts** (*str*) – nslookup additional command line options

Returns<span class="colon">:</span>
parsed nslookup results as dictionary

Return type<span class="colon">:</span>
dict\[str, Any\]

<!-- -->

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">Firewall</span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall" class="headerlink" title="Link to this definition">¶</a>
Linux iptables network firewall.

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">add_drop_rule_ip6tables</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">option</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">valid_ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall.add_drop_rule_ip6tables" class="headerlink" title="Link to this definition">¶</a>
Add drop rule to ip6tables.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **option** (*str*) – ip6tables command line options

-   **valid_ip** (*str*) – ip to be blocked from device

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">add_drop_rule_iptables</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">option</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">valid_ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall.add_drop_rule_iptables" class="headerlink" title="Link to this definition">¶</a>
Add drop rule to iptables.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **option** (*str*) – iptables command line options, set -s for source and -d for destination

-   **valid_ip** (*str*) – ip to be blocked from device

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">del_drop_rule_ip6tables</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">option</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">valid_ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall.del_drop_rule_ip6tables" class="headerlink" title="Link to this definition">¶</a>
Delete drop rule from ip6tables.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **option** (*str*) – ip6tables command line options

-   **valid_ip** (*str*) – ip to be unblocked

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">del_drop_rule_iptables</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">option</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">valid_ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall.del_drop_rule_iptables" class="headerlink" title="Link to this definition">¶</a>
Delete drop rule from iptables.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **option** (*str*) – iptables command line options, set -s for source and -d for destination

-   **valid_ip** (*str*) – ip to be unblocked

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">ip6tables_list</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nvL</span> <span class="pre">--line-number'</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall.ip6tables_list" class="headerlink" title="Link to this definition">¶</a>
Return ip6tables rules as dictionary.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **opts** (*str*) – command line arguments for ip6tables command

-   **extra_opts** (*str*) – extra command line arguments for ip6tables command

Returns<span class="colon">:</span>
ip6tables rules dictionary

Return type<span class="colon">:</span>
dict\[str, list\[dict\]\]

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">iptables_list</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nvL</span> <span class="pre">--line-number'</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall.iptables_list" class="headerlink" title="Link to this definition">¶</a>
Return iptables rules as dictionary.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **opts** (*str*) – command line arguments for iptables command

-   **extra_opts** (*str*) – extra command line arguments for iptables command

Returns<span class="colon">:</span>
iptables rules dictionary

Return type<span class="colon">:</span>
dict\[str, list\[dict\]\]

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">is_6table_empty</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nvL</span> <span class="pre">--line-number'</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall.is_6table_empty" class="headerlink" title="Link to this definition">¶</a>
Return True if ip6tables is empty.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **opts** (*str*) – command line arguments for ip6tables command

-   **extra_opts** (*str*) – extra command line arguments for ip6tables command

Returns<span class="colon">:</span>
True if ip6tables is empty, False otherwise

Return type<span class="colon">:</span>
bool

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">is_table_empty</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nvL</span> <span class="pre">--line-number'</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.Firewall.is_table_empty" class="headerlink" title="Link to this definition">¶</a>
Return True if iptables is empty.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **opts** (*str*) – command line arguments for iptables command

-   **extra_opts** (*str*) – extra command line arguments for iptables command

Returns<span class="colon">:</span>
True if iptables is empty, False otherwise

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">NwUtility</span></span><a href="#boardfarm3_docsis.use_cases.net_tools.NwUtility" class="headerlink" title="Link to this definition">¶</a>
OneFW network utility.

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">netstat_all_tcp</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nlp'</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">DataFrame</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.NwUtility.netstat_all_tcp" class="headerlink" title="Link to this definition">¶</a>
Get all UDP ports.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **opts** (*str*) – command line options

-   **extra_opts** (*str*) – extra command line options

Returns<span class="colon">:</span>
parsed netstat output

Return type<span class="colon">:</span>
DataFrame

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">netstat_all_udp</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nlp'</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">DataFrame</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.NwUtility.netstat_all_udp" class="headerlink" title="Link to this definition">¶</a>
Get all udp ports.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **opts** (*str*) – command line options

-   **extra_opts** (*str*) – extra command line options

Returns<span class="colon">:</span>
parsed netstat output

Return type<span class="colon">:</span>
DataFrame

<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">netstat_listening_ports</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nlp'</span></span>*, *<span class="n"><span class="pre">extra_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">DataFrame</span></span></span><a href="#boardfarm3_docsis.use_cases.net_tools.NwUtility.netstat_listening_ports" class="headerlink" title="Link to this definition">¶</a>
Get all listening ports.

Parameters<span class="colon">:</span>
-   **device_type** (*Type\[CableModem\]*) – type of the device

-   **opts** (*str*) – command line options

-   **extra_opts** (*str*) – extra command line options

Returns<span class="colon">:</span>
parsed netstat output

Return type<span class="colon">:</span>
DataFrame

</div>

</div>

<span id="document-snmp"></span>

<div id="snmp-use-cases" class="section">

## SNMP Use Cases<a href="#snmp-use-cases" class="headerlink" title="Link to this heading">¶</a>

<div id="module-boardfarm3_docsis.use_cases.snmp" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3_docsis<a href="#module-boardfarm3_docsis.use_cases.snmp" class="headerlink" title="Link to this heading">¶</a>

SNMP Use Cases.

<span class="sig-name descname"><span class="pre">get_mib_oid</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mib_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">device</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a href="#boardfarm3_docsis.use_cases.snmp.get_mib_oid" class="headerlink" title="Link to this definition">¶</a>
Return the Object Identifier (OID) for a given MIB.

Parameters<span class="colon">:</span>
-   **mib_name** (*str*) – MIB name. Will be searched in loaded MIB libraries.

-   **device** (*CPE*) – CPE device instance

Returns<span class="colon">:</span>
OID of the MIB

Return type<span class="colon">:</span>
str

<!-- -->

<span class="sig-name descname"><span class="pre">snmp_bulk_get</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*, *<span class="n"><span class="pre">mib_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">community</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'private'</span></span>*, *<span class="n"><span class="pre">non_repeaters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span>*, *<span class="n"><span class="pre">max_repetitions</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span>*, *<span class="n"><span class="pre">retries</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">3</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">100</span></span>*, *<span class="n"><span class="pre">extra_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">cmd_timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">30</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.snmp.snmp_bulk_get" class="headerlink" title="Link to this definition">¶</a>
Perform SNMP BulkGet on the device with given arguments.

Parameters<span class="colon">:</span>
-   **board** (*CPE*) – CPE device instance

-   **wan** (*WAN*) – WAN device instance

-   **cmts** (*CMTS*) – CMTS device instance

-   **mib_name** (*str*) – MIB name used to perform SNMP query

-   **index** (*int* *\|* *None*) – index used along with mib_name, defaults to None

-   **community** (*str*) – SNMP Community string, defaults to “private”

-   **non_repeaters** (*int*) – value treated as get request, defaults to 0

-   **max_repetitions** (*int*) – value treated as get next operation, defaults to 10

-   **retries** (*int*) – number of time commands are executed on exception, defaults to 3

-   **timeout** (*int*) – timeout in seconds, defaults to 100

-   **extra_args** (*str*) – extra arguments to be passed in the command, defaults to “”

-   **cmd_timeout** (*int*) – timeout to wait for command to give otuput

Returns<span class="colon">:</span>
output of snmpbulkget command

Return type<span class="colon">:</span>
list\[tuple\[str, str, str\]\]

<!-- -->

<span class="sig-name descname"><span class="pre">snmp_get</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mib_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*, *<span class="n"><span class="pre">index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span>*, *<span class="n"><span class="pre">community</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'private'</span></span>*, *<span class="n"><span class="pre">extra_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span>*, *<span class="n"><span class="pre">retries</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">3</span></span>*, *<span class="n"><span class="pre">cmd_timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">30</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.snmp.snmp_get" class="headerlink" title="Link to this definition">¶</a>
SNMP Get board MIB from WAN device via SNMPv2.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Verify Nm Access IP value via SNMP Get

-   Verify the LLC filter rules removed for IPv4 via SNMP

-   Get the values of \[mib_name\] via SNMP

</div>

Parameters<span class="colon">:</span>
-   **mib_name** (*str*) – MIB name. Will be searched in loaded MIB libraries.

-   **wan** (*WAN*) – WAN device instance

-   **board** (*CPE*) – CPE device instance

-   **cmts** (*CMTS*) – CMTS device instance

-   **index** (*int*) – MIB index, defaults to 0

-   **community** (*str*) – public/private, defaults to “private”

-   **extra_args** (*str*) – see `man snmpget` for extra args, defaults to “”

-   **timeout** (*int*) – seconds, defaults to 10

-   **retries** (*int*) – number of retries, defaults to 3

-   **cmd_timeout** (*int*) – timeout to wait for command to give otuput

Returns<span class="colon">:</span>
value, type, full SNMP output

Return type<span class="colon">:</span>
tuple\[str, str, str\]

<!-- -->

<span class="sig-name descname"><span class="pre">snmp_set</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mib_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">stype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*, *<span class="n"><span class="pre">index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span>*, *<span class="n"><span class="pre">community</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'private'</span></span>*, *<span class="n"><span class="pre">extra_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span>*, *<span class="n"><span class="pre">retries</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">3</span></span>*, *<span class="n"><span class="pre">cmd_timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">30</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.snmp.snmp_set" class="headerlink" title="Link to this definition">¶</a>
SNMP Set board MIB from WAN device via SNMPv2.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Perform SNMP Set operation on \[mib_name\]

-   Reset the DUT using SNMP command

-   Set the values of \[mib_name\] via SNMP

</div>

Parameters<span class="colon">:</span>
-   **mib_name** (*str*) – MIB name. Will be searched in loaded MIB libraries.

-   **value** (*str*) – value to be set.

-   **stype** (*str*) –

    defines the datatype of value to be set for mib_name. One of the following values:

    -   i: INTEGER,

    -   u: unsigned INTEGER,

    -   t: TIMETICKS,

    -   a: IPADDRESS,

    -   o: OBJID,

    -   s: STRING,

    -   x: HEX STRING,

    -   d: DECIMAL STRING,

    -   b: BITS

    -   U: unsigned int64,

    -   I: signed int64,

    -   F: float,

    -   D: double

-   **wan** (*WAN*) – WAN device instance

-   **board** (*CPE*) – CPE device instance

-   **cmts** (*CMTS*) – CMTS device instance

-   **index** (*int*) – MIB index, defaults to 0

-   **community** (*str*) – public/private, defaults to “private”

-   **extra_args** (*str*) – see `man snmpset` for extra args, defaults to “”

-   **timeout** (*int*) – seconds, defaults to 10

-   **retries** (*int*) – number of retries, defaults to 3

-   **cmd_timeout** (*int*) – timeout to wait for command to give otuput

Returns<span class="colon">:</span>
value, type, full SNMP output

Return type<span class="colon">:</span>
tuple\[str, str, str\]

<!-- -->

<span class="sig-name descname"><span class="pre">snmp_walk</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mib_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*, *<span class="n"><span class="pre">index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span>*, *<span class="n"><span class="pre">community</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'private'</span></span>*, *<span class="n"><span class="pre">extra_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span>*, *<span class="n"><span class="pre">retries</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">3</span></span>*, *<span class="n"><span class="pre">cmd_timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">30</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.snmp.snmp_walk" class="headerlink" title="Link to this definition">¶</a>
SNMP Walk board MIB from WAN device via SNMPv2.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Do SNMP Walk on \[mib_name\] MIB object on DUT

-   Perform SNMP Walk on DUT

</div>

Parameters<span class="colon">:</span>
-   **mib_name** (*str*) – MIB name. Will be searched in loaded MIB libraries.

-   **wan** (*WAN*) – WAN device instance

-   **board** (*CPE*) – CPE instance

-   **cmts** (*CMTS*) – CMTS device instance

-   **index** (*int*) – MIB index, defaults to 0

-   **community** (*str*) – public/private, defaults to “private”

-   **extra_args** (*str*) – see `man snmpwalk` for extra args, defaults to “”

-   **timeout** (*int*) – seconds, defaults to 10

-   **retries** (*int*) – number of retries, defaults to 3

-   **cmd_timeout** (*int*) – timeout to wait for command to give otuput

Returns<span class="colon">:</span>
(dictionary of mib_oid as key and tuple(mib value, mib type) as value, complete output)

Return type<span class="colon">:</span>
tuple\[dict\[str, List\[str\]\], str\]

</div>

</div>

<span id="document-tr069"></span>

<div id="tr069-use-cases" class="section">

## TR069 Use Cases<a href="#tr069-use-cases" class="headerlink" title="Link to this heading">¶</a>

<div id="module-boardfarm3_docsis.use_cases.tr069" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3_docsis<a href="#module-boardfarm3_docsis.use_cases.tr069" class="headerlink" title="Link to this heading">¶</a>

TR-069 Use cases.

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">AddObjectResponse</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">response</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">object_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span><a href="#boardfarm3_docsis.use_cases.tr069.AddObjectResponse" class="headerlink" title="Link to this definition">¶</a>
Store output of TR-069 AddObject RPC.

Raises<span class="colon">:</span>
**UseCaseFailure** – in case of parsing errors

<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">instance_number</span></span><span class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">int</span></span><a href="#boardfarm3_docsis.use_cases.tr069.AddObjectResponse.instance_number" class="headerlink" title="Link to this definition">¶</a>
Store the Instance Number of the newly created Object.

Once created, a Parameter or sub-object within this Object can be later referenced by using this Instance Number Identifier (defined in Section A.2.2.1) in the Path Name. The Instance Number assigned by the CPE is arbitrary.

Note the fact that Instance Numbers are arbitrary means that they do not define a useful Object ordering, e.g. the ACS cannot assume that a newly created Object will have a higher Instance Number than its existing sibling Objects.

Returns<span class="colon">:</span>
instance number

Return type<span class="colon">:</span>
int

<!-- -->

<span class="sig-name descname"><span class="pre">Download</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">url</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">filetype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">targetfilename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">filesize</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">username</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">password</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">commandkey</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">delayseconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">successurl</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">failureurl</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.Download" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call Download.

This method is used by the ACS to cause the CPE to download a specified file from the designated location.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute Download RPC via ACS

</div>

Parameters<span class="colon">:</span>
-   **url** (*str*) – specifies the source file location. HTTP and HTTPS transports MUST be supported

-   **filetype** (*str*) – An integer followed by a space followed by the file type description. Only the following values are currently defined for the FileType argument: 1. Firmware Upgrade Image 2. Web Content 3. Vendor Configuration File 4. Tone File 5. Ringer File 6. Stored Firmware Image

-   **targetfilename** (*str*) – The name of the file to be used on the target file system.

-   **filesize** (*int*) – The size of the file to be downloaded in bytes

-   **username** (*str*) – Username to be used by the CPE to authenticate with the file server

-   **password** (*str*) – Password to be used by the CPE to authenticate with the file server

-   **commandkey** (*str*) – The string the CPE uses to refer to a particular download

-   **delayseconds** (*int*) – This argument has different meanings for Unicast and Multicast downloads

-   **successurl** (*str*) – this argument contains the URL, the CPE should redirect the user’s browser to if the download completes successfully

-   **failureurl** (*str*) – this argument contains the URL, the CPE should redirect the user’s browser to if the download completes unsuccessfully

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
Return the list of Dictionary containing the keys Status,StartTime and CompleteTime

Return type<span class="colon">:</span>
list\[dict\[str, Any\]\]

<!-- -->

<span class="sig-name descname"><span class="pre">GPA</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.GPA" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call GetParameterAttributes.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute GetParameterAttributes RPC

-   Execute GPA RPC

-   Execute GPA on param

</div>

Parameters<span class="colon">:</span>
-   **param** (*str*) – name of the parameter

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
list of dictionary with keys Name, AccessList, Notification indicating the attributes of the parameter

Return type<span class="colon">:</span>
list\[dict\[str, Any\]\]

<!-- -->

<span class="sig-name descname"><span class="pre">GPN</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param_path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">next_level</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">120</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.GPN" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call GetParametersName.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   GPN of \[\]

-   GetParameterNames RPC

</div>

Parameters<span class="colon">:</span>
-   **param_path** (*str*) – name of the parameter

-   **next_level** (*bool*) – If false, the response MUST contain the Parameter or Object whose name exactly matches the ParameterPath argument

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

-   **timeout** (*int*) – Timeout for the GPN RPC call, defaults to 120

Returns<span class="colon">:</span>
list of dictionary with key, type and value

Return type<span class="colon">:</span>
list\[dict\[str, Any\]\]

<!-- -->

<span class="sig-name descname"><span class="pre">GPV</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.GPV" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call GetParameterValues.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute GetParameterValues RPC by providing param name

-   Perform GPV on parameter

-   using GPV via ACS

</div>

Usage:

<div class="highlight-python notranslate">

<div class="highlight">

    GPV(params=["param1", "param2"])

</div>

</div>

Parameters<span class="colon">:</span>
-   **params** (*str* *\|* *list\[str\]*) – List of parameters

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
List of dict of Param,Value pairs

Return type<span class="colon">:</span>
List\[RPCOutput\]

<!-- -->

<span class="sig-name descname"><span class="pre">GetRPCMethods</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.GetRPCMethods" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call GetRPCMethods.

Parameters<span class="colon">:</span>
-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
list of all the RPC methods

Return type<span class="colon">:</span>
List\[str\]

<!-- -->

<span class="sig-name descname"><span class="pre">Reboot</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">command_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.Reboot" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call Reboot.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Perform reboot on DUT

-   Reboot the DUT

-   Execute Reboot RPC from ACS

</div>

Parameters<span class="colon">:</span>
-   **command_key** (*str*) – The string to return in the CommandKey element of the InformStruct when the CPE reboots and calls the Inform method.

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Raises<span class="colon">:</span>
**UseCaseFailure** – in case of board not online after reset

<!-- -->

<span class="sig-name descname"><span class="pre">SPA</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">notification_change</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">access_change</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">access_list</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.SPA" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call SetParameterValues.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute SetParameterAttributes RPC

-   Execute SPA RPC by providing ParameterName

-   Perform SPA on

</div>

Example usage:

<div class="highlight-python notranslate">

<div class="highlight">

    SPA([{"Device.WiFi.SSID.1.SSID": "1"}], True, False, [])

</div>

</div>

Parameters<span class="colon">:</span>
-   **param** (*list\[dict\[str,* *str\]\]* *\|* *dict\[str,* *str\]*) – parameter as key of dictionary and notification as its value

-   **notification_change** (*bool*) – If true, the value of Notification replaces the current notification setting for this Parameter or group of Parameters. If false, no change is made to the notification setting

-   **access_change** (*bool*) – If true, the value of AccessList replaces the current access list for this Parameter or group of Parameters. If false, no change is made to the access list.

-   **access_list** (*list*) – Array of zero or more entities for which write access to the specified Parameter(s) is granted

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

<!-- -->

<span class="sig-name descname"><span class="pre">SPV</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.SPV" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call SetParameterValues.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Perform SetParameterValues RPC by providing parameter

-   Execute SPV RPC by providing parameter name

-   Execute SPV from ACS

</div>

Usage:

<div class="highlight-python notranslate">

<div class="highlight">

    SPV(params=[{"param1": "value1"}, {"param2": 123}])

</div>

</div>

Parameters<span class="colon">:</span>
-   **params** (*list\[dict\[str,* *Any\]\]*) – Dict or list of Dict\[parameters, values\]

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
List of dict of Param,Value pairs

Return type<span class="colon">:</span>
int

<!-- -->

<span class="sig-name descname"><span class="pre">ScheduleInform</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">delay_seconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">command_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.ScheduleInform" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call ScheduleInform.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute ScheduleInform RPC from ACS

</div>

Parameters<span class="colon">:</span>
-   **delay_seconds** (*int*) – The number of seconds from the time this method is called to the time the CPE is requested to initiate a one-time Inform method call

-   **command_key** (*str*) – The string to return in the CommandKey element of the InformStruct when the CPE calls the Inform method.

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

<!-- -->

<span class="sig-name descname"><span class="pre">add_object</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">object_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">parameter_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><a href="#document-tr069#boardfarm3_docsis.use_cases.tr069.AddObjectResponse" class="reference internal" title="boardfarm3_docsis.use_cases.tr069.AddObjectResponse"><span class="pre">AddObjectResponse</span></a></span></span><a href="#boardfarm3_docsis.use_cases.tr069.add_object" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call AddObject.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute AddObject RPC by providing parameter name

-   Add the \[\] entry by Add object from ACS

-   Add new instance to \[\] by Add object from ACS

</div>

Usage:

<div class="highlight-python notranslate">

<div class="highlight">

    out = add_object(object_name)
    instance_number = out.instance_number
    response = out.response

</div>

</div>

Parameters<span class="colon">:</span>
-   **object_name** (*str*) – Name of the object to be added

-   **parameter_key** (*str* *\|* *None*) – The optional string value to set the ParameterKey.

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
AddObjectResponse with values response & instance_number

Return type<span class="colon">:</span>
<a href="#document-tr069#boardfarm3_docsis.use_cases.tr069.AddObjectResponse" class="reference internal" title="boardfarm3_docsis.use_cases.tr069.AddObjectResponse">AddObjectResponse</a>

<!-- -->

<span class="sig-name descname"><span class="pre">del_object</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">object_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">parameter_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.del_object" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call DeleteObject.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Delete the \[\] entry using Delete Object RPC from ACS

-   Login to ACS and delete

-   Execute DeleteObject RPC from ACS

</div>

Usage:

<div class="highlight-python notranslate">

<div class="highlight">

    del_object(object_name)

</div>

</div>

Parameters<span class="colon">:</span>
-   **object_name** (*str*) – Name of the object to be added

-   **parameter_key** (*str* *\|* *None*) – The optional string value to set the ParameterKey.

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
delete object response value

Return type<span class="colon">:</span>
int

<!-- -->

<span class="sig-name descname"><span class="pre">download</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">url</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">filetype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">targetfilename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">filesize</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">username</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">password</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">commandkey</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">delayseconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">successurl</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">failureurl</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.download" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call Download.

This method is used by the ACS to cause the CPE to download a specified file from the designated location.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute Download RPC via ACS

</div>

Parameters<span class="colon">:</span>
-   **url** (*str*) – specifies the source file location. HTTP and HTTPS transports MUST be supported

-   **filetype** (*str*) – An integer followed by a space followed by the file type description. Only the following values are currently defined for the FileType argument: 1. Firmware Upgrade Image 2. Web Content 3. Vendor Configuration File 4. Tone File 5. Ringer File 6. Stored Firmware Image

-   **targetfilename** (*str*) – The name of the file to be used on the target file system.

-   **filesize** (*int*) – The size of the file to be downloaded in bytes

-   **username** (*str*) – Username to be used by the CPE to authenticate with the file server

-   **password** (*str*) – Password to be used by the CPE to authenticate with the file server

-   **commandkey** (*str*) – The string the CPE uses to refer to a particular download

-   **delayseconds** (*int*) – This argument has different meanings for Unicast and Multicast downloads

-   **successurl** (*str*) – this argument contains the URL, the CPE should redirect the user’s browser to if the download completes successfully

-   **failureurl** (*str*) – this argument contains the URL, the CPE should redirect the user’s browser to if the download completes unsuccessfully

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
Return the list of Dictionary containing the keys Status,StartTime and CompleteTime

Return type<span class="colon">:</span>
list\[dict\[str, Any\]\]

<!-- -->

<span class="sig-name descname"><span class="pre">factory_reset</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.factory_reset" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 FactoryReset RPC call and guarantee the board is back online.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Factory Reset the DUT

-   Perform factory reset on the CPE

</div>

Usage:

<div class="highlight-python notranslate">

<div class="highlight">

    factory_reset()

</div>

</div>

Parameters<span class="colon">:</span>
-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Raises<span class="colon">:</span>
**UseCaseFailure** – in case of board not online after reset

<!-- -->

<span class="sig-name descname"><span class="pre">get_ccsptr069_pid</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.get_ccsptr069_pid" class="headerlink" title="Link to this definition">¶</a>
Return the CcspTr069PaSsp process id.

Parameters<span class="colon">:</span>
**board** (*CPE*) – The CPE device instance

Returns<span class="colon">:</span>
The pid of CcspTr069PaSsp process

Return type<span class="colon">:</span>
int \| None

<!-- -->

<span class="sig-name descname"><span class="pre">get_parameter_attributes</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.get_parameter_attributes" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call GetParameterAttributes.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute GetParameterAttributes RPC

-   Execute GPA RPC

-   Execute GPA on param

</div>

Parameters<span class="colon">:</span>
-   **param** (*str*) – name of the parameter

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
list of dictionary with keys Name, AccessList, Notification indicating the attributes of the parameter

Return type<span class="colon">:</span>
list\[dict\[str, Any\]\]

<!-- -->

<span class="sig-name descname"><span class="pre">get_parameter_names</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param_path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">next_level</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">120</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.get_parameter_names" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call GetParametersName.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   GPN of \[\]

-   GetParameterNames RPC

</div>

Parameters<span class="colon">:</span>
-   **param_path** (*str*) – name of the parameter

-   **next_level** (*bool*) – If false, the response MUST contain the Parameter or Object whose name exactly matches the ParameterPath argument

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

-   **timeout** (*int*) – Timeout for the GPN RPC call, defaults to 120

Returns<span class="colon">:</span>
list of dictionary with key, type and value

Return type<span class="colon">:</span>
list\[dict\[str, Any\]\]

<!-- -->

<span class="sig-name descname"><span class="pre">get_parameter_values</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.get_parameter_values" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call GetParameterValues.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute GetParameterValues RPC by providing param name

-   Perform GPV on parameter

-   using GPV via ACS

</div>

Usage:

<div class="highlight-python notranslate">

<div class="highlight">

    GPV(params=["param1", "param2"])

</div>

</div>

Parameters<span class="colon">:</span>
-   **params** (*str* *\|* *list\[str\]*) – List of parameters

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
List of dict of Param,Value pairs

Return type<span class="colon">:</span>
List\[RPCOutput\]

<!-- -->

<span class="sig-name descname"><span class="pre">get_rpc_methods</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.get_rpc_methods" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call GetRPCMethods.

Parameters<span class="colon">:</span>
-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
list of all the RPC methods

Return type<span class="colon">:</span>
List\[str\]

<!-- -->

<span class="sig-name descname"><span class="pre">is_dut_online_on_acs</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.is_dut_online_on_acs" class="headerlink" title="Link to this definition">¶</a>
Check if the DUT is online on ACS.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Verify the DUT registration status on the ACS

-   Make sure that DUT is registered on the ACS.

</div>

Parameters<span class="colon">:</span>
-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
True if devices is registered with ACS and GPV is successful for Device.DeviceInfo.SoftwareVersion, else False

Return type<span class="colon">:</span>
bool

<!-- -->

<span class="sig-name descname"><span class="pre">reboot</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">command_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.reboot" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call Reboot.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Perform reboot on DUT

-   Reboot the DUT

-   Execute Reboot RPC from ACS

</div>

Parameters<span class="colon">:</span>
-   **command_key** (*str*) – The string to return in the CommandKey element of the InformStruct when the CPE reboots and calls the Inform method.

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Raises<span class="colon">:</span>
**UseCaseFailure** – in case of board not online after reset

<!-- -->

<span class="sig-name descname"><span class="pre">restart_tr069_agent</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.restart_tr069_agent" class="headerlink" title="Link to this definition">¶</a>
Restart the TR-069 agent by killing the process based on the PID.

Parameters<span class="colon">:</span>
**board** (*CPE*) – CPE device instance

Raises<span class="colon">:</span>
**ValueError** – when the CcspTr069PaSsp is not alive

<!-- -->

<span class="sig-name descname"><span class="pre">schedule_inform</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">delay_seconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">command_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.schedule_inform" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call ScheduleInform.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute ScheduleInform RPC from ACS

</div>

Parameters<span class="colon">:</span>
-   **delay_seconds** (*int*) – The number of seconds from the time this method is called to the time the CPE is requested to initiate a one-time Inform method call

-   **command_key** (*str*) – The string to return in the CommandKey element of the InformStruct when the CPE calls the Inform method.

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

<!-- -->

<span class="sig-name descname"><span class="pre">set_parameter_attributes</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">notification_change</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">access_change</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">access_list</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.set_parameter_attributes" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call SetParameterValues.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Execute SetParameterAttributes RPC

-   Execute SPA RPC by providing ParameterName

-   Perform SPA on

</div>

Example usage:

<div class="highlight-python notranslate">

<div class="highlight">

    SPA([{"Device.WiFi.SSID.1.SSID": "1"}], True, False, [])

</div>

</div>

Parameters<span class="colon">:</span>
-   **param** (*list\[dict\[str,* *str\]\]* *\|* *dict\[str,* *str\]*) – parameter as key of dictionary and notification as its value

-   **notification_change** (*bool*) – If true, the value of Notification replaces the current notification setting for this Parameter or group of Parameters. If false, no change is made to the notification setting

-   **access_change** (*bool*) – If true, the value of AccessList replaces the current access list for this Parameter or group of Parameters. If false, no change is made to the access list.

-   **access_list** (*list*) – Array of zero or more entities for which write access to the specified Parameter(s) is granted

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

<!-- -->

<span class="sig-name descname"><span class="pre">set_parameter_values</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span><a href="#boardfarm3_docsis.use_cases.tr069.set_parameter_values" class="headerlink" title="Link to this definition">¶</a>
Perform TR-069 RPC call SetParameterValues.

<div class="admonition hint">

Hint

This Use Case implements statements from the test suite such as:

-   Perform SetParameterValues RPC by providing parameter

-   Execute SPV RPC by providing parameter name

-   Execute SPV from ACS

</div>

Usage:

<div class="highlight-python notranslate">

<div class="highlight">

    SPV(params=[{"param1": "value1"}, {"param2": 123}])

</div>

</div>

Parameters<span class="colon">:</span>
-   **params** (*list\[dict\[str,* *Any\]\]*) – Dict or list of Dict\[parameters, values\]

-   **acs** (*ACS* *\|* *None*) – ACS server that will perform GPV

-   **board** (*CPE* *\|* *None*) – CPE on which to perform TR-069 method

Returns<span class="colon">:</span>
List of dict of Param,Value pairs

Return type<span class="colon">:</span>
int

</div>

</div>

</div>

</div>

<div class="clearer">

</div>

</div>

</div>

</div>

<div id="show_right_sidebar">

<a href="#" class="toggle_right_sidebar"><span class="icon">&lt;</span><span>Page contents</span></a>

</div>

<div id="right_sidebar">

<a href="#" class="toggle_right_sidebar"><span class="icon">&gt;</span><span>Page contents:</span></a>

<div class="page_toc">

<span class="caption-text">Use Cases</span>

-   <a href="#document-connectivity" class="reference internal">Connectivity Use Cases</a>
    -   <a href="#document-connectivity#module-boardfarm3_docsis.use_cases.connectivity" class="reference internal">from boardfarm3_docsis</a>
-   <a href="#document-docsis" class="reference internal">Docsis Use Cases</a>
    -   <a href="#document-docsis#module-boardfarm3_docsis.use_cases.docsis" class="reference internal">from boardfarm3_docsis</a>
-   <a href="#document-erouter" class="reference internal">Erouter Use Cases</a>
    -   <a href="#document-erouter#module-boardfarm3_docsis.use_cases.erouter" class="reference internal">from boardfarm3_docsis</a>
-   <a href="#document-net_tools" class="reference internal">Net_tools Use Cases</a>
    -   <a href="#document-net_tools#module-boardfarm3_docsis.use_cases.net_tools" class="reference internal">from boardfarm3_docsis</a>
-   <a href="#document-snmp" class="reference internal">SNMP Use Cases</a>
    -   <a href="#document-snmp#module-boardfarm3_docsis.use_cases.snmp" class="reference internal">from boardfarm3_docsis</a>
-   <a href="#document-tr069" class="reference internal">TR069 Use Cases</a>
    -   <a href="#document-tr069#module-boardfarm3_docsis.use_cases.tr069" class="reference internal">from boardfarm3_docsis</a>

</div>

</div>

<div class="clearer">

</div>

</div>

<div class="button_nav_wrapper">

<div class="button_nav">

<div class="left">

</div>

<div class="right">

</div>

</div>

</div>

<div class="footer" role="contentinfo">

© Copyright 2025, Various. Created using [Sphinx](https://www.sphinx-doc.org/) 9.0.4.

</div>

Styled using the [Piccolo Theme](https://github.com/piccolo-orm/piccolo_theme)
