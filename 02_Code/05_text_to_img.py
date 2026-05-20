import sk_tools.yt_function as yt_func

# # Read from json file:
segments = yt_func.readListFromJson('output/segments.json')
print(type(segments))
print("Retrieved Data:", segments[:2])
print("==="*10)
print("Visual Prompts:", segments[0]['visual_prompt'])
print("Duration:", segments[0]['approx_duration'])
