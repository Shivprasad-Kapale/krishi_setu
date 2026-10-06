from modules.community import load_community_data

data = load_community_data()
post = data["posts"][0]
lang_code = "en"
selected_district = "Nashik"
p_text_display = post["text"].get(lang_code, post["text"].get("mr", list(post["text"].values())[0]))
expert_badge = ""

card_html = f"""
<div style="background: #ffffff; border-radius: 16px; padding: 18px 20px; margin-bottom: 12px; border: 1px solid #e0e8e1; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
    <div style="display: flex; gap: 12px; align-items: flex-start;">
        <div style="width: 44px; height: 44px; border-radius: 50%; background: {post.get('avatar_color', '#2e7d32')}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; flex-shrink: 0; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
            {post.get('avatar_initial', 'श')}
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 700; font-size: 15px; color: #1b2e1f; display: flex; align-items: center; flex-wrap: wrap;">
                {post['author']} {expert_badge}
            </div>
            <div style="font-size: 12px; color: #7a8a7d; margin-top: 3px;">
                📍 {post.get('village', selected_district)} · 🕒 {post.get('time', 'Recently')} · <span style="background: #f1f8e9; color: #2e7d32; padding: 1px 7px; border-radius: 8px; font-weight: 600;">{post.get('category', 'Agri')}</span>
            </div>
        </div>
    </div>
    <div style="font-size: 14.5px; line-height: 1.6; color: #22331f; margin: 14px 0 10px 0; background: #fafdfa; padding: 12px 14px; border-radius: 10px; border-left: 3px solid #66bb6a;">
        {p_text_display}
    </div>
</div>
"""

clean_lines = [line.strip() for line in card_html.splitlines() if line.strip()]
result = "".join(clean_lines)
print("LENGTH:", len(result))
print("SAMPLE:")
print(result[:300])
