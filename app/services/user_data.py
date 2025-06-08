# ← fetch_user_profile(), insert_user()

from .supabase_client import supabase

def create_user_profile(auth_id, email, username, role):
    # 🔍 Debug: Check current session context
    user_session = supabase.auth.get_user()
    print("🧪 Current Supabase user session:", user_session)

    # ✅ Prepare insert payload

    result = supabase.table("user_profiles").insert({
        "auth_id": auth_id,
        "email": email,
        "username": username,
        "role": role

    }).execute()

    print(result)  # 👈 will show error if exists
    return result
